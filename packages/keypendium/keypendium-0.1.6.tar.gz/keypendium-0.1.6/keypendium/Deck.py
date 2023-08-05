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
