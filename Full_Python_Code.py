import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression
import requests
import plotly.io as pio
pio.renderers.default = "chrome"

df = pd.read_csv(r"D:\API_SP.DYN.TFRT.IN_DS2_en_csv_v2_230\API_SP.DYN.TFRT.IN_DS2_en_csv_v2_230.csv", 
                 skiprows=4) ##Skip the first 4 rows of metadata

df = df.loc[:, ~df.columns.str.contains("Unnamed")] ##Remove unnamed columns

df_long = df.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="FertilityRate"
) ##Convert from wide to long format

df_long["Year"] = df_long["Year"].astype(int)
df_long["FertilityRate"] = pd.to_numeric(df_long["FertilityRate"], errors="coerce") ##Convert to numeric, coerce errors to NaN

df.head()

cols_to_drop = ["Indicator Code", "Unnamed: 0", "Unnamed: 69"]

df_long = df_long.drop(columns=[c for c in cols_to_drop if c in df_long.columns])

df.head()

df_long = df_long.dropna(subset=["FertilityRate"])

df_long.head()
df_long.tail()
df_long.info()
df_long["Year"].unique()[:10]

print(df_long.info())

with open(r"D:\API_SP.DYN.TFRT.IN_DS2_en_csv_v2_230\API_SP.DYN.TFRT.IN_DS2_en_csv_v2_230.csv") as f:
    for _ in range(20):
        print(f.readline().rstrip())
        
        
df.describe(include="all").T

df.info()

df.nunique().sort_values()

for column in df.columns:
    print(f"column: {column}", df[column].unique())
    
df.isna().sum().sort_values(ascending=False)

numeric_cols = df.select_dtypes(include=["int64","float64","int32","float32"]).columns.tolist()
numeric_cols

country = "United Kingdom"   # change this to any country you want

subset = df_long[df_long["Country Name"] == country]

plt.figure(figsize=(10,5))
sns.lineplot(data=subset, x="Year", y="FertilityRate")
plt.title(f"Fertility Rate Over Time — {country}")
plt.ylabel("Births per Woman")
plt.xlabel("Year")
plt.grid(True)
plt.show()
fig = px.line(subset, x="Year", y="FertilityRate", title=f"Fertility Rate Over Time — {country}",
              labels={"FertilityRate": "Births per Woman"})

countries = ["United Kingdom", "France", "Germany"]  # edit freely

subset = df_long[df_long["Country Name"].isin(countries)]

plt.figure(figsize=(12,6))
sns.lineplot(data=subset, x="Year", y="FertilityRate", hue="Country Name")
plt.title("Fertility Rate Comparison")
plt.ylabel("Births per Woman")
plt.xlabel("Year")
plt.grid(True)
plt.show()

year = 2020

top10 = (
    df_long[df_long["Year"] == year]
    .sort_values("FertilityRate", ascending=False)
    .head(10)
)

top10

