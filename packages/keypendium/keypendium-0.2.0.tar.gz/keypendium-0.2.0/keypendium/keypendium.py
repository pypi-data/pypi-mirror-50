#!/usr/bin/env python

"""
Keyforge Compendium API: https://keyforge-compendium.com/docs
"""

import requests
import json
from requests.auth import HTTPBasicAuth

class Card:
    """
    Card model object representing a Card returned from the Cards
    endpoint. Each data point can be accessed as a property, and
    by spec each should be present, even if with None as data. (i.e.
    accessing these should be safe from KeyNotFoundExceptions)

    Args:
        data (json object): Json object representing a single card
    """
    def __init__(self, data):
        self.json = data

    @property
    def title(self):
        return self.json['title']

    @property
    def number(self):
        return self.json['number']

    @property
    def is_maverick(self):
        return self.json['is_maverick']

    @property
    def card_type(self):
        return self.json['card_type']

    @property
    def front_image(self):
        return self.json['front_image']

    @property
    def text(self):
        return self.json['text']

    @property
    def traits(self):
        return self.json['traits']

    @property
    def rarity(self):
        return self.json['rarity']

    @property
    def artist(self):
        return self.json['artist']

    @property
    def house_name(self):
        return self.json['house_name']

    @property
    def amber(self):
        return self.json['amber']

    #alias for the amber property
    @property
    def aember(self):
        return self.amber

    @property
    def power(self):
        return self.json['power']

    @property
    def armor(self):
        return self.json['armor']

    @property
    def cards_decks_count(self):
        return self.json['cards_decks_count']

    @property
    def faqs(self):
        if self.json['faqs'] is []:
            return None
        else:
            return [FAQ(x) for x in self.json['faqs']]
        
    @property
    def tags(self):
        if self.json['tags'] is []:
            return None
        else:
            return [Tag(x) for x in self.json['tags']]

class Deck:
    """
    Deck model object representing a Deck returned from the Decks
    endpoint. Each data point can be accessed as a property, and
    by spec each should be present, even if with None as data. (i.e.
    accessing these should be safe from KeyNotFoundExceptions)

    Args:
        data (json object): Json object representing a single deck
    """
    def __init__(self, data):
        self.json = data

    @property
    def name(self):
        return self.json['name']

    @property
    def uuid(self):
        return self.json['uuid']

    @property
    def a_rating(self):
        return self.json['a_rating']

    @property
    def b_rating(self):
        return self.json['b_rating']

    @property
    def c_rating(self):
        return self.json['c_rating']

    @property
    def e_rating(self):
        return self.json['e_rating']

    @property
    def consistency_rating(self):
        return self.json['consistency_rating']

    @property
    def creature_count(self):
        return self.json['creature_count']

    @property
    def action_count(self):
        return self.json['action_count']

    @property
    def artifact_count(self):
        return self.json['artifact_count']

    @property
    def upgrade_count(self):
        return self.json['upgrade_count']

    @property
    def uncommon_count(self):
        return self.json['uncommon_count']

    @property
    def common_count(self):
        return self.json['common_count']

    @property
    def rare_count(self):
        return self.json['rare_count']

    @property
    def fixed_count(self):
        return self.json['fixed_count']

    @property
    def variant_count(self):
        return self.json['variant_count']

    @property
    def maverick_count(self):
        return self.json['maverick_count']

    @property
    def sas_rating(self):
        return self.json['sas_rating']

    @property
    def cards_rating(self):
        return self.json['cards_rating']

    @property
    def synergy_rating(self):
        return self.json['synergy_rating']

    @property
    def house_names(self):
        return self.json['house_names']

    @property
    def cards(self):
        return [Card(x) for x in self.json['cards']]

class FAQ:
    """
    FAQ model object representing a single FAQ. FAQs are found on cards
    and represent commonly asked questions about rules or corner cases.
    A list of these (with any length, including 0) is present on each
    Card object. The question and answer properties are the meat of the
    FAQ object.

    Args:
        data (json object): Json object representing a single faq
    """
    def __init__(self, data):
        self.json = data

    @property
    def id(self):
        return self.json['id']

    @property
    def question(self):
        return self.json['question']

    @property
    def answer(self):
        return self.json['answer']

    @property
    def card_id(self):
        return self.json['card_id']

    @property
    def created_at(self):
        return self.json['created_at']

    @property
    def updated_at(self):
        return self.json['updated_at']

    @property
    def rule_source_id(self):
        return self.json['rule_source_id']

    @property
    def source_id(self):
        return self.json['source_id']

    @property
    def rule_id(self):
        return self.json['rule_id']

