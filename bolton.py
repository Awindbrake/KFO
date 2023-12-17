import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd


# LaTeX-Code für die Tonnsche Relation
tonns_ratio_latex = r"""
\text{Tonn Index} = \frac{\text{Summe der unteren Inzisivenbreiten (SIUK)}}{\text{Summe der oberen Inzisivenbreiten (SIOK)}} \times 100
"""

# Translating the given Moyers probability table into a Python dictionary
# The dictionary will have keys that are the measurements of the SIUK (Summe der Inzisivi im Unterkiefer)
# and the values will be nested dictionaries with keys as percentages and values as the required space.

moyers_table_lower_jaw_complete = {
    19.5: {95: 21.1, 85: 20.5, 75: 20.1, 65: 19.8, 50: 19.4, 35: 19, 25: 18.7, 15: 18.4, 5: 17.7},
    20.0: {95: 21.4, 85: 20.8, 75: 20.4, 65: 20.1, 50: 19.7, 35: 19.3, 25: 19, 15: 18.7, 5: 18},
    20.5: {95: 21.7, 85: 21.1, 75: 20.7, 65: 20.4, 50: 20, 35: 19.6, 25: 19.3, 15: 19, 5: 18.3},
    21.0: {95: 22.0, 85: 21.4, 75: 21.0, 65: 20.7, 50: 20.3, 35: 19.9, 25: 19.6, 15: 19.3, 5: 18.6},
    21.5: {95: 22.3, 85: 21.7, 75: 21.3, 65: 21.0, 50: 20.6, 35: 20.2, 25: 19.9, 15: 19.6, 5: 18.9},
    22.0: {95: 22.6, 85: 22.0, 75: 21.6, 65: 21.3, 50: 20.9, 35: 20.5, 25: 20.2, 15: 19.8, 5: 19.2},
    22.5: {95: 22.9, 85: 22.3, 75: 21.9, 65: 21.6, 50: 21.2, 35: 20.8, 25: 20.5, 15: 20.1, 5: 19.5},
    23.0: {95: 23.2, 85: 22.6, 75: 22.2, 65: 21.9, 50: 21.5, 35: 21.1, 25: 20.8, 15: 20.4, 5: 19.8},
    23.5: {95: 23.5, 85: 22.9, 75: 22.5, 65: 22.2, 50: 21.8, 35: 21.4, 25: 21.1, 15: 20.7, 5: 20.1},
    24.0: {95: 23.8, 85: 23.2, 75: 22.8, 65: 22.5, 50: 22.1, 35: 21.7, 25: 21.4, 15: 21, 5: 20.4},
    24.5: {95: 24.1, 85: 23.5, 75: 23.1, 65: 22.8, 50: 22.4, 35: 22, 25: 21.7, 15: 21.3, 5: 20.7},
    25.0: {95: 24.4, 85: 23.8, 75: 23.4, 65: 23.1, 50: 22.7, 35: 22.3, 25: 22, 15: 21.6, 5: 21},
}

moyers_table_upper_jaw_complete = {
    19.5: {95: 21.6, 85: 21, 75: 20.6, 65: 20.4, 50: 20, 35: 19.6, 25: 19.4, 15: 19, 5: 18.5},
    20.0: {95: 21.8, 85: 21.3, 75: 20.9, 65: 20.6, 50: 20.3, 35: 19.9, 25: 19.7, 15: 19.3, 5: 18.8},
    20.5: {95: 22.1, 85: 21.5, 75: 21.2, 65: 20.9, 50: 20.6, 35: 20.2, 25: 19.9, 15: 19.6, 5: 19},
    21.0: {95: 22.4, 85: 21.8, 75: 21.5, 65: 21.2, 50: 20.8, 35: 20.5, 25: 20.2, 15: 19.9, 5: 19.3},
    21.5: {95: 22.7, 85: 22.1, 75: 21.8, 65: 21.5, 50: 21.1, 35: 20.8, 25: 20.5, 15: 20.2, 5: 19.6},
    22.0: {95: 22.9, 85: 22.4, 75: 22, 65: 21.8, 50: 21.4, 35: 21, 25: 20.8, 15: 20.4, 5: 19.9},
    22.5: {95: 23.2, 85: 22.6, 75: 22.3, 65: 22, 50: 21.7, 35: 21.3, 25: 21, 15: 20.7, 5: 20.1},
    23.0: {95: 23.5, 85: 22.9, 75: 22.6, 65: 22.3, 50: 21.9, 35: 21.6, 25: 21.3, 15: 21, 5: 20.4},
    23.5: {95: 23.8, 85: 23.2, 75: 22.9, 65: 22.6, 50: 22.2, 35: 21.9, 25: 21.6, 15: 21.3, 5: 20.7},
    24.0: {95: 24, 85: 23.5, 75: 23.1, 65: 22.8, 50: 22.5, 35: 22.1, 25: 21.9, 15: 21.5, 5: 21},
    24.5: {95: 24.3, 85: 23.7, 75: 23.4, 65: 23.1, 50: 22.8, 35: 22.4, 25: 22.1, 15: 21.8, 5: 21.2},
    25.0: {95: 24.6, 85: 24, 75: 23.7, 65: 23.4, 50: 23, 35: 22.7, 25: 22.4, 15: 22.1, 5: 21.5},
}




