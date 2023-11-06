import streamlit as st
import pandas as pd


sheets_dict = pd.read_excel("EDatas.xlsx", sheet_name=None)

sheets_dict.pop('Constituency Profile', None)


st.title("Koratla Constituency Voter List")
st.sidebar.title("Mandals List")


def get_row_count(df, village_name):
    return len(df[df['Village'] == village_name])

def get_constituency_profile(sheets_dict):
    profile_data = {
        "Mandal": [],
        "Number of Villages": [],
        "Total Votes": []
    }
    for mandal, df in sheets_dict.items():
        profile_data["Mandal"].append(mandal)
        profile_data["Number of Villages"].append(df['Village'].nunique())
        profile_data["Total Votes"].append(df['Total'].sum())
    return pd.DataFrame(profile_data)


def load_and_aggregate_data(df, village):
    # Group by 'Village' and sum up the 'Male', 'Female', and 'Total'
    aggregated_data = df.groupby('Village', as_index=False).agg({
        'Male': 'sum',
        'Female': 'sum',
        'Total': 'sum'
    })
    # Filter the aggregated data for the selected village
    village_data = aggregated_data[aggregated_data['Village'] == village]
    return village_data


# Sidebar selection for Mandal
option = st.sidebar.selectbox(
    'Select The Mandal',
    ['Constituency Profile', 'IbrahimPatnam', 'Mallapur', 'Koratla', 'Metpalli']
)

if option == "Constituency Profile":
    st.title("Constituency Profile Overview")
    constituency_profile = get_constituency_profile(sheets_dict)
    st.dataframe(constituency_profile)
    st.markdown(f"### Total Votes in Constituency: {constituency_profile['Total Votes'].sum()}")
else:
    st.title(f"{option} Mandal")
    current_df = sheets_dict[option]

    if 'aggregated_data' not in st.session_state:
        st.session_state.aggregated_data = {}

    if option not in st.session_state.aggregated_data:
        st.session_state.aggregated_data[option] = current_df.groupby('Village', as_index=False).agg({
            'Male': 'sum',
            'Female': 'sum',
            'Total': 'sum'
        })

    selected_village = st.sidebar.selectbox("Select Village", sorted(current_df['Village'].unique().tolist()))
    btn = st.sidebar.button("Details of the Village")

    if btn:
        village_data = load_and_aggregate_data(st.session_state.aggregated_data[option], selected_village)
        st.title(f"Voters of {selected_village}")
        st.dataframe(village_data)
        village_row_count = get_row_count(current_df, selected_village)
        st.write(f"The number of Booths in {selected_village} is {village_row_count}.")
        village_data = current_df[current_df['Village'] == selected_village]
        st.dataframe(village_data)


















