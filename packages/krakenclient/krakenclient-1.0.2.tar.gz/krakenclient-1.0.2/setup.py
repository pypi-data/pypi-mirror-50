from setuptools import setup
# from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


INSTALL_REQUIRE = [
	'krakenex==2.1.0'
]

setup(
    name='krakenclient',
    version='1.0.2',
    packages=['krakenclient'],
    url='https://github.com/ApacheDatastreams/krakenclient',
    license='MIT',
    author='Apache Datastreams',
    author_email='admin@apachedatastreams.com',
    description='A simple Kraken client API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires=">=3",
    install_requires=INSTALL_REQUIRE,
    classifiers = [
                  "Programming Language :: Python :: 3",
                  "License :: OSI Approved :: MIT License",
                  "Operating System :: OS Independent",
              ]
)