def calculate_tonns_relation(sum_upper_anterior, sum_lower_anterior):
    """
    Berechnet die Tonnsche Relation basierend auf den Schneidezahnbreiten.

    :param upper_anterior_teeth: Liste der Breiten der vorderen Zähne im Oberkiefer.
    :param lower_anterior_teeth: Liste der Breiten der vorderen Zähne im Unterkiefer.
    :return: Ein Dictionary mit den berechneten Werten für die Tonnsche Relation und das Verhältnis.
    """
    

    # Tonnsche Relation berechnen
    tonns_ratio = round(((sum_lower_anterior / sum_upper_anterior) * 100),1)

    # Überschuss bestimmen
    if tonns_ratio > 74:
        surplus = 'Überschuss im Unterkiefer (UK)'
    elif tonns_ratio < 74:
        surplus = 'Überschuss im Oberkiefer (OK)'
    else:
        surplus = 'Ausgeglichenes Verhältnis'

    result = f"Tonn Index: {tonns_ratio},\n{surplus}"

    return result, tonns_ratio, surplus

def Frontzahnbreiten(zahnbreiten, anzahl_frontzähne):
    upper_anterior_teeth = [zahnbreiten.get(f"1.{i}", 0) for i in range(1, anzahl_frontzähne+1)] + \
                        [zahnbreiten.get(f"2.{i}", 0) for i in range(1, anzahl_frontzähne+1)]
    upper_anterior_sum = sum(upper_anterior_teeth)
    lower_anterior_teeth = [zahnbreiten.get(f"3.{i}", 0) for i in range(1, anzahl_frontzähne+1)] + \
                        [zahnbreiten.get(f"4.{i}", 0) for i in range(1, anzahl_frontzähne+1)]
    lower_anterior_sum = sum(lower_anterior_teeth)

    return upper_anterior_sum, lower_anterior_sum

#Interface

st.title("Modellanalyse")
st.subheader("Auswertung von KFO Modellen")
# Input for the vorderen Zähne

with st.expander("Eingabefelder zeigen"):
    
    st.subheader("Eingabe der Zahnbreiten")
    zahnbreiten = {}

    # Quadranten definieren
    quadranten = {
        "Quadrant 1 (Oben Rechts)": [f"1.{i}" for i in range(1, 9)],
        "Quadrant 2 (Oben Links)": [f"2.{i}" for i in range(1, 9)],
        "Quadrant 3 (Unten Links)": [f"3.{i}" for i in range(1, 9)],
        "Quadrant 4 (Unten Rechts)": [f"4.{i}" for i in range(1, 9)]
    }

    # Eingabefelder für jeden Zahn erstellen
    for quadrant_name, teeth in quadranten.items():
        st.subheader(f"{quadrant_name}")
        # Erste vier Zähne in der ersten Reihe
        cols = st.columns(4)
        for i in range(4):
            with cols[i]:
                zahnbreiten[teeth[i]] = st.number_input(f"{teeth[i]}:", min_value=0.0, format="%.2f")
        # Nächste vier Zähne in der zweiten Reihe
        cols = st.columns(4)
        for i in range(4, 8):
            with cols[i - 4]:
                zahnbreiten[teeth[i]] = st.number_input(f"{teeth[i]}:", min_value=0.0, format="%.2f")

    # Button zum Senden der Daten
    if st.button('Daten absenden'):
        st.write("Daten erfolgreich gesendet.")
    

