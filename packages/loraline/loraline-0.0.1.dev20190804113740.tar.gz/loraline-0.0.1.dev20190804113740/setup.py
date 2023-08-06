
from setuptools import setup, find_packages
from loraline.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='loraline',
    version=VERSION,
    description='Loraline configures LoRaWAN transceivers to host devices',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Alexandros Antoniades',
    author_email='alex.rogue.antoniades@gmail.com',
    url='https://github.com/alexantoniades/loraline',
    license='Apache 2.0',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'loraline': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        loraline = loraline.main:main
    """,
)
