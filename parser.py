import pandas as pd


def parse_ed_generators(file):
    """
    Expected CSV columns:
    generator,pmin,pmax,cost
    """

    df = pd.read_csv(file)

    generators = []

    for _, row in df.iterrows():
        generators.append({
            "name": row["generator"],
            "pmin": float(row["pmin"]),
            "pmax": float(row["pmax"]),
            "cost": float(row["cost"])
        })

    return generators


def parse_bus_csv(file):
    """
    Expected CSV columns:
    bus_id,load
    """

    df = pd.read_csv(file)

    buses = {}

    for _, row in df.iterrows():
        buses[row["bus_id"]] = float(row["load"])

    return buses


def parse_generator_csv(file):
    """
    Expected CSV columns:
    gen_id,bus,pmin,pmax,cost
    """

    df = pd.read_csv(file)

    generators = {}

    for _, row in df.iterrows():
        generators[row["gen_id"]] = {
            "bus": row["bus"],
            "pmin": float(row["pmin"]),
            "pmax": float(row["pmax"]),
            "cost": float(row["cost"])
        }

    return generators


def parse_line_csv(file):
    """
    Expected CSV columns:
    line_id,from_bus,to_bus,x,limit
    """

    df = pd.read_csv(file)

    lines = {}

    for _, row in df.iterrows():
        lines[row["line_id"]] = {
            "from_bus": row["from_bus"],
            "to_bus": row["to_bus"],
            "x": float(row["x"]),
            "limit": float(row["limit"])
        }

    return lines
