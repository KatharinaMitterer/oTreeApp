from otree.api import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import threading

class C(BaseConstants):
    NAME_IN_URL = 'Experiment'
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
    #nur ein Spieler der Schätzfrage2 schon beantortet hat --> also IUnfrage vollständig ausgefüllt hat

    for p in subsession.get_players():
        if p.schaetzfrage2 != '':
            #Sammeln der Antworten aller Teilnehmer für Histogram:
            schaetzfrage1_antworten.append(float(p.schaetzfrage1))
            #Aufteilung Teilnehmer in besorgt und unbesorgt
            if p.frage1 == '1' or p.frage1 == '2':
                schaetzfrage1_antworten_besorgter_teilnehmer.append(float(p.schaetzfrage1))
            if p.frage1 == '3' or p.frage1 == '4':
                schaetzfrage1_antworten_unbesorgter_teilnehmer.append(float(p.schaetzfrage1))

    median_besorgter_teilnehmer = np.median(schaetzfrage1_antworten_besorgter_teilnehmer)
    median_unbesorgter_teilnehmer = np.median(schaetzfrage1_antworten_unbesorgter_teilnehmer)

    # Histogramm erstellen
    bins = [5, 15.5, 25.5, 35.5, 45.5, 55.5, 65.5, 75.5, 85.5, 95.5, 105.5, 110.5]
    bin_labels = ['0-10 %', '11-20 %', '21-30 %', '31-40 %', '41-50 %', '51-60 %', '61-70 %', '71-80 %', '81-90 %',
                  '91-100 %', '>100 %', '']

    n, bins, patches = plt.hist(schaetzfrage1_antworten, bins=bins, color='blue', align='left')

    plt.xticks(bins, bin_labels, rotation=45)


    value_bin = next(idx for idx, val in enumerate(bins) if val > float(player.schaetzfrage1))
    patches[value_bin - 1].set_fc('lightblue')

    # richtige Antwort als grüner Strich
    plt.axvline(65.5, color='green', linewidth=2, label='Richtige Antwort')
    for i in range(len(bins) - 1):
        if (median_besorgter_teilnehmer >= bins[i]) and (median_besorgter_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='orange', linewidth=2,
                        label='Median der gruppierten Daten von Teilnehmer*innen\n die über Klimawandel besorgt sind')
            break
    for i in range(len(bins) - 1):
        if (median_unbesorgter_teilnehmer >= bins[i]) and (median_unbesorgter_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='red', linewidth=2,
                        label='Median der gruppierten Daten von Teilnehmer*innen\ndie über Klimawandel nicht besorgt sind')
            break

    plt.legend(bbox_to_anchor=(0.5, -0.25), ncol=3, loc='lower center', fontsize=15)


    # nur ganzzahlige Zahlen für y-Achse anzeigen
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.yticks(size=12)


    # Achsenbeschriftung hinzufügen
    plt.xlabel('Geschätzte Prozentzahl [%]', size=16)
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
        if p.schaetzfrage2 != '':
            # Sammeln der Antworten aller Teilnehmer für Histogram:
            schaetzfrage2_antworten.append(float(p.schaetzfrage2))
            # Aufteilung Teilnehmer in besorgt und unbesorgt
            if p.frage2 == '1' or p.frage2 == '2':
                schaetzfrage2_antworten_negative_einstellung.append(float(p.schaetzfrage2))
            if p.frage2 == '3' or p.frage2 == '4':
                schaetzfrage2_antworten_positive_einstellung.append(float(p.schaetzfrage2))

    durchschnitt_negative_teilnehmer = np.median(schaetzfrage2_antworten_negative_einstellung)
    durchschnitt_positive_teilnehmer = np.median(schaetzfrage2_antworten_positive_einstellung)

    #Bins manuell erstellen
    bins = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
    bin_labels = ['0-5 %', '6-10 %', '11-15 %', '16-20 %', '21-25 %', '26-30 %',
                  '31-35 %', '36-40 %', '41-45 %', '46-50 %', '>50 %']

    n, bins, patches = plt.hist(schaetzfrage2_antworten, bins, color='blue', align='left')

    plt.xticks(bins, bin_labels, rotation=45)

    #eigene Antwort des Spielers hellblau färben
    value_bin = next(idx for idx, val in enumerate(bins) if val > player.schaetzfrage2)
    patches[value_bin - 1].set_fc('lightblue')

    # richtige Antwort als grüner Strich
    plt.axvline(7, color='green', linewidth=2, label='Richtige Antwort')

    #Zeichnet roten Strich durch die Mitte des Balkens mit dem Median der nicht besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_negative_teilnehmer >= bins[i]) and (durchschnitt_negative_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='red', linewidth=2,
                        label='Median der gruppierten Daten der Teilnehmer*innen\ndie den Weiterbetreib von AKWs negativ sehen')
            break

    # Zeichnet orangen Strich durch die Mitte des Balkens mit dem median der besorgten Teilnehmer
    for i in range(len(bins) - 1):
        if (durchschnitt_positive_teilnehmer >= bins[i]) and (durchschnitt_positive_teilnehmer < bins[i + 1]):
            plt.axvline(x=(bins[i] + bins[i + 1]) / 2, color='orange', linewidth=2,
                        label='Median der gruppierten Daten der Teilnehmer*innen\ndie den Weiterbetreib von AKWs positiv sehen')
            break

    plt.legend(bbox_to_anchor=(0.5, -0.25), ncol=3, loc='lower center', fontsize=15)

    # nur ganzzahlige Zahlen für y-Achse anzeigen
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    #Erzeugung der Achsenbeschriftungen für x als Intervalle
    #plt.xticks(bins, bins_names)
    #plt.yticks(size=12)

    # Achsenbeschriftung hinzufügen
    plt.xlabel('Geschätzte Prozentzahl [%]', size=16)
    plt.ylabel('Anzahl der Schätzungen', size=16)

    # Bild speichern
    plt.savefig('./_static/Bild_Ergebnisse2.pdf', format='pdf', bbox_inches='tight')
    return schaetzfrage2_antworten, schaetzfrage2_antworten_negative_einstellung, schaetzfrage2_antworten_positive_einstellung


