import streamlit as st
import pandas as pd
from solver_ed import solve_ed
from solver_sced import solve_dc_sced

st.set_page_config(page_title="SCED Simulator", layout="wide")

st.title("Power System Optimization Simulator")

mode = st.sidebar.selectbox(
    "Select Model",
    ["Economic Dispatch", "DC-SCED"]
)

if mode == "Economic Dispatch":
    st.header("Economic Dispatch")

    load = st.sidebar.number_input("Load Demand (MW)", min_value=1, value=500)
    num_gens = st.sidebar.number_input("Number of Generators", min_value=1, value=3)

    generator_data = []

    for i in range(num_gens):
        st.subheader(f"Generator {i+1}")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            name = st.text_input("Name", value=f"G{i+1}", key=f"name{i}")

        with col2:
            pmin = st.number_input("Min", value=50, key=f"min{i}")

        with col3:
            pmax = st.number_input("Max", value=300, key=f"max{i}")

        with col4:
            cost = st.number_input("Cost", value=100.0, key=f"cost{i}")

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
            "Dispatch": dispatch,
            "Cost": [g["cost"] for g in generator_data]
        })

        st.dataframe(results)
        st.success(f"Total Cost = ${total_cost:.2f}")

        st.bar_chart(results.set_index("Generator")["Dispatch"])

else:
    st.header("DC-SCED")

    if st.button("Run DC-SCED"):
        results = solve_dc_sced()

        st.subheader("Generator Dispatch")
        st.json(results["generation"])

        st.subheader("Bus Angles")
        st.json(results["angles"])

        st.subheader("Line Flows")
        st.json(results["flows"])

        st.success(f'Total Cost = ${results["cost"]:.2f}')
