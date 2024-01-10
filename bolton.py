import streamlit as st
import pandas as pd
import base64
import requests
import pandas as pd
import io
from io import StringIO


# LaTeX-Code für die Tonnsche Relation
tonns_ratio_latex = r"""
\text{Tonn Index} = \frac{\text{Summe der unteren Inzisivenbreiten (SIUK)}}{\text{Summe der oberen Inzisivenbreiten (SIOK)}} \times 100
"""
TOKEN = "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"
csv_url = 'https://raw.githubusercontent.com/Awindbrake/KFO/main/data.csv'

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

OK_nach_UK_dict = {
    'OK12': [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
    'UK12': [77.6, 78.5, 79.4, 80.3, 81.3, 82.2, 83.1, 84.0, 84.9, 85.8, 86.7, 87.6, 88.6, 89.5, 90.4, 91.3, 92.2, 93.1, 94.0, 95.0, 95.9, 96.8, 97.7, 98.6, 99.5, 100.4]
    }

UK_nach_OK_dict = {
    'UK12': [77.6, 78.5, 79.4, 80.3, 81.3, 82.2, 83.1, 84.0, 84.9, 85.8, 86.7, 87.6, 88.6, 89.5, 90.4, 91.3, 92.2, 93.1, 94.0, 95.0, 95.9, 96.8, 97.7, 98.6, 99.5, 100.4],
    'OK12': [85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110]
    }

# Function to find the corresponding value
def find_corresponding_value_OK(lower_sum_6_6, uk_to_ok_dict):
    # First, round lower_sum_6_6 to the closest value in the UK12 list
    closest_value = min(uk_to_ok_dict['UK12'], key=lambda x: abs(x - lower_sum_6_6))
    
    # Find the index of this value
    index = uk_to_ok_dict['UK12'].index(closest_value)
    
    # Return the corresponding OK12 value
    return uk_to_ok_dict['OK12'][index]

# Function to find the corresponding value
def find_corresponding_value_UK(upper_sum_6_6, ok_to_uk_dict):
    # First, round lower_sum_6_6 to the closest value in the UK12 list
    closest_value = min(ok_to_uk_dict['OK12'], key=lambda x: abs(x - upper_sum_6_6))
    
    # Find the index of this value
    index = ok_to_uk_dict['OK12'].index(closest_value)
    
    # Return the corresponding OK12 value
    return ok_to_uk_dict['UK12'][index]

# Function to calculate Tonns Relation
def calculate_tonns_relation(sum_upper_anterior, sum_lower_anterior):
    """
    Berechnet die Tonnsche Relation basierend auf den Schneidezahnbreiten.

    :param upper_anterior_teeth: Liste der Breiten der vorderen Zähne im Oberkiefer.
    :param lower_anterior_teeth: Liste der Breiten der vorderen Zähne im Unterkiefer.
    :return: Ein Dictionary mit den berechneten Werten für die Tonnsche Relation und das Verhältnis.
    """
    

    # Tonnschen Index berechnen
    try:
        tonns_ratio = round(((sum_lower_anterior / sum_upper_anterior) * 100),1)
    except ZeroDivisionError:
        tonns_ratio = 0

    # Überschuss bestimmen
    if tonns_ratio > 74:
        surplus = 'Überschuss im Unterkiefer (UK)'
    elif tonns_ratio < 74:
        surplus = 'Überschuss im Oberkiefer (OK)'
    else:
        surplus = 'Ausgeglichenes Verhältnis'

    result = f"Tonn Index: {tonns_ratio},\n{surplus}"

    return result, tonns_ratio, surplus

# Helper function to check decimal - if they end in .5 or .0 no rounding
def check_decimal(value):
    # Extract the decimal part of the number
    decimal_part = value % 1
    
    # Check if the decimal part is 0.5 or 0
    if decimal_part == 0.5 or decimal_part == 0:
        # If condition is met, do something
        return True
    else:
        # If condition is not met, do nothing
        return False

# round to next half number
def round_up_to_nearest_half(number):
    result = int(number*2+1)/2
    return result

# Anzeige der Zahnbreiten
def anzeige_zaehne(zahnbreiten):
    upper_teeth_3_3 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(1, 3) for j in range(1, 4)]
    upper_sum_3_3 = round(sum(upper_teeth_3_3),1)
    lower_teeth_3_3 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(3, 5) for j in range(1, 4)]
    lower_sum_3_3 = round(sum(lower_teeth_3_3),1)
    upper_teeth_6_6 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(1, 3) for j in range(1, 7)]
    upper_sum_6_6 = round(sum(upper_teeth_6_6),1)
    lower_teeth_6_6 = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(3, 5) for j in range(1, 7)]
    lower_sum_6_6 = round(sum(lower_teeth_6_6),1)
    
    with st.expander('Zahnübersicht (Eingabe) anzeigen'):
        # Werte für alle Zähne im Ober- und Unterkiefer extrahieren
        upper_teeth = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(1, 3) for j in range(1, 7)]
        upper_sum = sum(upper_teeth)
        lower_teeth = [zahnbreiten.get(f"{i}.{j}", 0) for i in range(3, 5) for j in range(1, 7)]
        lower_sum = sum(lower_teeth)


        # Neuordnung der Zahnbreiten für den Oberkiefer
        oberkiefer_reihenfolge_links = [f"2.{i}" for i in range(6, 0, -1)]
        oberkiefer_reihenfolge_rechts = [f"1.{i}" for i in range(1, 7)]

        # Neuordnung der Zahnbreiten für den Unterkiefer
        unterkiefer_reihenfolge_rechts = [f"3.{i}" for i in range(1, 7)]
        unterkiefer_reihenfolge_links = [f"4.{i}" for i in range(6, 0, -1)]

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
            st.dataframe(df_oberkiefer_links, hide_index=True)
            st.dataframe(df_unterkiefer_links, hide_index=True)

        with col2:
            st.dataframe(df_oberkiefer_rechts, hide_index=True)
            st.dataframe(df_unterkiefer_rechts, hide_index=True)

        st.write(f"Breiten der Zähne im Oberkiefer in Summe: {upper_sum} mm.")
        st.write(f"Breiten der Zähne im Unterkiefer in Summe {lower_sum} mm.")

        return lower_sum, upper_sum, upper_sum_3_3, lower_sum_3_3, upper_sum_6_6, lower_sum_6_6, df_oberkiefer_links, df_oberkiefer_rechts, df_unterkiefer_links, df_unterkiefer_rechts
    
