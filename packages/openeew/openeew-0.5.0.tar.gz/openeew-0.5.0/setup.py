from setuptools import setup, find_packages

setup(
    name='openeew',
    version='0.5.0',
    description='OpenEEW library for Python',
    author='Grillo',
    author_email='openeew@grillo.io',
    url='http://github.com/grillo/openeew-python',
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.5',
    install_requires=['pandas', 'aioboto3'],
    zip_safe=False
    )
