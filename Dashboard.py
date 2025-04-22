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
/* RWS-stijl knoppen */
    button[kind="primary"] {
        background-color: #154273 !important;
        color: white !important;
        border-radius: 6px !important;
        font-weight: bold;
    }

    /* Sliders achtergrondkleur en stijl */
    .stSlider > div[data-baseweb="slider"] {
        background-color: #f2f2f2 !important;
        padding: 0.2rem;
        border-radius: 8px;
    }

    .stSlider span[role="slider"] {
        background-color: #154273 !important;
        border: 2px solid #FFD100 !important;
    }

</style>
""", unsafe_allow_html=True)


# ==== SIDEBAR PARAMETERS ===
with st.sidebar:
    st.image("NIEUW-RWS-3488526-v1-logo_RWS_ministerie_Infrastructuur_en_Waterstaat_NL.png", width=300)
    st.markdown("<h2 style='color: #154273; font-size: 1.5rem; margin-bottom: 1rem;'>Input Parameters</h2>", unsafe_allow_html=True)

    st.markdown("<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1rem;'>Wegdek Specificaties</h3>", unsafe_allow_html=True)
    opp_m2 = st.number_input("Oppervlakte wegdek per rijbaan (m²)", min_value=100, value=70000, step=100)
    type_wegdek = st.selectbox("Type wegdek", ["1L-ZOAB", "2L-ZOAB"])
    aantal_rijbanen = st.slider("Aantal rijbanen", min_value=1, max_value=8, value=2)
    leeftijd_asfalt = st.slider("Leeftijd huidig asfalt (jaar)", min_value=0, max_value=6, value=0)
    jaren = st.slider("Duur simulatieperiode (jaren)", min_value=10, max_value=100, value=45)

    st.markdown("<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1rem;'>Kostenparameters</h3>", unsafe_allow_html=True)
    vaste_kosten = st.number_input("Vaste begeleidingskosten per behandeling (€)", min_value=0, value=200000, step=1000)

    with st.expander("Conventionele Aanpak", expanded=True):
        kost_asfalt = st.number_input("Materiaal kosten asfalt (€/m²)", value=15.0)
        kost_hinder_asfalt = st.number_input("Verkeershinderkosten asfalt (€/m²)", value=7.0)

    with st.expander("LVOv Behandeling", expanded=True):
        kost_lvov = st.number_input("Materiaal kosten LVOv (€/m²)", value=2.5)
        kost_hinder_lvov = st.number_input("Verkeershinderkosten LVOv (€/m²)", value=1.5)

# Levensduur per rijbaan (om en om rechts/links)
def bepaal_levensduur(type_wegdek, is_rechter):
    matrix = {
        ("1L-ZOAB", True): 11,
        ("1L-ZOAB", False): 17,
        ("2L-ZOAB", True): 9,
        ("2L-ZOAB", False): 13
    }
    return matrix.get((type_wegdek, is_rechter), 10)

kosten_conv = np.zeros(jaren + 1)
kosten_lvov_arr = np.zeros(jaren + 1)
co2_conv = np.zeros(jaren + 1)
co2_lvov_arr = np.zeros(jaren + 1)


# ====== KLASSEN EN SIMULATIE LOGICA ======

class Rijbaan:
    def __init__(self, is_rechter, levensduur, opp_m2, jaar_start):
        self.is_rechter = is_rechter
        self.levensduur_initieel = levensduur
        self.resterende_levensduur = levensduur
        self.laatste_lvo = jaar_start - 6  # zodat eerste LVOv op jaar_start + 6 mag
        self.jaar_laatste_vervanging = jaar_start

    def behandel_jaar(self, jaar, kosten_lvov_arr, kosten_conv, co2_lvov_arr, co2_conv,
                      kosten_asfalt, kosten_lvov, co2_asfalt, co2_lvov, vaste_kosten):

        # Check conventionele vervanging
        if self.resterende_levensduur <= 0:
            kosten_conv[jaar] += kosten_asfalt + vaste_kosten
            co2_conv[jaar] += co2_asfalt
            self.resterende_levensduur = self.levensduur_initieel
            self.laatste_lvo = jaar  # Na vervanging mag LVOv pas weer over 6 jaar
            self.jaar_laatste_vervanging = jaar

        # Check LVOv (na 6 jaar sinds aanleg of laatste vervanging)
        elif jaar - self.laatste_lvo >= 6:
            kosten_lvov_arr[jaar] += kosten_lvov + vaste_kosten
            co2_lvov_arr[jaar] += co2_lvov
            self.resterende_levensduur += 3
            self.laatste_lvo = jaar

        self.resterende_levensduur -= 1


# ====== SIMULATIE PER RIJBAAN MET KLASSE ======
rijbanen_obj = []

for rijbaan in range(aantal_rijbanen):
    is_rechter = rijbaan == 0  # eerste is rechter, rest links
    levensduur = bepaal_levensduur(type_wegdek, is_rechter)
    rijbanen_obj.append(Rijbaan(is_rechter, levensduur, opp_m2, jaar_start=0))

kosten_asfalt = (kost_asfalt + kost_hinder_asfalt) * opp_m2
kosten_lvov = (kost_lvov + kost_hinder_lvov) * opp_m2
co2_asfalt = 5 * opp_m2 / 1000
co2_lvov = 1.5 * opp_m2 / 1000

kosten_conv = np.zeros(jaren + 1)
kosten_lvov_arr = np.zeros(jaren + 1)
co2_conv = np.zeros(jaren + 1)
co2_lvov_arr = np.zeros(jaren + 1)

for jaar in range(jaren + 1):
    for baan in rijbanen_obj:
        baan.behandel_jaar(
            jaar,
            kosten_lvov_arr,
            kosten_conv,
            co2_lvov_arr,
            co2_conv,
            kosten_asfalt,
            kosten_lvov,
            co2_asfalt,
            co2_lvov,
            vaste_kosten
        )

kosten_conv_cum = np.cumsum(kosten_conv)
kosten_lvov_cum = np.cumsum(kosten_lvov_arr)
co2_conv_cum = np.cumsum(co2_conv)
co2_lvov_cum = np.cumsum(co2_lvov_arr)

# ==== Resultaten & Visualisatie ====

st.title("Analysetool Asfaltonderhoud ZOAB-wegdek")

import streamlit.components.v1 as components

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
            <strong>Type wegdek:</strong> {type_wegdek} |
            <strong>Rijbanen:</strong> {aantal_rijbanen} |
            <strong>Opp./rijbaan:</strong> {opp_m2:,} m²
        </p>
        <p style="
            color: #535353;
            font-size: 1rem;
            margin: 0.4rem 0;
            font-family: Arial, sans-serif;
        ">
            <strong>Leeftijd asfalt:</strong> {leeftijd_asfalt} jaar |
            <strong>Simulatieduur:</strong> {jaren} jaar
        </p>
        <p style="
            color: #535353;
            font-size: 1rem;
            margin: 0.4rem 0;
            font-family: Arial, sans-serif;
        ">
            <strong>Vaste kosten per behandeling:</strong> €{vaste_kosten:,}
        </p>
    </div>
""", height=200)




