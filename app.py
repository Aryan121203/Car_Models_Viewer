import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("CARS.csv")

# Clean the MSRP column
df["MSRP"] = df["MSRP"].replace("[$,]", "", regex=True).astype('int64')

st.title("Car Price Visualization App")

# Dropdown for car Type
car_types = df["Type"].unique()
selected_type = st.selectbox("Select Car Type", car_types)

# Filter by selected Type
filtered_by_type = df[df["Type"] == selected_type]

# Dropdown for Make
car_makes = filtered_by_type["Make"].unique()
selected_make = st.selectbox("Select Car Make", car_makes)

# Filter by selected Make
filtered_by_make = filtered_by_type[filtered_by_type["Make"] == selected_make]

# Show MSRP bar plot
st.subheader(f"MSRP of Models for {selected_make} - {selected_type}")
plt.figure(figsize=(12, 6))
sb.barplot(x="Model", y="MSRP", data=filtered_by_make, palette="winter")
plt.xticks(rotation=90)
st.pyplot(plt.gcf())  # Display the matplotlib figure
