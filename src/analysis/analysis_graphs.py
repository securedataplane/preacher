import numpy as np
import matplotlib.pyplot as plt
import math
from myplot import plot_lines

USE_DECIMAL = True # improved accuracy

if USE_DECIMAL:
    from decimal import Decimal, getcontext
    getcontext().prec = 100

# detection probability calculation functions


def inter(x,y):
    """ pairs between sets of sizes x and y """
	return x*y
    
def intra(x):
    """ internal pairs in set of size x """
	return (x*(x-1))/2
    
def explicit(k1, k2):
    """ explicit pair assignments between sets of sizes x and y """
	return inter(k1, k2)
    
def implicit(x, z): 
    """ implicit assignments (for attack location) involving a set of size x of one side and other z switches """
	return intra(x) + inter(x, z) 
    
def dp_pa3(p, n, k1, k2):
    """ detection probability for pair assignment """
    if USE_DECIMAL:
        p = Decimal(p)
        n = Decimal(n)
        k1 = Decimal(k2)
        k2 = Decimal(k2)
    q = p/(n-1)
    K12 = implicit(k1, n-k1-k2-1)
    K21 = implicit(k2, n-k1-k2-1)
    return float(1 - (1-q)**explicit(k1,k2)  * (1-(1- (1-q)**K12)*(1- (1-q)**K21)))


def dp_pa3_aprx(p, n, k1, k2):
    """ approximation for detection probability for pair assignment (assumes p << 1/n """
    if USE_DECIMAL:
        p = Decimal(p)
        n = Decimal(n)
        k1 = Decimal(k2)
        k2 = Decimal(k2)
    q = p/(n-1)
    K12 = implicit(k1, n-k1-k2-1)
    K21 = implicit(k2, n-k1-k2-1)
    return float(q*explicit(k1,k2)+ q*K12*q*K21 - q*explicit(k1,k2)*q*K12*q*K21)
    
def dp_ia(p, n, k1, k2):
    """ detection probability for independent assignment """
    if USE_DECIMAL:
        p = Decimal(p)
        n = Decimal(n)
        k1 = Decimal(k2)
        k2 = Decimal(k2)
    return float((1-(1-p)**k1)*(1-(1-p)**k2))
    
def dp_ia_aprx(p, n, k1, k2):
    """ approximation for detection probability for independent assignment (assumes p << 1/n """
    if USE_DECIMAL:
        p = Decimal(p)
        n = Decimal(n)
        k1 = Decimal(k2)
        k2 = Decimal(k2)
    return float(p*k1*p*k2)

is_dp_independent = lambda dp: dp in [dp_ia, dp_ia_aprx]

# constants 
Gb = 10**9 * 8
B = 8
pkt_avg_size = 400 * B # facebook
#detect_capacity_unit = 1000

# datacenter switch loads calculation functions
def ToR_out(tors):
    return tors * 8 * Gb
def DC_out(tors):
    return ToR_out(tors)* 0.2
def DC_in(tors):
    return ToR_out(tors)* 0.14
def DC_load(tors):
    """ Core switches (sampled) load """
    return DC_in(tors) + DC_out(tors) * 2
def Agg_in(tors):
    return ToR_out(tors)* 0.66
def Agg_load(tors):
    """ Agg switches (sampled) load """
    return Agg_in(tors) + DC_in(tors) * 2 + DC_out(tors) * 2
def ToR_load(tors):
    """ ToR switches (sampled) load """
    return ToR_out(tors)*2
def total_load(tors):
    """ total network (sampled) load """
    return ToR_load(tors) + Agg_load(tors) + DC_load(tors)


dp = dp_ia
is_independent = is_dp_independent(dp)


# graphs plotting functions