class Tag:
    """
    Tag model object representing a single Tag. Tags are found on cards
    and represent categorizations for kinds of cards. These are a list
    of meta information about cards maintained by the Keyforge Compendium
    team. Examples include 'AEmber bonus' or 'Actions'. A list of these
    (with any length, including 0) is present on each Card object.
    Args:
        data (json object): Json object representing a single tag
    """
    def __init__(self, data):
        self.json = data

    @property
    def id(self):
        return self.json['id']

    @property
    def name(self):
        return self.json['name']

    @property
    def description(self):
        return self.json['description']

    @property
    def hide_by_default(self):
        return self.json['hide_by_default']

    @property
    def created_at(self):
        return self.json['created_at']

    @property
    def updated_at(self):
        return self.json['updated_at']


class KeyPendium:
    """
    Simple Python wrapper for the Keyforge Compendium API.

    >>> KeyforgeCompendium('apikey', 'secret').Cards()

    """
    def __init__(self, key, secret):
        self.baseUrl = "https://keyforge-compendium.com/api/v1/"
        self.cardsUrl = "cards/{}"
        self.setsUrl = "sets/{}/cards/{}"
        self.decksUrlById = "decks/{}"
        self.decksUrlPaged = "decks?page_id={}"
        self.decksUrlByName = "decks/by_name/{}?page_id={}"
        self.decksUrlRandom = "decks/random/{}"
    
        self.key = key
        self.secret = secret

        self.basicAuth = HTTPBasicAuth(self.key, self.secret)
    
    def Cards(self, card_id=None, set_id=None):
        """
        Wrapper around the Cards API endpoint. Retrieves information
        about individual Keyforge cards. Calling this function without
        a card_id but WITH a set_id will return all cards for that set.
        Calling this endpoint without either parameter will return all
        cards in the default Call of the Archons set.

        Args:
            card_id (int) (optional): An individual card's id
            set_id (int) (optional): A set id. As of this writing (7/2/19)
                                     the only valid options are 1 and 2.

        Returns:
            List of Card objects. In the case that a card_id is passed in,
            a list of length one is returned.
        """
        
        if set_id is None:
            if card_id is None:
                return [Card(x) for x in self.MakeRequest(self.cardsUrl, [''])]
            else:
                return [Card(self.MakeRequest(self.cardsUrl, [card_id]))]
        else:
            if card_id is None:
                return [Card(x) for x in self.MakeRequest(self.setsUrl, [set_id, ''])]
            else:
                return [Card(self.MakeRequest(self.setsUrl, [set_id, card_id]))]

    def Decks(self, deck_name=None, page_id=None):
        """
        Wrapper around the Decks API endpoint. Retrieves information
        about publicly registered Keyforge Decks. Calling this endpoint
        without a page_id will return the first 10 pages of
        results. The deck_name parameter allows for name searching and requires
        a query string of at least 4 characters.

        Args:
            deck_name (str) (optional): The deck name search query string
            page_id (int) (optional): The page of results to retrieve. The API
                                      does not at this time provide information
                                      about your current page or the number of total
                                      pages, so you'll have to track these manually

        Returns:
            List of Deck objects.
        """
        results = []
        if page_id is None:
            page_id = 1

        if deck_name is None:
            active_url = self.decksUrlPaged
            params = [page_id]
        else:
            active_url = self.decksUrlByName
            params = [deck_name, page_id]

        response = [Deck(x) for x in self.MakeRequest(active_url, params)]
        results = results + response
        while len(response) > 0 and params[len(params)-1] < 10:
            params[len(params)-1] = params[len(params)-1] + 1
            response = [Deck(x) for x in self.MakeRequest(active_url, params)]
            results = results + response

        return results

    def Deck(self, deck_id=None):
        """
        Wrapper around the Decks API endpoint, specifically the functionality
        to retrieve a single deck by deck UUID. Calling this endpoint without
        a deck_id simply returns the very first public deck.

        Args:
            deck_id (uuid as str) (optional): The UUID for the deck. This can be found within
            the Decks API or on the main Keyforge site for a given deck.

        Returns;
            List containing a single Deck object.
        """
        if deck_id is None:
            return [self.Decks()[0]]
        return [Deck(self.MakeRequest(self.decksUrlById, [deck_id]))]

    def RandomDeck(self, num):
        """
        Wrapper around the Decks API endpoint, specifically the get random
        decks functionality. Note that if a high enough number is passed in this
        response will be paged. Since the values are random anyways, calling this
        function multiple times intead of using pagination is encouraged.

        Args:
            num (int): The number of random decks to return

        Returns:
            List of Deck objects.
        
        """
        if num is None:
            num = 5
        return [Deck(x) for x in self.MakeRequest(self.decksUrlRandom, [num])]

    def MakeRequest(self, url, params):
        """
        Helper function to abstract out the api calls to the Keyforge Compendium API.

        Args:
            url (str): The formatted url (containing {} for data insertion) to query
            params (list): A list of strings to format into the url string

        Returns:
            JSON object of the results
        """
        fullUrl = self.baseUrl + url.format(*params)
        test = json.loads(requests.get(fullUrl, auth=self.basicAuth).content)
        return test
