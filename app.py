import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# Load and clean data
df = pd.read_csv("CARS.csv")
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype('int64')

# Streamlit Page Setup
st.set_page_config(page_title="Aryan's Car Explorer", layout="wide")
st.markdown("<h1 style='text-align: center; color: #1f77b4;'>🚗 Aryan's Car Explorer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Explore and compare car prices interactively by Type, Make, and Model.</p>", unsafe_allow_html=True)
st.markdown("---")

# Custom CSS for modern styling
st.markdown("""
<style>
[data-testid="stMetric"] {
    background-color: #f0f2f6;
    padding: 10px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.header("🔧 Filter Options")

car_types = st.sidebar.multiselect("🚘 Select Car Types", sorted(df["Type"].unique()), default=list(df["Type"].unique()))
filtered_df = df[df["Type"].isin(car_types)]

car_makes = st.sidebar.multiselect("🏭 Select Car Makes", sorted(filtered_df["Make"].unique()), default=list(filtered_df["Make"].unique()))
filtered_df = filtered_df[filtered_df["Make"].isin(car_makes)]

min_price, max_price = int(filtered_df["MSRP"].min()), int(filtered_df["MSRP"].max())
price_range = st.sidebar.slider("💵 Select MSRP Range", min_price, max_price, (min_price, max_price))
filtered_df = filtered_df[(filtered_df["MSRP"] >= price_range[0]) & (filtered_df["MSRP"] <= price_range[1])]

search_model = st.sidebar.text_input("🔎 Search by Model Name")
if search_model:
    filtered_df = filtered_df[filtered_df["Model"].str.contains(search_model, case=False, na=False)]

# Show Toast if data is present
if not filtered_df.empty:
    st.toast("✅ Data filtered successfully!", icon="✅")
else:
    st.warning("No data matches your filters. Please try again.")
    st.stop()

# Summary Metrics
st.markdown("### 📊 Live Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Total Makes", filtered_df["Make"].nunique())
col2.metric("Total Models", filtered_df["Model"].nunique())
col3.metric("Average MSRP", f"${int(filtered_df['MSRP'].mean()):,}")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 MSRP Chart", "🌍 Origin & Boxplot", "📦 Treemap", "📄 Data Table"])

# Tab 1: MSRP Bar Chart
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

# Tab 2: Origin Pie Chart and Boxplot
with tab2:
    st.subheader("🌍 Origin Distribution")
    if "Origin" in filtered_df.columns:
        pie_fig = px.pie(filtered_df, names="Origin", title="Car Origin Breakdown", hole=0.4)
        st.plotly_chart(pie_fig, use_container_width=True)

    st.subheader("📦 MSRP Box Plot by Type")
    if "Type" in filtered_df.columns:
        box_fig = px.box(filtered_df, x="Type", y="MSRP", color="Type", points="all", title="MSRP Distribution by Type")
        st.plotly_chart(box_fig, use_container_width=True)

# Tab 3: Treemap
with tab3:
    st.subheader("📦 MSRP Treemap (Make → Model)")
    tree_fig = px.treemap(filtered_df, path=['Make', 'Model'], values='MSRP', title='Treemap of MSRP by Make and Model')
    st.plotly_chart(tree_fig, use_container_width=True)

# Tab 4: Data Table + AgGrid
with tab4:
    st.subheader("📄 Interactive Car Data Table")
    gb = GridOptionsBuilder.from_dataframe(filtered_df)
    gb.configure_pagination()
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
    grid_options = gb.build()
    AgGrid(filtered_df, gridOptions=grid_options, theme='alpine', height=400)

    # CSV Download
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Filtered Data as CSV", data=csv, file_name="filtered_cars.csv", mime="text/csv")
