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
