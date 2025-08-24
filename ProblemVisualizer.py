import sympy as sp
import matplotlib.pyplot as plt

def create_plot(constraints, symbols, solution=None, vertices=None):
    print(constraints, symbols, solution, vertices)
    x, y = list(symbols.values())[:2]

    fig, ax = plt.subplots()

    for constraint in constraints:
        lhs = constraint.lhs
        rhs = constraint.rhs
        eq = sp.Eq(lhs, rhs)

        try:
            sol = sp.solve(eq, y)
        except Exception as e:
            print(f"No se pudo resolver {eq} respecto a {y}: {e}")
            continue

        if sol:
            f = sp.lambdify(x, sol[0], "numpy")
            xs = range(0, 200)
            ys = [f(val) for val in xs]
            ax.plot(xs, ys, linestyle="--", label=str(eq))

    if vertices:
        vx = [v[x] for v in vertices]
        vy = [v[y] for v in vertices]
        ax.fill(vx, vy, alpha=0.3, label="Espacio de soluciones")
        ax.scatter(vx, vy, c="blue", s=50, label="Vértices")

    if solution:
        ax.scatter(solution[x], solution[y], c="red", s=100, label="Solución óptima")

    ax.set_xlabel(str(x))
    ax.set_ylabel(str(y))
    ax.legend()
    ax.set_title("Región factible y solución")

    return fig, ax
