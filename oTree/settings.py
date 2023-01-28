"""
running server:
cd <path to settings.py>
otree devserver
"""



from os import environ


SESSION_CONFIGS = [
    dict(
        name='Umfrage', app_sequence=['umfrage_gruppe3'], num_demo_participants=4
    ),
    dict(name='common_value_action',
        display_name="common_value_action",
        app_sequence=['common_value_auction'],
        num_demo_participants=3)]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [
    dict(name='umfrage_gruppe3', display_name='Umfrage'),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Wilkommen zum Demo der Umfrage von Gruppe 3! 
"""


SECRET_KEY = '{{ secret_key }}'

INSTALLED_APPS = ['otree']
