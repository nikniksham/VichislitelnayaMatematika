import matplotlib.pyplot as plt
from math import cos


def log_print(s, log):
    if log:
        print(s)


def draw_graph(x, y, name="График"):
    plt.plot(x[1:], y[1:], label="база")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(name)
    ax = plt.gca()
    # ax.axhline(y=0, color='k')
    # ax.axvline(x=100, color='k')
    plt.legend()
    plt.show()


def get_table(ys):
    table = [ys.copy()]
    for i in range(len(ys) - 1, 0, -1):
        table.append([])
        for j in range(i):
            table[-1].append(table[-2][j] - table[-2][j + 1])
    return table


def euler_simple(sx, ex, h, y0, func, count=None, logs=True, eps=None):
    log_print("i\tXi\t\tYi\t\t\tF(Xi,Yi)", logs)
    res = [[], []]
    xi, yi = sx, y0
    i = 0
    while xi < ex:
        if count and i == count:
            break
        if i > 2_000_000:
            print("Не сошлося")
            break
        xi += h
        f = func(xi, yi)
        y_loc = yi + h * f
        if eps and i > 0 and xi < ex:
            srav = euler_simple(xi-h/2, ex, h/2, yi, func, 2, False)[1][-1]
            r = abs(y_loc - srav)/(2**1 - 1)
            if r > eps:
                xi -= h
                h /= 4
                log_print(f"Вот так вот", logs)
                continue
        log_print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{f:.3f}", logs)
        res[0].append(xi)
        res[1].append(yi)
        yi = y_loc
        i += 1
    return res


def euler_super(sx, ex, h, y0, func, count=None, logs=True, eps=None):
    log_print("i\tXi\t\tYi\t\t\tF(Xi,Yi)\tYi+1\t\tF(Xi+1,Yi+1)", logs)
    res = [[], []]
    xi, yi = sx, y0
    i = 0
    while xi < ex:
        if count and i == count:
            break
        if i > 2_000_000:
            print("Не сошлося")
            break
        xi += h
        f = func(xi, yi)
        yi_1 = yi + h * f
        f_1 = func(sx+(i+1)*h, yi_1)
        y_loc = yi + h/2 * (f + f_1)
        if eps and i > 0 and xi < ex:
            srav = euler_super(xi-h/2, ex, h/2, yi, func, 2, False)[1][-1]
            r = abs(y_loc - srav)/(2**2 - 1)
            if r > eps:
                xi -= h
                h /= 4
                log_print(f"Вот так вот, но это супер эйлер", logs)
                continue
        log_print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{f:.3f}\t\t{yi_1:.3f}\t\t{f_1:.3f}", logs)
        res[0].append(xi)
        res[1].append(yi)
        yi = y_loc
        i += 1
    return res


def adams(sx, ex, h, y0, func, logs=True):
    tochnost = 4
    count = int((ex - sx)/h+1)
    res = euler_super(sx, ex, h, y0, func, tochnost, logs)
    if count > tochnost:
        fu = [func(sx+h*i, res[1][i]) for i in range(tochnost-1, -1, -1)]
        yi = res[1][-1]
        for i in range(tochnost, int((ex - sx)/h+1)):
            table = get_table(fu)
            # print(*table, sep="\n")
            # print(fu)
            xi = sx+i*h
            yi = yi + h*table[0][0] + h**2/2*table[1][0] + 5*h**3/12*table[2][0] + 3*h**4/8*table[3][0]
            fu.insert(0, func(xi, yi))
            fu.pop(-1)
            res[0].append(xi)
            res[1].append(yi)
            log_print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{fu[0]:.3f}", logs)
    return res


# sx, ex, h = 100, 105, 0.1
# sx, ex, h = 1, 100, 1
sx, ex, h = 0, 12.5, 0.1
# sx, ex, h = 8, 12, 0.1
y0 = 11
# func = lambda x, y: y + (1 + x) * y**0.3
# func = lambda x, y: y**2 / x
# func = lambda x, y: (x + y)/3 * x/y
# func = lambda x, y: y + (1+x)*y**2
func = lambda x, y: x**2 - 2*y
# func = lambda x, y: cos(x)/cos(y)
draw_graph(*euler_simple(sx, ex, h, y0, func, eps=0.1, logs=True), "Простой Эйлер")
print("-"*100)
draw_graph(*euler_super(sx, ex, h, y0, func, eps=0.1), "Супер Эйлер")
print("-"*100)
draw_graph(*adams(sx, ex, h, y0, func), "Адамс")
