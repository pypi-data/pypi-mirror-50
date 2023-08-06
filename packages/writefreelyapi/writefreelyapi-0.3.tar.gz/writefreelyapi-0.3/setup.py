from setuptools import setup

setup(
    name='writefreelyapi',
    version='0.3',
    author="CJ Eller",
    author_email="cjeller1592@gmail.com",
    description="An API client library for WriteFreely",
    license="MIT",
    py_modules=["writefreely", "uri", "posts", "user", "collection", "reader"],
    install_requires=["requests"],
    url="https://github.com/cjeller1592/Writeas-API",
 )
