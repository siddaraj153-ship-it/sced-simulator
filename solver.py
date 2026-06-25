from pyomo.environ import *

def solve_ed(load, g1_min, g1_max, g1_cost, g2_min, g2_max, g2_cost):

    model = ConcreteModel()

    model.P1 = Var(bounds=(g1_min, g1_max))
    model.P2 = Var(bounds=(g2_min, g2_max))

    model.obj = Objective(
        expr=g1_cost * model.P1 + g2_cost * model.P2,
        sense=minimize
    )

    model.balance = Constraint(
        expr=model.P1 + model.P2 == load
    )

    solver = SolverFactory('glpk')
    solver.solve(model)

    return {
        "P1": value(model.P1),
        "P2": value(model.P2),
        "cost": value(model.obj)
    }