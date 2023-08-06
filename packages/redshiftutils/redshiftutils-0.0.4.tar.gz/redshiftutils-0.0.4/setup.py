import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redshiftutils",
    version="0.0.4",
    author="Jos de Weger",
    author_email="info@josdeweger.nl",
    description="Simple psycopg2 wrapper for querying / updating Redshift",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/redhotminute",
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3',
        'psycopg2-binary',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)