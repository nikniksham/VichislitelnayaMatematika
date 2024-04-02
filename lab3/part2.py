from lab3 import user_input, method_trapezoid, method_rects, method_simpson
from math import pi, sin

integrals = ["1/x**2", "1/sin(pi*x)"]


def check_discontinuity(f, a, b):
    try:
        f(a)
        f(b)
        return False
    except Exception as e:
        return True


def check_convergence(f, a, b):
    if f == integrals[0] and a * b < 0:
        return True
    if f == integrals[1] and str(a)[0] != str(b)[0]:
        return True
    return False


while True:
    print(f"Выберите 1 из {len(integrals)} интегралов")
    for i, integ in enumerate(integrals, start=1):
        print(f"{i}: {integ}")
    inter = integrals[user_input(1, len(integrals), emp=2) - 1]
    integral = lambda x: eval(inter)

    print(f"От куда интегрируем? (по умолчанию a = 0)")
    a = user_input(-10000, 10000, True, emp=0)

    print(f"До куда интегрируем? (по умолчанию b = 1)")
    b = user_input(-10000, 10000, True, emp=1)

    if check_discontinuity(integral, a, b):
        print(f"Выбранный интеграл {inter} на отрезке [{a}; {b}] имеет разрыв (не существует)")
        continue
    if check_convergence(inter, a, b):
        print(f"Выбранный интеграл {inter} на отрезке [{a}; {b}] расходится (не существует)")
        continue

    print("Всё хорошо, интеграл существует")

    print(f"Каким методом решаем интеграл {inter}?")
    print(f"1 - Прямоугольники (правые)")
    print(f"2 - Прямоугольники (центральные)")
    print(f"3 - Прямоугольники (левые)")
    print(f"4 - Трапеции")
    print(f"5 - Симпсона")

    v = user_input(1, 5)

    print(f"Введите количество участков (по умолчанию n = 10)", "(кол-во участков должно быть чётным)" if v == 5 else "")
    n = user_input(1, 10000, emp=10)

    if 1 <= v <= 3:
        print("Вычисленное решение:", method_rects(integral, a, b, n, v))
    elif v == 4:
        print("Вычисленное решение:", method_trapezoid(integral, a, b, n))
    elif v == 5:
        print("Вычисленное решение:", method_simpson(integral, a, b, n))
