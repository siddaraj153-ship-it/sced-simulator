import streamlit as st
import pandas as pd
from solver import solve_ed

st.set_page_config(page_title="SCED Simulator", layout="wide")

st.title("Economic Dispatch Simulator")

load = st.sidebar.number_input("Load Demand (MW)", min_value=1, value=500)
num_gens = st.sidebar.number_input("Number of Generators", min_value=1, value=3)

generator_data = []

st.header("Generator Configuration")

for i in range(num_gens):
    st.subheader(f"Generator {i+1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name = st.text_input("Generator Name", value=f"G{i+1}", key=f"name{i}")

    with col2:
        pmin = st.number_input("Min MW", value=50, key=f"min{i}")

    with col3:
        pmax = st.number_input("Max MW", value=300, key=f"max{i}")

    with col4:
        cost = st.number_input("Cost ($/MWh)", value=100.0, key=f"cost{i}")

    generator_data.append({
        "name": name,
        "pmin": pmin,
        "pmax": pmax,
        "cost": cost
    })

if st.button("Run ED"):
    dispatch, total_cost = solve_ed(load, generator_data)

    results = pd.DataFrame({
        "Generator": [g["name"] for g in generator_data],
        "Dispatch (MW)": dispatch,
        "Cost": [g["cost"] for g in generator_data]
    })

    st.dataframe(results)
    st.success(f"Total Cost = ${total_cost:.2f}")

    st.bar_chart(results.set_index("Generator")["Dispatch (MW)"])
