from setuptools import setup
import os

working_dir = os.path.dirname(os.path.realpath(__file__))
requirementPath = working_dir + '/requirements.txt'
install_requires = []
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()
setup(
    name='coding_raymondcentral_nichols_2020',
    install_requires=install_requires,
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Connor Nichols',
    author_email='',
    description=''
)
