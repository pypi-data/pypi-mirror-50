import re

from setuptools import setup, find_packages


install_requires = ["boto3==1.9.196", "click==7.0", "requests-aws4auth==0.9"]

tests_requires = [
    "flake8==3.7.8",
    "isort==4.3.21",
    "pytest==5.0.1",
    "pytest-cov==2.7.1",
]

with open("README.md") as fh:
    long_description = re.sub(
        "<!-- start-no-pypi -->.*<!-- end-no-pypi -->\n",
        "",
        fh.read(),
        flags=re.M | re.S,
    )

setup(
    name="aws-es-query",
    version="0.2.0",
    author="Lab Digital B.V.",
    author_email="opensource@labdigital.nl",
    url="https://www.github.com/labd/aws-es-query/",
    description="Query tool for AWS ElasticSearch using IAM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    py_modules=["aws_es_query"],
    install_requires=install_requires,
    tests_require=tests_requires,
    extras_require={"test": tests_requires},
    entry_points={"console_scripts": {"aws-es-query=aws_es_query:main"}},
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
