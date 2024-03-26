from math import sqrt
from scipy.misc import derivative

dx = 0.00001


def user_input(a, b, is_frac=False, emp=None):
    while True:
        try:
            inp = input(f"{'Дробное число' if is_frac else 'Целую цифру'} от {a} до {b}\n")
            if inp == "" and emp is not None:
                return emp
            if is_frac:
                choice = float(inp)
            else:
                choice = int(inp)
            if a <= choice <= b:
                return choice
        except:
            pass


class Equation:
    def __init__(self, func, text):
        self.func = func
        self.text = text

    def root_exists(self, left, right):
        return (self.func(left) * self.func(right) < 0) \
               and (derivative(self.func, left, dx) * derivative(self.func, left, dx) > 0)


class Method:
    def __init__(self, eq: Equation, left, right, eps, logs=False):
        self.eq = eq
        self.left = left
        self.right = right
        self.eps = eps
        self.logs = logs

    def check(self):
        pass

    def solve(self):
        pass

    def set_eq(self, eq):
        self.eq = eq


class MethodHalfDivision(Method):
    def check(self):
        if not self.eq.root_exists(self.left, self.right):
            raise Exception("Отсутствует корень на заданном промежутке")

    def solve(self):
        self.check()

        f = self.eq.func
        a, b = self.left, self.right

        it = 0
        while True:
            it += 1
            x = (a + b) / 2
            if self.logs:
                print(f'{it}: a = {a:.3f}, b = {b:.3f}, x = {x:.3f}, '
                      f'f(a) = {f(a):.3f}, f(b) = {f(b):.3f}, f(x)={f(x):.3f}, |a-b| = {abs(a - b):.3f}')

            if abs(a - b) <= self.eps and abs(f(x)) <= self.eps:
                return x, f(x), it

            if f(a) * f(x) < 0:
                b = x
            else:
                a = x


class MethodSecant(Method):
    def check(self):
        if not self.eq.root_exists(self.left, self.right):
            raise Exception("Отсутствует корень на заданном промежутке")

    def solve(self):
        self.check()

        f = self.eq.func
        prev2 = (self.left + self.right)/2
        prev1 = prev2 + (self.left + self.right)/4
        it = 0
        while True:
            it += 1

            x = prev1 - ((prev1 - prev2) / (f(prev1) - f(prev2))) * f(prev1)
            if self.logs:
                print(f'{it}: x(i-1)={prev2:.3f}, x(i)={prev1:.3f}, x(i+1)={x:.3f}, f(x(i+1))={f(x):.3f}, |x(i+1)-x(i)|={abs(x-prev1):.3f}')

            if abs(x-prev1) <= self.eps or abs(f(x)) <= self.eps:
                return x, f(x), it
            prev2 = prev1
            prev1 = x


class MethodSimpleIteration(Method):
    def __init__(self, eq, left, right, eps, logs=False):
        super().__init__(eq, left, right, eps, logs)

        ders = [derivative(self.eq.func, self.left, dx), derivative(self.eq.func, self.right, dx)]
        mder = ders[0] if abs(ders[0]) > abs(ders[1]) else ders[1]
        _lambda = -1/mder
        self.fi = lambda x: x + _lambda * self.eq.func(x)
        self.dfi = lambda x: 1 + _lambda * derivative(self.eq.func, x, dx)

        self.max_iters = 10000

    def check(self):
        if not self.eq.root_exists(self.left, self.right):
            raise Exception("Отсутствует корень на заданном промежутке")

        if abs(self.dfi(self.left)) > 1 or abs(self.dfi(self.right)) > 1:
            raise Exception("Условие сходимости на интервале не выполняется!")

    def solve(self):
        self.check()

        f = self.eq.func
        prev = (self.left + self.right)/2
        it = 0
        while True:
            it += 1

            if it == 10000:
                raise Exception(f'Достигнуто {it} итераций, увы, не сошлось')

            x = self.fi(prev)
            diff = abs(x - prev)
            if self.logs:
                print(f'{it}: xk = {prev:.3f}, f(xk) = {f(prev):.3f}, '
                      f'xk+1 = 𝜑(𝑥𝑘) = {x:.3f}, |xk - xk+1| = {diff:.3f}')

            if abs(f(x)) <= self.eps:
                return x, f(x), it
            prev = x


