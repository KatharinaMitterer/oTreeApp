from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'umfrage_gruppe3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label='Wie alt bist du?', min=13, max=125)
    gender = models.StringField(
        choices=[['Male', 'männlich'], ['Female', 'weiblich']],
        label='Was ist dein Geschlecht?',
        widget=widgets.RadioSelect,
    )
    frage1 = models.StringField(
        label='''
        Auf einer Skala von 1-6, wie besorgt sind Sie über die 
        Auswirkungen der Klimaerwärmung auf unsere Umwelt und Gesellschaft?''',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6']],
        widget=widgets.RadioSelectHorizontal,
    )
    frage2 = models.StringField(
        label='''
        Wie wahrscheinlich ist es, dass die 
        Klimaerwärmung hauptsächlich von menschgemachten Aktivitäten verursacht wird?
        ''',
        choices=['A) Sehr unwahrscheinlich', 'B) Eher unwahrscheinlich', 'C) Eher wahrscheinlich', 'D) Sehr wahrscheinlich'],
        widget=widgets.RadioSelect,
    )
    frage3 = models.IntegerField(
        label='''
        Auf einer Skala von 1-6, wie oft schauen Sie sich Fußballspiele 
        an, einschließlich der Weltmeisterschaft?''',
        choices=[['1', '1'], ['2', '2'], ['3', '3'], ['4', '4'], ['5', '5'], ['6', '6']],
        widget=widgets.RadioSelectHorizontal,
    )


# FUNCTIONS
# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['age', 'gender']


class Frage1(Page):
    form_model = 'player'
    form_fields = ['frage1']

class Frage2(Page):
    form_model = 'player'
    form_fields = ['frage2']

class Frage3(Page):
    form_model = 'player'
    form_fields = ['frage3']


page_sequence = [Demographics, Frage1, Frage2, Frage3]
