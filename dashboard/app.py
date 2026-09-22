
import os
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data"
OUT = BASE / "outputs" / "datasets"

PRIMARY = "#2E3A2F"
SECONDARY = "#6B7F5B"
TERTIARY = "#D9C9B2"
ACCENT = "#C96F4F"
BACKGROUND = "#F8F6EE"
TEXT = "#20231F"
MUTED = "#6F716C"
WHITE = "#FFFFFF"
GRID = "#E6E1D7"

st.set_page_config(
    page_title="BrewInsights | Indian Coffee Market",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@500;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}
    .stApp {{
        background:
            radial-gradient(circle at 92% 5%, rgba(217,201,178,.30), transparent 23%),
            linear-gradient(180deg, #FBFAF6 0%, {BACKGROUND} 100%);
        color: {TEXT};
    }}
    [data-testid="stSidebar"] {{
        background: #F1EFE8;
        border-right: 1px solid #E4E0D6;
    }}
    .brand {{
        padding: 8px 8px 20px;
        border-bottom: 1px solid #DDD9CE;
        margin-bottom: 18px;
    }}
    .brand-row {{ display:flex; align-items:center; gap:12px; }}
    .brand-mark {{
        width:38px; height:38px; border-radius:50%;
        background:{PRIMARY}; color:white; display:flex;
        align-items:center; justify-content:center; font-size:20px;
    }}
    .brand-title {{
        font-size:18px; font-weight:700; letter-spacing:2px; color:{PRIMARY};
    }}
    .brand-sub {{
        font-size:10px; letter-spacing:1.2px; color:{MUTED}; margin-top:3px;
    }}
    .eyebrow {{
        font-size:11px; letter-spacing:2.5px; color:{MUTED};
        text-transform:uppercase; margin-bottom:8px;
    }}
    .hero-title {{
        font-size:48px; line-height:.98; font-weight:700;
        letter-spacing:-2.2px; color:{PRIMARY}; margin:0;
    }}
    .hero-title span {{ color:#999B96; }}
    .hero-sub {{ font-size:16px; color:#5E615C; margin-top:12px; }}
    .section-title {{ font-size:19px; font-weight:700; color:{TEXT}; margin-bottom:2px; }}
    .section-sub {{ color:{MUTED}; font-size:12px; margin-bottom:12px; }}
    .kpi {{
        background:rgba(255,255,255,.90); border:1px solid #E6E2D8;
        border-radius:20px; padding:16px 17px 14px; min-height:132px;
        box-shadow:0 8px 25px rgba(46,58,47,.05);
    }}
    .kpi-icon {{
        width:38px; height:38px; border-radius:50%;
        display:flex; align-items:center; justify-content:center;
        background:#EEEAE0; font-size:18px; margin-bottom:8px;
    }}
    .kpi-label {{ color:#646761; font-size:12px; }}
    .kpi-value {{ font-size:27px; font-weight:700; margin:3px 0; color:#161915; }}
    .kpi-note {{ color:{MUTED}; font-size:10px; }}
    .panel {{
        background:rgba(255,255,255,.90); border:1px solid #E6E2D8;
        border-radius:20px; padding:17px 19px 13px;
        box-shadow:0 8px 25px rgba(46,58,47,.045); margin-bottom:15px;
    }}
    .insight {{
        background:{PRIMARY}; color:white; border-radius:20px;
        padding:19px; min-height:135px;
    }}
    .insight h3 {{ margin:0 0 7px; font-size:20px; }}
    .insight p {{ margin:0; color:#E8ECE4; line-height:1.55; font-size:12px; }}
    .quote {{
        font-family:'Playfair Display', serif; font-size:22px;
        line-height:1.25; color:#4C514A; padding:17px 5px;
    }}
    .pill {{
        display:inline-block; padding:6px 11px; margin-right:5px;
        border-radius:999px; background:#EEEAE0; color:#555950; font-size:10px;
    }}
    .footer {{ text-align:center; color:#85877F; font-size:10px; padding:18px 0 5px; }}
    div[data-baseweb="select"] > div {{
        border-radius:12px; border-color:#DDD9CE; background:#FAF9F4;
    }}
    .stTabs [data-baseweb="tab-list"] {{ gap:7px; }}
    .stTabs [data-baseweb="tab"] {{ border-radius:12px; padding:7px 14px; }}
    .stTabs [aria-selected="true"] {{ background:{PRIMARY}; color:white; }}
    .small-note {{ color:{MUTED}; font-size:11px; line-height:1.5; }}
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data
def load_data():
    survey = pd.read_csv(DATA / "indian-coffee-all-responses final dataset.csv")
    city_rank = pd.read_csv(OUT / "market_entry_ranking.csv")
    city_scores = pd.read_csv(OUT / "city_opportunity_scores.csv")
    clusters = pd.read_csv(OUT / "consumer_cluster_assignments.csv")
    demand = pd.read_csv(DATA / "coffee_demand_by_period.csv")
    forecast = pd.read_csv(DATA / "coffee_demand_forecast.csv")
    partnership = pd.read_csv(OUT / "partnership_experiment_template.csv")
    return survey, city_rank, city_scores, clusters, demand, forecast, partnership

survey, city_rank, city_scores, clusters, demand, forecast, partnership = load_data()

# The cluster assignment file follows the survey row order.
if len(clusters) == len(survey):
    survey["cluster"] = clusters["cluster"].values
else:
    survey["cluster"] = np.nan

frequency_map = {
    "Rarely": 1, "1-2 times a week": 2, "1-2/week": 2,
    "3-4 times a week": 3, "3-4/week": 3, "Daily": 4,
    "Multiple times a day": 5,
}
willingness_map = {
    "Very Unlikely": 1, "Unlikely": 2, "Neutral": 3,
    "Somewhat Willing": 3, "Only With A Recommendation": 3,
    "Likely": 4, "Very Willing": 5, "Very Likely": 5,
}
purchase_map = {
    "Definitely Would Not Buy": 1, "Probably Would Not Buy": 2,
    "Not Sure": 3, "Probably Would Buy": 4, "Definitely Would Buy": 5,
}
survey["frequency_score"] = survey["coffeeFrequency"].map(frequency_map)
survey["willingness_score"] = survey["willingnessToTry"].map(willingness_map)
survey["purchase_score"] = survey["purchaseIntention"].map(purchase_map)
survey["new_brand_adoption"] = survey["purchaseIntention"].isin(
    ["Probably Would Buy", "Definitely Would Buy"]
)

def money(x):
    return f"₹{x:,.0f}"

def pct(value, total):
    return 0 if total == 0 else value / total * 100

def chart(fig, height=330):
    fig.update_layout(
        height=height,
        margin=dict(l=5, r=5, t=8, b=5),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans", color=TEXT),
        hoverlabel=dict(bgcolor=WHITE, font_size=12),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=GRID)
    fig.update_yaxes(showgrid=True, gridcolor="#EAE7DE", zeroline=False)
    return fig

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-row">
                <div class="brand-mark">☕</div>
                <div>
                    <div class="brand-title">BREWINSIGHTS</div>
                    <div class="brand-sub">INDIAN COFFEE MARKET INTELLIGENCE</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    page = st.radio(
        "Navigate",
        [
            "Overview",
            "Consumer Analytics",
            "Customer Segments",
            "Brand Adoption",
            "Spending Prediction",
            "City Intelligence",
            "Demand Forecast",
            "Partnership Test",
            "Data Explorer",
            "Methodology",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        """
        <div class="quote">
        Better Coffee.<br>
        Brighter Insights.
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="small-note">
        Survey-based intelligence covering consumer behaviour, spending,
        adoption, segmentation and city opportunity.
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div style="display:flex;justify-content:space-between;align-items:center;">
        <div class="eyebrow">PEOPLE &nbsp; • &nbsp; PREFERENCES &nbsp; • &nbsp; POSSIBILITIES</div>
        <div class="pill">INDIA • COFFEE MARKET</div>
    </div>
    """,
    unsafe_allow_html=True,
)

f1, f2, f3, f4 = st.columns(4)
cities = ["All India"] + sorted(survey["city"].dropna().astype(str).unique())
occupations = ["All"] + sorted(survey["occupation"].dropna().astype(str).unique())
coffee_types = ["All"] + sorted(survey["preferredCoffeeType"].dropna().astype(str).unique())
brands = ["All"] + sorted(survey["preferredBrand"].dropna().astype(str).unique())

with f1:
    city_filter = st.selectbox("Market", cities)
with f2:
    occupation_filter = st.selectbox("Occupation", occupations)
with f3:
    type_filter = st.selectbox("Coffee type", coffee_types)
with f4:
    brand_filter = st.selectbox("Brand", brands)

filtered = survey.copy()
if city_filter != "All India":
    filtered = filtered[filtered["city"].astype(str) == city_filter]
if occupation_filter != "All":
    filtered = filtered[filtered["occupation"].astype(str) == occupation_filter]
if type_filter != "All":
    filtered = filtered[filtered["preferredCoffeeType"].astype(str) == type_filter]
if brand_filter != "All":
    filtered = filtered[filtered["preferredBrand"].astype(str) == brand_filter]

# ---------------------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------------------
if page == "Overview":
    st.markdown(
        """
        <div class="hero-title">Coffee Market <span>Intelligence</span></div>
        <div class="hero-sub">A visual view of Indian coffee consumers, spending and market opportunity.</div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    n = len(filtered)
    avg_spend = filtered["monthlyCoffeeSpend"].mean() if n else 0
    avg_income = filtered["monthlyIncome"].mean() if n else 0
    adoption = filtered["new_brand_adoption"].mean() * 100 if n else 0
    city_count = filtered["city"].nunique() if n else 0
    top_market = city_rank.sort_values("rank").iloc[0]["city"] if len(city_rank) else "-"

    cols = st.columns(5)
    cards = [
        ("👥", "Respondents", f"{n:,}", "Current selection"),
        ("🏙", "Cities Covered", f"{city_count}", "In current selection"),
        ("₹", "Avg. Monthly Spend", money(avg_spend), "Per respondent"),
        ("▥", "Avg. Monthly Income", money(avg_income), "Per respondent"),
        ("♥", "New Brand Adoption", f"{adoption:.1f}%", "Purchase-intention proxy"),
    ]
    for col, (icon, label, value, note) in zip(cols, cards):
        with col:
            st.markdown(
                f'<div class="kpi"><div class="kpi-icon">{icon}</div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.55, 1])

    with left:
        st.markdown('<div class="panel"><div class="section-title">Coffee Spending Distribution</div><div class="section-sub">Monthly spend across respondents.</div>', unsafe_allow_html=True)
        spend = filtered["monthlyCoffeeSpend"].dropna()
        if len(spend):
            bins = [-np.inf, 100, 200, 400, 600, 800, 1000, 1500, np.inf]
            labels = ["0–100", "100–200", "200–400", "400–600", "600–800", "800–1000", "1000–1500", "1500+"]
            dist = pd.cut(spend, bins=bins, labels=labels).value_counts(sort=False).reset_index()
            dist.columns = ["Range", "Count"]
            dist["Share"] = dist["Count"] / dist["Count"].sum() * 100
            fig = px.bar(dist, x="Range", y="Share", text=dist["Share"].round(1),
                         color_discrete_sequence=[SECONDARY])
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            st.plotly_chart(chart(fig, 300), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="panel"><div class="section-title">Preferred Coffee Type</div><div class="section-sub">Preference mix in the current selection.</div>', unsafe_allow_html=True)
        pref = filtered["preferredCoffeeType"].fillna("Unknown").value_counts().reset_index()
        pref.columns = ["Coffee Type", "Count"]
        fig = px.pie(pref, names="Coffee Type", values="Count", hole=.58,
                     color_discrete_sequence=[PRIMARY, SECONDARY, TERTIARY, ACCENT, "#E9E4D9", "#C7C8C4"])
        fig.update_traces(textposition="inside", textinfo="percent")
        st.plotly_chart(chart(fig, 300), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    a, b, c = st.columns(3)
    with a:
        st.markdown('<div class="panel"><div class="section-title">Top Coffee Brands</div><div class="section-sub">Most selected brands.</div>', unsafe_allow_html=True)
        brand = filtered["preferredBrand"].fillna("Unknown").value_counts().head(6).reset_index()
        brand.columns = ["Brand", "Count"]
        brand["Share"] = brand["Count"] / max(1, len(filtered)) * 100
        fig = px.bar(brand.sort_values("Count"), x="Share", y="Brand", orientation="h",
                     text=brand.sort_values("Count")["Share"].round(1), color_discrete_sequence=[PRIMARY])
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(chart(fig, 280), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with b:
        st.markdown('<div class="panel"><div class="section-title">Consumption Frequency</div><div class="section-sub">How often respondents drink coffee.</div>', unsafe_allow_html=True)
        freq = filtered["coffeeFrequency"].fillna("Unknown").value_counts().reset_index()
        freq.columns = ["Frequency", "Count"]
        freq["Share"] = freq["Count"] / max(1, len(filtered)) * 100
        fig = px.bar(freq, x="Frequency", y="Share", text=freq["Share"].round(1),
                     color_discrete_sequence=[SECONDARY])
        fig.update_traces(texttemplate="%{text}%", textposition="outside")
        st.plotly_chart(chart(fig, 280), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    with c:
        st.markdown('<div class="panel"><div class="section-title">Cities by Average Spend</div><div class="section-sub">Highest observed monthly spend.</div>', unsafe_allow_html=True)
        city_view = filtered.groupby("city", as_index=False)["monthlyCoffeeSpend"].mean().sort_values("monthlyCoffeeSpend", ascending=False).head(6)
        fig = px.bar(city_view.sort_values("monthlyCoffeeSpend"), x="monthlyCoffeeSpend", y="city", orientation="h",
                     text=city_view.sort_values("monthlyCoffeeSpend")["monthlyCoffeeSpend"].round(0),
                     color_discrete_sequence=[TERTIARY])
        fig.update_traces(texttemplate="₹%{text}", textposition="outside")
        st.plotly_chart(chart(fig, 280), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="insight">
            <h3>Dashboard Note</h3>
            <p>
            Adoption is a survey-derived purchase-intention proxy. City opportunity is based on
            the project scoring model and should be read as an analytical signal rather than
            guaranteed market size or future sales.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------
# CONSUMER ANALYTICS
# ---------------------------------------------------------------------
elif page == "Consumer Analytics":
    st.markdown('<div class="hero-title">Consumer <span>Analytics</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Explore demographics, preferences and spending behaviour.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Demographics", "Preferences", "Spending"])
    with tabs[0]:
        x, y = st.columns(2)
        with x:
            age = filtered["age"].dropna()
            fig = px.histogram(filtered, x="age", nbins=20, color_discrete_sequence=[SECONDARY])
            st.markdown('<div class="panel"><div class="section-title">Age Distribution</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 330), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with y:
            occ = filtered["occupation"].value_counts().head(10).reset_index()
            occ.columns = ["Occupation", "Count"]
            fig = px.bar(occ.sort_values("Count"), x="Count", y="Occupation", orientation="h",
                         color_discrete_sequence=[TERTIARY])
            st.markdown('<div class="panel"><div class="section-title">Top Occupations</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 330), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        x, y = st.columns(2)
        with x:
            typ = filtered["preferredCoffeeType"].value_counts().reset_index()
            typ.columns = ["Type", "Count"]
            fig = px.bar(typ.sort_values("Count"), x="Count", y="Type", orientation="h",
                         color_discrete_sequence=[PRIMARY])
            st.markdown('<div class="panel"><div class="section-title">Coffee Type Preference</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 330), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with y:
            loc = filtered["purchaseLocation"].value_counts().reset_index()
            loc.columns = ["Location", "Count"]
            fig = px.pie(loc, names="Location", values="Count", hole=.5,
                         color_discrete_sequence=[PRIMARY, SECONDARY, TERTIARY, ACCENT])
            st.markdown('<div class="panel"><div class="section-title">Purchase Location</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 330), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

    with tabs[2]:
        x, y = st.columns(2)
        with x:
            fig = px.scatter(filtered, x="monthlyIncome", y="monthlyCoffeeSpend", opacity=.55,
                             color_discrete_sequence=[ACCENT])
            st.markdown('<div class="panel"><div class="section-title">Income vs Coffee Spend</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 340), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with y:
            fig = px.box(filtered, x="preferredCoffeeType", y="monthlyCoffeeSpend",
                         color_discrete_sequence=[SECONDARY])
            st.markdown('<div class="panel"><div class="section-title">Spend by Coffee Type</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 340), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# CUSTOMER SEGMENTS
# ---------------------------------------------------------------------
elif page == "Customer Segments":
    st.markdown('<div class="hero-title">Customer <span>Segments</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Existing K-Means assignments and profiles from the project.</div>', unsafe_allow_html=True)

    seg = filtered.dropna(subset=["cluster"]).copy()
    if len(seg):
        profile = seg.groupby("cluster").agg(
            Respondents=("cluster", "size"),
            Avg_Age=("age", "mean"),
            Avg_Income=("monthlyIncome", "mean"),
            Avg_Spend=("monthlyCoffeeSpend", "mean"),
            Avg_Price_Range=("preferredPriceRange", "mean"),
        ).reset_index()
        profile["Share"] = profile["Respondents"] / len(seg) * 100

        k1, k2, k3 = st.columns(3)
        with k1:
            st.markdown(f'<div class="kpi"><div class="kpi-icon">◉</div><div class="kpi-label">Segments</div><div class="kpi-value">{len(profile)}</div><div class="kpi-note">Existing cluster labels</div></div>', unsafe_allow_html=True)
        with k2:
            st.markdown(f'<div class="kpi"><div class="kpi-icon">₹</div><div class="kpi-label">Highest Avg. Spend</div><div class="kpi-value">{money(profile["Avg_Spend"].max())}</div><div class="kpi-note">Across displayed clusters</div></div>', unsafe_allow_html=True)
        with k3:
            st.markdown(f'<div class="kpi"><div class="kpi-icon">👥</div><div class="kpi-label">Profiled Respondents</div><div class="kpi-value">{len(seg):,}</div><div class="kpi-note">Current filter</div></div>', unsafe_allow_html=True)

        left, right = st.columns([1.35, 1])
        with left:
            fig = px.bar(profile.sort_values("Avg_Spend"), x="Avg_Spend", y=profile.sort_values("Avg_Spend")["cluster"].astype(str),
                         orientation="h", text=profile.sort_values("Avg_Spend")["Avg_Spend"].round(0),
                         color_discrete_sequence=[SECONDARY])
            fig.update_traces(texttemplate="₹%{text}", textposition="outside")
            fig.update_yaxes(title="Cluster")
            st.markdown('<div class="panel"><div class="section-title">Average Spend by Segment</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 390), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            fig = px.scatter(seg, x="monthlyIncome", y="monthlyCoffeeSpend", color=seg["cluster"].astype(str),
                             color_discrete_sequence=[PRIMARY, SECONDARY, ACCENT, TERTIARY, "#9A9C97"])
            fig.update_layout(legend_title_text="Cluster")
            st.markdown('<div class="panel"><div class="section-title">Income vs Spend</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 390), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        display = profile.rename(columns={
            "cluster": "Cluster", "Respondents": "Respondents", "Avg_Age": "Avg Age",
            "Avg_Income": "Avg Income", "Avg_Spend": "Avg Spend", "Avg_Price_Range": "Avg Price Range"
        }).copy()
        for col in ["Avg Income", "Avg Spend", "Avg Price Range"]:
            display[col] = display[col].round(0)
        display["Share"] = display["Share"].round(1).astype(str) + "%"
        st.markdown('<div class="panel"><div class="section-title">Segment Profile</div>', unsafe_allow_html=True)
        st.dataframe(display, width="stretch", hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No cluster assignments are available for the current filters.")

# ---------------------------------------------------------------------
# BRAND ADOPTION
# ---------------------------------------------------------------------
elif page == "Brand Adoption":
    st.markdown('<div class="hero-title">Brand <span>Adoption</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Survey-derived purchase-intention signal for a new coffee brand.</div>', unsafe_allow_html=True)

    adoption_rate = filtered["new_brand_adoption"].mean() * 100 if len(filtered) else 0
    likely = filtered["willingnessToTry"].isin(["Likely", "Very Likely", "Very Willing"]).sum()
    a, b, c = st.columns(3)
    for col, title, value, note in [
        (a, "Adoption Proxy", f"{adoption_rate:.1f}%", "Probably/Definitely would buy"),
        (b, "Willingness Signal", f"{pct(likely, len(filtered)):.1f}%", "Likely / very willing"),
        (c, "Responses", f"{len(filtered):,}", "Current selection"),
    ]:
        with col:
            st.markdown(f'<div class="kpi"><div class="kpi-icon">♥</div><div class="kpi-label">{title}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)

    left, right = st.columns(2)
    with left:
        pi = filtered["purchaseIntention"].value_counts().reset_index()
        pi.columns = ["Purchase Intention", "Count"]
        fig = px.bar(pi.sort_values("Count"), x="Count", y="Purchase Intention", orientation="h",
                     color_discrete_sequence=[PRIMARY])
        st.markdown('<div class="panel"><div class="section-title">Purchase Intention</div>', unsafe_allow_html=True)
        st.plotly_chart(chart(fig, 390), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    with right:
        wt = filtered["willingnessToTry"].value_counts().reset_index()
        wt.columns = ["Willingness", "Count"]
        fig = px.pie(wt, names="Willingness", values="Count", hole=.5,
                     color_discrete_sequence=[PRIMARY, SECONDARY, TERTIARY, ACCENT, "#E9E4D9"])
        st.markdown('<div class="panel"><div class="section-title">Willingness to Try</div>', unsafe_allow_html=True)
        st.plotly_chart(chart(fig, 390), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)

    st.info("Interpretation: this is a survey-based proxy created from purchase intention; it is not observed future purchasing behaviour.")

# ---------------------------------------------------------------------
# SPENDING PREDICTION
# ---------------------------------------------------------------------
elif page == "Spending Prediction":
    st.markdown('<div class="hero-title">Spending <span>Prediction</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Interactive holdout view of monthly coffee spending prediction.</div>', unsafe_allow_html=True)

    from sklearn.model_selection import train_test_split
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import OneHotEncoder, StandardScaler
    from sklearn.linear_model import Ridge
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    model_features = [c for c in [
        "age", "monthlyIncome", "preferredPriceRange", "coffeeFrequency",
        "preferredCoffeeType", "preferredBrand", "purchaseLocation", "purchaseMode",
        "priceSensitivity", "brandLoyalty", "willingnessToTry", "purchaseIntention",
        "frequency_score", "willingness_score", "purchase_score"
    ] if c in filtered.columns]

    model_df = filtered[model_features + ["monthlyCoffeeSpend"]].dropna().copy()
    if len(model_df) >= 100:
        X = model_df[model_features]
        y = model_df["monthlyCoffeeSpend"]
        numeric = X.select_dtypes(include=np.number).columns.tolist()
        categorical = [c for c in X.columns if c not in numeric]
        prep = ColumnTransformer([
            ("num", StandardScaler(), numeric),
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
        ])
        model = Pipeline([("prep", prep), ("model", Ridge(alpha=10))])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)
        model.fit(X_train, y_train)
        pred = model.predict(X_test)
        r2 = r2_score(y_test, pred)
        mae = mean_absolute_error(y_test, pred)
        rmse = mean_squared_error(y_test, pred) ** .5

        a, b, c = st.columns(3)
        for col, title, value, note in [
            (a, "R²", f"{r2:.3f}", "Holdout performance"),
            (b, "MAE", money(mae), "Average absolute error"),
            (c, "RMSE", money(rmse), "Root mean squared error"),
        ]:
            with col:
                st.markdown(f'<div class="kpi"><div class="kpi-icon">▥</div><div class="kpi-label">{title}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=y_test, y=pred, mode="markers",
                                 marker=dict(size=7, color=ACCENT, opacity=.55),
                                 name="Predictions"))
        lo = min(y_test.min(), pred.min())
        hi = max(y_test.max(), pred.max())
        fig.add_trace(go.Scatter(x=[lo, hi], y=[lo, hi], mode="lines",
                                 line=dict(color=PRIMARY, dash="dash"), name="Ideal"))
        fig.update_layout(xaxis_title="Actual monthly spend", yaxis_title="Predicted monthly spend")
        st.markdown('<div class="panel"><div class="section-title">Actual vs Predicted Spend</div><div class="section-sub">Dashboard demonstration model using Ridge regression.</div>', unsafe_allow_html=True)
        st.plotly_chart(chart(fig, 450), width="stretch")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Not enough complete observations after filtering to train the model.")

# ---------------------------------------------------------------------
# CITY INTELLIGENCE
# ---------------------------------------------------------------------
elif page == "City Intelligence":
    st.markdown('<div class="hero-title">City <span>Intelligence</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Compare city-level spending, adoption and the project market-entry score.</div>', unsafe_allow_html=True)

    city = filtered.groupby("city").agg(
        Responses=("city", "size"),
        Avg_Spend=("monthlyCoffeeSpend", "mean"),
        Avg_Income=("monthlyIncome", "mean"),
        Avg_Frequency=("frequency_score", "mean"),
        Adoption=("new_brand_adoption", "mean"),
    ).reset_index()
    city["Adoption"] *= 100

    min_resp = st.slider("Minimum city responses", 20, 250, 50, 10)
    city = city[city["Responses"] >= min_resp].copy()

    if len(city):
        left, right = st.columns(2)
        with left:
            plot_city = city.sort_values("Avg_Spend", ascending=False).head(12).sort_values("Avg_Spend")
            fig = px.bar(plot_city, x="Avg_Spend", y="city", orientation="h",
                         text=plot_city["Avg_Spend"].round(0), color_discrete_sequence=[PRIMARY])
            fig.update_traces(texttemplate="₹%{text}", textposition="outside")
            st.markdown('<div class="panel"><div class="section-title">Top Cities by Average Spend</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 420), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)
        with right:
            plot_city = city.sort_values("Adoption", ascending=False).head(12).sort_values("Adoption")
            fig = px.bar(plot_city, x="Adoption", y="city", orientation="h",
                         text=plot_city["Adoption"].round(1), color_discrete_sequence=[ACCENT])
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            st.markdown('<div class="panel"><div class="section-title">Cities by Adoption Signal</div>', unsafe_allow_html=True)
            st.plotly_chart(chart(fig, 420), width="stretch")
            st.markdown("</div>", unsafe_allow_html=True)

        city_score = city.merge(city_scores[["city", "market_entry_score", "rank", "city_tier"]], on="city", how="left")
        st.markdown('<div class="panel"><div class="section-title">City Comparison</div><div class="section-sub">Survey metrics plus the project existing city opportunity score.</div>', unsafe_allow_html=True)
        display = city_score.sort_values("market_entry_score", ascending=False).copy()
        display["Avg_Spend"] = display["Avg_Spend"].round(0).map(lambda x: f"₹{x:,.0f}")
        display["Avg_Income"] = display["Avg_Income"].round(0).map(lambda x: f"₹{x:,.0f}")
        display["Avg_Frequency"] = display["Avg_Frequency"].round(2)
        display["Adoption"] = display["Adoption"].round(1).map(lambda x: f"{x:.1f}%")
        display["market_entry_score"] = display["market_entry_score"].round(3)
        display = display.rename(columns={
            "city": "City", "Responses": "Responses", "Avg_Spend": "Avg Spend",
            "Avg_Income": "Avg Income", "Avg_Frequency": "Frequency Score",
            "Adoption": "Adoption Signal", "market_entry_score": "Entry Score",
            "rank": "Rank", "city_tier": "Tier"
        })
        st.dataframe(display, width="stretch", hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No cities meet the selected response threshold.")

# ---------------------------------------------------------------------
# DEMAND FORECAST
# ---------------------------------------------------------------------
elif page == "Demand Forecast":
    st.markdown('<div class="hero-title">Demand <span>Trend</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Observed survey-based demand index and the project forecast output.</div>', unsafe_allow_html=True)

    hist = demand.copy()
    fc = forecast.copy()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist["Period"], y=hist["Demand"], mode="lines+markers",
                             line=dict(color=SECONDARY, width=2), name="Observed"))
    fig.add_trace(go.Scatter(x=fc["Future_Period"], y=fc["Forecasted_Demand"], mode="lines+markers",
                             line=dict(color=ACCENT, width=2), name="Forecast"))
    fig.update_layout(xaxis_title="Period", yaxis_title="Demand index", legend=dict(orientation="h"))
    st.markdown('<div class="panel"><div class="section-title">Demand Trend and Forecast</div><div class="section-sub">Project output; not official historical market-sales data.</div>', unsafe_allow_html=True)
    st.plotly_chart(chart(fig, 440), width="stretch")
    st.markdown("</div>", unsafe_allow_html=True)

    a, b = st.columns(2)
    with a:
        st.markdown('<div class="panel"><div class="section-title">Forecast Output</div>', unsafe_allow_html=True)
        st.dataframe(fc.round(4), width="stretch", hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with b:
        st.markdown('<div class="panel"><div class="section-title">Model Comparison File</div>', unsafe_allow_html=True)
        comparison_path = DATA / "coffee_demand_model_comparison.csv"
        if comparison_path.exists():
            comp = pd.read_csv(comparison_path)
            st.dataframe(comp.round(4), width="stretch", hide_index=True)
        else:
            st.write("Model comparison file not found.")
        st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# PARTNERSHIP TEST
# ---------------------------------------------------------------------
elif page == "Partnership Test":
    st.markdown('<div class="hero-title">3 Corações <span>Test</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Partnership experiment setup and outcome comparison.</div>', unsafe_allow_html=True)

    st.info("The project data does not contain treatment/control observations. The template below is therefore a study design, not a measured partnership effect.")

    st.markdown('<div class="panel"><div class="section-title">Experiment Template</div><div class="section-sub">Fill treatment and control outcomes before estimating an effect.</div>', unsafe_allow_html=True)
    st.dataframe(partnership.head(20), width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload completed experiment CSV (optional)", type=["csv"])
    if uploaded is not None:
        exp = pd.read_csv(uploaded)
        if "group" not in exp.columns:
            st.warning("The uploaded file should contain a 'group' column.")
        else:
            counts = exp["group"].value_counts().rename_axis("Group").reset_index(name="Count")
            st.dataframe(counts, width="stretch", hide_index=True)
            outcome_cols = [c for c in ["purchase_intention", "willing_to_try", "price_sensitivity", "coffee_frequency"] if c in exp.columns]
            if outcome_cols:
                st.dataframe(exp.groupby("group")[outcome_cols].mean().round(3), width="stretch")

# ---------------------------------------------------------------------
# DATA EXPLORER
# ---------------------------------------------------------------------
elif page == "Data Explorer":
    st.markdown('<div class="hero-title">Data <span>Explorer</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Inspect and download the cleaned survey data used in the dashboard.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        search_city = st.text_input("Search city", "")
    with c2:
        rows = st.slider("Rows to display", 10, 250, 50, 10)

    explorer = filtered.copy()
    if search_city:
        explorer = explorer[explorer["city"].astype(str).str.contains(search_city, case=False, na=False)]

    st.markdown(f'<div class="panel"><div class="section-title">{len(explorer):,} matching records</div>', unsafe_allow_html=True)
    st.dataframe(explorer.head(rows), width="stretch", hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.download_button(
        "Download filtered CSV",
        explorer.to_csv(index=False).encode("utf-8"),
        file_name="coffee_market_filtered.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------------------
# METHODOLOGY
# ---------------------------------------------------------------------
elif page == "Methodology":
    st.markdown('<div class="hero-title">Project <span>Methodology</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Definitions and interpretation notes for the project outputs.</div>', unsafe_allow_html=True)

    sections = [
        ("Consumer segmentation", "The dashboard displays the existing K-Means cluster assignments created in the project and summarizes age, income, spend and price-range characteristics."),
        ("Brand adoption", "New-brand adoption is shown as a survey-derived proxy based on respondents selecting 'Probably Would Buy' or 'Definitely Would Buy'."),
        ("Spending prediction", "The interactive dashboard view uses a Ridge regression pipeline with scaled numeric variables and one-hot encoded categorical variables. It is a dashboard demonstration, not a replacement for the notebook benchmark."),
        ("City opportunity", "The city table uses the project saved market-entry score and its component signals. The score is an analytical index, not total addressable market size."),
        ("Demand forecasting", "The demand section displays the project survey-based demand series and saved forecast. It should not be read as official historical sales data because the source survey is not a time-indexed sales series."),
        ("Partnership test", "The partnership section provides the experiment template. No treatment effect is estimated without actual treatment/control observations."),
    ]
    for title, body in sections:
        st.markdown(f'<div class="panel"><div class="section-title">{title}</div><div class="small-note">{body}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="footer">BREWINSIGHTS • Indian Coffee Market Intelligence • Earthy Minimal UI</div>', unsafe_allow_html=True)
