from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='wswhl',
    version='0.1.0',
    description='Where Shall We Have Lunch',
    long_description=readme,
    author='Christopher Doyle',
    author_email='christophercormac@outlook.com',
    url='https://github.com/christopherdoyle/wswhl',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

