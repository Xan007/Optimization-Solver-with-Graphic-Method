import sympy as sp

def obtener_formas_x(funcion):
    x = sp.symbols('x')
    f = funcion
    ecuacion = sp.Eq(f, 0)

    pendientes = [ecuacion]
    formas = []

    while pendientes:
        eq = pendientes.pop()
        lhs, rhs = eq.lhs, eq.rhs

        # Si ya está en forma x = ...
        if lhs == x:
            formas.append(eq)
            continue

        # Si es un término con potencia
        if lhs.is_Pow and lhs.base == x:
            n = lhs.exp
            rhs_new = rhs ** (sp.Rational(1, n))
            pendientes.append(sp.Eq(x, rhs_new))
            pendientes.append(sp.Eq(x, -rhs_new))
            continue

        # Si es algo proporcional a x
        if lhs.is_Mul and lhs.has(x):
            coef, var = lhs.as_independent(x)
            if coef != 1:
                pendientes.append(sp.Eq(var, rhs/coef))
                continue

        # Si es una suma de términos, separar cada término
        if lhs.is_Add:
            for t in lhs.as_ordered_terms():
                resto = sp.simplify(lhs - t)
                pendientes.append(sp.Eq(t, rhs - resto))
            continue

        formas.append(eq)

    return [eq.rhs for eq in formas if eq.lhs == x]


def punto_fijo(funcion, valor_inicial, err_hasta_decimal):
    formas = obtener_formas_x(funcion)
    x = sp.Symbol("x")
    resultados = []

    for forma in formas:
        g = sp.lambdify(x, forma, "math")
        valor_anterior = valor_inicial
        iteracion = 0
        err_actual = float("inf")

        try:
            while err_actual >= err_hasta_decimal:
                valor_actual = g(valor_anterior)
                err_actual = abs((valor_actual - valor_anterior) / valor_actual)
                valor_anterior = valor_actual
                iteracion += 1

            resultados.append({
                "forma": str(forma),
                "iteraciones": iteracion,
                "valor": valor_anterior,
                "error": float(err_actual)
            })
        except:
            continue

    return resultados


res = punto_fijo(sp.sympify("-(1/2)*x**2 + 5/2 * x + 9/2"), 0, 0.001/100)
for r in res:
    print(r)
