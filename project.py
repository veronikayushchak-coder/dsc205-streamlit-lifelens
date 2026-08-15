import streamlit as st
import pandas as pd
import plotly.express as px


# Page setup
st.set_page_config(
    page_title="LifeLens | Global Life Expectancy",
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


# Find GDP column
gdp_column = None

for column in gdp_df.columns:

    if (
        "gdp" in column.lower()
        and "capita" in column.lower()
    ):
        gdp_column = column
        break


# Basic information
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

st.sidebar.divider()

st.sidebar.caption(
    "Data source: Our World in Data"
)


# =========================================================
# HOME
# =========================================================

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
        """
        LifeLens explores how life expectancy varies
        around the world, how it has changed over time,
        and how it is associated with economic and
        healthcare factors.
        """
    )

    st.divider()

    st.header("📊 Global Overview")

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

    st.divider()

    st.header(
        f"🌍 The World in {latest_year}"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🏆 Highest Life Expectancy"
        )

        st.metric(
            highest_latest["Country"],
            f"{highest_latest['Life Expectancy']:.1f} years"
        )

    with col2:

        st.subheader(
            "📉 Lowest Life Expectancy"
        )

        st.metric(
            lowest_latest["Country"],
            f"{lowest_latest['Life Expectancy']:.1f} years"
        )

    st.divider()

    st.header("🏆 Top 10 Countries")

    top10 = latest_data.sort_values(
        "Life Expectancy",
        ascending=False
    ).head(10)

    fig = px.bar(
        top10.sort_values(
            "Life Expectancy"
        ),
        x="Life Expectancy",
        y="Country",
        orientation="h",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=(
            f"Countries with the Highest "
            f"Life Expectancy — {latest_year}"
        }
    )

    fig.update_layout(
        xaxis_title="Life Expectancy (years)",
        yaxis_title="Country"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.info(
        "Use the navigation menu to explore countries, "
        "compare indicators, and investigate relationships."
    )


# =========================================================
# EXPLORE THE WORLD
# =========================================================

elif page == "🗺️ Explore the World":

    st.title("🗺️ Explore the World")

    st.write(
        "Explore how life expectancy differs across countries."
    )

    selected_year = st.select_slider(
        "Select Year",
        options=years,
        value=years[-1]
    )

    map_data = df[
        df["Year"] == selected_year
    ].dropna(
        subset=[
            "Country",
            "Life Expectancy",
            "Code"
        ]
    ).copy()

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
        title=(
            f"Life Expectancy Around the World — "
            f"{selected_year}"
        )
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

    highest = map_data.loc[
        map_data["Life Expectancy"].idxmax()
    ]

    lowest = map_data.loc[
        map_data["Life Expectancy"].idxmin()
    ]

    average = map_data[
        "Life Expectancy"
    ].mean()

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

    st.divider()

    st.subheader("🏆 Country Rankings")

    ranking_choice = st.radio(
        "Show",
        [
            "Highest",
            "Lowest"
        ],
        horizontal=True
    )

    if ranking_choice == "Highest":

        ranking = map_data.sort_values(
            "Life Expectancy",
            ascending=False
        ).head(10)

        ranking_title = "Top 10 Countries"

    else:

        ranking = map_data.sort_values(
            "Life Expectancy",
            ascending=True
        ).head(10)

        ranking_title = "Bottom 10 Countries"

    fig_rank = px.bar(
        ranking.sort_values(
            "Life Expectancy"
        ),
        x="Life Expectancy",
        y="Country",
        orientation="h",
        labels={
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=ranking_title
    )

    st.plotly_chart(
        fig_rank,
        use_container_width=True
    )


# =========================================================
# COUNTRY EXPLORER
# =========================================================

elif page == "🔎 Country Explorer":

    st.title("🔎 Country Explorer")

    st.write(
        "Select a country to explore its life expectancy history."
    )

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

        average = country_data[
            "Life Expectancy"
        ].mean()

        change = latest - first

        st.subheader(
            f"📊 {selected_country} Snapshot"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            st.metric(
                "First",
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
                "Average",
                f"{average:.1f} years"
            )

        with col5:

            st.metric(
                "Highest",
                f"{highest:.1f} years"
            )

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

        st.divider()

        st.subheader(
            "📋 Country Data"
        )

        table_data = country_data[
            [
                "Year",
                "Life Expectancy"
            ]
        ].copy()

        table_data["Life Expectancy"] = (
            table_data["Life Expectancy"]
            .round(1)
        )

        st.dataframe(
            table_data,
            use_container_width=True,
            hide_index=True
        )


# =========================================================
# COMPARE COUNTRIES
# =========================================================

elif page == "⚖️ Compare Countries":

    st.title("⚖️ Compare Countries")

    st.write(
        """
        Select an indicator and compare three countries
        for the same year.
        """
    )

    comparison = st.radio(
        "What would you like to compare?",
        [
            "Life Expectancy",
            "Health Spending",
            "GDP per Capita"
        ],
        horizontal=True
    )

    if comparison == "Life Expectancy":

        comparison_df = df.copy()

        value_column = "Life Expectancy"

    elif comparison == "Health Spending":

        comparison_df = health_df.copy()

        value_column = "Health Expenditure"

    else:

        comparison_df = gdp_df.copy()

        value_column = gdp_column

    if value_column is None:

        st.error(
            "The selected variable could not be found."
        )

        st.stop()

    available_years = sorted(
        comparison_df[
            comparison_df[value_column].notna()
        ]["Year"]
        .dropna()
        .unique()
    )

    if len(available_years) == 0:

        st.error(
            "No years are available for this selection."
        )

        st.stop()

    selected_year = st.selectbox(
        "Select Year",
        available_years,
        index=len(available_years) - 1
    )

    year_data = comparison_df[
        comparison_df["Year"] == selected_year
    ].dropna(
        subset=[
            "Country",
            value_column
        ]
    )

    available_countries = sorted(
        year_data["Country"].unique()
    )

    if len(available_countries) < 3:

        st.warning(
            "There are not enough countries with complete "
            "data for this year."
        )

        st.stop()

    st.subheader("🌎 Select Countries")

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

    selected_data = year_data[
        year_data["Country"].isin(
            selected_countries
        )
    ].copy()

    selected_data["Country"] = pd.Categorical(
        selected_data["Country"],
        categories=selected_countries,
        ordered=True
    )

    selected_data = selected_data.sort_values(
        "Country"
    )

    st.subheader("📊 Comparison")

    visualization = st.radio(
        "Choose visualization",
        [
            "Bar Chart",
            "Ranking"
        ],
        horizontal=True
    )

    if visualization == "Bar Chart":

        fig_compare = px.bar(
            selected_data,
            x="Country",
            y=value_column,
            text=value_column,
            category_orders={
                "Country": selected_countries
            },
            labels={
                value_column:
                    comparison
            },
            title=(
                f"{comparison} — {selected_year}"
            )
        )

        fig_compare.update_traces(
            texttemplate="%{text:.1f}",
            textposition="outside"
        )

    else:

        ranking_data = selected_data.sort_values(
            value_column,
            ascending=False
        )

        fig_compare = px.bar(
            ranking_data,
            x=value_column,
            y="Country",
            orientation="h",
            text=value_column,
            labels={
                value_column:
                    comparison
            },
            title=(
                f"{comparison} Ranking — "
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


# =========================================================
# RELATIONSHIPS
# =========================================================

elif page == "🔬 Relationships":

    st.title("🔬 Relationships")

    st.write(
        """
        Investigate whether countries with higher GDP
        or greater health spending tend to have higher
        life expectancy.
        """
    )

    factor = st.radio(
        "Choose a factor",
        [
            "GDP per Capita",
            "Health Spending"
        ],
        horizontal=True
    )

    # GDP
    if factor == "GDP per Capita":

        relationship_years = sorted(
            gdp_df[
                gdp_df[gdp_column].notna()
            ]["Year"]
            .dropna()
            .unique()
        )

        selected_year = st.selectbox(
            "Select Year",
            relationship_years,
            index=len(relationship_years) - 1,
            key="gdp_year"
        )

        factor_data = gdp_df[
            gdp_df["Year"] == selected_year
        ].copy()

        factor_column = gdp_column

        x_label = "GDP per Capita"

    # Health spending
    else:

        health_data = health_df[
            health_df["Health Expenditure"].notna()
        ][
            [
                "Country",
                "Year"
            ]
        ]

        life_data_years = df[
            df["Life Expectancy"].notna()
        ][
            [
                "Country",
                "Year"
            ]
        ]

        valid_health_years = health_data.merge(
            life_data_years,
            on=[
                "Country",
                "Year"
            ],
            how="inner"
        )

        relationship_years = sorted(
            valid_health_years["Year"]
            .dropna()
            .unique()
        )

        selected_year = st.selectbox(
            "Select Year",
            relationship_years,
            index=len(relationship_years) - 1,
            key="health_year"
        )

        factor_data = health_df[
            health_df["Year"] == selected_year
        ].copy()

        factor_column = "Health Expenditure"

        x_label = "Health Spending per Capita"

    # Life expectancy data
    life_data = df[
        df["Year"] == selected_year
    ][
        [
            "Country",
            "Year",
            "Life Expectancy"
        ]
    ]

    # Combine datasets
    relationship_data = factor_data.merge(
        life_data,
        on=[
            "Country",
            "Year"
        ],
        how="inner"
    )

    relationship_data = relationship_data.dropna(
        subset=[
            factor_column,
            "Life Expectancy"
        ]
    )

    st.subheader(
        f"📈 Life Expectancy vs {x_label}"
    )

    fig_relationship = px.scatter(
        relationship_data,
        x=factor_column,
        y="Life Expectancy",
        hover_name="Country",
        labels={
            factor_column:
                x_label,
            "Life Expectancy":
                "Life Expectancy (years)"
        },
        title=(
            f"Life Expectancy vs "
            f"{x_label} — {selected_year}"
        )
    )

    st.plotly_chart(
        fig_relationship,
        use_container_width=True
    )

    # Correlation
    if len(relationship_data) >= 2:

        correlation = relationship_data[
            [
                factor_column,
                "Life Expectancy"
            ]
        ].corr().iloc[0, 1]

        st.subheader("📊 Correlation")

        st.metric(
            "Correlation",
            f"{correlation:.2f}"
        )

        if correlation >= 0.7:

            st.success(
                "Strong positive relationship."
            )

        elif correlation >= 0.3:

            st.info(
                "Moderate positive relationship."
            )

        elif correlation > -0.3:

            st.info(
                "Weak relationship."
            )

        else:

            st.warning(
                "Negative relationship."
            )

        st.caption(
            "A positive correlation means that countries "
            "with higher values of this factor tend to have "
            "higher life expectancy. Correlation shows "
            "association, not causation."
        )


# Footer
st.sidebar.divider()

st.sidebar.caption(
    "LifeLens | DSC 205"
)
