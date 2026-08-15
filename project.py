import streamlit as st
import pandas as pd
import plotly.express as px


# Page setup
st.set_page_config(
    page_title="LifeLens",
    page_icon="🌎",
    layout="wide"
)


# Data URLs
LIFE_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit-lifelens/"
    "main/life-expectancy.csv"
)

GDP_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit-lifelens/"
    "main/life-expectancy-vs-gdp-per-capita.csv"
)

HEALTH_URL = (
    "https://raw.githubusercontent.com/"
    "veronikayushchak-coder/dsc205-streamlit-lifelens/"
    "main/life-expectancy-vs-health-expenditure.csv"
)


# Load data
@st.cache_data
def load_data():

    life = pd.read_csv(LIFE_URL)
    gdp = pd.read_csv(GDP_URL)
    health = pd.read_csv(HEALTH_URL)

    return life, gdp, health


df, gdp_df, health_df = load_data()


# Clean data
df = df.rename(
    columns={
        "Entity": "Country",
        "Life expectancy": "Life Expectancy"
    }
)

gdp_df = gdp_df.rename(
    columns={
        "Entity": "Country"
    }
)

health_df = health_df.rename(
    columns={
        "Entity": "Country",
        "Health expenditure per capita":
            "Health Expenditure"
    }
)


countries = sorted(
    df["Country"].dropna().unique()
)

years = sorted(
    df["Year"].dropna().unique()
)


# Sidebar
st.sidebar.title("🌎 LifeLens")

st.sidebar.write(
    "Understanding how the world lives."
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🗺️ Explore the World",
        "🔎 Country Explorer",
        "⚖️ Compare Countries",
        "🔬 Relationships"
    ]
)


# Home page
if page == "🏠 Home":

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
            "Life Expectancy":
                "Life Expectancy (years)"
        }
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


# Explore the World
elif page == "🗺️ Explore the World":

    st.title("🗺️ Explore the World")

    st.write(
        "See how life expectancy differs around the world."
    )


    # Select year
    selected_year = st.select_slider(
        "Select Year",
        options=years,
        value=years[-1]
    )


    # Get data for selected year
    map_data = df[
        df["Year"] == selected_year
    ].dropna(
        subset=[
            "Country",
            "Life Expectancy",
            "Code"
        ]
    )


    # Create map
    fig_map = px.choropleth(
        map_data,
        locations="Code",
        color="Life Expectancy",
        hover_name="Country",
        color_continuous_scale="YlGnBu",
        projection="natural earth",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=f"Life Expectancy — {selected_year}"
    )


    fig_map.update_layout(
        margin=dict(
            l=0,
            r=0,
            t=60,
            b=0
        )
    )


    st.plotly_chart(
        fig_map,
        use_container_width=True
    )


    # Calculate statistics
    highest = map_data.loc[
        map_data["Life Expectancy"].idxmax()
    ]

    lowest = map_data.loc[
        map_data["Life Expectancy"].idxmin()
    ]

    average = map_data[
        "Life Expectancy"
    ].mean()


    # Show statistics
    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Global Average",
            f"{average:.1f} years"
        )


    with col2:

        st.metric(
            "Highest",
            f"{highest['Life Expectancy']:.1f} years"
        )

        st.caption(
            highest["Country"]
        )


    with col3:

        st.metric(
            "Lowest",
            f"{lowest['Life Expectancy']:.1f} years"
        )

        st.caption(
            lowest["Country"]
        )


