import streamlit as st
import pandas as pd
from solver_ed import solve_ed
from solver_sced import solve_dc_sced
from parser import (
    parse_ed_generators,
    parse_bus_csv,
    parse_generator_csv,
    parse_line_csv
)

st.set_page_config(page_title="Power System Optimization", layout="wide")

st.title("Power System Optimization Simulator")

# Sidebar
model = st.sidebar.selectbox(
    "Select Model",
    ["Economic Dispatch", "DC-SCED"]
)

input_mode = st.sidebar.selectbox(
    "Input Mode",
    ["Manual", "CSV Upload"]
)

currency = st.sidebar.selectbox(
    "Currency",
    ["USD", "INR", "EUR", "GBP", "JPY"]
)

# ---------------------------
# ECONOMIC DISPATCH
# ---------------------------
if model == "Economic Dispatch":
    st.header("Economic Dispatch")

    if input_mode == "Manual":
        load = st.number_input("Load Demand (MW)", value=500)

        num_gens = st.number_input(
            "Number of Generators",
            min_value=1,
            value=3
        )

        generators = []

        for i in range(num_gens):
            st.subheader(f"Generator {i+1}")

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                name = st.text_input("Name", value=f"G{i+1}", key=f"name{i}")

            with col2:
                pmin = st.number_input("Pmin", value=50, key=f"pmin{i}")

            with col3:
                pmax = st.number_input("Pmax", value=300, key=f"pmax{i}")

            with col4:
                cost = st.number_input("Cost", value=20.0, key=f"cost{i}")

            generators.append({
                "name": name,
                "pmin": pmin,
                "pmax": pmax,
                "cost": cost
            })

        if st.button("Run ED"):
            dispatch, total_cost = solve_ed(load, generators)

            results = pd.DataFrame({
                "Generator": [g["name"] for g in generators],
                "Dispatch": dispatch,
                "Cost": [g["cost"] for g in generators]
            })

            st.dataframe(results)
            st.success(f"Total Cost = {total_cost:.2f} {currency}")
            st.bar_chart(results.set_index("Generator")["Dispatch"])

    else:
        load = st.number_input("Load Demand (MW)", value=500)
        gen_file = st.file_uploader("Upload generators.csv", type=["csv"])

        if gen_file is not None:
            generators = parse_ed_generators(gen_file)

            if st.button("Run ED"):
                dispatch, total_cost = solve_ed(load, generators)

                results = pd.DataFrame({
                    "Generator": [g["name"] for g in generators],
                    "Dispatch": dispatch,
                    "Cost": [g["cost"] for g in generators]
                })

                st.dataframe(results)
                st.success(f"Total Cost = {total_cost:.2f} {currency}")
                st.bar_chart(results.set_index("Generator")["Dispatch"])

# ---------------------------
# DC SCED
# ---------------------------
else:
    st.header("DC-SCED")

    if input_mode == "Manual":
        num_buses = st.number_input("Number of Buses", min_value=1, value=4)
        num_gens = st.number_input("Number of Generators", min_value=1, value=3)
        num_lines = st.number_input("Number of Lines", min_value=1, value=4)

        st.subheader("Bus Data")
        buses = {}

        for i in range(num_buses):
            col1, col2 = st.columns(2)
            with col1:
                bus_id = st.text_input("Bus ID", value=f"Bus{i+1}", key=f"bus{i}")
            with col2:
                load = st.number_input("Load", value=100, key=f"load{i}")

            buses[bus_id] = load

        st.subheader("Generator Data")
        generators = {}

        for i in range(num_gens):
            st.markdown(f"### Generator {i+1}")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                gen_id = st.text_input("Gen ID", value=f"G{i+1}", key=f"gen{i}")

            with col2:
                bus = st.selectbox("Bus", list(buses.keys()), key=f"gbus{i}")

            with col3:
                pmin = st.number_input("Pmin", value=50, key=f"gpmin{i}")

            with col4:
                pmax = st.number_input("Pmax", value=300, key=f"gpmax{i}")

            with col5:
                cost = st.number_input("Cost", value=20.0, key=f"gcost{i}")

            generators[gen_id] = {
                "bus": bus,
                "pmin": pmin,
                "pmax": pmax,
                "cost": cost
            }

        st.subheader("Line Data")
        lines = {}

        for i in range(num_lines):
            st.markdown(f"### Line {i+1}")
            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                line_id = st.text_input("Line ID", value=f"L{i+1}", key=f"line{i}")

            with col2:
                from_bus = st.selectbox("From", list(buses.keys()), key=f"from{i}")

            with col3:
                to_bus = st.selectbox("To", list(buses.keys()), key=f"to{i}")

            with col4:
                x = st.number_input("Reactance", value=0.1, key=f"x{i}")

            with col5:
                limit = st.number_input("Limit", value=200, key=f"limit{i}")

            lines[line_id] = {
                "from_bus": from_bus,
                "to_bus": to_bus,
                "x": x,
                "limit": limit
            }

        if st.button("Run DC-SCED"):
            results = solve_dc_sced(buses, generators, lines)

            st.subheader("Generator Dispatch")
            st.json(results["generation"])

            st.subheader("Bus Angles")
            st.json(results["angles"])

            st.subheader("Line Flows")
            st.json(results["flows"])

            st.success(f"Total Cost = {results['cost']:.2f} {currency}")

    else:
        bus_file = st.file_uploader("Upload bus.csv", type=["csv"])
        gen_file = st.file_uploader("Upload generator.csv", type=["csv"])
        line_file = st.file_uploader("Upload line.csv", type=["csv"])

        if bus_file and gen_file and line_file:
            buses = parse_bus_csv(bus_file)
            generators = parse_generator_csv(gen_file)
            lines = parse_line_csv(line_file)

            if st.button("Run DC-SCED"):
                results = solve_dc_sced(buses, generators, lines)

                st.subheader("Generator Dispatch")
                st.json(results["generation"])

                st.subheader("Bus Angles")
                st.json(results["angles"])

                st.subheader("Line Flows")
                st.json(results["flows"])

                st.success(f"Total Cost = {results['cost']:.2f} {currency}")
