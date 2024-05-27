def euler_simple(sx, ex, h, y0, func):
    print("i\tXi\t\tYi\t\t\tF(Xi,Yi)")
    xi, yi = sx, y0
    for i in range(int((ex - sx)/h+1)):
        xi = sx+i*h
        f = func(xi, yi)
        print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{f:.3f}")
        yi = yi + h * f


def euler_super(sx, ex, h, y0, func):
    print("i\tXi\t\tYi\t\t\tF(Xi,Yi)\tYi+1\t\tF(Xi+1,Yi+1)")
    xi, yi = sx, y0
    for i in range(int((ex - sx)/h+1)):
        xi = sx+i*h
        f = func(xi, yi)
        yi_1 = yi + h * f
        f_1 = func(sx+(i+1)*h, yi_1)
        print(f"{i}\t{xi:.3f}\t{yi:.3f}\t\t{f:.3f}\t\t{yi_1:.3f}\t\t{f_1:.3f}")
        yi = yi + h/2 * (f + f_1)


def adams(sx, ex, h, y0, func):
    pass


# sx, ex, h = 1, 2, 0.1
# sx, ex, h = 1, 10, 1
sx, ex, h = 1, 1.5, 0.1
y0 = -1
# func = lambda x, y: y + (1 + x) * y**2
# func = lambda x, y: y**2 / x
# func = lambda x, y: (x + y)/3 * x/y
func = lambda x, y: y + (1+x)*y**2
euler_simple(sx, ex, h, y0, func)
# euler_super(sx, ex, h, y0, func)