# Country Explorer
elif page == "🔎 Country Explorer":

    st.title("🔎 Country Explorer")

    st.write(
        "Select a country and explore its life expectancy history."
    )


    # Select country
    selected_country = st.selectbox(
        "Select Country",
        countries
    )


    country_data = df[
        df["Country"] == selected_country
    ].dropna(
        subset=["Life Expectancy"]
    ).sort_values("Year")


    if not country_data.empty:

        first = country_data[
            "Life Expectancy"
        ].iloc[0]

        latest = country_data[
            "Life Expectancy"
        ].iloc[-1]

        highest = country_data[
            "Life Expectancy"
        ].max()

        change = latest - first


        # Show statistics
        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "First Available",
                f"{first:.1f} years"
            )


        with col2:

            st.metric(
                "Latest",
                f"{latest:.1f} years"
            )


        with col3:

            st.metric(
                "Total Change",
                f"{change:+.1f} years"
            )


        with col4:

            st.metric(
                "Highest",
                f"{highest:.1f} years"
            )


        # Select time period
        st.divider()

        st.subheader(
            "📈 Life Expectancy Over Time"
        )


        min_year = int(
            country_data["Year"].min()
        )

        max_year = int(
            country_data["Year"].max()
        )


        if min_year < max_year:

            year_range = st.slider(
                "Choose time period",
                min_year,
                max_year,
                (min_year, max_year)
            )

        else:

            year_range = (
                min_year,
                max_year
            )


        filtered_country = country_data[
            (
                country_data["Year"]
                >= year_range[0]
            )
            &
            (
                country_data["Year"]
                <= year_range[1]
            )
        ]


        # Create line chart
        fig_country = px.line(
            filtered_country,
            x="Year",
            y="Life Expectancy",
            markers=True,
            labels={
                "Life Expectancy":
                    "Life Expectancy (years)"
            },
            title=(
                f"Life Expectancy — "
                f"{selected_country}"
            )
        )


        st.plotly_chart(
            fig_country,
            use_container_width=True
        )


        # Find highest and lowest years
        highest_row = country_data.loc[
            country_data["Life Expectancy"].idxmax()
        ]

        lowest_row = country_data.loc[
            country_data["Life Expectancy"].idxmin()
        ]


        col1, col2 = st.columns(2)


        with col1:

            st.info(
                f"🏆 Highest: "
                f"{highest_row['Life Expectancy']:.1f} "
                f"years in "
                f"{int(highest_row['Year'])}."
            )


        with col2:

            st.info(
                f"📉 Lowest: "
                f"{lowest_row['Life Expectancy']:.1f} "
                f"years in "
                f"{int(lowest_row['Year'])}."
            )


# Compare Countries
elif page == "⚖️ Compare Countries":

    st.title("⚖️ Compare Countries")

    st.write(
        "Compare life expectancy between three countries."
    )


    # Select year
    selected_year = st.selectbox(
        "Select Year",
        years,
        index=len(years) - 1
    )


    # Get data for selected year
    comparison_data = df[
        df["Year"] == selected_year
    ].dropna(
        subset=[
            "Country",
            "Life Expectancy"
        ]
    )


    available_countries = sorted(
        comparison_data["Country"].unique()
    )


    # Select countries
    col1, col2, col3 = st.columns(3)


    with col1:

        country1 = st.selectbox(
            "Country 1",
            available_countries,
            index=0,
            key="country1"
        )


    with col2:

        country2_options = [
            country
            for country in available_countries
            if country != country1
        ]

        country2 = st.selectbox(
            "Country 2",
            country2_options,
            index=0,
            key="country2"
        )


    with col3:

        country3_options = [
            country
            for country in available_countries
            if country not in [
                country1,
                country2
            ]
        ]

        country3 = st.selectbox(
            "Country 3",
            country3_options,
            index=0,
            key="country3"
        )


    selected_countries = [
        country1,
        country2,
        country3
    ]


    selected_data = comparison_data[
        comparison_data["Country"].isin(
            selected_countries
        )
    ]


    # Create comparison chart
    fig_compare = px.bar(
        selected_data,
        x="Country",
        y="Life Expectancy",
        text="Life Expectancy",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=(
            f"Life Expectancy Comparison — "
            f"{selected_year}"
        )
    )


    fig_compare.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )


    st.plotly_chart(
        fig_compare,
        use_container_width=True
    )


# Relationships
elif page == "🔬 Relationships":

    st.title("🔬 Relationships")

    st.write(
        "Explore relationships between life expectancy, "
        "GDP, and health spending."
    )
