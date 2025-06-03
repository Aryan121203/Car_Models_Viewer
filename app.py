import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("CARS.csv")
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype('int64')

# Streamlit Page Setup
st.set_page_config(page_title="Aryan's Car Explorer", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🚗 Aryan's Car Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>An interactive dashboard to explore and compare car prices.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔧 Filter Options")

car_types = st.sidebar.multiselect("🚘 Select Car Types", sorted(df["Type"].unique()), default=list(df["Type"].unique()))
filtered_df = df[df["Type"].isin(car_types)]

car_makes = st.sidebar.multiselect("🏭 Select Car Makes", sorted(filtered_df["Make"].unique()), default=list(filtered_df["Make"].unique()))
filtered_df = filtered_df[filtered_df["Make"].isin(car_makes)]

# Price range slider fix: handle case when min_price == max_price
min_price, max_price = int(filtered_df["MSRP"].min()), int(filtered_df["MSRP"].max())

if min_price < max_price:
    price_range = st.sidebar.slider("💵 Select MSRP Range", min_price, max_price, (min_price, max_price))
    filtered_df = filtered_df[(filtered_df["MSRP"] >= price_range[0]) & (filtered_df["MSRP"] <= price_range[1])]
else:
    st.sidebar.markdown(f"💵 Only one MSRP value available: **${min_price:,}**")

search_model = st.sidebar.text_input("🔎 Search by Model Name")
if search_model:
    filtered_df = filtered_df[filtered_df["Model"].str.contains(search_model, case=False, na=False)]

# Model dropdown filter
available_models = sorted(filtered_df["Model"].unique())
selected_model = st.sidebar.selectbox("🚗 Select Model (optional)", ["All"] + available_models)
if selected_model != "All":
    filtered_df = filtered_df[filtered_df["Model"] == selected_model]

# Display warning and stop if no data after filters
if filtered_df.empty:
    st.warning("No data matches your filters. Please try again.")
    st.stop()

# Show Live Summary
st.markdown("### 📋 Data Summary")
col1, col2, col3 = st.columns(3)
col1.metric("🛠 Total Makes", filtered_df["Make"].nunique())
col2.metric("🚘 Total Models", filtered_df["Model"].nunique())
col3.metric("📊 Avg MSRP", f"${int(filtered_df['MSRP'].mean()):,}")

# Tabs for organization
tab1, tab2, tab3 = st.tabs(["📈 MSRP Chart", "📊 Insights", "📄 Data Table"])

# MSRP Chart Tab
with tab1:
    st.subheader("💰 MSRP by Car Model")
    hover_cols = [col for col in ["Type", "Origin", "Engine Fuel Type"] if col in filtered_df.columns]
    fig = px.bar(
        filtered_df,
        x="Model",
        y="MSRP",
        color="Make",
        hover_data=hover_cols,
        title="MSRP Comparison of Models",
        height=600
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

# Insights Tab
with tab2:
    st.subheader("🌍 Car Origin Distribution")
    if "Origin" in filtered_df.columns:
        origin_fig = px.pie(
            filtered_df,
            names="Origin",
            title="Distribution of Cars by Origin",
            hole=0.4
        )
        st.plotly_chart(origin_fig, use_container_width=True)

    st.subheader("📦 MSRP Box Plot by Car Type")
    if "Type" in filtered_df.columns:
        box_fig = px.box(
            filtered_df,
            x="Type",
            y="MSRP",
            color="Type",
            title="Price Spread by Car Type",
            points="all"
        )
        st.plotly_chart(box_fig, use_container_width=True)

# Data Table Tab
with tab3:
    st.subheader("📄 Filtered Car Data")
    st.dataframe(filtered_df, use_container_width=True)

    # Download CSV
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="filtered_cars.csv",
        mime="text/csv"
    )
