# =============================================================================
# Copyright 2019 Grillo Holdings Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

import aioboto3
import boto3
import asyncio
import io
import json
from datetime import datetime, timedelta
from botocore import UNSIGNED
from botocore.client import Config


class AwsDataClient(object):
    """
    A client for downloading OpenEEW data stored as an
    AWS Public Dataset.
    """

    # Template of the country part of all record keys
    _RECORDS_KEY_COUNTRY_TEMPLATE = 'records/country_code={}/'
    # Template of the device part of all record keys
    _RECORDS_KEY_DEVICE_TEMPLATE = 'device_id={}/'
    # Template of the year-month-day part of all record keys
    _RECORDS_KEY_YMD_TEMPLATE = 'year={}/month={}/day={}/'
    # Template of the hour part of all record keys
    _RECORDS_KEY_HOUR_TEMPLATE = 'hour={}/'
    # Template of the year-month-day-hour part of all record keys
    _RECORDS_KEY_DATE_TEMPLATE = _RECORDS_KEY_YMD_TEMPLATE + \
        _RECORDS_KEY_HOUR_TEMPLATE
    # Template of the country part of all device metadata keys
    _DEVICES_KEY_TEMPLATE = 'devices/country_code={}/devices.jsonl'
    # Name of the S3 bucket where OpenEEW data is stored
    _S3_BUCKET_NAME = 'grillo-openeew'
    # Region of the S3 bucket where OpenEEW data is stored
    _S3_BUCKET_REGION = 'us-east-1'

    def __init__(self, country_code, s3_client=None):
        """
        Initialize AwsDataClient with the following parameters:

        :param country_code: The ISO 3166 two-letter country code
            for which data is required. It is case-insensitive
            as the value specified will be converted to lower case.
        :type country_code: str

        :param s3_client: The S3 client to use to access OpenEEW data
            on AWS. If no value is given, an anonymous S3 client
            will be used.
        :type s3_client: boto3.client.s3
        """

        self.country_code = country_code
        self._s3_client = s3_client or boto3.client(
                's3',
                region_name=self._S3_BUCKET_REGION,
                config=Config(signature_version=UNSIGNED)
                )

    @property
    def country_code(self):
        """
        :return: ISO 3166 two-letter country code of the client
            (in lower case). Any data returned by the client will
            be for this country.
        :rtype: str
        """
        return self._country_code

    @country_code.setter
    def country_code(self, value):
        self._country_code = value.lower()
        self._records_key_country_part = \
            self._RECORDS_KEY_COUNTRY_TEMPLATE.format(self._country_code)
        self._devices_key = \
            self._DEVICES_KEY_TEMPLATE.format(self._country_code)

    @staticmethod
    def _get_dt_from_str(date_utc):
        # Parses the input string with format YYYY-mm-dd HH:MM:SS into
        # a datetime.datetime object with UTC timezone

        try:
            return datetime.strptime(
                '{} +0000'.format(date_utc),
                '%Y-%m-%d %H:%M:%S %z'
                )
        except Exception as e:
            raise ValueError('The date must be in format YYYY-mm-dd HH:MM:SS')

    @classmethod
    def _get_records_key_date_part(cls, date_parts):
        # Returns the date part of the records key

        return cls._RECORDS_KEY_DATE_TEMPLATE.format(
            date_parts['year'],
            date_parts['month'],
            date_parts['day'],
            date_parts['hour']
            )

    def _get_device_ids_from_records(self):
        # Returns a list of all devices (device_id) that have records

        paginator = self._s3_client.get_paginator('list_objects_v2')

        pages = paginator.paginate(
                Bucket=self._S3_BUCKET_NAME,
                Prefix=self._records_key_country_part,
                Delimiter='/'
                )

        device_prefixes = [
                p.get('Prefix') for p in pages.search('CommonPrefixes')
                ]

        # Use [:-1] to remove the final /
        return [d.split('device_id=')[1][:-1] for d in device_prefixes]

    def _get_records_key_device_prefix(self, device_id):
        # Returns a key prefix including country_code and device_id

        return self._records_key_country_part + \
            self._RECORDS_KEY_DEVICE_TEMPLATE.format(device_id)

    @staticmethod
    def _get_date_parts_as_strings(dt):
        # Returns a dictionary with the date parts
        # in the necessary string format for working with record keys.
        # dt should be UTC

        return {
                'year': str(dt.year),
                'month': '%02d' % dt.month,
                'day': '%02d' % dt.day,
                'hour': '%02d' % dt.hour,
                'minute': '%02d' % dt.minute
                }

    @classmethod
    def _get_max_key_date_part_full(cls, dt):
        # Get maximum possible date part of key,
        # including minute and file extension

        date_parts = cls._get_date_parts_as_strings(dt)

        return cls._get_records_key_date_part(date_parts) + \
            '{}.jsonl'.format(date_parts['minute'])

    @classmethod
    def _get_key_date_parts_within_range(cls, start_dt, end_dt):
        # For given start and end dates, returns a list of key date parts
        # to be used as search prefixes, where each date part corresponds to
        # one day

        key_date_parts_within_range = []
        this_dt = start_dt
        while this_dt.date() <= end_dt.date():

            date_parts = \
                    cls._get_date_parts_as_strings(this_dt)

            key_date_parts_within_range.append(
                    cls._RECORDS_KEY_YMD_TEMPLATE.format(
                                    date_parts['year'],
                                    date_parts['month'],
                                    date_parts['day']
                                    )
                    )

            this_dt = this_dt + timedelta(days=1)

        return key_date_parts_within_range

    def _get_records_keys_to_download(self, start_dt, end_dt, device_ids=None):
        # Returns list of keys that contain required data.

        if end_dt < start_dt:
            raise ValueError('end date should not be earlier than start date')

        # A simple lower bound for keys to download (without making
        # assumptions on num minutes contained per file) is given by
        # the hour corresponding to the start date
        start_key_date_part_lower_bound = \
            self._get_records_key_date_part(
                self._get_date_parts_as_strings(start_dt)
                )

        # Get max possible key values that contain data for
        # start and end dates, respectively
        max_start_key_date_part_full = \
            self._get_max_key_date_part_full(start_dt)
        max_end_key_date_part_full = \
            self._get_max_key_date_part_full(end_dt)

        # Get list of date parts to be used as search prefixes
        key_date_parts_within_range = \
            self._get_key_date_parts_within_range(start_dt, end_dt)

        # Initialize empty list to store the keys to download
        keys_to_download = []
        paginator = self._s3_client.get_paginator('list_objects_v2')
        _device_ids = device_ids or self._get_device_ids_from_records()
        for d in _device_ids:

            device_prefix = self._get_records_key_device_prefix(d)

            for key_date_part in key_date_parts_within_range:
                # Initialize list to store all keys that might contain
                # data for the current device and chosen dates
                candidate_keys = []

                pages = paginator.paginate(
                            Bucket=self._S3_BUCKET_NAME,
                            Prefix=device_prefix + key_date_part
                            )

                for p in pages:
                    if 'Contents' not in p.keys():
                        continue
                    # Select those keys that contain data before the
                    # end date and no earlier than the hour of the
                    # start date
                    candidate_keys += [
                            o['Key'] for o in p['Contents']
                            if o['Key'] <= device_prefix +
                            max_end_key_date_part_full and
                            o['Key'] >= device_prefix +
                            start_key_date_part_lower_bound
                            ]

                if not candidate_keys:
                    continue

                # Check which keys contain data before the start date
                keys_before_start_date = [
                        k for k in candidate_keys
                        if k <= device_prefix + max_start_key_date_part_full
                        ]

                # If no keys contain data before start date, then no
                # further filter is required and we keep all of them
                if not keys_before_start_date:
                    keys_to_download += candidate_keys
                else:
                    # Of all keys that contain data before start date,
                    # only the max of these might actually contain relevant
                    # data
                    max_key_before_start_date = max(keys_before_start_date)
                    keys_to_download += [
                            k for k in candidate_keys
                            if k >= max_key_before_start_date
                            ]

        return keys_to_download

    @classmethod
    async def _get_records_from_key(cls, async_s3_client, key):
        # Gets records from a single key and converts them to a list of dicts

        with io.BytesIO() as bytes_stream:

            await async_s3_client.download_fileobj(
                cls._S3_BUCKET_NAME,
                key,
                bytes_stream
                )

            bytes_stream.seek(0)
            records = [json.loads(line) for line in bytes_stream.readlines()]

        return records

    @classmethod
    async def _download_keys(cls, keys_to_download):
        # Gets all records from list of keys.
        # Returns a list of lists of dicts

        # Set up async S3 client
        async_s3_client = aioboto3.client(
                's3',
                region_name=cls._S3_BUCKET_REGION,
                config=Config(signature_version=UNSIGNED)
                )

        # Define coroutines, one for each file to download
        coros = [
                cls._get_records_from_key(async_s3_client, k)
                for k in keys_to_download
                    ]

        key_records = await asyncio.gather(*coros)

        await async_s3_client.close()

        return key_records

    def get_filtered_records(self, start_date_utc, end_date_utc,
                             device_ids=None):
        """
        Returns accelerometer records filtered by date and device.

        :param start_date_utc: The UTC start date
            with format %Y-%m-%d %H:%M:%S. E.g. '2018-02-16 23:39:38'.
            Only records with a cloud_t equal to or greater than
            start_date_utc will be returned.
        :type start_date_utc: str

        :param end_date_utc: The UTC end date with same format as
            start_date_utc. Only records with a cloud_t
            equal to or less than end_date_utc will be returned.
        :type end_date_utc: str

        :param device_ids: List of device IDs that should be returned.
        :type device_ids: list[str]

        :return: A list of records, where each record is a dict
            obtained from the stored JSON value. For details about the
            JSON records, see
            `Data fields <https://github.com/grillo/openeew/tree/master/data#data-fields>`_
            for further information about how records are stored.
        :rtype: list[dict]
        """

        start_dt = self._get_dt_from_str(start_date_utc)
        end_dt = self._get_dt_from_str(end_date_utc)
        # Get the list of keys based on start and end dates

        keys_to_download = self._get_records_keys_to_download(
                start_dt,
                end_dt,
                device_ids
                )

        loop = asyncio.get_event_loop()

        key_records = loop.run_until_complete(
                self._download_keys(keys_to_download)
                )
        # Initialize empty list in which to store dicts
        records = []
        # Now loop through all keys to download and
        # concatenate the resulting lists of dicts

        for kr in key_records:
            # Keep all individual records that
            # meet the date filter
            records += [
                    d for d in kr
                    if d['cloud_t'] >= start_dt.timestamp() and
                    d['cloud_t'] <= end_dt.timestamp()
                    ]

        return records

    def get_devices_full_history(self):
        """
        Gets full history of device metadata.

        :return: A list of device metadata. See
            `Device metadata <https://github.com/grillo/openeew/tree/master/data#device-metadata>`_
            for information about the fields.
        :rtype: list[dict]
        """

        bytes_stream = io.BytesIO()
        self._s3_client.download_fileobj(
                self._S3_BUCKET_NAME,
                self._devices_key,
                bytes_stream
                )
        bytes_stream.seek(0)
        devices = [json.loads(line) for line in bytes_stream.readlines()]
        bytes_stream.close()

        return devices

    def get_current_devices(self):
        """
        Gets currently-valid device metadata. Fields are the same as
        for :func:`get_devices_full_history`.

        :return: A list of device metadata.
        :rtype: list[dict]
        """

        return [
                d for d in self.get_devices_full_history()
                if d['is_current_row']
                ]

    def get_devices_as_of_date(self, date_utc):
        """
        Gets device metadata as of a chosen UTC date. Fields are the
        same as for :func:`get_devices_full_history`.

        :param date_utc: The UTC date with format %Y-%m-%d %H:%M:%S.
            E.g. '2018-02-16 23:39:38'.
        :type date_utc: str

        :return: A list of device metadata.
        :rtype: list[dict]
        """

        ts = self._get_dt_from_str(date_utc).timestamp()

        return [
                d for d in self.get_devices_full_history()
                if d['effective_from'] <= ts and
                d['effective_to'] >= ts
                ]
