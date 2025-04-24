#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 19 18:28:16 2025

@author: sjouk
"""


import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configureer de pagina voor maximale breedte
st.set_page_config(
    page_title="Analysetool Asfaltonderhoud",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS op basis van RWS stijlgids
st.markdown("""
<style>
    /* Algemene kleuren & typografie */
    html, body, [class*="css"]  {
        background-color: #ffffff;
        color: #535353;
        font-family: "Arial", sans-serif;
    }
    .stApp {
        background-color: #ffffff;
    }

    /* Headers styling */
    .css-10trblm {  /* Main title */
        color: #154273 !important;
        font-family: "Arial", sans-serif !important;
        font-weight: 600 !important;
        font-size: 2.5rem !important;
    }
    .css-1629p8f {  /* Section headers */
        color: #154273 !important;
        font-family: "Arial", sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
    }
    /* Sidebar headers */
    .css-79elbk, .css-j7qwjs {  /* Sidebar headers */
        color: #154273 !important;
        font-family: "Arial", sans-serif !important;
        font-weight: 600 !important;
    }
    .css-79elbk {  /* Main sidebar header */
        font-size: 1.5rem !important;
    }
    .css-j7qwjs {  /* Sidebar subheaders */
        font-size: 1.2rem !important;
    }

    /* Grijze kaart voor Huidige configuratie */
    .rws-card {
        background-color: #f2f2f2;
        padding: 1.5rem 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid #e0e0e0;
    }
    .rws-card h3 {
        color: #154273;
        margin-top: 0;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
    }
    .rws-card p {
        color: #535353;
        font-size: 1rem;
        margin: 0.4rem 0;
    }

    /* Tabs boven visualisaties */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background-color: transparent;
        padding: 0.5rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        background-color: #FFFDD8 !important;
        border-radius: 0.3rem;
        color: black !important;
        font-weight: 600;
    }
    .stTabs [data-baseweb="tab"] > div {
        background-color: #FFFDD8 !important;
        color: black !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FFFDD8 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #FFFDD8 !important;
        color: black !important;
    }

    /* Delta-stijlen in st.metric() */
    div[data-testid="stMetricDelta"] div[class*="css"] {
        color: #2ca02c !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricDelta"] svg {
        fill: #2ca02c !important;
    }

    /* Achtergrond onder tab-inhoud */
    [data-testid="stHeader"] ~ div[data-testid="stVerticalBlock"] .stTabs ~ div {
        background-color: #FFD100 !important;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)



# ==== SIDEBAR PARAMETERS ====
with st.sidebar:
    st.image("NIEUW-RWS-3488526-v1-logo_RWS_ministerie_Infrastructuur_en_Waterstaat_NL.png", width=300)
    st.markdown("<h2 style='color: #154273; font-size: 1.5rem; margin-bottom: 1rem;'>Input Parameters</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1rem;'>Wegdek Specificaties</h3>", unsafe_allow_html=True)
    opp_m2 = st.number_input("Totaal oppervlak wegdek (m²)", min_value=1000, value=70000, step=1000)
    type_wegdek = st.selectbox("Type wegdek", ["1L-ZOAB", "2L-ZOAB"])
    aantal_rijbanen = st.number_input("Aantal rijbanen", min_value=1, max_value=8, value=2)
    leeftijd_asfalt = st.slider("Leeftijd huidig asfalt (jaar)", 0, 6, 0)
    simulatieduur = st.slider("Simulatieduur (jaren)", 10, 100, 45)

    st.markdown("<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1rem;'>Kostenparameters</h3>", unsafe_allow_html=True)
    vaste_kosten = st.number_input("Vaste kosten per onderhoudsactie (€)", min_value=0, value=200000, step=10000)

    with st.expander("Conventionele Aanpak", expanded=True):
        kost_asfalt = st.number_input("Asfalt: Materiaalkosten (€/m²)", value=15.0)
        kost_hinder_asfalt = st.number_input("Asfalt: Verkeershinderkosten (€/m²)", value=7.0)

    with st.expander("LVOv Behandeling", expanded=True):
        kost_lvov = st.number_input("LVOv: Materiaalkosten (€/m²)", value=2.5)
        kost_hinder_lvov = st.number_input("LVOv: Verkeershinderkosten (€/m²)", value=1.5)


# Levensduur lookup functie
def bepaal_levensduur(type_wegdek, positie):
    matrix = {
        ("1L-ZOAB", "Linker rijweg"): 17,
        ("1L-ZOAB", "Rechter rijweg"): 11,
        ("2L-ZOAB", "Linker rijweg"): 13,
        ("2L-ZOAB", "Rechter rijweg"): 9
    }
    return matrix.get((type_wegdek, positie), 10)

# Init arrays
kosten_conv = np.zeros(simulatieduur + 1)
kosten_lvov = np.zeros(simulatieduur + 1)
co2_conv = np.zeros(simulatieduur + 1)
co2_lvov = np.zeros(simulatieduur + 1)

# Berekeningen per rijbaan
oppervlak_per_baan = opp_m2 / aantal_rijbanen
kosten_asfalt_baan = (kost_asfalt + kost_hinder_asfalt) * oppervlak_per_baan
kosten_lvov_baan = (kost_lvov + kost_hinder_lvov) * oppervlak_per_baan
co2_asfalt_baan = 5 * oppervlak_per_baan / 1000
co2_lvov_baan = 1.5 * oppervlak_per_baan / 1000


# ==== CONVENTIONELE STRATEGIE ====
for baan in range(aantal_rijbanen):
    positie = "Rechter rijweg" if baan == 0 else "Linker rijweg"
    levensduur = bepaal_levensduur(type_wegdek, positie)
    jaar = levensduur - leeftijd_asfalt  # start op basis van resterende levensduur
    while jaar <= simulatieduur:
        kosten_conv[jaar] += kosten_asfalt_baan + vaste_kosten
        co2_conv[jaar] += co2_asfalt_baan
        jaar += levensduur  # volgende cyclus

# ==== LVOv STRATEGIE ====
for baan in range(aantal_rijbanen):
    positie = "Rechter rijweg" if baan == 0 else "Linker rijweg"
    levensduur_basis = bepaal_levensduur(type_wegdek, positie)
    levensduur_huidig = levensduur_basis
    jaar = 6 - leeftijd_asfalt  # eerste LVOv wanneer asfalt 6 jaar oud is

    while jaar <= simulatieduur:
        # LVOv-behandeling
        kosten_lvov[jaar] += kosten_lvov_baan + vaste_kosten
        co2_lvov[jaar] += co2_lvov_baan

        jaar_vervanging = jaar + levensduur_huidig
        if jaar_vervanging <= simulatieduur:
            # vervanging
            kosten_lvov[jaar_vervanging] += kosten_asfalt_baan + vaste_kosten
            co2_lvov[jaar_vervanging] += co2_asfalt_baan

            # na vervanging: +3 jaar levensduur & herstart cyclus na 6 jaar
            levensduur_huidig += 3
            jaar = jaar_vervanging + 6
        else:
            break

# ==== CUMULATIEVE SOMMEN ====
kosten_conv_cum = np.cumsum(kosten_conv)
kosten_lvov_cum = np.cumsum(kosten_lvov)
co2_conv_cum = np.cumsum(co2_conv)
co2_lvov_cum = np.cumsum(co2_lvov)

st.title("Analysetool Asfaltonderhoud ZOAB-wegdek")

import streamlit.components.v1 as components

levensduur_rechts = bepaal_levensduur(type_wegdek, "Rechter rijweg")
levensduur_links = bepaal_levensduur(type_wegdek, "Linker rijweg")

components.html(f"""
    <div style="
        background-color: #f2f2f2;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e0e0e0;
        font-family: Arial, sans-serif;
    ">
        <h3 style="
            color: #154273;
            margin-top: 0;
            margin-bottom: 0.8rem;
            font-size: 1.6rem;
            font-family: Arial, sans-serif;
        ">
            Huidige configuratie
        </h3>
        <p style="
            color: #535353;
            font-size: 1rem;
            margin: 0.4rem 0;
            font-family: Arial, sans-serif;
        ">
            <strong>Wegdek:</strong> {type_wegdek} |
            <strong>Aantal rijbanen:</strong> {aantal_rijbanen} |
            <strong>Oppervlakte:</strong> {opp_m2:,.0f} m²
        </p>
        <p style="
            color: #535353;
            font-size: 1rem;
            margin: 0.4rem 0;
            font-family: Arial, sans-serif;
        ">
            <strong>Leeftijd huidig asfalt:</strong> {leeftijd_asfalt} jaar |
            <strong>Simulatieduur:</strong> {simulatieduur} jaar |
            <strong>Levensduur:</strong> {levensduur_rechts} jr (rechter), {levensduur_links} jr (linker)
        </p>
    </div>
""", height=180)





st.header(f"Resultaten over {simulatieduur} jaar")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Financiële Impact")
    st.metric("Conventioneel", f"€{kosten_conv_cum[-1]:,.0f}")
    st.metric("LVOv", f"€{kosten_lvov_cum[-1]:,.0f}")
    besparing = kosten_conv_cum[-1] - kosten_lvov_cum[-1]
    besparing_pct = 100 * besparing / kosten_conv_cum[-1] if kosten_conv_cum[-1] else 0
    st.metric("Besparing", f"€{besparing:,.0f}", f"{besparing_pct:.1f}%")

with col2:
    st.subheader("Milieu Impact (CO₂)")
    st.metric("Conventioneel", f"{co2_conv_cum[-1]:.1f} ton")
    st.metric("LVOv", f"{co2_lvov_cum[-1]:.1f} ton")
    co2_besp = co2_conv_cum[-1] - co2_lvov_cum[-1]
    co2_besp_pct = 100 * co2_besp / co2_conv_cum[-1] if co2_conv_cum[-1] else 0
    st.metric("Besparing", f"{co2_besp:.1f} ton", f"{co2_besp_pct:.1f}%")

st.header("Visualisaties")
tab1, tab2, tab3 = st.tabs(["Cumulatieve Kosten", "Cumulatieve CO₂", "Jaarlijkse Kosten"])

# Set style for all plots
plt.rcParams['axes.labelcolor'] = '#154273'
plt.rcParams['axes.titlecolor'] = '#154273'
plt.rcParams['text.color'] = '#154273'


with tab1:
    fig1, ax1 = plt.subplots()
    ax1.plot(kosten_conv_cum, label="Conventioneel")
    ax1.plot(kosten_lvov_cum, label="LVOv")
    ax1.set_title("Cumulatieve Kosten (€)")
    ax1.set_xlabel("Jaar")
    ax1.set_ylabel("€")
    ax1.legend()
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots()
    ax2.plot(co2_conv_cum, label="Conventioneel")
    ax2.plot(co2_lvov_cum, label="LVOv")
    ax2.set_title("Cumulatieve CO₂-uitstoot (ton)")
    ax2.set_xlabel("Jaar")
    ax2.set_ylabel("CO₂ (ton)")
    ax2.legend()
    st.pyplot(fig2)

with tab3:
    fig3, ax3 = plt.subplots()
    jaren_range = range(simulatieduur + 1)
    width = 0.4
    ax3.bar([j - width/2 for j in jaren_range], kosten_conv, width, label="Conventioneel")
    ax3.bar([j + width/2 for j in jaren_range], kosten_lvov, width, label="LVOv")
    ax3.set_title("Jaarlijkse Kosten")
    ax3.set_xlabel("Jaar")
    ax3.set_ylabel("Kosten (€)")
    ax3.legend()
    st.pyplot(fig3)
