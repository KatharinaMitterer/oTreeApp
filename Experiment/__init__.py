from otree.api import *
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

class C(BaseConstants):
    NAME_IN_URL = 'Experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


def anzahl_spieler(subsession):
    # Funktion um Anzahl der Spieler zu bestimmen, die bisher gespielt haben

    # Laden der Daten der Spieler die schon in der Vergangenheit gespielt haben und in txt Datei gespeichert wurden
    data = pd.read_csv('./_rooms/gruppe3_room.txt', delimiter=',')

    # Anzahl der Spieler, die bisher and der Umfrage teilgenommen haben(laut Datei)
    anzahl = len(data)

    return anzahl


def plot_data_Ergebnisse1(subsession, player):
    # Funktion um Ergebnisse zu plotten für Schätzfrage 1

    fig = plt.figure(figsize=(16, 8))

    # Erstellung leerer Arrays für alle bisherigen Antworten und Gruppierung der Antworten
    schaetzfrage1_antworten = []
    schaetzfrage1_antworten_besorgter_teilnehmer = []
    schaetzfrage1_antworten_unbesorgter_teilnehmer = []

    # Speichern der Daten des aktuellen Spielers in txt Datei:
    with open("./_rooms/gruppe3_room.txt", "a") as file:
        file.write(f"\n{player.id}, {float(player.frage1)}, {float(player.frage2)}, "
                   f"{float(player.schaetzfrage1)}, {float(player.schaetzfrage2)}")

    # Laden der Daten der Spieler die schon in der Vergangenheit gespielt haben
    data = pd.read_csv('./_rooms/gruppe3_room.txt', delimiter=',', header=0,
                       names=['id', 'frage1', 'frage2', 'schaetzfrage1', 'schaetzfrage2'])

    # Einlesen aller bisherigen Daten für Vorab-Frage 1 und Schaetzfrage 1 aus der txt Datei entsprechend der Gruppierung
    if len(data) != 0:
        for row_index in range(0, len(data)):
            schaetzfrage1_antworten.append(float(data.loc[row_index,'schaetzfrage1']))
            if float(data.loc[row_index, 'frage1']) == 1.0 or float(data.loc[row_index, 'frage1']) == 2.0:
                schaetzfrage1_antworten_besorgter_teilnehmer.append(float(data.loc[row_index,'schaetzfrage1']))
            if float(data.loc[row_index, 'frage1']) == 3.0 or float(data.loc[row_index, 'frage1']) == 4.0:
                schaetzfrage1_antworten_unbesorgter_teilnehmer.append(float(data.loc[row_index,'schaetzfrage1']))

    # Berechnung des Medians der gruppierten Daten
    median_besorgter_teilnehmer = np.median(schaetzfrage1_antworten_besorgter_teilnehmer)
    median_unbesorgter_teilnehmer = np.median(schaetzfrage1_antworten_unbesorgter_teilnehmer)

    # Erstellung des Histogramm mit entsprechenden Bins
    bins = [5, 15.5, 25.5, 35.5, 45.5, 55.5, 65.5, 75.5, 85.5, 95.5, 105.5]
    bin_labels = ['0-10 %', '11-20 %', '21-30 %', '31-40 %', '41-50 %', '51-60 %', '61-70 %', '71-80 %', '81-90 %',
                  '91-100 %', '>100 %']

    n, bins, patches = plt.hist(schaetzfrage1_antworten, bins, color='lightblue', align='left', edgecolor='white', linewidth=6)

    plt.xticks(bins, bin_labels, rotation=45)

    # Einfärbung des Balkens in blau, der der Antwort des aktuellen Spielers entspricht
    value_bin = next(idx for idx, val in enumerate(bins) if val > float(player.schaetzfrage1))
    patches[value_bin - 1].set_fc('blue')

    # Erstellung einer grünen Geraden, die der richtigen Antwort entspricht
    plt.axvline(65.5, color='green', linewidth=6, label='Richtige Antwort')

    # Erstellung einer orangen Geraden, die dem Median der gruppierten Daten der Teilnehmer*innen
    # die über Klimawandel besorgt sind, enstpricht
    plt.axvline(median_besorgter_teilnehmer, color='orange', linewidth=2,
                    label='Median der Teilnehmer*innen\n die über Klimawandel besorgt sind', linestyle='-')

    # Erstellung einer orangen Geraden, die dem Median der gruppierten Daten der Teilnehmer*innen
    # die über Klimawandel nicht besorgt sind, enstpricht
    plt.axvline(median_unbesorgter_teilnehmer, color='red', linewidth=2,
                    label='Median der Teilnehmer*innen\ndie über Klimawandel nicht besorgt sind', linestyle='--')

    # Erzeugung der Legende unterhalb des Plots, in dem der Abstand unabhängig von der Anzahl der bisherigen Spieler fix bleibt
    distance_in_inches = 60
    distance_in_fig_coords = distance_in_inches / fig.dpi
    plt.legend(bbox_to_anchor=(0.5, -distance_in_fig_coords), ncol=3, loc='lower center', fontsize=15)

    # Nur ganzzahlige Zahlen für y-Achse anzeigen
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Achsenbeschriftung hinzufügen
    plt.xlabel('Geschätzte Prozentzahl [%]', size=16)
    plt.ylabel('Anzahl der Schätzungen', size=16)
    plt.yticks(size=12)
    plt.xticks(size=12)

    # Bild speichern
    plt.savefig('./_static/Bild_Ergebnisse1.pdf', format='pdf', bbox_inches='tight')

    return schaetzfrage1_antworten, schaetzfrage1_antworten_besorgter_teilnehmer, schaetzfrage1_antworten_unbesorgter_teilnehmer, player.frage1

