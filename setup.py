from setuptools import setup, find_packages

DESC = 'An example application for demonstrating TDD'

setup(
    name='insectipy',

    description=DESC,
    long_description=DESC,

    url='https://github.com/LocustSPW/insectipy',

    author='Jeremy Huntwork',
    author_email='jhuntwork@lightcubesolutions.com',

    version='0.1',
    zip_safe=True,

    packages=find_packages(exclude=['tests'])
)
