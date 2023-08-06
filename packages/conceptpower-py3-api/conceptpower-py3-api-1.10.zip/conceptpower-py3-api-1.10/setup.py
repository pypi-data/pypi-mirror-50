from distutils.core import setup

DISTNAME = 'conceptpower-py3-api'
AUTHOR = 'E. Peirson, Digital Innovation Group @ ASU'
AUTHOR_EMAIL = '"E. Peirson" <erick.peirson@asu.edu>'
MAINTAINER = 'T. Quinn Digital Innovation Group @ ASU'
MAINTAINER_EMAIL = '"T. Quinn" <tjquinn1@asu.edu>'
DESCRIPTION = ('A very simple library for querying a Conceptpower REST API.')
LICENSE = 'GNU GPL 3'
URL = 'https://github.com/tjquinn1/Conceptpower-API'
VERSION = '1.10'

PACKAGES = [ 'conceptpower',]

setup(
    name=DISTNAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    url=URL,
    version=VERSION,
    packages = PACKAGES,
    install_requires=[
        "requests",
    ],
)
