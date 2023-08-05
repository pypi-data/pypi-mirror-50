keypendium.py
=============

`keypendium` is an easy to use python wrapper for the [Keyforge Compendium API](http://keyforge-compendium). Head to the site, register, and request an api key to get started.

Installation
------------
Download using the `pip` installer:

	pip install keypendium

or download the source from git

	git clone https://github.com/caerulius/keypendium.git

Usage
-----

```from keypendium import Keypendium
myapi = Keypendium('my_api_key', 'my_secret')
myapi.Cards()
```