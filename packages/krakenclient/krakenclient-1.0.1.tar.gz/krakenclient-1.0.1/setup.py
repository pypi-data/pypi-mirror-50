import setuptools
from distutils.core import setup

INSTALL_REQUIRE = [
	'krakenex==2.1.0'
]

setup(
    name='krakenclient',
    version='1.0.1',
    packages=['krakenclient'],
    url='https://github.com/ApacheDatastreams/krakenclient',
    license='MIT',
    author='Apache Datastreams',
    author_email='admin@apachedatastreams.com',
    description='A simple Kraken client API',
    python_requires=">=3",
    install_requires=INSTALL_REQUIRE
)