# calculate anterior teeth width
def Frontzahnbreiten(zahnbreiten, anzahl_frontzähne):
    upper_anterior_teeth = [zahnbreiten.get(f"1.{i}", 0) for i in range(1, anzahl_frontzähne+1)] + \
                        [zahnbreiten.get(f"2.{i}", 0) for i in range(1, anzahl_frontzähne+1)]
    upper_anterior_sum = sum(upper_anterior_teeth)
    lower_anterior_teeth = [zahnbreiten.get(f"3.{i}", 0) for i in range(1, anzahl_frontzähne+1)] + \
                        [zahnbreiten.get(f"4.{i}", 0) for i in range(1, anzahl_frontzähne+1)]
    lower_anterior_sum = sum(lower_anterior_teeth)


    return upper_anterior_sum, lower_anterior_sum

# routine to save data
def update_csv_github(data_to_append, token):
    
    # GitHub API URL for the file
    api_url = "https://api.github.com/repos/Awindbrake/KFO/contents/data.csv"

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
    }

    # Step 1: Check if the file exists and get its content
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # File exists, read its content
        content = base64.b64decode(response.json()['content']).decode('utf-8')
        sha = response.json()['sha']
        existing_df = pd.read_csv(io.StringIO(content))
        # Append new data to existing DataFrame
        updated_df = pd.concat([existing_df, data_to_append])
    else:
        # File does not exist, use new data as the content
        updated_df = data_to_append
        sha = None

    # Convert updated DataFrame to CSV format
    output = io.StringIO()
    updated_df.to_csv(output, index=False)
    output.seek(0)
    csv_content_encoded = base64.b64encode(output.getvalue().encode('utf-8')).decode('utf-8')

    # Step 2: Create or update the file on GitHub
    commit_message = 'Update the file with new data' if sha else 'Create the file with initial data'
    payload = {
        'message': commit_message,
        'content': csv_content_encoded,
        'sha': sha,
    }
    put_response = requests.put(api_url, headers=headers, json=payload)
    put_response.raise_for_status()  # Handle errors for PUT request

    # Cleanup
    output.close()

