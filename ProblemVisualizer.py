import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def create_plot(constraints, symbols, solution=None, vertices=None):
    x, y = list(symbols.values())[:2]

    fig, ax = plt.subplots(figsize=(6, 6))

    # --- Estimar límites del gráfico con vértices/solución (si hay) ---
    pts = []
    if vertices:
        for v in vertices:
            if x in v and y in v:
                pts.append((float(v[x]), float(v[y])))
    if solution:
        pts.append((float(solution[x]), float(solution[y])))

    if pts:
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        xmin, xmax = min(xs), max(xs)
        ymin, ymax = min(ys), max(ys)

        dx = (xmax - xmin) or 1.0
        dy = (ymax - ymin) or 1.0
        xmin -= 0.2 * dx; xmax += 0.2 * dx
        ymin -= 0.2 * dy; ymax += 0.2 * dy
    else:
        xmin, xmax, ymin, ymax = 0.0, 10.0, 0.0, 10.0

    Xline = np.linspace(xmin, xmax, 400)
    Yline = np.linspace(ymin, ymax, 400)

    for r in constraints:
        eq = sp.Eq(r.lhs, r.rhs)
        
        try:
            sol = sp.solve(eq, y)
            if sol:
                if not sol[0].has(x):
                    Y = np.full_like(Xline, float(sol[0]), dtype=float)
                else:
                    f = sp.lambdify(x, sol[0], "numpy")
                    Y = f(Xline)
                ax.plot(Xline, Y, linestyle="--", label=str(eq.lhs) + " = " + str(eq.rhs))
                continue
        except Exception:
            pass

        try:
            sol = sp.solve(eq, x)
            if sol:
                if not sol[0].has(y):
                    X = np.full_like(Yline, float(sol[0]), dtype=float)
                else:
                    g = sp.lambdify(y, sol[0], "numpy")
                    X = g(Yline)
                ax.plot(X, Yline, linestyle="--", label=str(eq.lhs) + " = " + str(eq.rhs))
                continue
        except Exception:
            pass

    if vertices:
        vx, vy = [], []
        for v in vertices:
            if x in v and y in v:
                vx.append(float(v[x]))
                vy.append(float(v[y]))

        if vx and vy:
            vx = np.array(vx)
            vy = np.array(vy)

            order = np.argsort(np.arctan2(vy - vy.mean(), vx - vx.mean()))
            vx_ordered = vx[order]
            vy_ordered = vy[order]

            pts = list(zip(vx_ordered, vy_ordered))
            poly = Polygon(pts, closed=True, alpha=0.3, label="Espacio de soluciones", facecolor='green')
            ax.add_patch(poly)

            ax.scatter(vx, vy, s=40, zorder=3, label="Vértices")

    if solution:
        if x in solution and y in solution:
            sx, sy = float(solution[x]), float(solution[y])
        else:
            sx = sy = None
        if sx is not None and sy is not None:
            ax.scatter(sx, sy, s=100, zorder=4, edgecolor="black", label="Solución óptima")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel(str(x))
    ax.set_ylabel(str(y))
    ax.set_title("Región factible y solución")
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="best")

    return fig, ax
