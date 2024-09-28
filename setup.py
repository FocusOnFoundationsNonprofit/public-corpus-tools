from setuptools import setup, find_packages

# Read the contents of your requirements file
with open('dependencies/requirements_2024-09-26_add.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='corpus-tools',
    version='1.0',
    packages=find_packages(),
    install_requires=requirements,  # Use the requirements read from the file
)

# Terminal commands
'''
/usr/local/opt/python@3.11/bin/python3.11 -m venv .venv
source .venv/bin/activate
pip install -e .

To delete the virtual environment, run the following commands:
deactivate
rm -rf .venv
'''

