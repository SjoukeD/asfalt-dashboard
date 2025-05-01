import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import base64

# Encode logo image
def get_base64_logo():
    with open("NIEUW-RWS-3488526-v1-logo_RWS_ministerie_Infrastructuur_en_Waterstaat_NL.png", "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode()

base64_logo = get_base64_logo()

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
        font-family: "RijksoverheidSans", "Rijksoverheid Sans", sans-serif;
    }
    .stApp {
        background-color: #ffffff;
    }

    /* Headers styling */
    .css-10trblm {  /* Main title */
        color: #154273 !important;
        font-family: "RijksoverheidSans", "Rijksoverheid Sans", sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.5px !important;
        line-height: 1.2 !important;
        margin-bottom: 1.5rem !important;
        padding: 1.5rem 0 !important;
        border-bottom: 3px solid #154273 !important;
        text-transform: none !important;
    }

    /* Title container */
    .title-container {
        margin-bottom: 2rem;
        padding: 0.5rem 0;
    }

    /* Subtitle styling */
    .subtitle {
        color: #666666;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0.5rem;
        font-family: "RijksoverheidSans", "Rijksoverheid Sans", sans-serif;
    }
    }
    .css-1629p8f {  /* Section headers */
        color: #154273 !important;
        font-family: "RijksoverheidSans", "Rijksoverheid Sans", sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.8rem !important;
    }
    /* Sidebar headers */
    .css-79elbk, .css-j7qwjs {  /* Sidebar headers */
        color: #154273 !important;
        font-family: "RijksoverheidSans", "Rijksoverheid Sans", sans-serif !important;
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
        font-family: "RijksoverheidSans", "Rijksoverheid Sans", sans-serif;
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

    /* Logo styling */
    [data-testid="stSidebarNav"] img {
        background-color: #FFFDD8;
        padding: 1rem;
        border-radius: 0.5rem;
    }

</style>
""", unsafe_allow_html=True)



# ==== SIDEBAR PARAMETERS ====
# Display title and subtitle with professional styling
st.markdown("""
<div class="title-container">
    <h1 class="css-10trblm">Analysetool Asfaltonderhoud ZOAB-wegdek</h1>
    <p class="subtitle">Vergelijkende analyse van conventionele en LVOv onderhoudsmethoden</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    # Display logo
    st.markdown("""
        <div style='margin-bottom: 1rem;'>
            <img src='data:image/png;base64,{}' width='300'>
        </div>
    """.format(base64_logo), unsafe_allow_html=True)
    st.markdown("<h2 style='color: #154273; font-size: 1.5rem; margin-bottom: 1rem;'>Input Parameters</h2>", unsafe_allow_html=True)
    
    # Wegdek parameters
    st.subheader("Wegdek")
    type_wegdek = st.selectbox(
        "Type wegdek",
        ["1L-ZOAB", "2L-ZOAB", "ZOAB 0/8", "ZOAB 0/11", "DZOAB", "Fijn ZOAB", "ZOAB +"]
    )
    
    # Default levensduur op basis van type wegdek
    wegdek_defaults = {
        "1L-ZOAB": (17, 11),
        "2L-ZOAB": (13, 9),
        "ZOAB 0/8": (17, 11),
        "ZOAB 0/11": (18, 12),
        "DZOAB": (20, 14),
        "Fijn ZOAB": (15, 10),
        "ZOAB +": (14, 9)
    }
    default_left, default_right = wegdek_defaults[type_wegdek]
    
    # Aangepaste levensduur inputs
    st.subheader("Aangepaste Levensduur")
    custom_left = st.number_input(
        "Levensduur linker rijstrook (jaren)",
        min_value=5,
        max_value=30,
        value=default_left,
        help="Standaard: 17 jaar voor 1L-ZOAB, 13 jaar voor 2L-ZOAB"
    )
    custom_right = st.number_input(
        "Levensduur rechter rijstrook (jaren)",
        min_value=5,
        max_value=30,
        value=default_right,
        help="Standaard: 11 jaar voor 1L-ZOAB, 9 jaar voor 2L-ZOAB"
    )

    opp_m2 = st.number_input("Totaal oppervlak wegdek (m²)", min_value=1000, value=70000, step=1000)
    aantal_rijbanen = st.number_input("Aantal rijstroken", min_value=1, max_value=8, value=2)
    leeftijd_asfalt = st.slider("Leeftijd huidig asfalt (jaar)", 0, 6, 0)
    simulatieduur = st.slider("Contractsduur Onderhoud(jaren)", 10, 45, 45)

    # CO2 uitstoot parameters
    co2_conv = st.number_input(
        "CO₂ uitstoot per m² voor conventionele behandeling (ton)",
        min_value=0.0,
        max_value=0.1,
        value=0.00693,
        step=0.00001,
        format="%.5f"
    )
    co2_lvov = st.number_input(
        "CO₂ uitstoot per m² voor LVOv behandeling (ton)",
        min_value=0.0,
        max_value=0.1,
        value=0.000291,
        step=0.00001,
        format="%.5f"
    )

    st.markdown("<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1rem;'>Kostenparameters</h3>", unsafe_allow_html=True)
    vaste_kosten = st.number_input("Begeleidingskosten per onderhoudsactie (€)", min_value=0, value=200000, step=10000)

    with st.expander("Conventionele Aanpak", expanded=True):
        kost_asfalt = st.number_input("Asfalt: Materiaalkosten (€/m²)", value=35.0)
        kost_hinder_asfalt = st.number_input("Asfalt: Verkeershinderkosten (€/m²)", value=7.0)

    with st.expander("LVOv Behandeling", expanded=True):
        kost_lvov = st.number_input("LVOv: Materiaalkosten (€/m²)", value=1.5)
        kost_hinder_lvov = st.number_input("LVOv: Verkeershinderkosten (€/m²)", value=1.5)


# Levensduur lookup functie
def bepaal_levensduur(type_wegdek, positie, custom_left=None, custom_right=None):
    """Bepaalt de levensduur van het wegdek op basis van type en positie.
    
    Args:
        type_wegdek: Type asfalt (ZOAB 0/8, ZOAB 0/11, DZOAB, Fijn ZOAB, ZOAB +)
        positie: 'Linker rijweg' of 'Rechter rijweg'
        custom_left: Aangepaste levensduur voor linker rijweg
        custom_right: Aangepaste levensduur voor rechter rijweg
    """
    default_matrix = {
        ("1L-ZOAB", "Linker rijstrook"): 17,
        ("1L-ZOAB", "Rechter rijstrook"): 11,
        ("2L-ZOAB", "Linker rijstrook"): 13,
        ("2L-ZOAB", "Rechter rijstrook"): 9,
        ("ZOAB 0/8", "Linker rijstrook"): 17,
        ("ZOAB 0/8", "Rechter rijstrook"): 11,
        ("ZOAB 0/11", "Linker rijstrook"): 18,
        ("ZOAB 0/11", "Rechter rijstrook"): 12,
        ("DZOAB", "Linker rijstrook"): 20,
        ("DZOAB", "Rechter rijstrook"): 14,
        ("Fijn ZOAB", "Linker rijstrook"): 15,
        ("Fijn ZOAB", "Rechter rijstrook"): 10,
        ("ZOAB +", "Linker rijstrook"): 14,
        ("ZOAB +", "Rechter rijstrook"): 9
    }
    
    if positie == "Linker rijstrook" and custom_left is not None:
        return custom_left
    elif positie == "Rechter rijstrook" and custom_right is not None:
        return custom_right
    else:
        return default_matrix[(type_wegdek, positie)]

def kosten_linker_baan_conventioneel(type_wegdek, duur, oppervlakte, vaste_kosten,
                                     kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
                                     leeftijd_asfalt=0):
    """Simuleert jaarlijkse en cumulatieve kosten en CO₂-uitstoot voor conventionele strategie (linker rijstrook)."""
    levensduur = bepaal_levensduur(type_wegdek, "Linker rijstrook", custom_left, custom_right)
    jaarlijkse_kosten = [0] * duur
    jaarlijkse_co2 = [0] * duur
    cumulatieve_kosten = [0] * duur
    cumulatieve_co2 = [0] * duur

    # Bereken eerste onderhoudsmoment op basis van huidige leeftijd
    eerste_onderhoud = levensduur - leeftijd_asfalt
    if eerste_onderhoud <= 0:
        eerste_onderhoud = 1  # Als het asfalt al over de levensduur heen is, direct onderhoud

    # Start with no costs in year 0
    jaarlijkse_kosten[0] = 0
    jaarlijkse_co2[0] = 0

    # Conventionele strategie: vervang asfalt elke levensduur, begin vanaf eerste_onderhoud
    for jaar in range(1, duur):
        if jaar == eerste_onderhoud or (jaar > eerste_onderhoud and (jaar - eerste_onderhoud) % levensduur == 0):
            # Only apply fixed costs if this is not a single lane road
            if oppervlakte > 0:  # This means it's not a single lane road
                jaarlijkse_kosten[jaar] = vaste_kosten + (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            else:
                jaarlijkse_kosten[jaar] = oppervlakte * (kost_asfalt + kost_hinder_asfalt)
            jaarlijkse_co2[jaar] = oppervlakte * co2_conv  # CO2 uitstoot per m2

    # Bereken cumulatieve waarden
    for jaar in range(duur):
        if jaar == 0:
            cumulatieve_kosten[jaar] = jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = jaarlijkse_co2[jaar]
        else:
            cumulatieve_kosten[jaar] = cumulatieve_kosten[jaar-1] + jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = cumulatieve_co2[jaar-1] + jaarlijkse_co2[jaar]

    return jaarlijkse_kosten, cumulatieve_kosten, jaarlijkse_co2, cumulatieve_co2

def kosten_rechter_baan_conventioneel(type_wegdek, duur, oppervlakte, vaste_kosten,
                                     kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
                                     leeftijd_asfalt=0):
    """Simuleert jaarlijkse en cumulatieve kosten en CO₂-uitstoot voor conventionele strategie (rechter rijstrook)."""
    levensduur = bepaal_levensduur(type_wegdek, "Rechter rijstrook", custom_left, custom_right)
    jaarlijkse_kosten = [0] * duur
    jaarlijkse_co2 = [0] * duur
    cumulatieve_kosten = [0] * duur
    cumulatieve_co2 = [0] * duur

    # Bereken eerste onderhoudsmoment op basis van huidige leeftijd
    eerste_onderhoud = levensduur - leeftijd_asfalt
    if eerste_onderhoud <= 0:
        eerste_onderhoud = 1  # Als het asfalt al over de levensduur heen is, direct onderhoud

    # Start with no costs in year 0
    jaarlijkse_kosten[0] = 0
    jaarlijkse_co2[0] = 0

    # Conventionele strategie: vervang asfalt elke levensduur, begin vanaf eerste_onderhoud
    for jaar in range(1, duur):
        if jaar == eerste_onderhoud or (jaar > eerste_onderhoud and (jaar - eerste_onderhoud) % levensduur == 0):
            jaarlijkse_kosten[jaar] = vaste_kosten + (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            jaarlijkse_co2[jaar] = oppervlakte * 0.00693 # CO2 uitstoot per m2

    # Bereken cumulatieve waarden
    for jaar in range(duur):
        if jaar == 0:
            cumulatieve_kosten[jaar] = jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = jaarlijkse_co2[jaar]
        else:
            cumulatieve_kosten[jaar] = cumulatieve_kosten[jaar-1] + jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = cumulatieve_co2[jaar-1] + jaarlijkse_co2[jaar]

    return jaarlijkse_kosten, cumulatieve_kosten, jaarlijkse_co2, cumulatieve_co2

def kosten_linker_baan_lvov(type_wegdek, duur, oppervlakte, vaste_kosten,
                            kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
                            leeftijd_asfalt=0):
    """Simuleert jaarlijkse en cumulatieve kosten en CO₂-uitstoot voor LVOv-strategie (linker rijstrook)."""
    levensduur = bepaal_levensduur(type_wegdek, "Linker rijstrook", custom_left, custom_right)
    jaarlijkse_kosten = [0] * duur
    jaarlijkse_co2 = [0] * duur
    cumulatieve_kosten = [0] * duur
    cumulatieve_co2 = [0] * duur
    
    # Bereken eerste onderhoudsmoment op basis van huidige leeftijd
    eerste_onderhoud = 6 - leeftijd_asfalt  # LVOv start na 6 jaar
    if eerste_onderhoud <= 0:
        eerste_onderhoud = 1  # Als het asfalt al over de 6 jaar heen is, direct LVOv

    # Start with no costs in year 0
    jaarlijkse_kosten[0] = 0
    jaarlijkse_co2[0] = 0

    # LVOv strategie: begin na eerste_onderhoud (6 jaar - huidige leeftijd), herhaal elke 4 jaar
    # In de laatste 8 jaar geen LVOv meer, alleen eindkosten
    for jaar in range(1, duur):
        if jaar >= eerste_onderhoud and (jaar - eerste_onderhoud) % 4 == 0 and jaar <= duur - 8:
            jaarlijkse_kosten[jaar] = (oppervlakte * (kost_lvov + kost_hinder_lvov))
            jaarlijkse_co2[jaar] = oppervlakte * co2_lvov # CO2 uitstoot per m2
        elif jaar == duur:
            # Eindkosten in laatste jaar
            jaarlijkse_kosten[jaar-1] = (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            jaarlijkse_co2[jaar] = oppervlakte * co2_lvov # CO2 uitstoot per m2

    # Bereken cumulatieve waarden
    for jaar in range(duur):
        if jaar == 0:
            cumulatieve_kosten[jaar] = jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = jaarlijkse_co2[jaar]
        else:
            cumulatieve_kosten[jaar] = cumulatieve_kosten[jaar-1] + jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = cumulatieve_co2[jaar-1] + jaarlijkse_co2[jaar]

    return jaarlijkse_kosten, cumulatieve_kosten, jaarlijkse_co2, cumulatieve_co2

def kosten_rechter_baan_lvov(type_wegdek, duur, oppervlakte, vaste_kosten,
                             kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
                             leeftijd_asfalt=0):
    """Simuleert jaarlijkse en cumulatieve kosten en CO₂-uitstoot voor LVOv-strategie (rechter rijstrook)."""
    levensduur = bepaal_levensduur(type_wegdek, "Rechter rijstrook", custom_left, custom_right)
    jaarlijkse_kosten = [0] * duur
    jaarlijkse_co2 = [0] * duur
    cumulatieve_kosten = [0] * duur
    cumulatieve_co2 = [0] * duur
    
    # Bereken eerste onderhoudsmoment op basis van huidige leeftijd
    eerste_onderhoud = 6 - leeftijd_asfalt  # LVOv start na 6 jaar
    if eerste_onderhoud <= 0:
        eerste_onderhoud = 1  # Als het asfalt al over de 6 jaar heen is, direct LVOv

    # Start with no costs in year 0
    jaarlijkse_kosten[0] = 0
    jaarlijkse_co2[0] = 0

    # LVOv strategie: begin na eerste_onderhoud (6 jaar - huidige leeftijd), herhaal elke 4 jaar
    # In de laatste 8 jaar geen LVOv meer, alleen eindkosten
    for jaar in range(1, duur):
        if jaar >= eerste_onderhoud and (jaar - eerste_onderhoud) % 4 == 0 and jaar <= duur - 8:
            jaarlijkse_kosten[jaar] = vaste_kosten + (oppervlakte * (kost_lvov + kost_hinder_lvov))
            jaarlijkse_co2[jaar] = oppervlakte * co2_lvov # CO2 uitstoot per m2
        elif jaar == duur:
            # Eindkosten in laatste jaar
            jaarlijkse_kosten[jaar-1] = vaste_kosten + (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            jaarlijkse_co2[jaar-1] = oppervlakte * 0.000291  # CO2 uitstoot per m2

    # Bereken cumulatieve waarden
    for jaar in range(duur):
        if jaar == 0:
            cumulatieve_kosten[jaar] = jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = jaarlijkse_co2[jaar]
        else:
            cumulatieve_kosten[jaar] = cumulatieve_kosten[jaar-1] + jaarlijkse_kosten[jaar]
            cumulatieve_co2[jaar] = cumulatieve_co2[jaar-1] + jaarlijkse_co2[jaar]

    return jaarlijkse_kosten, cumulatieve_kosten, jaarlijkse_co2, cumulatieve_co2

# ... (rest of the code remains the same)
verdeling = {
    1: (1.0, 0.0),
    2: (0.5, 0.5),
    3: (1/3, 2/3),
    4: (0.25, 0.75),
    5: (0.2, 0.8),
    6: (1/6, 5/6),
    7: (1/7, 6/7),
    8: (0.125, 0.875)
}
perc_rechts, perc_links = verdeling[aantal_rijbanen]
opp_rechts = opp_m2 * perc_rechts
opp_links = opp_m2 * perc_links

# Strategiekeuze
duur = simulatieduur

# == Conventioneel
jr_k_r_conv, cum_k_r_conv, jr_c_r_conv, cum_c_r_conv = kosten_rechter_baan_conventioneel(
    type_wegdek, simulatieduur, opp_rechts, vaste_kosten,
    kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
    leeftijd_asfalt
)

jr_k_l_conv, cum_k_l_conv, jr_c_l_conv, cum_c_l_conv = kosten_linker_baan_conventioneel(
    type_wegdek, simulatieduur, opp_links, vaste_kosten,
    kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
    leeftijd_asfalt
)

kosten_conv = np.array(jr_k_r_conv) + np.array(jr_k_l_conv)
kosten_conv_cum = np.array(cum_k_r_conv) + np.array(cum_k_l_conv)
co2_conv = np.array(jr_c_r_conv) + np.array(jr_c_l_conv)
co2_conv_cum = np.array(cum_c_r_conv) + np.array(cum_c_l_conv)

# == LVOv
jr_k_r_lvov, cum_k_r_lvov, jr_c_r_lvov, cum_c_r_lvov = kosten_rechter_baan_lvov(
    type_wegdek, simulatieduur, opp_rechts, vaste_kosten,
    kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
    leeftijd_asfalt
)

jr_k_l_lvov, cum_k_l_lvov, jr_c_l_lvov, cum_c_l_lvov = kosten_linker_baan_lvov(
    type_wegdek, simulatieduur, opp_links, vaste_kosten,
    kost_asfalt, kost_hinder_asfalt, kost_lvov, kost_hinder_lvov,
    leeftijd_asfalt
)

kosten_lvov = np.array(jr_k_r_lvov) + np.array(jr_k_l_lvov)
kosten_lvov_cum = np.array(cum_k_r_lvov) + np.array(cum_k_l_lvov)
co2_lvov = np.array(jr_c_r_lvov) + np.array(jr_c_l_lvov)
co2_lvov_cum = np.array(cum_c_r_lvov) + np.array(cum_c_l_lvov)

import streamlit.components.v1 as components

levensduur_rechts = bepaal_levensduur(type_wegdek, "Rechter rijstrook")
levensduur_links = bepaal_levensduur(type_wegdek, "Linker rijstrook")

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
            <strong>Aantal rijstroken:</strong> {aantal_rijbanen} |
            <strong>Oppervlakte:</strong> {opp_m2:,.0f} m²
        </p>
        <p style="
            color: #535353;
            font-size: 1rem;
            margin: 0.4rem 0;
            font-family: Arial, sans-serif;
        ">
            <strong>Leeftijd huidig asfalt:</strong> {leeftijd_asfalt} jaar |
            <strong>Contractsduur:</strong> {simulatieduur} jaar |
            <strong>Levensduur:</strong> {levensduur_rechts} jr (rechter), {levensduur_links} jr (linker)
        </p>
    </div>
""", height=180)

st.markdown("""
<style>
    .results-hero {
        background-size: cover;
        background-position: center;
        position: relative;
        padding: 4rem 0;
        margin-bottom: 2rem;
    }
    .results-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(rgba(255, 255, 255, 0.85), rgba(255, 255, 255, 0.85));
    }
    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    .results-section { 
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    .results-header { 
        color: #154273;
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        font-family: 'RijksoverheidSans', system-ui, -apple-system, sans-serif;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    }
    .explanation-text {
        max-width: 800px;
        margin: 0 auto;
        text-align: center;
    }
    .explanation-text p {
        font-size: 1.4rem;
        line-height: 1.6;
        color: #1f2937;
        font-family: 'RijksoverheidSans', system-ui, -apple-system, sans-serif;
        text-shadow: 0 1px 1px rgba(255, 255, 255, 0.5);
    }
    .main-card {
        padding: 2rem;
        margin-bottom: 2rem;
    }
    .section-explanation {
        margin-bottom: 1.5rem;
    }
    .section-explanation p {
        font-size: 1rem;
        line-height: 1.5;
        color: #4b5563;
        margin: 0;
        font-family: 'RijksoverheidSans', system-ui, -apple-system, sans-serif;
    }
    .title-text {
        color: #154273;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        padding-bottom: 0.75rem;
        margin-bottom: 2rem;
        border-bottom: 4px solid #f5e251;
        font-family: 'RijksoverheidSans', system-ui, -apple-system, sans-serif;
        text-align: center;
    }
    .savings-card {
        background: #f3f4f6;
        border-radius: 8px;
        padding: 1.5rem;
    }
    [data-testid='stMetricLabel'] {
        font-size: 1rem !important;
        color: #374151 !important;
        font-weight: 500 !important;
        line-height: 1.4 !important;
        margin-bottom: 0.5rem !important;
    }
    [data-testid='stMetricValue'] {
        font-size: 2.5rem !important;
    }
    [data-testid='stMetricValue'] > div {
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        font-family: 'RijksoverheidSans', system-ui, -apple-system, sans-serif !important;
        color: #154273 !important;
    }
    [data-testid='stMetricDelta'] > div {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #16a34a !important;
    }
    div[data-testid='metric-container'] {
        gap: 0.25rem !important;
        padding: 0.75rem 0 !important;
        border-bottom: 1px solid #e5e7eb !important;
    }
    div[data-testid='metric-container']:last-child {
        border-bottom: none !important;
        padding-bottom: 0 !important;
    }
    div[data-testid='stHorizontalBlock'] > div {
        gap: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Load and encode the background image
from pathlib import Path
import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Get the background image
img_path = Path(__file__).parent / "Nederlandse-snelwegen_2.jpg"
encoded_img = get_base64_encoded_image(str(img_path))

# Create results section with background
st.markdown(f'''
<div class="results-hero" style="background-image: url(data:image/jpg;base64,{encoded_img});">
    <div class="hero-content">
        <h2 class="results-header">Resultaten over {simulatieduur} jaar</h2>
        <div class="explanation-text">
            <p>Deze resultaten tonen de vergelijking tussen de conventionele aanpak en de innovatieve LVOv methode voor wegonderhoud. 
            De berekeningen zijn gebaseerd op een periode van meerdere jaren en houden rekening met zowel financiële als milieu-impact.</p>
        </div>
    </div>
</div>
<div class="results-section">
''', unsafe_allow_html=True)


st.header("Resultaten")

# Add table styling
st.markdown("""
<style>
    .section-title {
        color: #154273;
        font-size: 2rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #154273;
        display: inline-block;
    }
    .section-description {
        color: #535353;
        font-size: 1rem;
        margin-bottom: 1.5rem;
        line-height: 1.5;
    }
    .financial-table {
        width: 100%;
        margin: 1.5rem 0 3rem 0;
        border-collapse: separate;
        border-spacing: 0;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .financial-table th {
        background-color: #154273;
        color: white;
        padding: 16px;
        text-align: left;
        font-size: 1.4rem;
    }
    .financial-table td {
        background-color: #f8f9fa;
        padding: 16px;
        border-bottom: 1px solid #dee2e6;
        font-size: 1.4rem;
    }
    .financial-table tr:last-child td {
        font-weight: bold;
        background-color: #FFFDD8;
        border-bottom: none;
    }
    .financial-table tr:hover td {
        background-color: #f0f0f0;
    }
    .financial-table tr:last-child:hover td {
        background-color: #fff5b8;
    }
</style>
""", unsafe_allow_html=True)

# Financial Impact Section
st.markdown("""
<div class='section-title'>Financiële Impact Analyse</div>
<div class='section-description'>
Deze tabel toont een vergelijking van de totale kosten tussen de conventionele aanpak en de LVOv-methode over de gehele simulatieperiode. 
De berekeningen omvatten zowel materiaalkosten als verkeershinderkosten. De 'Besparing met LVOv' regel laat zien hoeveel er potentieel 
bespaard kan worden door te kiezen voor de LVOv-aanpak.
</div>
""", unsafe_allow_html=True)

# Calculate financial savings percentage
kosten_besp_pct = ((kosten_conv_cum[-1] - kosten_lvov_cum[-1]) / kosten_conv_cum[-1]) * 100

financial_data = {
    'Aanpak': ['Conventioneel', 'LVOv', 'Besparing met LVOv'],
    'Totale Kosten': [
        f"€{kosten_conv_cum[-1]:,.0f}",
        f"€{kosten_lvov_cum[-1]:,.0f}",
        f"€{kosten_conv_cum[-1] - kosten_lvov_cum[-1]:,.0f} <span style='color: #28a745; margin-left: 10px;'>({kosten_besp_pct:.1f}%)</span>"
    ]
}

st.markdown("""
<table class='financial-table'>
    <tr>
        <th>Aanpak</th>
        <th>Totale Kosten</th>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
    </tr>
</table>
""".format(
    financial_data['Aanpak'][0], financial_data['Totale Kosten'][0],
    financial_data['Aanpak'][1], financial_data['Totale Kosten'][1],
    financial_data['Aanpak'][2], financial_data['Totale Kosten'][2]
), unsafe_allow_html=True)

# Environmental Impact Section
st.markdown("""
<div class='section-title'>Milieu Impact Analyse</div>
<div class='section-description'>
Deze tabel vergelijkt de CO₂-uitstoot van beide onderhoudsmethoden gedurende de simulatieperiode. De berekeningen zijn gebaseerd 
op de totale uitstoot tijdens onderhoudsactiviteiten, inclusief materiaalproductie en verkeershinder. De 'Besparing met LVOv' toont 
de potentiële CO₂-reductie die bereikt kan worden met de LVOv-methode.
</div>
""", unsafe_allow_html=True)

# Calculate CO2 savings percentage
co2_besp_pct = ((co2_conv_cum[-1] - co2_lvov_cum[-1]) / co2_conv_cum[-1]) * 100

environmental_data = {
    'Aanpak': ['Conventioneel', 'LVOv', 'Besparing met LVOv'],
    'CO₂ Uitstoot': [
        f"{co2_conv_cum[-1]:,.0f} ton",
        f"{co2_lvov_cum[-1]:,.0f} ton",
        f"{co2_conv_cum[-1] - co2_lvov_cum[-1]:,.0f} ton <span style='color: #28a745; margin-left: 10px;'>({co2_besp_pct:.1f}%)</span>"
    ]
}

st.markdown("""
<table class='financial-table'>
    <tr>
        <th>Aanpak</th>
        <th>CO₂ Uitstoot</th>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
    </tr>
    <tr>
        <td>{}</td>
        <td>{}</td>
    </tr>
</table>
""".format(
    environmental_data['Aanpak'][0], environmental_data['CO₂ Uitstoot'][0],
    environmental_data['Aanpak'][1], environmental_data['CO₂ Uitstoot'][1],
    environmental_data['Aanpak'][2], environmental_data['CO₂ Uitstoot'][2]
), unsafe_allow_html=True)

st.markdown("""
<style>
    .graph-header {
        color: #154273;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #FFFDD8;
    }
</style>
<div class='graph-header'>Visualisaties</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Cumulatieve Kosten", "Cumulatieve CO₂", "Jaarlijkse Kosten"])

# Set style for all plots
plt.rcParams['axes.labelcolor'] = '#154273'
plt.rcParams['axes.titlecolor'] = '#154273'
plt.rcParams['text.color'] = '#154273'

# Configure matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['axes.labelcolor'] = '#154273'
plt.rcParams['axes.titlecolor'] = '#154273'
plt.rcParams['text.color'] = '#154273'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3

# Create years array for x-axis
jaren = list(range(simulatieduur))  # 0 to simulatieduur-1

with tab1:
    fig_costs, ax_costs = plt.subplots(figsize=(10, 6))

    # Plot lines
    ax_costs.plot(jaren, kosten_conv_cum, label='Conventioneel', color='#154273', linewidth=2.5)
    ax_costs.plot(jaren, kosten_lvov_cum, label='LVOv', color='#f5e251', linewidth=2.5)

    # Customize title and labels
    ax_costs.set_title('Cumulatieve kosten over tijd', pad=20, fontsize=14, fontweight='bold')
    ax_costs.set_xlabel('Jaar', fontsize=12)
    ax_costs.set_ylabel('Kosten (€)', fontsize=12)

    # Customize grid
    ax_costs.grid(True, linestyle='--', alpha=0.7)

    # Customize legend
    ax_costs.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)

    # Format y-axis as currency
    fmt = ticker.FuncFormatter(lambda x, p: f'€{int(x):,}')
    ax_costs.yaxis.set_major_formatter(fmt)

    # Add spines (borders)
    for spine in ax_costs.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)

    # Customize ticks
    ax_costs.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(rotation=45)

    # Set background color
    ax_costs.set_facecolor('#f8f9fa')
    fig_costs.patch.set_facecolor('#ffffff')

    # Add subtle box around plot
    ax_costs.set_frame_on(True)
    ax_costs.patch.set_edgecolor('#e5e7eb')
    ax_costs.patch.set_linewidth(1)

    # Adjust layout
    plt.tight_layout()

    # Display the plot in Streamlit with custom CSS
    st.markdown('''
    <style>
        [data-testid="stImage"], [data-testid="stImage"] > img {
            background-color: white;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        }
    </style>
    ''', unsafe_allow_html=True)

    st.pyplot(fig_costs)

with tab2:
    fig_co2, ax_co2 = plt.subplots(figsize=(10, 6))

    # Plot lines
    ax_co2.plot(jaren, co2_conv_cum, label='Conventioneel', color='#154273', linewidth=2.5)
    ax_co2.plot(jaren, co2_lvov_cum, label='LVOv', color='#f5e251', linewidth=2.5)

    # Customize title and labels
    ax_co2.set_title('Cumulatieve CO$_2$ uitstoot over tijd', pad=20, fontsize=14, fontweight='bold')
    ax_co2.set_xlabel('Jaar', fontsize=12)
    ax_co2.set_ylabel('CO$_2$ uitstoot (ton)', fontsize=12)

    # Customize grid
    ax_co2.grid(True, linestyle='--', alpha=0.7)

    # Customize legend
    ax_co2.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)

    # Format y-axis
    fmt = ticker.FuncFormatter(lambda x, p: f'{int(x):,}')
    ax_co2.yaxis.set_major_formatter(fmt)

    # Add spines (borders)
    for spine in ax_co2.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)

    # Customize ticks
    ax_co2.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(rotation=45)

    # Set background color
    ax_co2.set_facecolor('#f8f9fa')
    fig_co2.patch.set_facecolor('#ffffff')

    # Add subtle box around plot
    ax_co2.set_frame_on(True)
    ax_co2.patch.set_edgecolor('#e5e7eb')
    ax_co2.patch.set_linewidth(1)

    # Adjust layout
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig_co2)

with tab3:
    fig_yearly, ax_yearly = plt.subplots(figsize=(10, 6))
    
    # Ensure both arrays have the same length
    min_len = min(len(kosten_conv), len(kosten_lvov))
    kosten_conv_plot = kosten_conv[:min_len]
    kosten_lvov_plot = kosten_lvov[:min_len]
    jaren = np.arange(min_len)
    width = 0.4
    
    # Plot bars
    ax_yearly.bar(jaren - width/2, kosten_conv_plot, width, label='Conventioneel', color='#154273')
    ax_yearly.bar(jaren + width/2, kosten_lvov_plot, width, label='LVOv', color='#f5e251')
    
    # Customize title and labels
    ax_yearly.set_title('Jaarlijkse kosten per aanpak', pad=20, fontsize=14, fontweight='bold')
    ax_yearly.set_xlabel('Jaar', fontsize=12)
    ax_yearly.set_ylabel('Kosten (€)', fontsize=12)
    
    # Customize grid
    ax_yearly.grid(True, linestyle='--', alpha=0.7, axis='y')  # Only horizontal grid lines
    
    # Customize legend
    ax_yearly.legend(frameon=True, fancybox=True, shadow=True, fontsize=10)
    
    # Format y-axis as currency
    fmt = ticker.FuncFormatter(lambda x, p: f'€{int(x):,}')
    ax_yearly.yaxis.set_major_formatter(fmt)
    
    # Add spines (borders)
    for spine in ax_yearly.spines.values():
        spine.set_visible(True)
        spine.set_linewidth(0.5)
    
    # Customize ticks
    ax_yearly.tick_params(axis='both', which='major', labelsize=10)
    plt.xticks(jaren, jaren, rotation=45)
    
    # Set background color
    ax_yearly.set_facecolor('#f8f9fa')
    fig_yearly.patch.set_facecolor('#ffffff')
    
    # Add subtle box around plot
    ax_yearly.set_frame_on(True)
    ax_yearly.patch.set_edgecolor('#e5e7eb')
    ax_yearly.patch.set_linewidth(1)
    
    # Adjust layout
    plt.tight_layout()
    
    # Display the plot in Streamlit
    st.pyplot(fig_yearly)

# Add tables below all graphs
st.markdown("""<hr style='margin: 2rem 0; border-color: #dee2e6;'>""", unsafe_allow_html=True)

# Table 1: Average costs and CO2 emissions
st.markdown('<div class="section-title">Gemiddelde Kosten en CO₂ Uitstoot per Jaar</div>', unsafe_allow_html=True)

# Calculate averages
avg_cost_conv = np.mean(kosten_conv)
avg_cost_lvov = np.mean(kosten_lvov)
avg_co2_conv = np.mean(co2_conv)
avg_co2_lvov = np.mean(co2_lvov)

# Add specific styling for bottom tables
st.markdown("""
<style>
    .bottom-table tr:hover td {
        background-color: #f8f9fa !important;
    }
</style>
""", unsafe_allow_html=True)

# Create averages table HTML
avg_table_html = '<table class="financial-table bottom-table"><thead><tr>'
avg_table_html += '<th>Methode</th><th>Gemiddelde Kosten per Jaar</th><th>Gemiddelde CO₂ Uitstoot per Jaar (ton)</th>'
avg_table_html += '</tr></thead><tbody>'

# Add conventional row
avg_table_html += f'<tr>'
avg_table_html += f'<td>Conventioneel</td>'
avg_table_html += f'<td>€{avg_cost_conv:,.0f}</td>'
avg_table_html += f'<td>{avg_co2_conv:.1f}</td>'
avg_table_html += '</tr>'

# Add LVOv row
avg_table_html += f'<tr>'
avg_table_html += f'<td>LVOv</td>'
avg_table_html += f'<td>€{avg_cost_lvov:,.0f}</td>'
avg_table_html += f'<td>{avg_co2_lvov:.1f}</td>'
avg_table_html += '</tr>'

avg_table_html += '</tbody></table>'
st.markdown(avg_table_html, unsafe_allow_html=True)

# Table 2: Yearly costs comparison
st.markdown("""<div style='margin-top: 2rem;'></div>""", unsafe_allow_html=True)
st.markdown('<div class="section-title">Jaarlijkse Kosten Vergelijking</div>', unsafe_allow_html=True)

# Create yearly costs comparison table
yearly_data = []
for i, (conv, lvov) in enumerate(zip(kosten_conv, kosten_lvov)):
    yearly_data.append({
        'Jaar': i,
        'Conventioneel': conv,
        'LVOv': lvov
    })

# Convert to HTML table
yearly_table_html = '<table class="financial-table bottom-table"><thead><tr>'
yearly_table_html += '<th>Jaar</th><th>Conventioneel (€)</th><th>LVOv (€)</th>'
yearly_table_html += '</tr></thead><tbody>'

for row in yearly_data:
    yearly_table_html += f'<tr>'
    yearly_table_html += f'<td>{row["Jaar"]}</td>'
    # Color conventional costs
    conv_color = '#dc3545' if row["Conventioneel"] > 0 else '#000000'
    yearly_table_html += f'<td style="color: {conv_color}">€{row["Conventioneel"]:,.0f}</td>'
    # Color LVOv costs
    lvov_color = '#dc3545' if row["LVOv"] > 0 else '#000000'
    yearly_table_html += f'<td style="color: {lvov_color}">€{row["LVOv"]:,.0f}</td>'
    yearly_table_html += '</tr>'

yearly_table_html += '</tbody></table>'
st.markdown(yearly_table_html, unsafe_allow_html=True)
