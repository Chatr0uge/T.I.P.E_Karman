import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import seaborn as sns
import matplotlib.cm as cm
method = ['RK45', 'RK23', 'DOP853', 'Radau', 'BDF', 'LSODA']
B = 0.2
n = np.linspace(0, 7, 500)
tol = 10**(-6)

sns.set_context("paper")


def equations(n, f):
    fp = np.zeros(3)
    fp[0] = f[1]
    fp[1] = f[2]
    fp[2] = -f[0]*f[2]-B*(1-f[1]**2)
    return fp


def solve_FS(B):
    n = np.linspace(0, 7, 500)
    f0 = [0, 0, 0.04]
    sol = solve_ivp(equations, (n[0], n[-1]), f0, t_eval=n)
    a = 0
    b = 7
    i = 0
    while abs(sol.y[1][-1]-1) > tol:  # NOTE:"Shooting method"  On procède pardichotomie
        i = i+1
        if sol.y[1][-1]-1 > 0:
            b = f0[2]
        if sol.y[1][-1]-1 < 0:
            a = f0[2]
        f0[2] = (a+b)/2
        sol = solve_ivp(equations, (n[0], n[-1]), f0, t_eval=n)
    return (sol, i)


fig, ax = plt.subplots()
pal1 = sns.color_palette("hls", 6)
L = [-.04, -.12, -.19884, -.16, 0, .5]
L.sort()

plt.subplot(1, 1, 1)
for B in L:
    c = cm.coolwarm((L.index(B)+1)/8., 1)
    solve = solve_FS(B)
    sol = solve[0]
    i = solve[1]
    f = sol.y[0]
    fp = sol.y[1]
    plt.plot(fp, n, linewidth=1, color=c,
             label='$B={B}$'.format(B=B))
    plt.legend(loc='best')
    print(i)
ax.set_xlim(-0.2, 1.1)
plt.show()
