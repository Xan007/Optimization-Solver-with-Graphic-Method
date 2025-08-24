import sympy as sp

class ProblemSolver:
    def __init__(self, problem: dict):
        self.problem = problem
        self.vertices = None
        self.solution = None

    def vertice_in_solution(self, vertice: dict):
        variables = self.problem.get("variables", {}).keys()
        constraints = self.problem.get("constraints", [])

        in_solution = True
        for constraint in constraints:
            if not constraint.subs(vertice):
                in_solution = False
        return in_solution                
            

    def find_vertices(self):
        if self.vertices:
            return self.vertices

        vertices = []
        constraints = self.problem.get("constraints", [])
        
        for i in range(len(constraints)):
            for j in range(i+1, len(constraints)):
                eq1 = sp.Eq(constraints[i].lhs, constraints[i].rhs)
                eq2 = sp.Eq(constraints[j].lhs, constraints[j].rhs)
                try:
                    sol = sp.solve((eq1, eq2), list(self.problem["variables"].keys()))
                    if sol not in vertices and self.vertice_in_solution(sol):
                        vertices.append(sol)
                except Exception:
                    pass
        self.vertices = vertices
        
        return vertices

    def solve_objective(self):
        obj = self.problem["objective_function"]
        obj_type = self.problem.get("objective", "max")

        lastResult = None
        if obj_type == "max":
            lastResult = 0
        elif obj_type == "min":
            lastResult = float("inf")

        vertices = self.find_vertices()
        solution_vertice = None

        for vertice in vertices:
            result = obj.subs(vertice)
            
            if obj_type == "max" and result > lastResult:
                lastResult = result
                solution_vertice = vertice
            elif obj_type == "min" and result < lastResult:
                lastResult = result
                solution_vertice = vertice

        self.solution = solution_vertice
