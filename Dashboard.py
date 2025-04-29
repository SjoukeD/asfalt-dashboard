

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
    simulatieduur = st.slider("Contractsduur (jaren)", 10, 45, 45)

    st.markdown("<h3 style='color: #154273; font-size: 1.2rem; margin-top: 1rem;'>Kostenparameters</h3>", unsafe_allow_html=True)
    vaste_kosten = st.number_input("Begeleidingskosten per onderhoudsactie (€)", min_value=0, value=200000, step=10000)

    with st.expander("Conventionele Aanpak", expanded=True):
        kost_asfalt = st.number_input("Asfalt: Materiaalkosten (€/m²)", value=15.0)
        kost_hinder_asfalt = st.number_input("Asfalt: Verkeershinderkosten (€/m²)", value=7.0)

    with st.expander("LVOv Behandeling", expanded=True):
        kost_lvov = st.number_input("LVOv: Materiaalkosten (€/m²)", value=2.5)
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
            jaarlijkse_kosten[jaar] = vaste_kosten + (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            jaarlijkse_co2[jaar] = oppervlakte * 0.05  # CO2 uitstoot per m2

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
            jaarlijkse_co2[jaar] = oppervlakte * 0.05  # CO2 uitstoot per m2

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
            jaarlijkse_kosten[jaar] = vaste_kosten + (oppervlakte * (kost_lvov + kost_hinder_lvov))
            jaarlijkse_co2[jaar] = oppervlakte * 0.01  # CO2 uitstoot per m2
        elif jaar == duur:
            # Eindkosten in laatste jaar
            jaarlijkse_kosten[jaar-1] = vaste_kosten + (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            jaarlijkse_co2[jaar-1] = oppervlakte * 0.05  # CO2 uitstoot per m2

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
            jaarlijkse_co2[jaar] = oppervlakte * 0.01  # CO2 uitstoot per m2
        elif jaar == duur:
            # Eindkosten in laatste jaar
            jaarlijkse_kosten[jaar-1] = vaste_kosten + (oppervlakte * (kost_asfalt + kost_hinder_asfalt))
            jaarlijkse_co2[jaar-1] = oppervlakte * 0.05  # CO2 uitstoot per m2

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

st.title("Analysetool Asfaltonderhoud ZOAB-wegdek")

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
    # Debug prints
    st.write(f"Simulatieduur: {simulatieduur}")
    st.write(f"Length kosten_conv: {len(kosten_conv)}")
    st.write(f"Length kosten_lvov: {len(kosten_lvov)}")
    
    fig3, ax3 = plt.subplots()
    jaren = np.arange(len(kosten_conv))  # Use length of data instead of simulatieduur
    width = 0.4
    
    # Ensure both arrays have the same length
    min_len = min(len(kosten_conv), len(kosten_lvov))
    kosten_conv_plot = kosten_conv[:min_len]
    kosten_lvov_plot = kosten_lvov[:min_len]
    jaren = np.arange(min_len)
    
    ax3.bar(jaren - width/2, kosten_conv_plot, width, label="Conventioneel")
    ax3.bar(jaren + width/2, kosten_lvov_plot, width, label="LVOv")
    ax3.set_title("Jaarlijkse Kosten")
    ax3.set_xlabel("Jaar")
    ax3.set_ylabel("Kosten (€)")
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    st.pyplot(fig3)
