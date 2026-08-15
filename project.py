import streamlit as st
import pandas as pd
import plotly.express as px


# Page setup
st.set_page_config(
    page_title="LifeLens",
    page_icon="🌎",
    layout="wide"
)


# Data URL
LIFE_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit-lifelens/"
    "main/life-expectancy.csv"
)


# Load data
@st.cache_data
def load_data():

    life = pd.read_csv(LIFE_URL)

    return life


df = load_data()


# Clean data
df = df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)


countries = sorted(
    df["Country"].dropna().unique()
)

years = sorted(
    df["Year"].dropna().unique()
)


# Calculate statistics
latest_year = int(years[-1])

latest_data = df[
    df["Year"] == latest_year
].dropna(
    subset=["Life Expectancy"]
)

average_latest = latest_data[
    "Life Expectancy"
].mean()


highest_latest = latest_data.loc[
    latest_data["Life Expectancy"].idxmax()
]

lowest_latest = latest_data.loc[
    latest_data["Life Expectancy"].idxmin()
]


# Home page
st.title("🌎 LifeLens")

st.subheader(
    "Understanding how the world lives."
)

st.write(
    "Explore life expectancy around the world."
)


# Show statistics
col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Countries",
        len(countries)
    )


with col2:

    st.metric(
        "Latest Year",
        latest_year
    )


with col3:

    st.metric(
        "Global Average",
        f"{average_latest:.1f} years"
    )


with col4:

    st.metric(
        "Years of Data",
        f"{int(years[-1] - years[0])}+"
    )


# Highest and lowest
st.divider()

st.subheader(
    f"🌍 The World in {latest_year}"
)


col1, col2 = st.columns(2)


with col1:

    st.metric(
        "🏆 Highest Life Expectancy",
        f"{highest_latest['Life Expectancy']:.1f} years",
        highest_latest["Country"]
    )


with col2:

    st.metric(
        "📉 Lowest Life Expectancy",
        f"{lowest_latest['Life Expectancy']:.1f} years",
        lowest_latest["Country"]
    )


# Top 10 countries
st.divider()

st.subheader(
    f"🏆 Top 10 Countries in {latest_year}"
)


top10 = latest_data.sort_values(
    "Life Expectancy",
    ascending=False
).head(10)


fig = px.bar(
    top10.sort_values("Life Expectancy"),
    x="Life Expectancy",
    y="Country",
    orientation="h",
    labels={
        "Life Expectancy": "Life Expectancy (years)"
    }
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# Show data
st.divider()

st.subheader("Data Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)
