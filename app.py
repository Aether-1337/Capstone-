import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import requests


## Page format

st.set_page_config(
    page_title="Global Fertility Dashboard",
    page_icon="🌍",
    layout="wide"
)


## Load and prepare data

@st.cache_data
def load_data():
    fertility_raw = pd.read_csv("Data/API_SP.DYN.TFRT.IN_DS2_en_csv_v2_230.csv", skiprows=4)

    year_cols = [c for c in fertility_raw.columns if c.isdigit()]
    df = fertility_raw[["Country Name"] + year_cols].copy()

    df_long = df.melt(
        id_vars="Country Name",
        var_name="Year",
        value_name="Fertility Rate"
    )
    df_long["Year"] = df_long["Year"].astype(int)
    df_long = df_long.dropna(subset=["Fertility Rate"])

    trend_list = []
    for country, group in df_long.groupby("Country Name"):
        y = group["Fertility Rate"].sort_index()

        if len(y) > 1:
            pct_change = (y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100
        else:
            pct_change = np.nan

        trend_list.append({"Country Name": country, "Pct Change": pct_change})

    trend_df = pd.DataFrame(trend_list)

    url = "https://api.worldbank.org/v2/country?format=json&per_page=400"
    raw = requests.get(url).json()
    countries = pd.DataFrame(raw[1])

    countries["region"] = countries["region"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )
    countries["incomeLevel"] = countries["incomeLevel"].apply(
        lambda x: x["value"] if isinstance(x, dict) else None
    )

    regions = countries[["name", "region", "incomeLevel"]].copy()
    regions.columns = ["Country Name", "Region", "Income Level"]

    merged = trend_df.merge(regions, on="Country Name", how="left")

    return merged, df_long



## Load data 

df, df_long = load_data()



## Helper: recompute pct change for selected year range

def compute_pct_change_for_range(df_long, start, end):
    df_range = df_long[(df_long["Year"] >= start) & (df_long["Year"] <= end)]

    trend_list = []
    for country, group in df_range.groupby("Country Name"):
        y = group["Fertility Rate"].sort_index()

        if len(y) > 1:
            pct_change = (y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100
        else:
            pct_change = np.nan

        trend_list.append({"Country Name": country, "Pct Change": pct_change})

    return pd.DataFrame(trend_list)




## Sidebar filters

years = sorted(df_long["Year"].unique())
min_year, max_year = st.sidebar.select_slider(
    "Year Range",
    options=years,
    value=(min(years), max(years))
)

def compute_pct_change_for_range(df_long, start, end):
    df_range = df_long[(df_long["Year"] >= start) & (df_long["Year"] <= end)]

    trend_list = []
    for country, group in df_range.groupby("Country Name"):
        y = group["Fertility Rate"].sort_index()

        if len(y) > 1:
            pct_change = (y.iloc[-1] - y.iloc[0]) / y.iloc[0] * 100
        else:
            pct_change = np.nan

        trend_list.append({"Country Name": country, "Pct Change": pct_change})

    return pd.DataFrame(trend_list)

trend_df = compute_pct_change_for_range(df_long, min_year, max_year)
df = trend_df.merge(df[["Country Name", "Region", "Income Level"]], on="Country Name", how="left")

st.sidebar.header("Filters")

region_options = ["All"] + sorted(df["Region"].dropna().unique().tolist())
selected_region = st.sidebar.selectbox("Region", region_options)

income_options = ["All"] + sorted(df["Income Level"].dropna().unique().tolist())
selected_income = st.sidebar.selectbox("Income Level", income_options)

filtered = df.copy()
if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]
if selected_income != "All":
    filtered = filtered[filtered["Income Level"] == selected_income]



## Metrics

col1, col2, col3 = st.columns(3)

col1.metric(
    "Countries Included",
    f"{df['Country Name'].nunique()}"
)

col2.metric(
    "Largest % Decline",
    df.nsmallest(1, "Pct Change")["Country Name"].iloc[0],
    f"{df['Pct Change'].min():.2f}%"
)

col3.metric(
    "Largest % Increase",
    df.nlargest(1, "Pct Change")["Country Name"].iloc[0],
    f"{df['Pct Change'].max():.2f}%"
)


## Tabs

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Global Map",
    "📈 Country Trends",
    "📊 Compare Countries",
    "🏆 Rankings",
    "🔮 Forecasting"
])



