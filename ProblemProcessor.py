import sympy as sp
import json

class ProblemProcessor:
    def __init__(self):
        self.problem = {}
        self.raw_problem = None

    def load_from_text(self, raw_problem_text):
        try:
            raw_problem_text = raw_problem_text.replace("`", "")
            self.set_raw_problem(json.loads(raw_problem_text))
        except Exception as e:
            print(e)

    def set_raw_problem(self, raw_problem):
        self.raw_problem = raw_problem

    def get_symbols(self):
        return {symbol.name : symbol for symbol in self.problem["variables"].keys()}

    def process(self):
        self.problem["constraints"] = []
        self.problem["variables"] = {}
        self.problem["objective_function"] = None

        # Variables
        print("variables")

        try:
            if self.raw_problem.get("variables"):
                if not isinstance(self.raw_problem["variables"], dict):
                    raise ValueError("'variables' must be a dictionary")
                for var, description in self.raw_problem["variables"].items():
                    self.problem["variables"][sp.Symbol(var)] = description
        except Exception as e:
            raise Exception(f"Error while processing variables: {e}")

        # Constraints
        print("constraints")
        print(self.get_symbols())
        try:
            if self.raw_problem.get("constraints"):
                if not isinstance(self.raw_problem["constraints"], list):
                    raise ValueError("'constraints' must be a list")
                for unparsed_expression in self.raw_problem["constraints"]:
                    self.problem["constraints"].append(sp.sympify(unparsed_expression, locals=self.get_symbols(), evaluate=False))
        except Exception as e:
            raise Exception(f"Error while processing constraints: {e}")

        # Objective function
        print("objetive function")
        try:
            if self.raw_problem.get("objective_function"):
                expr = self.raw_problem["objective_function"]
                if not isinstance(expr, str):
                    raise ValueError("'objective_function' must be a string")
                self.problem["objective_function"] = sp.sympify(expr, locals=self.get_symbols(), evaluate=False)
        except Exception as e:
            raise Exception(f"Error while processing objective function: {e}")

        # Objective (max or min)
        print("objetive")
        try:
            if self.raw_problem.get("objective"):
                if self.raw_problem["objective"] not in ["max", "min"]:
                    raise ValueError("'objective' must be either 'max' or 'min'")
                self.problem["objective"] = self.raw_problem.get("objective")
        except Exception as e:
            raise Exception(f"Error while processing objective: {e}")

        return True
