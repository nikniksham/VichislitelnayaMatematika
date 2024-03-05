import copy


def find_opredelitel(matr):
    if len(matr) == 2:
        return matr[0][0] * matr[1][1] - matr[0][1] * matr[1][0]
    opr = 0
    for i in range(len(matr)):
        new_matr = []
        for y in range(1, len(matr)):
            row = []
            for x in range(len(matr)):
                if x != i:
                    row.append(matr[y][x])
            new_matr.append(row)
        opr += find_opredelitel(new_matr) * matr[0][i] * (1 if i % 2 == 0 else -1)
    return opr


def sub_row_from_row_with_coef(row_vich: list, row_umen: list, koef):
    return [row_umen[i] - row_vich[i]*koef for i in range(len(row_vich))]


def norm_row(row: list, a):
    return [el/a for el in row] if a != 0 else [0, 0, 0]


def solve_matrix(matr_orig: list, resh):
    otveti = [0 for i in range(len(resh))]

    matr = copy.deepcopy(matr_orig)
    for i in range(len(resh)):
        matr[i].append(resh[i])

    for y in range(len(matr[0])-1):
        max_ind, max_el = 0, None
        for x in range(y, len(matr)):
            if not max_el or matr[x][y] > max_el:
                max_el, max_ind = matr[x][y], x
        matr[y], matr[max_ind] = matr[max_ind], matr[y]
        matr[y] = norm_row(matr[y], matr[y][y])
        for i in range(y+1, len(matr[0])-1):
            matr[i] = sub_row_from_row_with_coef(matr[y], matr[i], matr[i][y]/matr[y][y] if matr[y][y] != 0 else 0)

    # print(*matr, sep="\n")
    for i in range(len(matr)-1, -1, -1):
        otveti[i] = matr[i][-1]
        # print(f"---- i = {i} ----")
        for j in range(len(matr)-1, i, -1):
            # print(i, j, matr[i][j], otveti[j])
            otveti[i] -= matr[i][j] * otveti[j]
        # print(otveti)

    # proverka
    for i in range(len(matr_orig)):
        su = 0
        for j in range(len(matr_orig[i])):
            su += matr_orig[i][j]*otveti[j]
        print(round(su, 8))
    return otveti


matr = []
resh = []
with open("test/matr5.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        line = list(map(float, line.split()))
        matr.append(line[:-1])
        resh.append(line[-1])
    # print(matr, resh)
print(solve_matrix(matr, resh))
