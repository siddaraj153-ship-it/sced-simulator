from pyomo.environ import *
from pyomo.contrib.appsi.solvers import Highs


def solve_ed(load, generators):
    n = len(generators)

    model = ConcreteModel()

    model.G = RangeSet(0, n - 1)
    model.P = Var(model.G, within=NonNegativeReals)

    model.obj = Objective(
        expr=sum(generators[g]["cost"] * model.P[g] for g in model.G),
        sense=minimize
    )

    model.balance = Constraint(
        expr=sum(model.P[g] for g in model.G) == load
    )

    def gen_limits_rule(model, g):
        return (generators[g]["pmin"], model.P[g], generators[g]["pmax"])

    model.gen_limits = Constraint(model.G, rule=gen_limits_rule)

    solver = Highs()
    solver.solve(model)

    dispatch = [value(model.P[g]) for g in model.G]
    total_cost = value(model.obj)

    return dispatch, total_cost
