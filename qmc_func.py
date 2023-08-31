def ToBase(b, n): 
    ls = []
    while n != 0 : 
        ls.append(n % b) 
        n = n // b
    return ls

def brifunc(b, n):
    fval = 0    
    for ind, val in enumerate(ToBase(b, n)):
        fval += val / (b ** (ind + 1))
    return fval

def vdc_seq(b, n):
    return [brifunc(b, x) for x in range(n)]

def Halton_seq(bases, n):
    """
    Input: bases (iterable) and n is the number of points to generate
    Output: Return an array of Halton sequence (each row is a point in Halton sequence)
    """
    import numpy as np 

    ls = []
    for x in bases:
        ls.append(vdc_seq(x, n))
    
    ls = np.array(ls).T
    return ls 

def BM(vis = True,*, time, steps, samples):
    import numpy as np
    import matplotlib.pyplot as plt
    n = steps+1
    T = time 
    d = samples 
    times = np.linspace(0, T, n)
    dB = np.sqrt(times[1]) * np.random.normal(size = (n-1, d)) # n-1 rows because B0 is 0, so we exclude that 
    B0 = np.zeros(shape = (1,d)) 
    Bt = np.concatenate((B0, np.cumsum(dB, axis = 0)), axis = 0)
    if vis:
        plt.plot(times, Bt)
        plt.show()
        return times, Bt
    else:
        return times, Bt
    
def GBM(vis = True, *, S0, time, steps, samples, vol, rfr):
    import numpy as np 
    import matplotlib.pyplot as plt
    times, Bt = BM(vis = False, time = time, steps = steps, samples = samples)
    times_d = np.tile(times, (samples,1)).T 
    St = S0 * np.exp((rfr - vol**2 /2)* times_d + vol * Bt)
    if vis:
        plt.plot(times, St)
        plt.show()
        return times, St
    else: 
        return times, St

def BS_option_call(*, maturity, S0, rfr, strike, time = 0, vol):
    import numpy as np 
    from scipy.stats import norm

    if time > strike:
        raise 'Time parameter is more than maturity parameter'
    
    d1 = (np.log(S0 / strike)  + (rfr + vol**2 /2) * (maturity - time)) / (vol * np.sqrt(maturity - time))
    d2 = (np.log(S0 / strike)  + (rfr - vol**2 /2) * (maturity - time)) / (vol * np.sqrt(maturity - time))
    return S0 * norm.cdf(d1) - np.exp(- rfr * (maturity - time)) * strike * norm.cdf(d2)

def BB_Sobol(vis = True, *, time, samples, steps):
    from scipy.stats import qmc
    from scipy.stats import norm
    import numpy as np
    import matplotlib.pyplot as plt 

    if np.log2(samples) != int(np.log2(samples)) or np.log2(steps) != int(np.log2(steps)):
        raise 'Samples or steps are not a power of 2'
    
    T = time
    disc = steps 
    n_sims = samples 

    disc_log2 = round(np.log2(disc))
    n_sims_log2 = round(np.log2(n_sims))

    S = qmc.Sobol(d = disc , scramble = True)
    sobol = S.random_base2(n_sims_log2)
    invnorm_sobol = norm.ppf(sobol)
    Wt = np.empty([1, disc + 1]) # placeholder
    times = np.linspace(0, T, disc + 1) 

    for i in range(n_sims):
        sobol_ls = invnorm_sobol[i,:]
        WT = np.sqrt(T) * sobol_ls[0]
        ls = [(0,0), (T, WT)]
        n = 1 
        while n <= disc_log2 : 
            for i, j in enumerate(ls[:-1]):
                ls.append((0.5 * (j[0] + ls[i+1][0]), 0.5 * (j[1] + ls[i+1][1]) + np.sqrt(T / 2 ** (n + 1)) * sobol_ls[i+1]))

            n += 1
            ls = sorted(ls) 
        
        ls_arr = np.array(ls)
        Wt = np.vstack((Wt, ls_arr[:, 1]))
    
    Wt = Wt.T
    if vis:
        plt.plot(times, Wt)
        plt.xlabel('Time $T$')
        plt.ylabel('Brownian bridge paths')
        plt.title('{} Brownian bridge paths by Sobol\' Sequece'.format(samples))
        plt.show()
        return times, Wt
    else:
        return times, Wt

def GBB_Sobol(vis = True, *, S0, time, steps, samples, vol, rfr):
    import numpy as np 
    import matplotlib.pyplot as plt 
    
    times, Bt = BB_Sobol(vis = False, time = time, steps = steps, samples = samples)
    times_d = np.tile(times, (samples+1,1)).T 
    St = S0 * np.exp((rfr - vol**2 /2)* times_d + vol * Bt)
    if vis:
        plt.plot(times, St)
        plt.show()
        return times, St
    else: 
        return times, St
    
def prime(n):
    import math
    X = 0
    i = 2
    flag = False
    ls = []
    while(X < n):
        flag = True
        for j in range(2, math.floor(math.sqrt(i)) + 1):
            if (i%j == 0):
                flag = False
                break
        if(flag):
            ls.append(i)
            X+=1
        i+=1
    return ls

def BB_Halton(vis = True, *, time, samples, steps):
    from scipy.stats import norm
    import numpy as np
    import matplotlib.pyplot as plt 

    if np.log2(steps) != int(np.log2(steps)):
        raise 'Samples or steps are not a power of 2'
    
    T = time
    disc = steps  # discretisation steps
    n_sims = samples + 1 # number of simulations

    disc_log2 = round(np.log2(disc)) # log 2 discretisation steps 

    halton = Halton_seq(prime(disc), n_sims)
    invnorm_halton = norm.ppf(halton)
    Wt = np.zeros([1, disc + 1]) # placeholder
    times = np.linspace(0, T, disc + 1) 

    for i in range(n_sims):
        halton_ls = invnorm_halton[i,:]
        WT = np.sqrt(T) * halton_ls[0]
        ls = [(0,0), (T, WT)]
        n = 1 
        while n <= disc_log2 : 
            for i, j in enumerate(ls[:-1]):
                ls.append((0.5 * (j[0] + ls[i+1][0]), 0.5 * (j[1] + ls[i+1][1]) + np.sqrt(T / 2 ** (n + 1)) * halton_ls[i+1]))

            n += 1
            ls = sorted(ls) 
        
        ls_arr = np.array(ls)
        Wt = np.vstack((Wt, ls_arr[:, 1]))
    
    Wt = Wt.T[:, 2:] # to not include the placeholder
    if vis:
        plt.plot(times, Wt)
        plt.xlabel('Time $T$')
        plt.ylabel('Brownian bridge paths')
        plt.title('{} Brownian bridge paths by Halton Sequence'.format(samples))
        plt.show()
        return times, Wt
    else:
        return times, Wt

def GBB_Halton(vis = True, *, S0, time, steps, samples, vol, rfr):
    import numpy as np 
    import matplotlib.pyplot as plt
    
    times, Bt = BB_Halton(vis = False, time = time, steps = steps, samples = samples)
    times_d = np.tile(times, (samples,1)).T 
    St = S0 * np.exp((rfr - vol**2 /2)* times_d + vol * Bt)
    if vis:
        plt.plot(times, St)
        plt.xlabel('Time $T$')
        plt.ylabel('Stock price $S_T$')
        plt.title('{} Brownian bridge simulations by Halton sequence'.format(samples))
        plt.show()
        return times, St
    else: 
        return times, St