# routine to load data
def load_data_from_github(url):
    # Send a GET request to the GitHub raw content URL of your CSV file
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful

    # Read the content of the file into a pandas DataFrame
    csv_data = StringIO(response.text)
    df = pd.read_csv(csv_data)
    return df


#----------- Dateneingabe-----------------------------

st.title("Modellanalyse - Auswertung von KFO Modellen")
st.subheader("Dateneingabe")

st.write('Sollen frühere Analysen geladen werden oder Anlage Neupatient?')
mode = st.radio("Auswahl", ("neue Analyse", "lade existierende Analyse"), index=0)

if mode == "lade existierende Analyse":
    
    # Load the data
    data_df = load_data_from_github(csv_url)

    # List of columns to drop (by index)
    columns_to_drop = list(range(1, 21))  # This will drop columns with indices from 1 to 20

    # Drop the columns
    data_df = data_df.drop(data_df.columns[columns_to_drop], axis=1)

    # Get unique values from the 'pat_id' column
    pat_ids = data_df['pat_id'].unique()

    # Create a select box for user to choose a pat_id
    pat_id = st.selectbox('Select Patient ID', pat_ids)
    selected_row = data_df[data_df['pat_id'] == pat_id].iloc[0] if not data_df[data_df['pat_id'] == pat_id].empty else None
    
else:
    # Logic for entering new patient data
    selected_row = None
    pat_id = st.text_input("Patient-ID:")



with st.expander("Eingabefelder zeigen"):
    
    st.subheader("Eingabe der Zahnbreiten")
    st.write("**Quadranten aus Sicht des Behandlers**")
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
                default_value = selected_row[teeth[i]] if selected_row is not None else 0.0
                zahnbreiten[teeth[i]] = st.number_input(f"{teeth[i]}:", min_value=0.0, value=default_value, format="%.2f")
        # Nächste vier Zähne in der zweiten Reihe
        cols = st.columns(4)
        for i in range(4, 6):
            with cols[i - 4]:
                default_value = selected_row[teeth[i]] if selected_row is not None else 0.0
                zahnbreiten[teeth[i]] = st.number_input(f"{teeth[i]}:", min_value=0.0, value=default_value, format="%.2f")


# ------- Auswertungen -------------------------------

upper_anterior_sum, lower_anterior_sum_orig = Frontzahnbreiten(zahnbreiten, 2)
lower_sum, upper_sum, upper_sum_3_3, lower_sum_3_3, upper_sum_6_6, lower_sum_6_6, df_oberkiefer_links, df_oberkiefer_rechts, df_unterkiefer_links, df_unterkiefer_rechts = anzeige_zaehne(zahnbreiten)

if not check_decimal(lower_anterior_sum_orig):
    lower_anterior_sum = round_up_to_nearest_half(lower_anterior_sum_orig)
else:
    lower_anterior_sum = lower_anterior_sum_orig

st.write(f"Summe Schneidezahnbreite Oberkiefer (SIOK): {upper_anterior_sum} mm.")
st.write(f"Summe Schneidezahnbreiten Unterkiefer (SIUK): {lower_anterior_sum_orig} mm. => gerundet auf **{lower_anterior_sum}** mm.")

st.subheader("Stützzonenanalyse nach Moyers (75%-Grenze)")

col1, col2 = st.columns(2)
try:
    
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


#--Auswertung Tonn Index -------------------

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


#--Auswertung Breitenrelation nach Bolton ---------

st.subheader('Breitenrelation nach Bolton ')
st.markdown('''**Summe der Breiten 
           aller permanenten Zähne (6-6) im Unterkiefer geteilt durch Summe aller permanenten Zähne (6-6) im Oberkiefer.**''')


try:
    ttsr = round(((lower_sum/ upper_sum) * 100),2)
    upper_anterior_sum, lower_anterior_sum = Frontzahnbreiten(zahnbreiten, 3)
    atsr = round(((lower_anterior_sum / upper_anterior_sum) * 100),2)
    ratio = round(((upper_sum_6_6/lower_sum_6_6)*100),2)
