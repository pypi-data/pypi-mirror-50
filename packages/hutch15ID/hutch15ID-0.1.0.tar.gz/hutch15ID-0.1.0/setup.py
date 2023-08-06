from setuptools import setup, find_packages

setup(
    name = 'hutch15ID',
    version = '0.1.0',
    keywords='reflectometer, interface, bulk, beam',
    description = 'In this library, you can find anything in the hutch of sector 15ID-C',
    license = 'MIT License',
    url = 'https://github.com/zhul9311/hutch15ID.git',
    author = 'Zhu Liang',
    author_email = 'zliang8@uic.edu',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)