## TAB 1 — Global Map

with tab1:
    st.title("🌍 Global Fertility Rate Trends")
    

    fig = px.choropleth(
        filtered,
        locations="Country Name",
        locationmode="country names",
        color="Pct Change",
        color_continuous_scale="RdBu_r",
        title="Global Fertility Rate Trends (Percentage Change per Year)",
        hover_name="Country Name",
        hover_data=["Region", "Income Level", "Pct Change"]

    )
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        "Download Filtered Data",
        filtered.to_csv(index=False),
        "filtered_fertility_data.csv",
        "text/csv"
    )


## TAB 2 — Country Trends

with tab2:
    st.title("📈 Fertility Rate Over Time")

    country = st.selectbox("Select a country", sorted(df_long["Country Name"].unique()))

    subset = df_long[df_long["Country Name"] == country]

    fig = px.line(
        subset,
        x="Year",
        y="Fertility Rate",
        title=f"Fertility Rate Over Time — {country}",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)


## TAB 3 — Compare Countries


with tab3:
    st.title("📊 Compare Countries")

    countries = st.multiselect(
        "Select countries to compare",
        sorted(df_long["Country Name"].unique()),
        default=["United Kingdom", "France", "Germany"]
    )

    subset = df_long[df_long["Country Name"].isin(countries)]

    fig = px.line(
        subset,
        x="Year",
        y="Fertility Rate",
        color="Country Name",
        title="Fertility Rate Comparison",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)


## TAB 4 - Rankings 

with tab4:
    st.title("🏆 Rankings")

    st.subheader("Top 10 Largest % Declines")
    top10 = df.nsmallest(10, "Pct Change")
    st.dataframe(top10)

    st.subheader("Top 10 Largest % Increases")
    bottom10 = df.nlargest(10, "Pct Change")
    st.dataframe(bottom10)

## Forecasting function

def forecast_linear(df_long, country, years_ahead=20):
    subset = df_long[df_long["Country Name"] == country].sort_values("Year")

    x = subset["Year"].values
    y = subset["Fertility Rate"].values

    # Fit linear model
    coef = np.polyfit(x, y, 1)
    slope, intercept = coef

    # Predict future years
    last_year = x.max()
    future_years = np.arange(last_year + 1, last_year + years_ahead + 1)
    future_pred = slope * future_years + intercept

    # Build forecast dataframe
    forecast_df = pd.DataFrame({
        "Year": future_years,
        "Fertility Rate": future_pred,
        "Type": "Forecast"
    })

    # Historical data
    hist_df = subset.copy()
    hist_df["Type"] = "Historical"

    return pd.concat([hist_df, forecast_df], ignore_index=True)


## TAB 5 - Forecasting

with tab5:
    st.title("🔮 Fertility Forecasting")

    country = st.selectbox(
        "Select a country to forecast",
        sorted(df_long["Country Name"].unique()),
        key="forecast_country"
    )

    years_ahead = st.slider(
        "Forecast horizon (years)",
        min_value=5,
        max_value=50,
        value=20
    )

    forecast_df = forecast_linear(df_long, country, years_ahead)

    fig = px.line(
        forecast_df,
        x="Year",
        y="Fertility Rate",
        color="Type",
        title=f"{country} — {years_ahead}-Year Fertility Forecast",
        markers=True
    )

    fig.add_hline(y=2.1, line_dash="dot", line_color="red")

    st.plotly_chart(fig, use_container_width=True)

    future_value = forecast_df[forecast_df["Type"] == "Forecast"]["Fertility Rate"].iloc[-1]
    st.metric(
        f"Projected Fertility in {forecast_df['Year'].max()}",
        f"{future_value:.2f}"
    )