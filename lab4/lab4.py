import sympy
from sympy import *
from math import log, e
from ma


def draw_graph(x, y, func):



def calc_s_delta(x, y, func, logs=True):
    n = len(x)
    acc = 4
    s = 0
    sr_zn = 0
    for i in range(n):
        res = round(func(x[i]), acc)
        eps = round(res - y[i], acc)
        s += eps ** 2
        sr_zn += func(x[i])
        if logs:
            print(f"({x[i], y[i]}), {res}, {eps}")

    sr_zn /= n
    if logs:
        print("-"*100)
    delta = (s / n) ** 0.5
    R = 1 - s/sum([(ye - sr_zn)**2 for ye in y])
    return [s, delta, R, func]


def make_table(func, a, b, h):
    x, y = [], []
    for i in range(int((b-a)/h)+1):
        x.append(a + i*h)
        y.append(func(x[-1]))
    return x, y


def linear_approximation(x, y, logs=True):
    print("ЛИНЕЙНАЯ АППРОКСИМАЦИЯ")
    n = len(x)
    sx = sum(x)
    sxx = sum([el**2 for el in x])
    sy = sum(y)
    sxy = sum([x[i] * y[i] for i in range(n)])
    a = (sxy - sx * sy / n) / (sxx - sx * sx / n)
    b = sy / n - sx / n * a

    if logs:
        print(f"a = {a}")
        print(f"b = {sy / n - sx / n * a}")
        print(f"y = {a} * x + {b}")
        print()

    res = calc_s_delta(x, y, lambda x: a * x + b, logs)
    x_s = sum(x) / n
    y_s = sum(y) / n
    r = sum([(x[i] - x_s) * (y[i] - y_s) for i in range(n)])
    r = r / (sum([(x[i] - x_s) ** 2 for i in range(n)]) * sum([(y[i] - y_s) ** 2 for i in range(n)])) ** 0.5
    res.append(r)
    return res


def quadratic_approximation(x, y, logs=True):
    print("КВАДРАТИЧНАЯ АППРОКСИМАЦИЯ")
    n = len(x)
    kx = [round(sum([el**(deg+1) for el in x]), 3) for deg in range(4)]
    kxy = [round(sum([x[i]**deg * y[i] for i in range(n)]), 3) for deg in range(3)]
    kx.insert(0, n)
    a = f"{kx[0]}*a + {kx[1]}*a1 + {kx[2]}*a2 - {kxy[0]}"
    a1 = f"{kx[1]}*a + {kx[2]}*a1 + {kx[3]}*a2 - {kxy[1]}"
    a2 = f"{kx[2]}*a + {kx[3]}*a1 + {kx[4]}*a2 - {kxy[2]}"

    if logs:
        print(a, a1, a2, sep="\n")
        print("\nРешим систему\n")

    k_a2 = str(solveset(sympify(a2), "a2"))[1:-1]
    k_a1 = str(solveset(sympify(a1).subs("a2", k_a2), "a1"))[1:-1]

    if logs:
        print(f"a2 = {k_a2}")
        print(f"a1 = {k_a1}")
        print()
    a_resh = float(sympy.Float(str(solveset(sympify(a).subs("a2", k_a2).subs("a1", k_a1), "a"))[1:-1]))
    a1_resh = float(sympy.Float(simplify(k_a1).subs("a", a_resh)))
    a2_resh = float(sympy.Float(simplify(k_a2).subs("a", a_resh).subs("a1", a1_resh)))

    if logs:
        print(f"a = {a_resh}")
        print(f"a1 = {a1_resh}")
        print(f"a2 = {a2_resh}")
        print(f"y = {a2_resh} * x**2 + {a1_resh} * x + {a_resh}")
        print()

    return calc_s_delta(x, y, lambda x: a_resh + a1_resh * x + a2_resh * x**2, logs)


