import matplotlib.pyplot as plt
from math import factorial, cos, sin, exp


def get_range(start, finish, count, bonus=True):
    if bonus:
        h = (finish - start)*1.2
        return [start + h*i/count - h/10 for i in range(count+1)]
    h = finish - start
    return [start + h*i/count for i in range(count+1)]


def draw_graph(func_points, x, y, name="График"):
    # plt.figure(figsize=(5, 2.7), layout='constrained')
    plt.plot(x, y, label="база")
    for i in range(len(func_points[0])):
        plt.plot(func_points[0][i], func_points[1][i], 'ro')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(name)
    ax = plt.gca()
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    plt.legend()
    plt.show()


def get_points_from_func(a, b, count, func):
    xr, yr = [], []
    for i in range(count):
        x = a + i * (a-b)/count
        xr.append(x)
        yr.append(eval(func))
    return [xr, yr]


def get_table(ys):
    table = [ys.copy()]
    for i in range(len(ys) - 1, 0, -1):
        table.append([])
        for j in range(i):
            table[-1].append(table[-2][j + 1] - table[-2][j])
    return table


def lagrange(func_points, need_points):
    res = []
    for point in need_points:
        zn = 0
        for i in range(len(func_points[0])):
            verh, niz = 1, 1
            for j in range(len(func_points[0])):
                if i != j:
                    verh *= (point - func_points[0][j])
                    niz *= (func_points[0][i] - func_points[0][j])
            zn += func_points[1][i] * verh/niz
        res.append(zn)
    return res


def newton(func_points, need_points):
    h = func_points[0][1] - func_points[0][0]
    table = get_table(func_points[1])
    res = []
    for point in need_points:
        res.append(0)
        q = (point - func_points[0][0])/h
        for i in range(len(table)):
            loc = table[i][0] / factorial(i) * (q if i > 0 else 1)
            for j in range(i-1):
                loc *= (q - (j+1))
                # print((j+1), i)
            res[-1] += loc
    return res


def gauss(func_points, need_points):
    h = func_points[0][1] - func_points[0][0]
    table = get_table(func_points[1])
    res = []
    for point in need_points:
        mi, ip = 999999999, 0
        for ind, el in enumerate(func_points[0]):
            if abs(point - el) < mi:
                mi = abs(point - el)
                ip = ind
        t = (point - func_points[0][ip]) / h
        zsf, lr = 0 if point > func_points[0][ip] else 1, 0
        for i in range(len(table)):
            r = table[i][ip - int((i+zsf)/2)] * (t if i > 0 else 1) / factorial(i)
            for j in range(i-1):
                r *= (t - (-1)**(j+zsf) * (int(j/2)+1))
            lr += r
        res.append(lr)
    return res


points = [[1, 2, 3, 4, 5], [3, 2, 4, 5, 1]]
# points = [[0.1, 0.2, 0.3, 0.4, 0.5], [1.25, 12.38, 3.79, 1.44, 7.14]]
# points = [[1, 2, 3, 4, 5], [4.7, 8.4, 12.3, 13.2, 13.9]]
# points = get_points_from_func(1, 10, 11, "exp(x)*cos(x)")
x = get_range(min(points[0]), max(points[0]), 1000, False)

h, mid = points[0][1]-points[0][0], points[0][len(points[0])//2]
x_gauss = get_range(mid - h/2, mid + h/2, 100, False)

print(*get_table(points[1]), sep="\n")

try:
    y_lagrange = lagrange(points, x)
    y_newton = newton(points, x)
    draw_graph(points, x, y_lagrange)
    draw_graph(points, x, y_newton)
except Exception as e:
    print("Как ты это сломал???")
    print(e)

try:
    y_gauss = gauss(points, x_gauss)
    draw_graph(points, x_gauss, y_gauss)
except Exception as e:
    print("Ничего удивительного, метод кал")
    print(e)

