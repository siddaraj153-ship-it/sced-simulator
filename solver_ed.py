from pyomo.environ import *
from pyomo.contrib.appsi.solvers import Highs


def solve_ed(load, generators):
    """
    generators format:
    [
        {"name":"G1","pmin":50,"pmax":300,"cost":20},
        {"name":"G2","pmin":30,"pmax":200,"cost":25}
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

    # Power balance
    model.balance = Constraint(
        expr=sum(model.P[g] for g in model.G) == load
    )

    # Generator limits
    def gen_limits(model, g):
        return (
            generators[g]["pmin"],
            model.P[g],
            generators[g]["pmax"]
        )

    model.gen_limits = Constraint(model.G, rule=gen_limits)

    solver = Highs()
    solver.solve(model)

    dispatch = []
    total_cost = value(model.obj)

    for g in model.G:
        dispatch.append(value(model.P[g]))

    return dispatch, total_cost
