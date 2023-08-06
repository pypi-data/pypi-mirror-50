from setuptools import setup, find_packages
import pathlib

a = pathlib.Path(__file__).parent

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup(
    name='carsharefile',
    version='0.2',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    author='Sam Rubanowitz',
    packages=find_packages(),
    author_email='therealsamurban@gmail.com',
    description='Python Package that provides easy interaction with the ShareFile API.',
    install_requires=["http", "mimetypes", "urllib"]
)