def tests0():
    """ show load vs. time graphs for a single assignment strategy for different locations """
    global is_independent
    is_independent = is_dp_independent(dp)
    TORS = [20, 50, 75, 100]
    xs = []
    ys = []
    Ns = []
    Hs = []
    for tors in TORS:
        aggs = math.ceil(tors * 0.1)  # tors * 2  / 24
        cores = math.ceil(tors * 0.05)  # aggs * 2  / 10 ?
        n = tors + aggs + cores
        Ns.append(n)
        Hs.append(tors * 20)
        loads = []
        times = []
        for p in np.arange(0, 0.001, 0.0000001):
            samples = total_load(tors) * p / pkt_avg_size
            loads.append(samples)
            prob = dp(p, n, 2, 2)  # attacker at core
            # attacked_load = DC_in(tors) / (tors*20)**2 # assuming uniform between hosts
            attacked_load = DC_in(tors) / (20 ** 2 * tors * (aggs - 1) / aggs)  # assuming uniform between hosts
            attacked_pkts = attacked_load / pkt_avg_size
            detect_pkts = 1 / prob
            detect_time = detect_pkts / attacked_pkts
            times.append(detect_time)
        plt.plot(loads, times)
        xs.append(loads)
        ys.append(times)
    # plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Samples rate (pps)')
    plt.ylabel('Expected detection time (s)')
    plt.show()
    y_names = ["%dT" % i for i in TORS]
    plot_lines(xs, ys, name="bad_core_in" + "_IA" * is_independent,
               xlabel='Samples rate (pps)', ylabel='Expected detection time (s)', y_names=y_names,
               xscale="log", ylim=[0, 600 * (1 + 9 * is_independent)], xlim=[0, 10 ** (5 + 1 * is_independent)],
               legend_loc="lower left")

    xs = []
    ys = []
    Ns = []
    Hs = []
    for tors in TORS:
        aggs = math.ceil(tors * 0.1)  # tors * 2  / 24
        cores = math.ceil(tors * 0.05)  # aggs * 2  / 10 ?
        n = tors + aggs + cores
        Ns.append(n)
        Hs.append(tors * 20)
        loads = []
        times = []
        for p in np.arange(0, 0.001, 0.0000001):
            samples = total_load(tors) * p / pkt_avg_size
            loads.append(samples)
            prob = dp(p, n, 1, 2)  # attacker at agg to out
            attacked_load = DC_out(tors) * 2 / (tors * 20)  # assuming uniform between hosts
            attacked_pkts = attacked_load / pkt_avg_size
            detect_pkts = 1 / prob
            detect_time = detect_pkts / attacked_pkts
            times.append(detect_time)
        plt.plot(loads, times)
        xs.append(loads)
        ys.append(times)
    # plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Samples rate (pps)')
    plt.ylabel('Expected detection time (s)')
    plt.show()
    y_names = ["%dT" % i for i in TORS]
    plot_lines(xs, ys, name="bad_agg_out" + "_IA" * is_independent,
               xlabel='Samples rate (pps)', ylabel='Expected detection time (s)', y_names=y_names,
               xscale="log", ylim=[0, 600 * (1 + 9 * is_independent)], xlim=[0, 10 ** (5 + 1 * is_independent)])

    xs = []
    ys = []
    Ns = []
    Hs = []
    for tors in TORS:
        aggs = math.ceil(tors * 0.1)  # tors * 2  / 24
        cores = math.ceil(tors * 0.05)  # aggs * 2  / 10 ?
        n = tors + aggs + cores
        Ns.append(n)
        Hs.append(tors * 20)
        loads = []
        times = []
        for p in np.arange(0, 0.001, 0.0000001):
            samples = total_load(tors) * p / pkt_avg_size
            loads.append(samples)
            prob = dp(p, n, 1, 1)  # attacker at agg to in
            attacked_load = (ToR_out(tors) - DC_out(tors)) / (
                        20 ** 2 * tors * tors / aggs - tors * 20 ** 2)  # assuming uniform between hosts
            attacked_pkts = attacked_load / pkt_avg_size
            detect_pkts = 1 / prob
            detect_time = detect_pkts / attacked_pkts
            times.append(detect_time)
        plt.plot(loads, times)
        xs.append(loads)
        ys.append(times)
    # plt.yscale('log')
    plt.xscale('log')
    plt.xlabel('Samples rate (pps)')
    plt.ylabel('Expected detection time (s)')
    plt.show()
    y_names = ["%dT" % i for i in TORS]
    plot_lines(xs, ys, name="bad_agg_in" + "_IA" * is_independent,
               xlabel='Samples rate (pps)', ylabel='Expected detection time (s)', y_names=y_names,
               xscale="log", ylim=[0, 3600 * (1 + 9 * is_independent)], xlim=[0, 2 * 10 ** (5 + 1 * is_independent)],
               legend_loc="lower left")


