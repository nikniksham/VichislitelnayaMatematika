import matplotlib.pyplot as plt


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


def euler_simple(sx, ex, h, y0, func, logs=True):
    print("i\tXi\t\tYi\t\t\tF(Xi,Yi)")
    res = [[], []]
    xi, yi = sx, y0
    for i in range(int((ex - sx)/h+1)):
        xi = sx+i*h
        f = func(xi, yi)
        print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{f:.3f}")
        res[0].append(xi)
        res[1].append(yi)
        yi = yi + h * f
    return res


def euler_super(sx, ex, h, y0, func, count=None, logs=True):
    print("i\tXi\t\tYi\t\t\tF(Xi,Yi)\tYi+1\t\tF(Xi+1,Yi+1)")
    res = [[], []]
    xi, yi = sx, y0
    for i in range(min(int((ex - sx)/h+1), count if count else 9999999)):
        xi = sx+i*h
        f = func(xi, yi)
        yi_1 = yi + h * f
        f_1 = func(sx+(i+1)*h, yi_1)
        print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{f:.3f}\t\t{yi_1:.3f}\t\t{f_1:.3f}")
        res[0].append(xi)
        res[1].append(yi)
        yi = yi + h/2 * (f + f_1)
    return res


def adams(sx, ex, h, y0, func, logs=True):
    tochnost = 4
    count = int((ex - sx)/h+1)
    res = euler_super(sx, ex, h, y0, func, tochnost)
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
            print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{fu[0]:.3f}")
    return res



# sx, ex, h = 100, 105, 0.1
# sx, ex, h = 1, 10, 1
# sx, ex, h = 1, 1.5, 0.1
sx, ex, h = 0, 1, 0.1
y0 = 1
# func = lambda x, y: y + (1 + x) * y**2
# func = lambda x, y: y**2 / x
# func = lambda x, y: (x + y)/3 * x/y
# func = lambda x, y: y + (1+x)*y**2
func = lambda x, y: x**2 - 2*y
draw_graph(*euler_simple(sx, ex, h, y0, func), "Простой Эйлер")
print("-"*100)
draw_graph(*euler_super(sx, ex, h, y0, func), "Супер Эйлер")
print("-"*100)
draw_graph(*adams(sx, ex, h, y0, func), "Адамс")
