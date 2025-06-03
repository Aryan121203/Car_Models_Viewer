import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("CARS.csv")
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype('int64')

st.set_page_config(page_title="Car Price Visualizer", layout="wide")
st.title("🚗 Car Price Visualization App by Aryan")

st.markdown("Use the filters in the sidebar to explore car pricing trends based on Type, Make, and MSRP.")

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
car_types = st.sidebar.multiselect("Select Car Types", sorted(df["Type"].unique()), default=list(df["Type"].unique()))
filtered_df = df[df["Type"].isin(car_types)]

car_makes = st.sidebar.multiselect("Select Car Makes", sorted(filtered_df["Make"].unique()), default=list(filtered_df["Make"].unique()))
filtered_df = filtered_df[filtered_df["Make"].isin(car_makes)]

min_price, max_price = int(filtered_df["MSRP"].min()), int(filtered_df["MSRP"].max())
price_range = st.sidebar.slider("Select MSRP Range", min_price, max_price, (min_price, max_price))
filtered_df = filtered_df[(filtered_df["MSRP"] >= price_range[0]) & (filtered_df["MSRP"] <= price_range[1])]

# Main area
if filtered_df.empty:
    st.warning("No data available for the selected filters. Try changing the filters.")
else:
    st.subheader("📊 MSRP of Car Models")
    fig = px.bar(filtered_df, x="Model", y="MSRP", color="Make", hover_data=["Type", "Origin"],
                 title="Model-wise MSRP Comparison", height=600)
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📄 View Filtered Data"):
        st.dataframe(filtered_df)

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Filtered Data as CSV", data=csv, file_name="filtered_cars.csv", mime="text/csv")
