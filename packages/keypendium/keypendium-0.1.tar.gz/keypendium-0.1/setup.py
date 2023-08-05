from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='keypendium',
    version='0.1',
    author='Andrew Wilcox',
    author_email='andrew.wilcox0@gmail.com',
    description='A Wrapper for the keyforge-compendium.com API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=['keypendium']
)
