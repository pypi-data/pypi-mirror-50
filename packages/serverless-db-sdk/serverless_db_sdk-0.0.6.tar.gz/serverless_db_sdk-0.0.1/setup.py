from setuptools import setup, find_packages


def requirements():

    with open('requirements.txt', 'r') as fileobj:
        requirements = [line.strip() for line in fileobj]
        return requirements


setup(
    name="serverless_db_sdk",
    version="0.0.1",
    keywords=("pip", "serverless", "serverless db", "serverless_db_sdk"),
    description="serverless_db_sdk",
    long_description="serverless_db_sdk for python",
    license="MIT Licence",

    url="http://qcloud.com",
    author="rangeli",
    author_email="709738544@qq.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pymysql"]
)
