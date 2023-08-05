from setuptools import setup, find_packages
#from pip.req import parse_requirements
#https://stackoverflow.com/questions/25192794/no-module-named-pip-req

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

with open("README.rst") as file:
    long_description = file.read()

install_reqs = parse_requirements('requirements.txt')
reqs = install_reqs
# REFERENCE:
# http://stackoverflow.com/questions/14399534/how-can-i-reference-requirements-txt-for-the-install-requires-kwarg-in-setuptool

setup(
    name = 'dictsheet',
    version = '0.0.11',
    keywords = ('dictsheet', 'spreadsheet', 'gspread'),
    description = 'Dict wrapper for google spreadsheet',
    license = 'MIT License',
    install_requires = reqs,
    data_files = ['requirements.txt', 'README.md', 'LICENSE.txt'],
    url = 'https://github.com/previa/dictsheet',
    long_description = long_description,
    author = 'Chandler Huang, Xander Li',
    author_email = 'previa@gmail.com',
    
    packages = find_packages(),
    platforms = 'any',
    classifiers = [
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
)
