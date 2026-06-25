from pyomo.environ import *
from pyomo.contrib.appsi.solvers import Highs


def solve_dc_sced():
    buses = {
        "Bus1": 100,
        "Bus2": 200,
        "Bus3": 150,
        "Bus4": 250
    }

    generators = {
        "G1": {"bus": "Bus1", "pmin": 50, "pmax": 400, "cost": 20},
        "G2": {"bus": "Bus2", "pmin": 50, "pmax": 300, "cost": 40},
        "G3": {"bus": "Bus4", "pmin": 50, "pmax": 250, "cost": 60}
    }

    lines = {
        "L1": {"from_bus": "Bus1", "to_bus": "Bus2", "x": 0.1, "limit": 200},
        "L2": {"from_bus": "Bus2", "to_bus": "Bus3", "x": 0.15, "limit": 150},
        "L3": {"from_bus": "Bus3", "to_bus": "Bus4", "x": 0.1, "limit": 200},
        "L4": {"from_bus": "Bus1", "to_bus": "Bus4", "x": 0.2, "limit": 100}
    }

    model = ConcreteModel()

    model.B = Set(initialize=list(buses.keys()))
    model.G = Set(initialize=list(generators.keys()))
    model.L = Set(initialize=list(lines.keys()))

    model.Pg = Var(model.G)
    model.theta = Var(model.B)
    model.Flow = Var(model.L)

    model.obj = Objective(
        expr=sum(generators[g]["cost"] * model.Pg[g] for g in model.G),
        sense=minimize
    )

    def gen_limits(model, g):
        return (
            generators[g]["pmin"],
            model.Pg[g],
            generators[g]["pmax"]
        )

    model.gen_limits = Constraint(model.G, rule=gen_limits)

    model.slack = Constraint(expr=model.theta["Bus1"] == 0)

    def flow_rule(model, l):
        line = lines[l]
        return model.Flow[l] == (
            model.theta[line["from_bus"]] -
            model.theta[line["to_bus"]]
        ) / line["x"]

    model.flow_constraint = Constraint(model.L, rule=flow_rule)

    def line_limits(model, l):
        limit = lines[l]["limit"]
        return (-limit, model.Flow[l], limit)

    model.line_limits = Constraint(model.L, rule=line_limits)

    def power_balance(model, b):
        generation = sum(
            model.Pg[g] for g in model.G
            if generators[g]["bus"] == b
        )

        inflow = sum(
            model.Flow[l] for l in model.L
            if lines[l]["to_bus"] == b
        )

        outflow = sum(
            model.Flow[l] for l in model.L
            if lines[l]["from_bus"] == b
        )

        return generation + inflow - outflow == buses[b]

    model.balance = Constraint(model.B, rule=power_balance)

    solver = Highs()
    solver.solve(model)

    results = {
        "generation": {g: value(model.Pg[g]) for g in model.G},
        "angles": {b: value(model.theta[b]) for b in model.B},
        "flows": {l: value(model.Flow[l]) for l in model.L},
        "cost": value(model.obj)
    }

    return results
