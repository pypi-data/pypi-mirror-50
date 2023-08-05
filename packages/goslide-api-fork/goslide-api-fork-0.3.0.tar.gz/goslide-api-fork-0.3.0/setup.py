'''
Install goslide.io Open Cloud API
'''

import setuptools

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setuptools.setup(
    name='goslide-api-fork',
    version='0.3.0',
    url='https://github.com/zbessarab/goslide-api',
    license='Apache License 2.0',
    author='Alexander Kuiper',
    author_email='ualex73@gmail.com',
    description='Python API to utilise the goslide.io Open Cloud API',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=['aiohttp', 'asyncio'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
