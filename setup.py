from setuptools import setup
import os

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_requires = [] # Examples: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(
    name='coding_raymondcentral_nichols_2020',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Connor Nichols',
    author_email='',
    description=''
)