class Player(BasePlayer):

    frage1 = models.StringField(initial='',
        label='''
        1.) Auf einer Skala von 1-4 wie besorgt sind Sie über die Auswirkungen der Klimawandels auf unsere Umwelt und
         Gesellschaft?<br><br>
        ''',
        choices=[['1', '1 = Gar nicht besorgt'], ['2', '2 = Eher nicht besorgt'], ['3', '3 = Eher besorgt'], ['4', '4 = Sehr besorgt']],
        widget=widgets.RadioSelectHorizontal,
    )
    frage2 = models.StringField(initial='',
        label='''
        <br><br><br>
        2.) Auf einer Skala von 1-4, wie positiv stehen Sie einem Weiterbetrieb von Atomkraftwerken gegenüber?<br><br>''',
        choices=[['1', '1 = Sehr negativ'], ['2', '2 = Eher negativ'], ['3', '3 = Eher positiv'], ['4', '4 = Sehr positiv']],
        widget=widgets.RadioSelectHorizontal,
    )
    schaetzfrage1 = models.StringField(initial='',
            label="Um wie viel Prozent schätzen Sie, haben die CO2-Emissionen weltweit \
            seit 1990 zugenommen (Stand Ende 2021)?", choices=[['5','0-10 %'], ['15.5', '11-20 %'], ['25.5','21-30 %'],
                        ['35.5','31-40 %'], ['45.5','41-50 %'],['55.5','51-60 %'], ['65.5','61-70 %'], ['75.5','71-80 %'],
                        ['85.5','81-90 %'], ['95.5', '91-100 %'], ['105.5','>100 %']],
    )

    schaetzfrage2 = models.StringField(initial='',
         label="Wie hoch schätzen die den Beitrag von Atomkraftwerken (AKWs)\
         zu unserem Strommix in Deutschland (in Prozent)?",
         choices=[['2.5', '0-5 %'], ['8.0', '6-10 %'], ['13.0', '11-15 %'], ['18.0', '16-20 %'], ['23.0', '21-25 %'],
                  ['28.0', '26-30 %'], ['33.0', '31-35 %'], ['38.0', '36-40 %'], ['43.0', '41-45 %'], ['48.0', '46-50 %'],
                  ['53.0', '>50 %']],
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
            schaetzfrage1_antwort=player.field_display('schaetzfrage1'),
            anzahl_bisheriger_teilnehmer=anzahl_spieler(player.subsession),)


class Ergebnisse2(Page):
    @staticmethod
    def vars_for_template(player: Player):
        plot_data_Ergebnisse2(player.subsession, player)
        return dict(schaetzfrage2_antwort=player.field_display('schaetzfrage2'),
                anzahl_bisheriger_teilnehmer=anzahl_spieler(player.subsession))


class Ende(Page):
    pass


page_sequence = [Anweisung, Vorab_Fragen, Schaetzfrage1, Schaetzfrage2, Ergebnisse1, Ergebnisse2, Ende]
