from setuptools import setup

setup(
    name='writeasapi',
    version='0.1.9.4.5',
    author="CJ Eller",
    author_email="cjeller1592@gmail.com",
    description="An API client library for Write.as",
    license="MIT",
    py_modules=["writeas", "uri", "posts", "wauser", "collection", "readwa"],
    install_requires=["requests"],
    url="https://github.com/cjeller1592/Writeas-API",
 )
