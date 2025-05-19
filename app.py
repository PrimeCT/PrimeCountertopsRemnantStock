
import streamlit as st
import pandas as pd

# Função para carregar logo
st.set_page_config(page_title="Prime Countertops Remnants", layout="wide")
st.markdown(
    f"<div style='background-color: white; padding: 10px;'><img src='Logo.png' width='300'></div>",
    unsafe_allow_html=True
)

# Menu lateral
menu = st.sidebar.radio("Menu", ["View Remnants", "Admin (Protected)"])

# Carregar CSV
@st.cache_data
def load_data():
    return pd.read_csv("remnants.csv")

df = load_data()

if menu == "View Remnants":
    st.title("Available Remnants")

    # Filtro por material
    material_options = ["All"] + sorted(df['material'].unique())
    selected_material = st.selectbox("Filter by Material", material_options)

    # Campo de busca
    search_term = st.text_input("Search by Color or ID")

    # Aplicar filtros
    filtered_df = df.copy()
    if selected_material != "All":
        filtered_df = filtered_df[filtered_df["material"] == selected_material]
    if search_term:
        filtered_df = filtered_df[
            filtered_df["color"].str.contains(search_term, case=False, na=False) |
            filtered_df["id"].astype(str).str.contains(search_term)
        ]

    for index, row in filtered_df.iterrows():
        st.subheader(f"{row['color']} ({row['material']})")
        st.image(row["image_url"], width=400)
        st.write(f"Size: {row['size']}")
        st.write("---")

elif menu == "Admin (Protected)":
    st.title("Admin Area")
    password = st.text_input("Enter password", type="password")
    if password == "PrimeCountertops":
        st.success("Access Granted")
        uploaded_file = st.file_uploader("Upload new CSV to replace stock", type="csv")
        if uploaded_file is not None:
            with open("remnants.csv", "wb") as f:
                f.write(uploaded_file.read())
            st.success("Stock updated successfully. Refresh the page to see changes.")
    else:
        st.warning("Access Restricted")
