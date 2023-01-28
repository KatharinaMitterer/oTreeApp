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


def anzahl_spieler(subsession):
    #Anzahl der Spieler, die bisher and der Umfrage teilgenommen haben, d.h. schaetzfrage 2 beantwortet hatten
    anzahl = 0
    for player in subsession.get_players():
        if player.schaetzfrage2 != 0:
            anzahl += 1
    return anzahl


def plot_data_Ergebnisse1(subsession, player):

    plt.figure(figsize=(16, 8))

    # Zähle die Anzahl der Antworten für jede Antwortmöglichkeit
    schaetzfrage1_antworten=[]
    schaetzfrage1_antworten_besorgter_teilnehmer = []
    schaetzfrage1_antworten_unbesorgter_teilnehmer = []

    # Holt Antworten der Vorab-Frage 1 und Schaetzfrage1

    for p in subsession.get_players():
        if p.schaetzfrage1 != 0:
            #Sammeln der Antworten aller Teilnehmer für Histogram:
            schaetzfrage1_antworten.append(p.schaetzfrage1)
            #Aufteilung Teilnehmer in besorgt und unbesorgt
            if p.frage1 == '1' or p.frage1 == '2':
                schaetzfrage1_antworten_besorgter_teilnehmer.append(p.schaetzfrage1)
            if p.frage1 == '3' or p.frage1 == '4':
                schaetzfrage1_antworten_unbesorgter_teilnehmer.append(p.schaetzfrage1)

    durchschnitt_besorgter_teilnehmer = np.mean(schaetzfrage1_antworten_besorgter_teilnehmer)
    durchschnitt_unbesorgter_teilnehmer = np.mean(schaetzfrage1_antworten_unbesorgter_teilnehmer)

    # Histogramm erstellen
    n, bins, patches = plt.hist(schaetzfrage1_antworten, bins=range(0, 101, 5), color='blue', align='mid')

    #eigene Antwort des Spielers hellblau färben
    value_bin = next(idx for idx, val in enumerate(bins) if val > player.schaetzfrage1)
    patches[value_bin - 1].set_fc('lightblue')

    # richtige Antwort als grüner Strich
    plt.axvline(60, color='green', linewidth=2, label='Richtige ANtwort')

    plt.annotate(text='Richtige Antwort',
                 xy=(60, n.max()),
                 xytext=(60 - 9, n.max()*1.1), color='green',
                 arrowprops=dict(facecolor='green', shrink=0.05), size=15, zorder=10)

    #Zeichnet roten Strich durch die Mitte des Balkens mit dem Durschnitt der nicht besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_unbesorgter_teilnehmer >= bins[i]) and (durchschnitt_unbesorgter_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='red', linewidth=2)
            plt.annotate(text='Mittelwert der Teilnehmer*innen die\nüber Klimawandel nicht besorgt sind', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 20, n.max() * 1.2), color='red',
                         arrowprops=dict(facecolor='red', shrink=0.05), size=15, zorder=5)
            break

    # Zeichnet orangen Strich durch die Mitte des Balkens mit dem Durschnitt der besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_besorgter_teilnehmer >= bins[i]) and (durchschnitt_besorgter_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='orange', linewidth=2)
            plt.annotate(text='Mittelwert der Teilnehmer*innen die\nüber Klimawandel besorgt sind ', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 20, n.max() * 1.2), color='orange',
                         arrowprops=dict(facecolor='orange', shrink=0.05), size=15, zorder=5)
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
    return schaetzfrage1_antworten, schaetzfrage1_antworten_besorgter_teilnehmer, schaetzfrage1_antworten_unbesorgter_teilnehmer, player.frage1

