import streamlit as st
import pandas as pd


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


# Show data
st.divider()

st.subheader("Data Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)
