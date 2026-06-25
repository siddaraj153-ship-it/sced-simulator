import streamlit as st
from solver import solve_ed

st.title("Economic Dispatch Simulator")

st.header("Load Input")
load = st.number_input("Load Demand (MW)", min_value=100, max_value=5000, value=500)

st.header("Generator Inputs")

g1_min = st.number_input("G1 Min", value=50)
g1_max = st.number_input("G1 Max", value=300)
g1_cost = st.number_input("G1 Cost ($/MWh)", value=100)

g2_min = st.number_input("G2 Min", value=50)
g2_max = st.number_input("G2 Max", value=400)
g2_cost = st.number_input("G2 Cost ($/MWh)", value=150)

if st.button("Solve Dispatch"):
    result = solve_ed(
        load,
        g1_min, g1_max, g1_cost,
        g2_min, g2_max, g2_cost
    )

    st.header("Results")
    st.write(f"G1 Dispatch: {result['P1']} MW")
    st.write(f"G2 Dispatch: {result['P2']} MW")
    st.write(f"Total Cost: {result['cost']}")