global_trend = (
    df_long.groupby("Year")["FertilityRate"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(10,5))
sns.lineplot(data=global_trend, x="Year", y="FertilityRate")
plt.title("Global Average Fertility Rate Over Time")
plt.ylabel("Births per Woman")
plt.xlabel("Year")
plt.grid(True)
plt.show()

numeric_cols = df.select_dtypes(include=["number"]).columns

df[numeric_cols].hist(bins=40, figsize=(14,10))
plt.tight_layout()

numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

n_cols = 3
n_rows = int(np.ceil(len(numeric_cols) / n_cols))

fig, axes = plt.subplots(n_rows, n_cols, figsize=(18, 4 * n_rows))
axes = axes.flatten()

for ax, col in zip(axes, numeric_cols):
    # Drop NaNs to avoid seaborn warnings
    data = df[col].dropna()

    # Skip columns with no valid data
    if data.empty:
        ax.set_visible(False)
        continue

    sns.kdeplot(
        data=data,
        fill=True,
        alpha=0.5,
        ax=ax
    )

    ax.set_title(col, fontsize=12)
    ax.set_xlabel("")
    ax.set_ylabel("Density")

# Hide any unused axes
for ax in axes[len(numeric_cols):]:
    ax.set_visible(False)

plt.suptitle("Fertility Rate Distribution by Year")
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.show()

highest_each_year = df.melt(
    id_vars=["Country Name"],
    value_vars=numeric_cols,
    var_name="Year",
    value_name="FertilityRate"
).sort_values(["Year", "FertilityRate"], ascending=[True, False]).groupby("Year").first()

highest_each_year.head()

df_2020 = df[["Country Name", "2020"]].dropna().sort_values("2020", ascending=False).head(10)
df_2020

corr = df[numeric_cols].corr()

plt.figure(figsize=(12,10))
sns.heatmap(corr, cmap="coolwarm", center=0)
plt.title("Correlation Between Years")
plt.show()

[c for c in df.columns if not c.isdigit() and c not in 
 ["Country Name", "Country Code", "Indicator Name", "Indicator Code"]]

for col in df.columns:
    print(repr(col))
    
df_long = df.melt(
    id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
    var_name="Year",
    value_name="FertilityRate"
)

df_long["Year"] = df_long["Year"].astype(int)
df_long["FertilityRate"] = pd.to_numeric(df_long["FertilityRate"], errors="coerce")

df_long = df_long.drop(columns=["Indicator Code"])

df_long.head()
df_long.info()

def slope(series):
    s = series.dropna()
    if len(s) < 2:
        return None
    X = np.arange(len(s)).reshape(-1, 1)
    y = s.values
    model = LinearRegression().fit(X, y)
    return model.coef_[0]


trend = (
    df_long.groupby("Country Name")
           .apply(lambda g: slope(g["FertilityRate"]))
           .dropna()
           .sort_values()
)

top10 = trend.head(10)       # most negative slopes (fastest decline)
bottom10 = trend.tail(10)    # most positive slopes (increasing or slowest decline)

top10 = trend.head(10)
bottom10 = trend.tail(10)

fig, axes = plt.subplots(1, 2, figsize=(18, 7))

# --- Left: Fastest decline ---
axes[0].barh(top10.index, top10.values, color="steelblue")
axes[0].set_title("Top 10 Fastest Declining Fertility Rates")
axes[0].set_xlabel("Slope (change per year)")
axes[0].invert_yaxis()

# Add annotations
for i, v in enumerate(top10.values):
    axes[0].text(v, i, f"{v:.3f}", va="center", ha="left")

# --- Right: Slowest decline / increasing ---
axes[1].barh(bottom10.index, bottom10.values, color="darkorange")
axes[1].set_title("Bottom 10 (Increasing or Slowest Decline)")
axes[1].set_xlabel("Slope (change per year)")
axes[1].invert_yaxis()

for i, v in enumerate(bottom10.values):
    axes[1].text(v, i, f"{v:.3f}", va="center", ha="left")

plt.tight_layout()
plt.show()

url = "http://api.worldbank.org/v2/country?format=json&per_page=400"

response = requests.get(url)
data = response.json()   # this is a list: [metadata, countries]

countries = pd.DataFrame(data[1])  # second element contains the table

countries["region"] = countries["region"].apply(lambda x: x["value"] if isinstance(x, dict) else None)
countries["incomeLevel"] = countries["incomeLevel"].apply(lambda x: x["value"] if isinstance(x, dict) else None)

regions = countries[["name", "region", "incomeLevel"]].copy()
regions.columns = ["Country Name", "Region", "Income Level"]

trend_df = trend.reset_index()
trend_df.columns = ["Country Name", "Slope"]

trend_with_region = trend_df.merge(regions, on="Country Name", how="left")



fig = px.choropleth(
    trend_with_region,
    locations="Country Name",
    locationmode="country names",
    color="Slope",
    color_continuous_scale="RdBu_r",
    title="Global Fertility Rate Trends (Slope per Year)",
    hover_name="Country Name",
    hover_data=["Region", "Income Level", "Slope"]
)

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Slope",
        ticks="outside"
    )
)

fig.show()