upper_anterior_sum, lower_anterior_sum = Frontzahnbreiten(zahnbreiten, 2)
st.write(f"Summe Schneidezahnbreite Oberkiefer (SIOK): {upper_anterior_sum} mm.")
st.write(f"Summe Schneidezahnbreiten Unterkiefer (SIUK): {lower_anterior_sum} mm.")

st.subheader("Stützzonenanalyse nach Moyers (75%-Grenze)")
#st.write("Es wird die Moyers-Tabelle verwendet. Hier wird die Summe der mesiodistalen Breiten der unteren Inzisivi (SIUK) übergeben . Dieser Wert ist ein Maß für die Breite der vorderen Zähne im Kiefer und dient als Schlüssel, um den Platzbedarf für die bleibenden Zähne (Eckzahn, 1. Prämolar und 2. Prämolar) sowohl im Ober- als auch im Unterkiefer zu ermitteln.")
col1, col2 = st.columns(2)
try:
    required_space_lower_jaw = moyers_table_lower_jaw_complete[lower_anterior_sum][75]
    required_space_upper_jaw = moyers_table_upper_jaw_complete[lower_anterior_sum][75]
    
    required_space_upper_jaw = moyers_table_upper_jaw_complete[lower_anterior_sum][75]
    platzangebot_ok_rechts = col1.number_input(f"Platzangebot OK rechts", min_value=0.0, format="%.2f")
    platzangebot_ok_links = col2.number_input(f"Platzangebot OK links", min_value=0.0, format="%.2f")
    st.write(f'Platzbedarf OK: **{required_space_upper_jaw} mm.**')
    
    required_space_lower_jaw = moyers_table_lower_jaw_complete[lower_anterior_sum][75]
    platzangebot_uk_rechts = col1.number_input(f"Platzangebot UK rechts", min_value=0.0, format="%.2f")
    platzangebot_uk_links = col2.number_input(f"Platzangebot UK links", min_value=0.0, format="%.2f")
    st.write(f'Platzbedarf UK: **{required_space_lower_jaw} mm.**')
    diff_OK_rechts = round((platzangebot_ok_rechts - required_space_upper_jaw),1)
    diff_OK_links = round((platzangebot_ok_links - required_space_upper_jaw),1)
    diff_UK_rechts = round((platzangebot_uk_rechts - required_space_lower_jaw),1)
    diff_UK_links = round((platzangebot_uk_links - required_space_lower_jaw),1)

    st.write("**Differenz Platzangebot - Platzbedarf**")
    col3, col4 = st.columns(2)
    
    col3.write("**Oberkiefer**")
    col3.write(f'rechts: {diff_OK_rechts}')
    col3.write(f'links: {diff_OK_links}')
    col4.write("**Unterkiefer**")
    col4.write(f'rechts: {diff_UK_rechts}')
    col4.write(f'links: {diff_UK_links}')



   

except KeyError:
    st.markdown(f"""Achtung: Der SIUK-Wert liegt mit **{lower_anterior_sum}** außerhalb der Moyers-Tabelle.""")