def cubic_approximation(x, y, logs=True):
    print("КУБИЧЕСКАЯ АППРОКСИМАЦИЯ")
    n = len(x)
    kx = [round(sum([el ** (deg + 1) for el in x]), 3) for deg in range(6)]
    kxy = [round(sum([x[i] ** deg * y[i] for i in range(n)]), 3) for deg in range(4)]
    kx.insert(0, n)
    a = f"{kx[0]}*a + {kx[1]}*a1 + {kx[2]}*a2 + {kx[3]}*a3 - {kxy[0]}"
    a1 = f"{kx[1]}*a + {kx[2]}*a1 + {kx[3]}*a2 + {kx[4]}*a3 - {kxy[1]}"
    a2 = f"{kx[2]}*a + {kx[3]}*a1 + {kx[4]}*a2 + {kx[5]}*a3 - {kxy[2]}"
    a3 = f"{kx[3]}*a + {kx[4]}*a1 + {kx[5]}*a2 + {kx[6]}*a3 - {kxy[3]}"

    if logs:
        print(a, a1, a2, a3, sep="\n")
        print("\nРешим систему\n")

    k_a3 = str(solveset(sympify(a3), "a3"))[1:-1]
    k_a2 = str(solveset(sympify(a2).subs("a3", k_a3), "a2"))[1:-1]
    k_a1 = str(solveset(sympify(a1).subs("a3", k_a3).subs("a2", k_a2), "a1"))[1:-1]

    if logs:
        print(f"a3 = {k_a3}")
        print(f"a2 = {k_a2}")
        print(f"a1 = {k_a1}")
        print()

    a_resh = float(sympy.Float(str(solveset(sympify(a).subs("a3", k_a3).subs("a2", k_a2).subs("a1", k_a1), "a"))[1:-1]))
    a1_resh = float(sympy.Float(simplify(k_a1).subs("a", a_resh)))
    a2_resh = float(sympy.Float(simplify(k_a2).subs("a", a_resh).subs("a1", a1_resh)))
    a3_resh = float(sympy.Float(simplify(k_a3).subs("a", a_resh).subs("a1", a1_resh).subs("a2", a2_resh)))

    if logs:
        print(f"a = {a_resh}")
        print(f"a1 = {a1_resh}")
        print(f"a2 = {a2_resh}")
        print(f"a3 = {a3_resh}")
        print(f"y = {a3_resh} * x**3 + {a2_resh} * x**2 + {a1_resh} * x + {a_resh}")
        print()

    return calc_s_delta(x, y, lambda x: a_resh + a1_resh * x + a2_resh * x ** 2 + a3_resh * x ** 3, logs)


def exponential_approximation(x, y, logs=True):
    print("ЭКСПОНЕНЦИАЛЬНАЯ АППРОКСИМАЦИЯ")
    ln = lambda x: log(x, e)
    lny = [ln(ye) for ye in y]
    n = len(x)
    b = (n * sum([x[i] * lny[i] for i in range(n)]) - sum(x) * sum(lny)) / (n * sum([xe**2 for xe in x]) - sum(x)**2)
    a = (sum(lny) / n) - (sum(x) * b / n)

    if logs:
        print(f"a = {a}\t b = {b}")
        print(f"y = y**({a} + {b} * x)")

    return calc_s_delta(x, y, lambda x: e**(a + b * x), logs)


def logarithmic_approximation(x, y, logs=True):
    print("ЛОГАРИФМИЧЕСКАЯ АППРОКСИМАЦИЯ")
    ln = lambda x: log(x, e)
    lnx = [ln(xe) for xe in x]
    n = len(x)
    b = (n * sum([y[i] * lnx[i] for i in range(n)]) - sum(lnx) * sum(y)) / (n * sum([lnxe**2 for lnxe in lnx]) - sum(lnx)**2)
    a = sum(y) / n - sum(lnx) * b / n
    if logs:
        print(f"a = {a}\t b = {b}")
        print(f"y = {a} + {b} * ln(x)")

    return calc_s_delta(x, y, lambda x: a + b * ln(x), logs)


def degree_approximation(x, y, logs=True):
    print("СТЕПЕННАЯ АППРОКСИМАЦИЯ")
    ln = lambda x: log(x, e)
    lnx = [ln(xe) for xe in x]
    lny = [ln(ye) for ye in y]
    n = len(x)
    b = (n * sum([lnx[i]*lny[i] for i in range(n)]) - sum(lnx) * sum(lny)) / (n * sum(lnxe**2 for lnxe in lnx) - sum(lnx)**2)
    a = e**(sum(lny)/n - sum(lnx) * b / n)

    if logs:
        print(f"a = {a}\t b = {b}")
        print(f"y = {a} * x**{b}")

    return calc_s_delta(x, y, lambda x: a * x**b, logs)


x, y = make_table(lambda x: 2*x/(x**4 + 17), 0.0001, 2, 0.2)

# x = [57, 58, 59, 62, 64, 64, 65, 68, 69, 69, 71, 81, 83, 91]
# y = [158, 163, 164, 165, 168, 171, 172, 175, 175, 176, 178, 182, 183, 183]

logs = False
print(linear_approximation(x, y, logs), "\n-----------------------")
print(quadratic_approximation(x, y, logs), "\n-----------------------")
print(cubic_approximation(x, y, logs), "\n-----------------------")
print(exponential_approximation(x, y, logs), "\n-----------------------")
print(logarithmic_approximation(x, y, logs), "\n-----------------------")
print(degree_approximation(x, y, logs), "\n-----------------------")

