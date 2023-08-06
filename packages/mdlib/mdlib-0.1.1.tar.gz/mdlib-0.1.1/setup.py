from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'mdlib',
    version = '0.1.1',
    keywords='markdown',
    description = 'A lib for markdown.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    license = 'MIT License',
    url = 'https://github.com/Lavender-Tree/mdlib',
    author = 'Lavender Tree',
    author_email = 'lavender.tree9988@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
)