def plot_data_Ergebnisse2(subsession, player):
    # Funktion um Ergebnisse zu plotten für Schätzfrage 2

    # Laden der Daten der Spieler die schon in der Vergangenheit gespielt haben
    data = pd.read_csv('./_rooms/gruppe3_room.txt', delimiter=',', header=0,
                       names=['id', 'frage1', 'frage2', 'schaetzfrage1', 'schaetzfrage2'])

    fig = plt.figure(figsize=(16, 8))

    # Erstellung leerer Arrays für alle bisherigen Antworten und Gruppierung der Antworten
    schaetzfrage2_antworten = []
    schaetzfrage2_antworten_positive_einstellung = []
    schaetzfrage2_antworten_negative_einstellung = []

    # Einlesen aller bisherigen Daten für Vorab-Frage 2 und Schaetzfrage 2 aus der txt Datei entsprechend der Gruppierung
    if len(data) != 0:
        for row_index in range(0, len(data)):
            schaetzfrage2_antworten.append(float(data.loc[row_index, 'schaetzfrage2']))
            if float(data.loc[row_index, 'frage2']) == 1.0 or float(data.loc[row_index, 'frage2']) == 2.0:
                schaetzfrage2_antworten_negative_einstellung.append(float(data.loc[row_index, 'schaetzfrage2']))
            if float(data.loc[row_index, 'frage2']) == 3.0 or float(data.loc[row_index, 'frage2']) == 4.0:
                schaetzfrage2_antworten_positive_einstellung.append(float(data.loc[row_index, 'schaetzfrage2']))

    # Berechnung des Medians der gruppierten Daten
    median_negative_einstellung = np.median(schaetzfrage2_antworten_negative_einstellung)
    median_positive_einstellung = np.median(schaetzfrage2_antworten_positive_einstellung)

    # Erstellung des Histogramm mit entsprechenden Bins
    bins = [2.5, 8.0, 13.0, 18.0, 23.0, 28.0, 33.0, 38.0, 43.0, 48.0, 53.0]
    bin_labels = ['0-5 %', '6-10 %', '11-15 %', '16-20 %', '21-25 %', '26-30 %',
                  '31-35 %', '36-40 %', '41-45 %', '46-50 %', '>50 %']

    n, bins, patches = plt.hist(schaetzfrage2_antworten, bins, color='lightblue', align='left', edgecolor='white', linewidth=6)

    plt.xticks(bins, bin_labels, rotation=45)

    # Einfärbung des Balkens in blau, der der Antwort des aktuellen Spielers entspricht
    value_bin = next(idx for idx, val in enumerate(bins) if val > float(player.schaetzfrage2))
    patches[value_bin - 1].set_fc('blue')

    # Erstellung einer grünen Geraden, die der richtigen Antwort entspricht
    plt.axvline(8, color='green', linewidth=6, label='Richtige Antwort')

    # Erstellung einer roten Geraden, die dem Median der gruppierten Daten der Teilnehmer*innen
    # die den Weiterbetreib von AKWs negativ sehen
    plt.axvline(median_negative_einstellung, color='red', linewidth=2,
                label='Median der Teilnehmer*innen\ndie den Weiterbetreib von AKWs negativ sehen',  linestyle='-')

    # Erstellung einer orangen Geraden, die dem Median der gruppierten Daten der Teilnehmer*innen
    # die den Weiterbetreib von AKWs positiv sehen
    plt.axvline(median_positive_einstellung, color='orange', linewidth=2,
                label='Median der Teilnehmer*innen\ndie den Weiterbetreib von AKWs positiv sehen',  linestyle='--')

    # Erzeugung der Legende unterhalb des Plots, in dem der Abstand unabhängig von der Anzahl der bisherigen Spieler fix bleibt
    distance_in_inches = 60
    distance_in_fig_coords = distance_in_inches / fig.dpi
    plt.legend(bbox_to_anchor=(0.5, -distance_in_fig_coords), ncol=3, loc='lower center', fontsize=15)

    # Nur ganzzahlige Zahlen für y-Achse anzeigen
    ax = plt.gca()
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Achsenbeschriftung hinzufügen
    plt.xlabel('Geschätzte Prozentzahl [%]', size=16)
    plt.ylabel('Anzahl der Schätzungen', size=16)
    plt.yticks(size=12)
    plt.xticks(size=12)

    # Bild speichern
    plt.savefig('./_static/Bild_Ergebnisse2.pdf', format='pdf', bbox_inches='tight')

    return schaetzfrage2_antworten, schaetzfrage2_antworten_negative_einstellung, schaetzfrage2_antworten_positive_einstellung


