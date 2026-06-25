from pyomo.environ import *
from pyomo.contrib.appsi.solvers import Highs


def solve_ed(load, generators):
    """
    generators = [
        {"pmin": 50, "pmax": 300, "cost": 100},
        {"pmin": 50, "pmax": 400, "cost": 150}
    ]
    """

    n = len(generators)

    model = ConcreteModel()

    model.G = RangeSet(0, n - 1)
    model.P = Var(model.G, within=NonNegativeReals)

    # Objective
    model.obj = Objective(
        expr=sum(generators[g]["cost"] * model.P[g] for g in model.G),
        sense=minimize
    )

    # Balance constraint
    model.balance = Constraint(
        expr=sum(model.P[g] for g in model.G) == load
    )

    # Generator limits
    def gen_limits_rule(model, g):
        return (generators[g]["pmin"], model.P[g], generators[g]["pmax"])

    model.gen_limits = Constraint(model.G, rule=gen_limits_rule)

    solver = Highs()
    solver.solve(model)

    dispatch = []
    total_cost = value(model.obj)

    for g in model.G:
        dispatch.append(value(model.P[g]))

    return dispatch, total_cost
