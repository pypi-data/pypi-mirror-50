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
