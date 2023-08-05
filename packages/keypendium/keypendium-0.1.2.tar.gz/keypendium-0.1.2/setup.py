from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='keypendium',
    version='0.1.2',
    author='caerulius',
    author_email='cae@polywhack.com',
    description='A Wrapper for the keyforge-compendium.com API',
    long_description=long_description,
    scripts=['keypendium']
)