st.header(f"Resultaten over {jaren} jaar")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Financiële Impact")
    st.metric("Conventionele aanpak", f"€{kosten_conv_cum[-1]:,.0f}")
    st.metric("LVOv aanpak", f"€{kosten_lvov_cum[-1]:,.0f}")
    besparing = kosten_conv_cum[-1] - kosten_lvov_cum[-1]
    besparing_pct = (besparing / kosten_conv_cum[-1]) * 100
    st.metric("Besparing", f"€{besparing:,.0f}", f"{besparing_pct:.1f}%")

with col2:
    st.subheader("Milieu Impact")
    st.metric("Conventionele aanpak", f"{co2_conv_cum[-1]:.1f} ton")
    st.metric("LVOv aanpak", f"{co2_lvov_cum[-1]:.1f} ton")
    co2_besp = co2_conv_cum[-1] - co2_lvov_cum[-1]
    co2_besp_pct = (co2_besp / co2_conv_cum[-1]) * 100
    st.metric("Besparing", f"{co2_besp:.1f} ton", f"{co2_besp_pct:.1f}%")

st.header("Visualisaties")
tab1, tab2, tab3 = st.tabs(["Cumulatieve Kosten", "Cumulatieve CO₂", "Jaarlijkse Kosten"])

# Set style for all plots
plt.rcParams['axes.labelcolor'] = '#154273'
plt.rcParams['axes.titlecolor'] = '#154273'
plt.rcParams['text.color'] = '#154273'

with tab1:
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(range(jaren + 1), kosten_conv_cum, label="Conventioneel", color="#154273")
    ax1.plot(range(jaren + 1), kosten_lvov_cum, label="LVOv", color="#FFD100")
    ax1.set_xlabel("Jaar", color='#154273', fontsize=11)
    ax1.set_ylabel("Cumulatieve kosten (€)", color='#154273', fontsize=11)
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.tick_params(colors='#154273')
    ax1.legend()
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(range(jaren + 1), co2_conv_cum, label="Conventioneel", color="#154273")
    ax2.plot(range(jaren + 1), co2_lvov_cum, label="LVOv", color="#FFD100")
    ax2.set_xlabel("Jaar", color='#154273', fontsize=11)
    ax2.set_ylabel("Cumulatieve CO₂-uitstoot (ton)", color='#154273', fontsize=11)
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.tick_params(colors='#154273')
    ax2.legend()
    st.pyplot(fig2)

with tab3:
    fig3, ax3 = plt.subplots(figsize=(12, 6))
    x = range(jaren + 1)
    width = 0.35
    ax3.bar([i - width/2 for i in x], kosten_conv, width, label="Conventioneel", color="#154273", alpha=0.7)
    ax3.bar([i + width/2 for i in x], kosten_lvov_arr, width, label="LVOv", color="#FFD100", alpha=0.7)
    ax3.set_xlabel("Jaar", color='#154273', fontsize=11)
    ax3.set_ylabel("Kosten (€)", color='#154273', fontsize=11)
    ax3.grid(True, linestyle='--', alpha=0.7)
    ax3.tick_params(colors='#154273')
    ax3.legend()
    st.pyplot(fig3)
