from otree.api import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import threading

class C(BaseConstants):
    NAME_IN_URL = 'umfrage_gruppe3'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


def get_number_current_players(group: Group):
    def count_voters(self):
        return sum([p.has_voted for p in self.get_players()])



def plot_data_Ergebnisse1(group):

    plt.figure(figsize=(16, 8))
    players = group.get_players()
    schaetzfrage1_antworten=[]
    # Zähle die Anzahl der Antworten für jede Antwortmöglichkeit
    schaetzfrage1_antworten_besorgter_teilnehmer = []
    schaetzfrage1_antworten_unbesorgter_teilnehmer = []

    # Holt Antworten der Vorab-Frage 1 und Schaetzfrage1
    for p in players:
        if p.schaetzfrage1 != None:
            schaetzfrage1_antworten.append(p.schaetzfrage1)

    for p in group.get_players():
        #besorgeter Teilnehmer
        if p.frage1 in [1,2]:
            schaetzfrage1_antworten_besorgter_teilnehmer.append(p.schaetzfrage1)
        if p.frage1 in[3,4]:
            schaetzfrage1_antworten_unbesorgter_teilnehmer.append(p.schaetzfrage1)

    durchschnitt_besorgter_teilnehmer = np.mean(schaetzfrage1_antworten_besorgter_teilnehmer)
    durchschnitt_unbesorgter_teilnehmer = np.mean(schaetzfrage1_antworten_unbesorgter_teilnehmer)

    # Histogramm erstellen
    n, bins, patches = plt.hist(schaetzfrage1_antworten, bins=range(0, 101, 5), color='blue', align='mid')

    # Balken im Intervall von 56 bis 60 grün färben
    patches[11].set_fc('green')

    value_bin = next(idx for idx, val in enumerate(bins) if val > player.schaetzfrage1)
    patches[value_bin - 1].set_fc('lightblue')

    #Zeichnet roten Strich durch die Mitte des Balkens mit dem Durschnitt der nicht besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_unbesorgter_teilnehmer >= bins[i]) and (durchschnitt_unbesorgter_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='red', linewidth=2)
            plt.annotate(s='Mittelwert der Teilnehmer*innen die über Klimawandel nicht besorgt sind', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 5, n.max() * 1.1),
                         arrowprops=dict(facecolor='red', shrink=0.05))
            break

    # Zeichnet orangen Strich durch die Mitte des Balkens mit dem Durschnitt der besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_besorgter_teilnehmer >= bins[i]) and (durchschnitt_besorgter_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='orange', linewidth=2)
            plt.annotate(s='Mittelwert der Teilnehmer*innen die über Klimawandel besorgt sind ', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 5, n.max() * 1.1),
                         arrowprops=dict(facecolor='orange', shrink=0.05))
            break


    # nur ganzzahlige Zahlen für y-Achse anzeigen
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    #Erzeugung der Achsenbeschriftungen für x als Intervalle
    plt.xticks(range(0, 101, 5), size=12)
    plt.yticks(size=12)


    # Achsenbeschriftung hinzufügen
    plt.xlabel('Geschätze Prozentzahl [%]', size=16)
    plt.ylabel('Anzahl der Schätzungen', size=16)

    # Bild speichern
    plt.savefig('./_static/Bild_Ergebnisse1.pdf', format='pdf', bbox_inches='tight')

def plot_data_Ergebnisse2(group):

    plt.figure(figsize=(16, 8))

    # Holt Antworten der Schaetzfrage2
    schaetzfrage2_antworten = [p.schaetzfrage2 for p in group.get_players()]

    # Aufteilung in Teilnehmer die dem Weiterbetrieb von AKWs positiv gegenüber stehen und jene die eine negativ

    schaetzfrage2_antworten_positive_einstellung=[]
    schaetzfrage2_antworten_negative_einstellung=[]

    for p in group.get_players():
        if p.frage2 in [1,2]:
            schaetzfrage2_antworten_negative_einstellung.append(p.schaetzfrage2)
        if p.frage2 in[3,4]:
            schaetzfrage2_antworten_positive_einstellung.append(p.schaetzfrage2)

    durchschnitt_positive_teilnehmer = np.mean(schaetzfrage2_antworten_positive_einstellung)
    durchschnitt_negative_teilnehmer = np.mean(schaetzfrage2_antworten_negative_einstellung)

    # Histogramm erstellen
    n, bins, patches = plt.hist(schaetzfrage2_antworten, bins=range(0, 100, 2), color='blue')
    plt.xlim(2, 42)

    # Balken im Intervall von 7 bis 9 bis 60 grün färben
    patches[2].set_fc('green')

    value_bin = next(idx for idx, val in enumerate(bins) if val > player.schaetzfrage2)
    patches[value_bin - 1].set_fc('lightblue')

    #Zeichnet roten Strich durch die Mitte des Balkens mit dem Durschnitt der nicht besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_positive_teilnehmer >= bins[i]) and (durchschnitt_negative_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='red', linewidth=2)
            plt.annotate(s='Mittelwert der Teilnehmer*innen die über Klimawandel nicht besorgt sind', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 5, n.max() * 1.1),
                         arrowprops=dict(facecolor='red', shrink=0.05))
            break

    # Zeichnet orangen Strich durch die Mitte des Balkens mit dem Durschnitt der besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_positive_teilnehmer >= bins[i]) and (durchschnitt_negative_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='orange', linewidth=2)
            plt.annotate(s='Mittelwert der Teilnehmer*innen die über Klimawandel besorgt sind ', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 5, n.max() * 1.1),
                         arrowprops=dict(facecolor='orange', shrink=0.05))
            break

    # Achsenbeschriftung hinzufügen
    plt.xlabel('Geschätze Prozentzahl [%]')
    plt.ylabel('Anzahl der Schätzungen')
    # nur ganzzahlige Zahlen für y-Achse anzeigen
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Erzeugung der Achsenbeschriftungen für x als Intervalle
    # Erzeugung der Achsenbeschriftungen für x als Intervalle
    plt.xticks(range(0, 101, 5), size=12)
    plt.yticks(size=12)

    # Bild speichern
    plt.savefig('./_static/Bild_Ergebnisse2.pdf', format='pdf', bbox_inches='tight')