with st.expander('Alle Zähne'):
    # Werte für alle Zähne im Ober- und Unterkiefer extrahieren
    upper_teeth = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(1, 3) for j in range(1, 9)]
    upper_sum = sum(upper_teeth)
    lower_teeth = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(3, 5) for j in range(1, 9)]
    lower_sum = sum(lower_teeth)



    # Neuordnung der Zahnbreiten für den Oberkiefer
    oberkiefer_reihenfolge_links = [f"2.{i}" for i in range(8, 0, -1)]
    oberkiefer_reihenfolge_rechts = [f"1.{i}" for i in range(1, 9)]

    # Neuordnung der Zahnbreiten für den Unterkiefer
    unterkiefer_reihenfolge_rechts = [f"3.{i}" for i in range(1, 9)]
    unterkiefer_reihenfolge_links = [f"4.{i}" for i in range(8, 0, -1)]

    # Erstellen eines DataFrames für den Oberkiefer
    oberkiefer_breiten_links = {tooth: zahnbreiten[tooth] for tooth in oberkiefer_reihenfolge_links}
    oberkiefer_breiten_rechts = {tooth: zahnbreiten[tooth] for tooth in oberkiefer_reihenfolge_rechts}

    df_oberkiefer_links = pd.DataFrame([oberkiefer_breiten_links], index=["Breite"]).round(1)
    df_oberkiefer_rechts = pd.DataFrame([oberkiefer_breiten_rechts], index=["Breite"]).round(1)

    # Erstellen eines DataFrames für den Unterkiefer
    unterkiefer_breiten_links = {tooth: zahnbreiten[tooth] for tooth in unterkiefer_reihenfolge_links}
    unterkiefer_breiten_rechts = {tooth: zahnbreiten[tooth] for tooth in unterkiefer_reihenfolge_rechts}

    df_unterkiefer_links = pd.DataFrame([unterkiefer_breiten_links], index=["Breite"]).round(1)
    df_unterkiefer_rechts = pd.DataFrame([unterkiefer_breiten_rechts], index=["Breite"]).round(1)

    # Anzeigen der DataFrames in Streamlit
    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df_oberkiefer_links)
        st.dataframe(df_unterkiefer_links)

    with col2:
        st.dataframe(df_oberkiefer_rechts)
        st.dataframe(df_unterkiefer_rechts)

    st.write(f"Breiten der Zähne im Oberkiefer in Summe: {upper_sum} mm.")
    st.write(f"Breiten der Zähne im Unterkiefer in Summe {lower_sum} mm.")

tonns_result, tonns_ratio, surplus = calculate_tonns_relation(upper_anterior_sum, lower_anterior_sum)
st.subheader('Tonn Index - Resultate')
st.write("---")
st.latex(tonns_ratio_latex)
st.write("---")
col5, col6 = st.columns(2)

col5.write(f"Summe Unterkiefer (SIUK):   ")
col6.write(f'**{lower_anterior_sum}** mm.')
col5.write(f"Summe Oberkiefer  (SIOK):   ")
col6.write(f'**{upper_anterior_sum}** mm.')

col5.write(f'Tonn Index: ')
col6.write(f'**{tonns_ratio} %**')
col6.write(f'**{surplus}**')



ttsr = round(((lower_sum/ upper_sum) * 100),2)
upper_anterior_sum, lower_anterior_sum = Frontzahnbreiten(zahnbreiten, 3)
atsr = round(((lower_anterior_sum / upper_anterior_sum) * 100),2)



st.subheader('Breitenrelation nach Bolton ')
#st.write('**Overall Ratio):**')
st.markdown('''**Summe der Breiten 
           aller permanenten Zähne (6-6) im Unterkiefer geteilt durch Summe aller permanenten Zähne (6-6) im Oberkiefer.**''')


# Berechnung der Teilreihen
upper_teeth_3_3 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(1, 3) for j in range(1, 4)]
upper_sum_3_3 = sum(upper_teeth_3_3)
lower_teeth_3_3 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(3, 5) for j in range(1, 4)]
lower_sum_3_3 = sum(lower_teeth_3_3)
upper_teeth_6_6 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(1, 3) for j in range(1, 7)]
upper_sum_6_6 = sum(upper_teeth_6_6)
lower_teeth_6_6 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(3, 5) for j in range(1, 7)]
lower_sum_6_6 = sum(lower_teeth_6_6)



col1, col2 = st.columns(2)
col1.write(f'Overall Ratio:   ')
col2.write(f"**{ttsr}** %")
col1.write(f'Summe 6-6 OK:')
col2.write(f'**{upper_sum_6_6}** mm.')
col1.write(f'Summe 6-6 OK:')
col2.write(f'**{upper_sum_6_6}** mm.')


st.markdown('''**Summe der Breiten 
           aller permanenten Frontzähne (3-3) im Unterkiefer geteilt durch Summe aller permanenten Frontzähne (3-3) im Oberkiefer.**''')
col3, col4 = st.columns(2)
col3.write(f'Anterior Ratio: ')
col4.write(f'**{atsr}** %')
col3.write(f'Summe 3-3 OK:')
col4.write(f'**{upper_sum_3_3}** mm.')
col3.write(f'Summe 3-3 UK:')
col4.write(f'**{lower_sum_3_3}** mm.')

        