def plot_data_Ergebnisse2(subsession, player):

    plt.figure(figsize=(16, 8))

    # Zähle die Anzahl der Antworten für jede Antwortmöglichkeit
    schaetzfrage2_antworten = []
    schaetzfrage2_antworten_positive_einstellung = []
    schaetzfrage2_antworten_negative_einstellung = []

    # Holt Antworten der Vorab-Frage 2 und Schaetzfrage2

    for p in subsession.get_players():
        if p.schaetzfrage2 != 0:
            # Sammeln der Antworten aller Teilnehmer für Histogram:
            schaetzfrage2_antworten.append(p.schaetzfrage2)
            # Aufteilung Teilnehmer in besorgt und unbesorgt
            if p.frage2 == '1' or p.frage2 == '2':
                schaetzfrage2_antworten_negative_einstellung.append(p.schaetzfrage2)
            if p.frage2 == '3' or p.frage2 == '4' :
                schaetzfrage2_antworten_positive_einstellung.append(p.schaetzfrage2)

    durchschnitt_negative_teilnehmer = np.mean(schaetzfrage2_antworten_negative_einstellung)
    durchschnitt_positive_teilnehmer = np.mean(schaetzfrage2_antworten_positive_einstellung)

    # Histogramm erstellen
    n, bins, patches = plt.hist(schaetzfrage2_antworten, bins=range(0, 101, 5), color='blue', align='mid')

    #eigene Antwort des Spielers hellblau färben
    value_bin = next(idx for idx, val in enumerate(bins) if val > player.schaetzfrage2)
    patches[value_bin - 1].set_fc('lightblue')

    # richtige Antwort als grüner Strich
    plt.axvline(60, color='green', linewidth=2)
    plt.annotate(text='Richtige Antwort',
                 xy=(7, n.max()),
                 xytext=(7 - 1, n.max()*1.1), color='green',
                 arrowprops=dict(facecolor='green', shrink=0.05), size=15, zorder=10)

    #Zeichnet roten Strich durch die Mitte des Balkens mit dem Durschnitt der nicht besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_negative_teilnehmer >= bins[i]) and (durchschnitt_negative_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='red', linewidth=2)
            plt.annotate(text='Mittelwert der Teilnehmer*innen die\nden Weiterbetreib von AKWs negativ sehen', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 20, n.max() * 1.2), color='red',
                         arrowprops=dict(facecolor='red', shrink=0.05), size=15, zorder=5)
            break

    # Zeichnet orangen Strich durch die Mitte des Balkens mit dem Durschnitt der besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_positive_teilnehmer >= bins[i]) and (durchschnitt_positive_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='orange', linewidth=2)
            plt.annotate(text='Mittelwert der Teilnehmer*innen die\nden Weiterbetreib von AKWs positiv sehen', xy=((bins[i] + bins[i + 1]) / 2, n.max()),
                         xytext=((bins[i] + bins[i + 1]) / 2 - 20, n.max() * 1.2), color='orange',
                         arrowprops=dict(facecolor='orange', shrink=0.05), size=15, zorder=5)
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
    plt.savefig('./_static/Bild_Ergebnisse2.pdf', format='pdf', bbox_inches='tight')
    return schaetzfrage2_antworten, schaetzfrage2_antworten_negative_einstellung, schaetzfrage2_antworten_positive_einstellung


class Player(BasePlayer):

    frage1 = models.StringField(initial=0,
        label='''
        1.) Auf einer Skala von 1-4 wie besorgt sind Sie über die Auswirkungen der Klimawandels auf unsere Umwelt und
         Gesellschaft?<br><br>
        ''',
        choices=[[1, '1 = Gar nicht besorgt'], [2, '2 = Eher nicht besorgt'], [3, '3 = Eher besorgt'], [4, '4 = Sehr besorgt']],
        widget=widgets.RadioSelectHorizontal,
    )
    frage2 = models.StringField(initial=0,
        label='''
        <br><br><br>
        2.) Auf einer Skala von 1-4, wie positiv stehen Sie einem Weiterbetrieb von Atomkraftwerken gegenüber?<br><br>''',
        choices=[['1', '1 = Sehr negativ'], ['2', '2 = Eher negativ'], ['3', '3 = Eher positiv'], ['4', '4 = Sehr positiv']],
        widget=widgets.RadioSelectHorizontal,
    )
    schaetzfrage1 = models.IntegerField(initial=0,
            label="Um wie viel Prozent schätzen Sie, haben die CO2-Emissionen weltweit \
            seit 1990 zugenommen (Stand Ende 2021)?",
            min=0
    )
    schaetzfrage2 = models.IntegerField(initial=0,
         label="Wie hoch schätzen die den Beitrag von Atomkraftwerken (AKWs)\
         zu unserem Strommix in Deutschland (in Prozent)?", min=0, max=100
    )

# FUNCTIONS
# PAGES
class Anweisung(Page):
    pass

class Vorab_Fragen(Page):
    form_model = 'player'
    form_fields = ['frage1', 'frage2']

class Schaetzfrage1(Page):
    form_model = 'player'
    form_fields = ['schaetzfrage1']

class Schaetzfrage2(Page):
    form_model = 'player'
    form_fields = ['schaetzfrage2']


class Ergebnisse1(Page):
    @staticmethod
    def vars_for_template(player: Player):
        plot_data_Ergebnisse1(player.subsession, player)
        return dict(
            schaetzfrage1_antwort=player.schaetzfrage1,
            differenz_prozentpunkte_schaetzfrage1=abs(60 - player.schaetzfrage1),
            anzahl_bisheriger_teilnehmer=anzahl_spieler(player.subsession),
            hallo=plot_data_Ergebnisse1(player.subsession, player))


class Ergebnisse2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        plot_data_Ergebnisse2(player.subsession, player)
        return dict(schaetzfrage2_antwort=player.schaetzfrage2,
                differenz_prozentpunkte_schaetzfrage2=abs(7 - player.schaetzfrage2),
                anzahl_bisheriger_teilnehmer=anzahl_spieler(player.subsession))


class Ende(Page):
    pass


page_sequence = [Anweisung, Vorab_Fragen, Schaetzfrage1, Schaetzfrage2, Ergebnisse1, Ergebnisse2, Ende]
