import unittest

from keypendium import KeyforgeCompendium

key = 'e581d2b73e329a2abfb866d5741eb9d99297e148'
secret = '4a68cc1b179f2ab09390f252224d1a4f1ba992308c6976cb13cd792a491bf700d721b5948c332e3c'

def initialize():
    """
    Sets up a KeyforgeCompendium object for use in testing.

    Args:
        key (str): API key from keyforge-compendium.com
        secret (str): API secret from keyforge-compendium.com

    Return:
        Instance of the KeyforgeCompendium API Wrapper
    """

    return KeyforgeCompendium(key, secret)

class CardsClassTest(unittest.TestCase):
    def test_no_parameters(self):
        kfc = initialize()
        response = kfc.Cards()
        self.assertTrue(all(isinstance(x.title, str) for x in response))

    def test_card_id(self):
        kfc = initialize()
        response = kfc.Cards(card_id='1')
        self.assertTrue(response[0].title == 'Anger')
        self.assertTrue(len(response) == 1)

    def test_set_id(self):
        kfc = initialize()
        response = kfc.Cards(set_id='1')
        response2 = kfc.Cards(set_id='2')
        self.assertTrue(len(response) == 370)
        self.assertTrue(len(response) == 370)

    def test_card_id_set_id(self):
        kfc = initialize()
        response = kfc.Cards(card_id='1', set_id='2')
        self.assertTrue(response[0].title == '1-2 Punch')

class DecksClassTest(unittest.TestCase):
    def test_no_parameters(self):
        kfc = initialize()
        response = kfc.Decks()
        self.assertTrue(len(response) > 0)
        self.assertTrue(all(isinstance(x.name, str) for x in response))

    def test_deck_name(self):
        kfc = initialize()
        response = kfc.Decks(deck_name="Test")
        self.assertTrue(all("test" in x.name.lower() for x in response))

    def test_deck_page_id(self):
        kfc = initialize()
        response = kfc.Decks(page_id=1)
        response2 = kfc.Decks(page_id=2)

        self.assertTrue(len(response) - 10 == len(response2))
        self.assertTrue(response != response2)
        self.assertTrue(all(x.name != response[0].name for x in response2))

    def test_deck_name_deck_page_id(self):
        kfc = initialize()
        response = kfc.Decks(deck_name="Test")
        response2 = kfc.Decks(deck_name="Test", page_id=2)

        self.assertTrue(len(response) - 10 == len(response2))
        self.assertTrue(response != response2)
        self.assertTrue(all(x.name != response[0].name for x in response2))

class DeckClassTest(unittest.TestCase):
    def test_no_parameters(self):
        kfc = initialize()
        response = kfc.Deck()
        response2 = kfc.Decks()

        self.assertTrue(response[0].name == response2[0].name)

    def test_deck_id(self):
        kfc = initialize()
        response = kfc.Deck('989b8ca3-3190-4fd0-9478-217bcc95e7f3')

        self.assertTrue(response[0].name == 'Bronson "Ens. Diesel" Walbert')

class RandomDeck(unittest.TestCase):
    def test_no_parameters(self):
        kfc = initialize()
        response = kfc.RandomDeck(None)

        self.assertTrue(len(response) == 5)

    def test_num(self):
        kfc = initialize()
        response = kfc.RandomDeck(4)

        self.assertTrue(len(response) == 4)

if __name__ == '__main__':
    unittest.main()
