from typing import Callable

def rk4(f: Callable[[float, float], float], t0: float, y0: float, h: float, n: int) -> float:
    y = y0
    t = t0

    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0
    
    for _ in range(n):
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        y = y + (k1 + 2*k2 + 2*k3 + k4)/6
        t = t + h

    return y

def rk4_full(f: Callable[[float, float], float], t0: float, y0: float, h: float, n: int) \
    -> tuple[list[float], list[float], list[(float | None)], list[(float | None)], list[(float | None)], list[(float | None)]]:

    y = y0
    t = t0

    k1 = 0
    k2 = 0
    k3 = 0
    k4 = 0

    l_t = []
    l_y = []
    l_k1 = []
    l_k2 = []
    l_k3 = []
    l_k4 = []
    
    for i in range(n + 1):
        if i < n:
            k1 = h * f(t, y)
            k2 = h * f(t + h/2, y + k1/2)
            k3 = h * f(t + h/2, y + k2/2)
            k4 = h * f(t + h, y + k3)
        else:
            k1 = k2 = k3 = k4 = None

        l_t.append(t)
        l_y.append(y)
        l_k1.append(k1)
        l_k2.append(k2)
        l_k3.append(k3)
        l_k4.append(k4)

        if k1 is not None:
            y = y + (k1 + 2*k2 + 2*k3 + k4)/6
        
        t = t + h

    return y, l_t, l_y, l_k1, l_k2, l_k3, l_k4

def rk4_print_table(y, l_t, l_y, l_k1, l_k2, l_k3, l_k4):
    print(f"{'i':<4} | {'t':<8} | {'y':<10} | {'k1':<10} | {'k2':<10} | {'k3':<10} | {'k4':<10}")
    print("-" * 75)
    for i in range(len(l_t)):
        i_val = f"{i:<4}"
        t_val = f"{l_t[i]:.6f}"
        y_val = f"{l_y[i]:.6f}"
        k1_val = f"{l_k1[i]:.6f}" if l_k1[i] is not None else "None"
        k2_val = f"{l_k2[i]:.6f}" if l_k2[i] is not None else "None"
        k3_val = f"{l_k3[i]:.6f}" if l_k3[i] is not None else "None"
        k4_val = f"{l_k4[i]:.6f}" if l_k4[i] is not None else "None"
        print(f"{i_val:<4} | {t_val:<8} | {y_val:<10} | {k1_val:<10} | {k2_val:<10} | {k3_val:<10} | {k4_val:<10}")

if __name__ == "__main__":
    #################
    # Usage example #
    #################

    import math

    # Differential equation: y' = y * sin^3(t)
    # Initial conditions: y(0) = 1
    # Interval: [0, 3]
    # Step size: 0.5

    f = lambda t, y: y * math.sin(t)**3
    t0 = 0
    y0 = 1
    h = 0.5
    n = int((3 - t0) / h)

    # y0 = 1
    # y1 = 1.0143100585964484
    # y2 = 1.195522844012162
    # y3 = 1.8141324164206203
    # y4 = 2.881306926997134
    # y5 = 3.6536819063557124
    # y6 = 3.789845254718446
    for i in range(n + 1):
        print(f'y{i} = {rk4(f, t0, y0, h, i)}')

    print()

    # i    | t        | y          | k1         | k2         | k3         | k4        
    # ---------------------------------------------------------------------------
    # 0    | 0.000000 | 1.000000   | 0.000000   | 0.007572   | 0.007600   | 0.055516  
    # 1    | 0.500000 | 1.014310   | 0.055886   | 0.165046   | 0.173689   | 0.353919  
    # 2    | 1.000000 | 1.195523   | 0.356160   | 0.586960   | 0.636272   | 0.909032  
    # 3    | 1.500000 | 1.814132   | 0.900267   | 1.078609   | 1.121087   | 1.103388  
    # 4    | 2.000000 | 2.881307   | 1.083122   | 0.806161   | 0.773545   | 0.391716
    # 5    | 2.500000 | 3.653682   | 0.391591   | 0.107005   | 0.103050   | 0.005279
    # 6    | 3.000000 | 3.789845   | None       | None       | None       | None
    rk4_print_table(*rk4_full(f, t0, y0, h, n))