class Player(BasePlayer):

    # Definition der Felder eines Spielers

    frage1 = models.StringField(initial=0,
        label="<b>1.) Auf einer Skala von 1-4 wie besorgt sind Sie über die Auswirkungen der Klimawandels auf unsere \
        Umwelt und Gesellschaft?</b><br><br>",
        choices=[['1', '1 = Gar nicht besorgt'], ['2', '2 = Eher nicht besorgt'], ['3', '3 = Eher besorgt'], ['4', '4 = Sehr besorgt']],
        widget=widgets.RadioSelectHorizontal,
    )
    frage2 = models.StringField(initial=0,
        label=" <br><br><br>\
        <b>2.) Auf einer Skala von 1-4, wie positiv stehen Sie einem Weiterbetrieb von Atomkraftwerken gegenüber?</b><br><br>",
        choices=[['1', '1 = Sehr negativ'], ['2', '2 = Eher negativ'], ['3', '3 = Eher positiv'], ['4', '4 = Sehr positiv']],
        widget=widgets.RadioSelectHorizontal,
    )
    schaetzfrage1 = models.StringField(initial=0,
            label="<b>Um wie viel Prozent schätzen Sie, haben die CO2-Emissionen weltweit \
            seit 1990 zugenommen (Stand Ende 2021)?</b>", choices=[['5','0-10 %'], ['15.5', '11-20 %'], ['25.5','21-30 %'],
                        ['35.5','31-40 %'], ['45.5','41-50 %'],['55.5','51-60 %'], ['65.5','61-70 %'], ['75.5','71-80 %'],
                        ['85.5','81-90 %'], ['95.5', '91-100 %'], ['105.5','>100 %']],
    )

    schaetzfrage2 = models.StringField(initial=0,
         label="<b>Wie hoch schätzen Sie den Beitrag von Atomkraftwerken (AKWs)\
         zu unserem Strommix in Deutschland (in Prozent)?</b>",
         choices=[['2.5', '0-5 %'], ['8.0', '6-10 %'], ['13.0', '11-15 %'], ['18.0', '16-20 %'], ['23.0', '21-25 %'],
                  ['28.0', '26-30 %'], ['33.0', '31-35 %'], ['38.0', '36-40 %'], ['43.0', '41-45 %'], ['48.0', '46-50 %'],
                  ['53.0', '>50 %']],
    )

#Definition der Seiten für das Experiment

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


#Sequenz der Seiten für das Experiment
page_sequence = [Anweisung, Vorab_Fragen, Schaetzfrage1, Schaetzfrage2, Ergebnisse1, Ergebnisse2, Ende]