def test(k1, k2, atk_load_func, name, y_max, x_max, legend_loc):
    """ show load vs. time graph for a single assignment strategy for specific locations"""
    TORS = [20, 50, 75, 100]
    xs = []
    ys = []
    Ns = []
    Hs = []
    for tors in TORS:
        aggs = math.ceil(tors * 0.1) # tors * 2  / 24
        cores = math.ceil(tors * 0.05) # aggs * 2  / 10 ?
        n = tors + aggs + cores
        Ns.append(n)
        Hs.append(tors*20)
        loads = []
        times = []
        for p in np.arange(0, 0.001, 0.0000001):
            samples = total_load(tors) * p / pkt_avg_size
            loads.append(samples)
            prob = dp(p, n, k1, k2)
            attacked_load = atk_load_func(tors, aggs) # assuming uniform between hosts
            attacked_pkts = attacked_load / pkt_avg_size
            detect_pkts = 1/prob
            detect_time = detect_pkts/attacked_pkts
            times.append(detect_time)
        #plt.plot(loads, times)
        xs.append(loads)
        ys.append(times)
    ##plt.yscale('log')
    #plt.xscale('log')
    #plt.xlabel('Samples rate (pps)')
    #plt.ylabel('Expected detection time (s)')
    #plt.show()
    y_names = ["%dT"%i for i in TORS]
    plot_lines(xs, ys, name=name,
        xlabel='Samples rate (pps)', ylabel='Expected detection time (s)', y_names=y_names,
        xscale="log", ylim=[0,y_max], xlim=[0, x_max], legend_loc=legend_loc)


def tests():
    """ show load vs. time graphs for a single assignment strategy for different locations (revision of tests0) """
    global is_independent
    is_independent = is_dp_independent(dp)
    test(k1=2, k2=2,
         atk_load_func=lambda tors,aggs: DC_in(tors) / (20**2*tors*(aggs-1)/aggs),
         name="bad_core_in"+"_IA"*is_independent,
         y_max=600*(1+9*is_independent),
         x_max=10**(5+1*is_independent),
         legend_loc="lower left")
    test(k1=1, k2=2,
         atk_load_func=lambda tors,aggs: DC_out(tors) * 2 / (tors * 20),
         name="bad_agg_out" + "_IA" * is_independent,
         y_max=600*(1+9*is_independent),
         x_max=10**(5+1*is_independent),
         legend_loc="upper right")
    test(k1=1, k2=1,
         atk_load_func=lambda tors, aggs: (ToR_out(tors) - DC_out(tors)) / (20**2 * tors * tors / aggs - tors * 20**2),
         name="bad_agg_in" + "_IA" * is_independent,
         y_max=3600 * (1 + 9 * is_independent),
         x_max=2 * 10 ** (5 + 1 * is_independent),
         legend_loc="lower left")


def test_cmp(k1, k2, atk_load_func, name, y_max, x_max):
    """ compare load vs. time for two assignment strategies """
    TORS = [20, 100]
    xs = []
    ys = []
    Ns = []
    Hs = []
    for dp in [dp_pa3, dp_ia]:
        for tors in TORS:
            aggs = math.ceil(tors * 0.1) # tors * 2  / 24
            cores = math.ceil(tors * 0.05) # aggs * 2  / 10 ?
            n = tors + aggs + cores
            Ns.append(n)
            Hs.append(tors*20)
            loads = []
            times = []
            for p in np.arange(0, 0.001, 0.0000001):
                samples = total_load(tors) * p / pkt_avg_size
                loads.append(samples)
                prob = dp(p, n, k1, k2)
                attacked_load = atk_load_func(tors, aggs) # assuming uniform between hosts
                attacked_pkts = attacked_load / pkt_avg_size
                detect_pkts = 1/prob
                detect_time = detect_pkts/attacked_pkts
                times.append(detect_time)
            #plt.plot(loads, times)
            xs.append(loads)
            ys.append(times)
    ##plt.yscale('log')
    #plt.xscale('log')
    #plt.xlabel('Samples rate (pps)')
    #plt.ylabel('Expected detection time (s)')
    #plt.show()
    y_names = ["PA\\_%dT"%i for i in TORS] + ["IA\\_%dT"%i for i in TORS]
    plot_lines(xs, ys, name=name,
        xlabel='Samples rate (pps)', ylabel='Expected detection time (s)', y_names=y_names, #yscale="log",
        xscale="log",
               ylim=[0,y_max], xlim=[0, x_max],
               legend_loc='upper left', bbox_to_anchor=(1.05, 1))

