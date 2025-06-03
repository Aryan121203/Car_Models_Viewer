import streamlit as st
import pandas as pd
import plotly.express as px

# Load and clean data
df = pd.read_csv("CARS.csv")
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype('int64')

# Streamlit Page Setup
st.set_page_config(page_title="Aryan's Car Explorer", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🚗 Aryan's Car Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explore and compare car prices interactively by Type, Make, and Model.</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar filters
st.sidebar.header("🔧 Filter Options")

car_types = st.sidebar.multiselect("🚘 Select Car Types", sorted(df["Type"].unique()), default=list(df["Type"].unique()))
filtered_df = df[df["Type"].isin(car_types)]

car_makes = st.sidebar.multiselect("🏭 Select Car Makes", sorted(filtered_df["Make"].unique()), default=list(filtered_df["Make"].unique()))
filtered_df = filtered_df[filtered_df["Make"].isin(car_makes)]

min_price, max_price = int(filtered_df["MSRP"].min()), int(filtered_df["MSRP"].max())
price_range = st.sidebar.slider("💵 Select MSRP Range", min_price, max_price, (min_price, max_price))
filtered_df = filtered_df[(filtered_df["MSRP"] >= price_range[0]) & (filtered_df["MSRP"] <= price_range[1])]

# Metrics Display
if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("🔼 Highest Price", f"${filtered_df['MSRP'].max():,}")
    col2.metric("🔽 Lowest Price", f"${filtered_df['MSRP'].min():,}")
    col3.metric("📊 Average Price", f"${int(filtered_df['MSRP'].mean()):,}")
else:
    st.warning("No data matches your filters. Please adjust the filters in the sidebar.")
    st.stop()

st.markdown("---")

# Hover data: only include columns that exist
possible_hover_cols = ["Type", "Origin", "Engine Fuel Type"]
hover_cols = [col for col in possible_hover_cols if col in filtered_df.columns]

# Plotting
st.subheader("📈 MSRP Distribution by Model")
fig = px.bar(
    filtered_df,
    x="Model",
    y="MSRP",
    color="Make" if "Make" in filtered_df.columns else None,
    hover_data=hover_cols,
    title="MSRP Comparison of Selected Models",
    height=600
)
fig.update_layout(xaxis_tickangle=-45, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)

# Expandable Data Table
with st.expander("🔍 View Filtered Data Table"):
    st.dataframe(filtered_df, use_container_width=True)

# CSV Download Button
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_cars.csv",
    mime="text/csv",
)