except ZeroDivisionError:
    ttsr = 0
    atsr = 0
    ratio = 0


if ttsr <91.3:
    text_ttsr = "OK-Zahnmaterial relativ zu groß"
    corresponding_value = find_corresponding_value_OK(lower_sum_6_6, UK_nach_OK_dict)
    text_korrektur = f"Im OK muss auf {corresponding_value} mm reduziert werden."

elif ttsr >91.3:
    text_ttsr = "UK-Zahnmaterial relativ zu groß"
    corresponding_value = find_corresponding_value_UK(upper_sum_6_6, OK_nach_UK_dict)
    text_korrektur = f"Im UK muss auf {corresponding_value} mm reduziert werden."

if atsr <77.2:
    text_atsr = "OK-Zahnmaterial relativ zu groß"
elif atsr >77.2:
    text_atsr = "UK-Zahnmaterial relativ zu groß"


col1, col2 = st.columns(2)
col1.write(f'Overall Ratio:   ')
col2.write(f"**{ttsr}** % ({text_ttsr})")
# st.write('--- NOCH ZU TESTEN ---')
# st.markdown(f''':red[**{text_korrektur}**]''')
# st.write("---")
# col1.write(f'Summe 6-6 OK:')
# col2.write(f'**{upper_sum_6_6}** mm.')
# col1.write(f'Summe 6-6 UK:')
# col2.write(f'**{lower_sum_6_6}** mm.')
# #col2.write(f'ratio = {ratio} %')

col1.write()


st.markdown('''**Summe der Breiten 
           aller permanenten Frontzähne (3-3) im Unterkiefer geteilt durch Summe aller permanenten Frontzähne (3-3) im Oberkiefer.**''')
col3, col4 = st.columns(2)
col3.write(f'Anterior Ratio: ')
col4.write(f'**{atsr}** % ({text_atsr})')
col3.write(f'Summe 3-3 OK:')
col4.write(f'**{upper_sum_3_3}** mm.')
col3.write(f'Summe 3-3 UK:')
col4.write(f'**{lower_sum_3_3}** mm.')



##-------------Daten speichern ----------------

st.write("---")
if st.button("save to file"):

    data = {
    'pat_id':[pat_id],
    'upper_anterior_sum': [upper_anterior_sum],
    'lower_anterior_sum': [lower_anterior_sum],
    'required_space_upper_jaw': [required_space_upper_jaw],
    'required_space_lower_jaw': [required_space_lower_jaw],
    'platzangebot_ok_rechts': [platzangebot_ok_rechts],
    'platzangebot_ok_links': [platzangebot_ok_links],
    'platzangebot_uk_rechts': [platzangebot_uk_rechts],
    'platzangebot_uk_links': [platzangebot_uk_links],
    'diff_OK_rechts': [diff_OK_rechts],
    'diff_OK_links': [diff_OK_links],
    'diff_UK_rechts': [diff_UK_rechts],
    'diff_UK_links': [diff_UK_links],
    'tonns_ratio': [tonns_ratio],
    'surplus': [surplus],
    'upper_sum_3_3': [upper_sum_3_3],
    'lower_sum_3_3': [lower_sum_3_3],
    'upper_sum_6_6': [upper_sum_6_6],
    'lower_sum_6_6': [lower_sum_6_6],
    'ttsr': [ttsr],
    'atsr': [atsr]
}   
    df_values = pd.DataFrame(data)
    df_oberkiefer_links_sv = df_oberkiefer_links.reset_index(drop=True)
    df_oberkiefer_rechts_sv = df_oberkiefer_rechts.reset_index(drop=True)
    df_unterkiefer_links_sv = df_unterkiefer_links.reset_index(drop=True)
    df_unterkiefer_rechts_sv = df_unterkiefer_rechts.reset_index(drop=True)


    final_df = pd.concat([
        df_values,
        df_oberkiefer_rechts_sv,
        df_oberkiefer_links_sv,
        df_unterkiefer_rechts_sv,
        df_unterkiefer_links_sv
    ], axis=1)

    #st.dataframe(final_df)
    csv_file_name = 'data.csv'
    final_df.to_csv(csv_file_name, index=False) 
    update_csv_github(final_df, TOKEN)