def sanity(k1, k2, name="sanity", n=None, tors=100):
    """ test approximations and inequalities """
    if n is None:
        aggs = math.ceil(tors * 0.1) # tors * 2  / 24
        cores = math.ceil(tors * 0.05) # aggs * 2  / 10 ?
        n = tors + aggs + cores
    xs = []
    ys = []
    ps = [0.5**i for i in range(30)]
    #ps = np.arange(0, 0.01, 0.0000001)[:100]
    for dp in [dp_pa3, dp_ia, dp_pa3_aprx, dp_ia_aprx]:
        dps = []
        for p in ps:
            prob = dp(p, n, k1, k2)
            dps.append(prob)
        #plt.plot(loads, times)
        xs.append(list(ps))
        ys.append(dps)
    #print xs
    #print ys[0]
    #print ys[1]
    
    a = [0, 1, 2]
    res = [(ps[i], float(ys[a[0]][i] - ys[a[1]][i]), float(ys[a[0]][i] - ys[a[2]][i])) for i in range(len(ys[0]))]
    for r in res:
        print r[0], r[1], r[2]
    if 1:
        y_names = ["PA","IA"] + ["PA-X","IA-X"]
        plot_lines(xs, ys, name=name,
            xlabel='Probability', ylabel='Expected detection time (s)', y_names=y_names, yscale="log",
            xscale="log",
                   #ylim=[0,y_max], xlim=[0, x_max],
                   legend_loc='upper left', bbox_to_anchor=(1.05, 1))

def test_cmp2(k1, k2, name):
    """ compare sampling vs. detection probabilities for two assignment strategies """
    TORS = [20, 100]
    xs = []
    ys = []
    for dp in [dp_pa3, dp_ia]:
        for tors in TORS:
            aggs = math.ceil(tors * 0.1) # tors * 2  / 24
            cores = math.ceil(tors * 0.05) # aggs * 2  / 10 ?
            n = tors + aggs + cores
            dps = []
            ps = np.arange(0, 0.01, 0.0000001)
            for p in ps:
                prob = dp(p, n, k1, k2)
                dps.append(prob)
            #plt.plot(loads, times)
            xs.append(list(ps))
            ys.append(dps)
    ##plt.yscale('log')
    #plt.xscale('log')
    #plt.xlabel('Samples rate (pps)')
    #plt.ylabel('Expected detection time (s)')
    #plt.show()
    y_names = ["PA\\_%dT"%i for i in TORS] + ["IA\\_%dT"%i for i in TORS]
    plot_lines(xs, ys, name=name,
        xlabel='Sample probability', ylabel='Detection probability', y_names=y_names, #yscale="log",
        #xscale="log",
               legend_loc='upper left', bbox_to_anchor=(1.05, 1))

if __name__ == "__main__":
    USE_DECIMAL = False
    dp = dp_ia
    #tests0()
    tests()
    dp = dp_pa3
    #tests0()
    tests()
    
    test_cmp(k1=2, k2=2,
         atk_load_func=lambda tors,aggs: DC_in(tors) / (20**2*tors*(aggs-1)/aggs),
         name="bad_core_in_CMP",
         y_max=3600,
         x_max=10**6)
    
    #test_cmp2(k1=2, k2=2,
    #     name="bad_core_in_Prob_CMP")
    
    USE_DECIMAL = True    
    sanity(k1=3, k2=3)
