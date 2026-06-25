import streamlit as st
import pandas as pd
from solver import solve_dc_sced

st.set_page_config(page_title="SCED Simulator", layout="wide")

st.title("SCED / Economic Dispatch Simulator")

st.sidebar.header("System Settings")
load = st.sidebar.number_input("Total Load Demand (MW)", min_value=1, value=500)
num_gens = st.sidebar.number_input("Number of Generators", min_value=1, value=3)

st.header("Generator Configuration")

generator_data = []

for i in range(num_gens):
    st.subheader(f"Generator {i+1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name = st.text_input(f"Generator Name", value=f"G{i+1}", key=f"name{i}")

    with col2:
        pmin = st.number_input(f"{name} Min MW", min_value=0, value=50, key=f"min{i}")

    with col3:
        pmax = st.number_input(f"{name} Max MW", min_value=1, value=300, key=f"max{i}")

    with col4:
        cost = st.number_input(f"{name} Cost ($/MWh)", min_value=0.0, value=100.0, key=f"cost{i}")

    generator_data.append({
        "name": name,
        "pmin": pmin,
        "pmax": pmax,
        "cost": cost
    })

if st.button("Run SCED"):
    dispatch, total_cost = solve_ed(load, generator_data)

    results = pd.DataFrame({
        "Generator": [g["name"] for g in generator_data],
        "Dispatch (MW)": dispatch,
        "Cost ($/MWh)": [g["cost"] for g in generator_data]
    })

    st.header("Results")
    st.dataframe(results)

    st.success(f"Total Cost = ${total_cost:.2f}")

    st.subheader("Dispatch Graph")
    st.bar_chart(results.set_index("Generator")["Dispatch (MW)"])

    st.subheader("Cost Graph")
    st.bar_chart(results.set_index("Generator")["Cost ($/MWh)"])