class System:
    def __init__(self):
        pass

    def f(self, xy):
        x, y = xy
        return [1 - y ** 2 - x ** 2, x ** 2 - 0.5 - y]

    def fi1(self, x, y):
        return sqrt(1 - y ** 2)

    def fi2(self, x, y):
        return x ** 2 - 0.5

    def solve(self, prev, eps, max_it=10000):
        it = 0
        while True:
            it += 1

            if it > max_it:
                raise Exception(f"Не сошлось за {max_it} итераций")

            cur = [self.fi1(*prev), self.fi2(*prev)]
            if abs(((cur[0] - prev[0]) ** 2 + (cur[1] - prev[1]) ** 2) ** 0.5) < eps:
                return cur, it
            prev = cur


eqs = [
    Equation(lambda x: -0.38*x**3 - 3.42*x**2 + 2.51*x + 8.75, "-0.38*x**3 - 3.42*x**2 + 2.51*x + 8.75"),
    Equation(lambda x: x**3 - 1.89*x**2 - 2*x + 1.76, "x**3 - 1.89*x**2 - 2*x + 1.76"),
    Equation(lambda x: x**3 + 4.81*x**2 - 17.37*x + 5.38, "x**3 + 4.81*x**2 - 17.37*x + 5.38")
]
methods = ["половинного деления", "секущих", "простой итерации"]

while True:
    print("Что решаем? Систему(1) или уравнение(2)?")
    ch_sp = ch_eq = user_input(1, 2)
    # ch_sp = 2

    if ch_sp == 1:
        print("Введите x0 (пустая строка x0 = 0.5)")
        x0 = user_input(0, 1, True, 0.5)
        # x0 = 0.5

        print("Введите y0 (пустая строка y0 = 0.5)")
        y0 = user_input(0, 0.7, True, 0.5)
        # y0 = 0.5

        print("Введите эпсилон (пустая строка e = 0.001)")
        eps = user_input(0, 1, True, 0.001)
        # eps = 0.001

        system = System()
        xy_solution, iterations = system.solve((x0, y0), eps)
        print(f"\nНеизвестные: x = {xy_solution[0]:.5f}, y = {xy_solution[1]:.5f}")
        print(f"Количество итераций: {iterations}")
        print(f'Невязка: {system.f(xy_solution)[0]}, {system.f(xy_solution)[1]}')

    if ch_sp == 2:
        print("Выберите одно из уравнений:")
        for ind, e in enumerate(eqs, start=1):
            print(f"№: {ind}, уравнение: {e.text}")

        eq = eqs[user_input(1, len(eqs)) - 1]
        # eq = eqs[0]

        print("Выберите метод решения:")
        for ind, e in enumerate(methods, start=1):
            print(f"№: {ind}, метод: {e}")
        method = user_input(1, len(methods))

        print("Введите левую границу (пустая строка left = 1.5)")
        left = user_input(-10000, 10000, True, 1.5)
        # left = -5

        print("Введите правую границу (пустая строка right = 3)")
        right = user_input(-10000, 10000, True, 3)
        # right = 0

        print("Введите эпсилон (пустая строка e = 0.001)")
        eps = user_input(0, 1, True, 0.001)
        # eps = 0.001

        if method == 1:
            sol = MethodHalfDivision(eq, left, right, eps, True)
        elif method == 2:
            sol = MethodSecant(eq, left, right, eps, True)
        else:
            sol = MethodSimpleIteration(eq, left, right, eps, True)
        try:
            ans = sol.solve()
            print(f"Результат вычислений: {ans[0]}\nКоличество итераций: {ans[2]}")
        except Exception as e:
            print(f"Возникла ошибка: {e}")
