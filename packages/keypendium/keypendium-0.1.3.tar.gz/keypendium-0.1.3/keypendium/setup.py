from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='keypendium',
    version='0.1.4',
    author='caerulius',
    author_email='cae@polywhack.com',
    description='A Wrapper for the keyforge-compendium.com API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['keypendium'],
    test_suite='test.py'
)
