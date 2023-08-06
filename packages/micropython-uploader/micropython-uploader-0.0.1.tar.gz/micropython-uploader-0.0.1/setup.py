from setuptools import setup, find_packages

with open("README.md") as f:
    longDescr = f.read()

setup(
    name='micropython-uploader',
    version='0.0.1',
    packages=find_packages(),
    author='Alex Yurev',
    author_email='sapfir999999@yandex.ru',
    long_description=longDescr,
    url='https://github.com/Sapfir0/micropython-uploader',
)


