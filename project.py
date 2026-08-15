import streamlit as st
import pandas as pd


# Page configuration
st.set_page_config(
    page_title="LifeLens",
    page_icon="🌎",
    layout="wide"
)


# Life expectancy dataset
LIFE_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit-lifelens/"
    "main/life-expectancy.csv"
)


# Load the data
@st.cache_data
def load_data():
    life = pd.read_csv(LIFE_URL)
    return life


df = load_data()


# Clean column names
df = df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)


# Get basic information from the data
countries = sorted(
    df["Country"].dropna().unique()
)

years = sorted(
    df["Year"].dropna().unique()
)


# App title
st.title("🌎 LifeLens")

st.subheader(
    "Understanding how the world lives."
)

st.write(
    "Explore life expectancy around the world."
)


# Preview the data
st.dataframe(
    df.head(10)
)