class Player(BasePlayer):

    frage1 = models.StringField(
        label='''
        1.) Auf einer Skala von 1-4 wie besorgt sind Sie über die Auswirkungen der Klimawandels auf unsere Umwelt und
         Gesellschaft?<br><br>
        ''',
        choices=[[1, '1 = Gar nicht besorgt'], [2, '2 = Eher nicht besorgt'], [3, '3 = Eher besorgt'], [4, '4 = Sehr besorgt']],
        widget=widgets.RadioSelectHorizontal,
    )
    frage2 = models.StringField(
        label='''
        <br><br><br>
        2.) Auf einer Skala von 1-4, wie positiv stehen Sie einem Weiterbetrieb von Atomkraftwerken gegenüber?<br><br>''',
        choices=[['1', '1 = Sehr negativ'], ['2', '2 = Eher negativ'], ['3', '3 = Eher positiv'], ['4', '4 = Sehr positiv']],
        widget=widgets.RadioSelectHorizontal,
    )
    frage3 = models.StringField(
        label='''
        <br><br><br>
        3.) Auf einer Skala von 1-4, wie positiv empfanden Sie die Austragung der Fußball-WM 2022 in Katar?<br><br>''',
        choices=[['1', '1 = Sehr negativ'], ['2', '2 = Eher negativ'], ['3', '3 = Eher positiv'], ['4', '4 = Sehr positiv']],
        widget=widgets.RadioSelectHorizontal,
    )
    schaetzfrage1 = models.IntegerField(
            label="Um wie viel Prozent schätzen Sie, haben die CO2-Emissionen weltweit \
            seit 1990 zugenommen (Stand Ende 2021)?",
            min=0, max=100
    )
    schaetzfrage2 = models.IntegerField(label = "Wie hoch schätzen die den Beitrag von Atomkraftwerken (AKWs)\
         zu unserem Strommix in Deutschland (in Prozent)?", min=0, max=100
    )
    schaetzfrage3 = models.IntegerField(label="Wie viele Arbeiter schätzen Sie sind im Rahmen der\
         WM-Vorbereitungen in Katar ums Leben gekommen?",
    )




# FUNCTIONS
# PAGES
class Anweisung(Page):
    pass

class Vorab_Fragen(Page):
    form_model = 'player'
    form_fields = ['frage1', 'frage2', 'frage3']

class Schaetzfrage1(Page):
    form_model = 'player'
    form_fields = ['schaetzfrage1']

class Schaetzfrage2(Page):
    form_model = 'player'
    form_fields = ['schaetzfrage2']

class Schaetzfrage3(Page):
    form_model = 'player'
    form_fields = ['schaetzfrage3']


class Ergebnisse1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        #plot_data_Ergebnisse1(player.group)
        return dict(
            schaetzfrage1_antwort=player.schaetzfrage1,
            differenz_prozentpunkte_schaetzfrage1=abs(60 - player.schaetzfrage1),
            anzahl_bisheriger_teilnehmer=len(player.in_all_rounds())
        )

class Ergebnisse2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        #plot_data_Ergebnisse2(player.group)
        return dict(schaetzfrage2_antwort=player.schaetzfrage2,
                differenz_prozentpunkte_schaetzfrage2=abs(7 - player.schaetzfrage2),
                anzahl_bisheriger_teilnehmer=get_number_current_players.count_voters(player.group),
                hallo=player)


class Ende(Page):
    pass


page_sequence = [Anweisung, Vorab_Fragen, Schaetzfrage1, Schaetzfrage2, Ergebnisse1, Ergebnisse2, Ende]
