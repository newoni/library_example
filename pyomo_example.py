#<20.04.28> by KH
'''
conda install -c conda-forge pyomo pyomo.extra
conda install -c conda-forge ipopt glpk
'''

from pyomo.environ import *

class Optimization:
    def __init__(self):
        pass

    def set_model(self):
        self.model = ConcreteModel() #Concrete v.s. Abstract 2가지 있음. (pulp도 Concrete, Abstract는 수학적 기호 활용)

    def set_parameter(self):
        self.model.IDX = range(10)
        self.model.IDX2 = Set(initialize = [1,2,5])  # set은 python, Set은 pyomo 변수, initial이라고 꼭 써줘야함.
        self.model.IDX3 = RangeSet(5)        #range는 0 부터시작, RangeSet은 1부터 시작

    def set_variable(self):
        self.model.x = Var(initialize=-1.2, bounds=(-2,2))       # 단순 변수 선언
        self.model.y = Var(initialize=1.0, bounds=(-2,2))
        self.model.a_variable = Var(within = NonNegativeReals)   # 다양한 변수 선언 방식
        self.model.b_variable = Var(within = Binary)
        self.model.c_variable = Var(self.model.IDX)   # 벡터 형식의 변수 선언

    def set_constraints(self):
        self.model.c1 = Constraint(expr = self.model.a_variable + 5 * self.model.b_variable <= self.model.x)    # 제약 조건 선언
        self.model.c2 = Constraint(expr = sum(self.model.c_variable[i] for i in self.model.IDX) <= self.model.a_variable)

        self.model.limits = ConstraintList()         # 제 조건 list 선언 (for 문 활용에 용이)
        self.model.limits.add(30*self.model.x + 15*self.model.y <= 100)
        self.model.limits.add(15*self.model.x + 30*self.model.y <=50)

    def set_object_function(self):
        self.model.obj = Objective(expr= (1-self.model.x)**2 + 100*(self.model.y-self.model.x**2)**2, sense=minimize)

    def set_solver(self):
        self.solver = SolverFactory("ipopt")

    def solve(self):
        self.solver.solve(self.model, tee=True)

if __name__ == "__main__":
    test_model = Optimization()
    test_model.set_model()
    test_model.set_parameter()
    test_model.set_variable()
    test_model.set_constraints()
    test_model.set_object_function()
    test_model.set_solver()
    test_model.solve()

    print("*** Solution ***")
    print("x: ", value(test_model.model.x))
    print("y: ", value(test_model.model.y))

