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
