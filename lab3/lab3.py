def user_input(a, b, is_frac=False, emp=None):
    negoday = False
    while True:
        try:
            inp = input(f"{'Негодяй, введи ' if negoday else ''}{'дробное число' if is_frac else 'целую цифру'} от {a} до {b}\n")
            if inp == "" and emp is not None:
                return emp
            if is_frac:
                choice = float(inp)
            else:
                choice = int(inp)
            if a <= choice <= b:
                return choice
        except:
            negoday = True


def method_rects(f, a, b, n, method=1):
    # method == 1 - левые
    # method == 2 - центральные
    # method == 3 - правые
    s, shag = 0, (b-a)/n
    for i in range(n):
        s += f(a + shag * (i + (method - 1)/2)) * shag
    return s


def method_trapezoid(f, a, b, n, ):
    s, shag = 0, (b-a)/n
    for i in range(n):
        s += (f(a + shag * i) + f(a + shag * (i + 1)))/2 * shag
    return s


def method_simpson(f, a, b, n):
    if n % 2:
        n += 1
        print(f"Самый умный? n (принудительно) = {n}")
    s = 0
    for i in range(n+1):
        k = 1 if i in [0, n] else 4 if i % 2 else 2
        s += k * f(a + (b-a)/n * i)
    return s * (b-a) / 3 / n


if __name__ == '__main__':
    integrals = ["7*x**2 + 2*x", "3*x**3 - 4*x**2 + 7*x - 17"]
    while True:
        print(f"Выберите 1 из {len(integrals)} интегралов (по умолчанию решаем второй)")
        for i, integ in enumerate(integrals, start=1):
            print(f"{i}: {integ}")
        integral = integrals[user_input(1, len(integrals), emp=2) - 1]

        print(f"Решаем интеграл {integral} каким методом?")
        print(f"1 - Прямоугольники (правые)")
        print(f"2 - Прямоугольники (центральные)")
        print(f"3 - Прямоугольники (левые)")
        print(f"4 - Трапеции")
        print(f"5 - Симпсона")

        v = user_input(1, 5)

        print(f"От куда интегрируем? (по умолчанию a = 1)")
        a = user_input(-10000, 10000, True, emp=1)

        print(f"До куда интегрируем? (по умолчанию b = 2)")
        b = user_input(-10000, 10000, True, emp=2)

        print(f"Введите количество участков (по умолчанию n = 10)", "(кол-во участков должно быть чётным)" if v == 5 else "")
        n = user_input(1, 10000, emp=10)

        if 1 <= v <= 3:
            print("Вычисленное решение:", method_rects(lambda x: eval(integral), a, b, n, v))
            print("Точность вычислений по правилу Рунге:", (method_rects(lambda x: eval(integral), a, b, n,) - method_rects(lambda x: eval(integral), a, b, n * 2))/(2**2 - 1))
        elif v == 4:
            print("Вычисленное решение:", method_trapezoid(lambda x: eval(integral), a, b, n))
            print("Точность вычислений по правилу Рунге:", (method_trapezoid(lambda x: eval(integral), a, b, n,) - method_trapezoid(lambda x: eval(integral), a, b, n * 2))/(2**2 - 1))

        elif v == 5:
            print("Вычисленное решение:", method_simpson(lambda x: eval(integral), a, b, n))
            print("Точность вычислений по правилу Рунге:", (method_simpson(lambda x: eval(integral), a, b, n,) - method_simpson(lambda x: eval(integral), a, b, n * 2))/(2**4 - 1))

        print()
