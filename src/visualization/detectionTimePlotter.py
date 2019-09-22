#!/usr/bin/env python
#Author: Kashyap Thimmaraju
#Email: kashyap.thimmaraju@sect.tu-berlin.de
#This script is intended to parse and plot the
#detection time results from the Preacher experiments.
import json
import pprint
import matplotlib.pyplot as plt
import numpy as np

# data variables
dataPath = "/../../evaluation/data/detectionTime/"
## the randomPairAssignment path contains data and results
## for random pair assignment but not purely independent.
## Henceforth, use the pureIndependentAssignment path.
dataFile = "baselineAggDropDetectionTime.json"
# pureIndependentPairAssignmentDontAttackSamples
baselineAggDrop = "pureIndependentPairAssignmentDontAttackSamples/baselineAggDropDetectionTime.json"
baselineAggInject = "pureIndependentPairAssignmentDontAttackSamples/baselineAggInjectDetectionTime.json"
baselineCoreDrop = "pureIndependentPairAssignmentDontAttackSamples/baselineCoreDropDetectionTime.json"
baselineCoreInject = "pureIndependentPairAssignmentDontAttackSamples/baselineCoreInjectDetectionTime.json"
psamp2AggDrop = "pureIndependentPairAssignmentDontAttackSamples/psamp2AggDropDetectionTime.json"
psamp2AggInject = "pureIndependentPairAssignmentDontAttackSamples/psamp2AggInjectDetectionTime.json"
psamp2CoreDrop = "pureIndependentPairAssignmentDontAttackSamples/psamp2CoreDropDetectionTime.json"
psamp2CoreInject = "pureIndependentPairAssignmentDontAttackSamples/psamp2CoreInjectDetectionTime.json"
psamp3AggDrop = "pureIndependentPairAssignmentDontAttackSamples/psamp3AggDropDetectionTime.json"
psamp3AggInject = "pureIndependentPairAssignmentDontAttackSamples/psamp3AggInjectDetectionTime.json"
psamp3CoreDrop = "pureIndependentPairAssignmentDontAttackSamples/psamp3CoreDropDetectionTime.json"
psamp3CoreInject = "pureIndependentPairAssignmentDontAttackSamples/psamp3CoreInjectDetectionTime.json"
# collusionCase1PureIndependentPairAssignment
psamp1AggMirrorCollusionCase1 = "collusionCase1PureIndependentPairAssignment/baselineCollusion021221Case1DetectionTime.json"
psamp2AggMirrorCollusionCase1 = "collusionCase1PureIndependentPairAssignment/psamp2Collusion021221Case1DetectionTime.json"
psamp3AggMirrorCollusionCase1 = "collusionCase1PureIndependentPairAssignment/psamp3Collusion021221Case1DetectionTime.json"
psamp1AggCoreMirrorCollusionCase1 = "collusionCase1PureIndependentPairAssignment/baselineCollusion021411221Case1DetectionTime.json"
psamp2AggCoreMirrorCollusionCase1 = "collusionCase1PureIndependentPairAssignment/psamp2Collusion021411221Case1DetectionTime.json"
psamp3AggCoreMirrorCollusionCase1 = "collusionCase1PureIndependentPairAssignment/psamp3Collusion021411221Case1DetectionTime.json"

# formal analysis variables for plotting
baselineP_pa_agg = 1280.65634689
baselineP_pa_core = 960.562349528
psamp2P_pa_agg = 602.982884961
psamp2P_pa_core = 452.313557639
psamp3P_pa_agg = 379.867557017
psamp3P_pa_core = 284.982359148
# experimental variables
samplingRatios = ['0.0046', '0.0092', '0.0139']
hashFunctions = ['payload']
assignments = ['static', 'dynamic']
updateRates = ['2']
updateSizes = ['2']
attackPositions = ['aggregate', 'core']
colludingPositions = ['colludingSwitch1_of:0000000000000201_colludingSwitch2_of:0000000000020201','colludingSwitch1_of:0000000000000201-of:0000000000040101_colludingSwitch2_of:0000000000040101-of:0000000000020201']
attacks = ['drop', 'inject']
detectionResults = ["seeds", "timeStamp", "packetsSent"]
# results variables
resultsPath = "../../plots/"
# matplotlib variables
lineStyles = ['dotted', 'dotted', 'dotted', 'dashed', 'dashed']
# lineColours = ['#0000CD', '#097054', '#6599FF', '#5B7444']
lineColours = ['#405774', '#CD6607', '#6787B0', '#F6A03D'] #Blues for gcc, Oranges for clang
# lineStyles = ['', '', '', '', '']
# markerStyles = ['1', '2', '3', '4', 'D']
markerStyles = ['', '', '']
# markerStyles = ['D', 's', 'o', '^', 'D']
fontsize = 8
labels = [u'drop', u'inject']
figCounter = 1
figSubplot = 111

def getDetectionData(detectionDict, samplingRatio, hashFunction, assignment, attackPosition, attack, updateRate='2', updateSize='2'):
    print "getDetectionData(detectionDict, attackPosition)"
    detectionData = []
    if assignment == 'static':
        rawDetectionData = detectionDict[samplingRatio][hashFunction][assignment][attackPosition][attack]
    elif assignment == 'dynamic':
        rawDetectionData = detectionDict[samplingRatio][hashFunction][assignment][updateRate][updateSize][attackPosition][attack]
    for i in range(0, len(rawDetectionData)):
        # print rawDetectionData[i][2]
        if rawDetectionData[i][2] == None:
            continue
        detectionData.append(rawDetectionData[i][2])
    return detectionData

def getSeeds(detectionDict, samplingRatio, hashFunction, assignment, attackPosition, attack, updateRate='2', updateSize='2'):
    print "getSeeds()"
    seeds = []
    if assignment == 'static':
        print "Static"
        rawSeedData = detectionDict[samplingRatio][hashFunction][assignment][attackPosition][attack]
    elif assignment == 'dynamic':
        print 'dynamic'
        rawSeedData = detectionDict[samplingRatio][hashFunction][assignment][updateRate][updateSize][attackPosition][attack]
    for i in range(0, len(rawSeedData)):
        keys = rawSeedData[i][0].keys()
        seeds.append(int(keys[0]))
    seeds.sort()
    seeds = set(seeds)
    return seeds

def plotAttack(attack, aggStatic, aggDynamic, coreStatic, coreDynamic):
    print "plotAttack()"
    if attack == 'drop':
        fig = plt.figure(1, figsize=(8.75, 4.6), frameon=True)
        ax = plt.subplot(111)
    elif attack == 'inject':
        fig = plt.figure(2, figsize=(8.75, 4.6), frameon=True)
        ax = plt.subplot(111)
    data = [aggStatic]
    data.append(aggDynamic)
    data.append(coreStatic)
    data.append(coreDynamic)
    plt.boxplot(data)
    plt.ylabel('Packets till detection')
    plt.xlabel('Hash Assignment')
    c = 0
    ax.text(c+1, 11020.0, u'Aggregate Switch')
    ax.text(c+3, 11020.0, u'Core Switch')
    xmark = ['Static', 'Dynamic', 'Static', 'Dynamic']
    plt.xticks(range(1, 5), tuple(xmark))
    box = ax.get_position()
    ax.set_yscale('log')
    ax.set_position([box.x0, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey',alpha=.5)
    ax.set_axisbelow(True)
    fileName = attack + resultsFile
    plt.savefig(resultsPath + fileName, dpi=(2500))

def plotAttacks(aggStaticDrop, aggDynamicDrop, coreStaticDrop, coreDynamicDrop,
                aggStaticInject, aggDynamicInject, coreStaticInject, coreDynamicInject,
                resultsFile='combined'):
    print "plotAttacks()"
    fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    data = [aggStaticDrop, aggStaticInject, aggDynamicDrop, aggDynamicInject,
            coreStaticDrop, coreStaticInject, coreDynamicDrop, coreDynamicInject]
    plt.boxplot(data)
    plt.ylabel('Packet sent till detection.')
    plt.xlabel('Assignment')
    c = 0
    ax.text(c+2, 11020.0, u'Aggregate Switch')
    ax.text(c+6, 11020.0, u'Core Switch')
    plt.plot([4.5, 4.5], [-1, 10000], color='#000000')
    xmark = ['Drop\n                Static', 'Inject', 'Drop\n                Dynamic', 'Inject',
             'Drop\n                Static', 'Inject', 'Drop\n                Dynamic', 'Inject']
    plt.xticks(range(1, 10), tuple(xmark))
    box = ax.get_position()
    ax.set_yscale('log')
    ax.set_position([box.x0, box.y0 + box.height * 0.15 , box.width * 1.0, box.height * 0.85])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey',alpha=.5)
    ax.set_axisbelow(True)
    # fileName = "combined100AggInjectAlso" + resultsFile
    # plt.show()
    plt.savefig(resultsPath + resultsFile, dpi=(2500))

def baseline():
    print "baseline()"
    print "Baseline"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggDrop).read()))
    baseAggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    baseAggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggInject).read()))
    baseAggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    baseAggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreDrop).read()))
    baseCoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    baseCoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreInject).read()))
    baseCoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    baseCoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "baseAggDropStatic:" + str(len(baseAggDropStatic))
    print "baseAggDropDynamic:" + str(len(baseAggDropDynamic))
    print "baseAggInjectStatic:" + str(len(baseAggInjectStatic))
    print "baseAggInjectDynamic:" + str(len(baseAggInjectDynamic))
    print "baseCoreDropStatic:" + str(len(baseCoreDropStatic))
    print "baseCoreDropDynamic:" + str(len(baseCoreDropDynamic))
    print "baseCoreInjectStatic:" + str(len(baseCoreInjectStatic))
    print "baseCoreInjectDynamic:" + str(len(baseCoreInjectDynamic))
    print "Now plot the results."
    resultsFile = "randomPairAssignment/baselineDetectionTime.pdf"
    plotAttacks(baseAggDropStatic, baseAggDropDynamic, baseCoreDropStatic, baseCoreDropDynamic,
                baseAggInjectStatic, baseAggInjectDynamic, baseCoreInjectStatic, baseCoreInjectDynamic,
                resultsFile)

def psamp2():
    print "psamp2()"
    print "samplingRate=0.0092"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggDrop).read()))
    psamp2AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp2AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggInject).read()))
    psamp2AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp2AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreDrop).read()))
    psamp2CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp2CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreInject).read()))
    psamp2CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp2CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp2AggDropStatic:" + str(len(psamp2AggDropStatic))
    print "psamp2AggDropDynamic:" + str(len(psamp2AggDropDynamic))
    print "psamp2AggInjectStatic:" + str(len(psamp2AggInjectStatic))
    print "psamp2AggInjectDynamic:" + str(len(psamp2AggInjectDynamic))
    print "psamp2CoreDropStatic:" + str(len(psamp2CoreDropStatic))
    print "psamp2CoreDropDynamic:" + str(len(psamp2CoreDropDynamic))
    print "psamp2CoreInjectStatic:" + str(len(psamp2CoreInjectStatic))
    print "psamp2CoreInjectDynamic:" + str(len(psamp2CoreInjectDynamic))
    print "Now plot the results."
    resultsFile = "randomPairAssignment/psamp2DetectionTime.pdf"
    plotAttacks(psamp2AggDropStatic, psamp2AggDropDynamic, psamp2CoreDropStatic, psamp2CoreDropDynamic,
                psamp2AggInjectStatic, psamp2CoreInjectStatic, psamp2AggInjectDynamic, psamp2CoreInjectDynamic,
                resultsFile)

def psamp3():
    print "psamp3()"
    print "samplingRate=0.0139"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggDrop).read()))
    psamp3AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp3AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggInject).read()))
    psamp3AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp3AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreDrop).read()))
    psamp3CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp3CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreInject).read()))
    psamp3CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp3CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp3AggDropStatic:" + str(len(psamp3AggDropStatic))
    print "psamp3AggDropDynamic:" + str(len(psamp3AggDropDynamic))
    print "psamp3AggInjectStatic:" + str(len(psamp3AggInjectStatic))
    print "psamp3AggInjectDynamic:" + str(len(psamp3AggInjectDynamic))
    print "psamp3CoreDropStatic:" + str(len(psamp3CoreDropStatic))
    print "psamp3CoreDropDynamic:" + str(len(psamp3CoreDropDynamic))
    print "psamp3CoreInjectStatic:" + str(len(psamp3CoreInjectStatic))
    print "psamp3CoreInjectDynamic:" + str(len(psamp3CoreInjectDynamic))
    print "Now plot the results."
    resultsFile = "randomPairAssignment/psamp3DetectionTime.pdf"
    plotAttacks(psamp3AggDropStatic, psamp3AggDropDynamic, psamp3CoreDropStatic, psamp3CoreDropDynamic,
                psamp3AggInjectStatic, psamp3CoreInjectStatic, psamp3AggInjectDynamic, psamp3CoreInjectDynamic,
                resultsFile)

def formalAnalysisResults():
    print "formalAnalysisResults()"
    for i in range(1, 4):
        # p = .0046
        p = 0.004638671875 * i
        print "p=" + str(p)
        # p = .00927734375
        n = 20
        Bagg = 1
        Aagg = 3
        Bcore = 2
        Acore = 2

        def colissions(a, b, T):
            print "cols =", a * b / T
            return a * b / T

        D = (n - 1) / p

        print "D =", D

        factorial = lambda x: x * factorial(x - 1)
        exp_pairs = lambda A, B: A * B
        # imp_pairs = lambda A,B: colissions(A*(n-1-B),B*(n-1-A),D)
        imp_pairs = lambda A, B: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, D)

        P_pa = lambda A, B: 1 - (1 - p / (n - 1)) ** (exp_pairs(A, B) + imp_pairs(A, B))
        P_pa_agg = P_pa(Aagg, Bagg)
        P_pa_core = P_pa(Acore, Bcore)
        if i == 1:
            baselineP_pa_agg = 1.0/P_pa_agg
            baselineP_pa_core = 1.0/P_pa_core
        elif i == 2:
            psamp2P_pa_agg = 1.0/P_pa_agg
            psamp2P_pa_core = 1.0/P_pa_core
        elif i == 3:
            psamp3P_pa_agg = 1.0/P_pa_agg
            psamp3P_pa_core = 1.0/P_pa_core
        print "For static drop considering implicit pairs:"
        print "for agg: P_pa=", P_pa_agg, "avg pkts", 1 / P_pa_agg
        print "for core: P_pa=", P_pa_core, "avg pkts", 1 / P_pa_core

        P_pa = lambda A, B: 1 - (1 - p / (n - 1)) ** (exp_pairs(A, B) + imp_pairs(A, B))
        P_pa_agg = P_pa(Aagg, Bagg)
        P_pa_core = P_pa(Acore, Bcore)
        print "For static inject considering implicit pairs:"
        print "for agg: P_pa=", P_pa_agg, "avg pkts", 1 / P_pa_agg
        print "for core: P_pa=", P_pa_core, "avg pkts", 1 / P_pa_core

        update_avg_interval = 2.0
        update_size = 2
        a_time = 2 * 60 * 60
        updates = a_time / update_avg_interval * update_size
        P_dpa0 = lambda A, B: P_pa(A, B)  # lambda A,B:1-(1-p/(n-1))**(exp_pairs(A,B) + imp_pairs(A,B))

        # avg_time_dpa = lambda A,B,u,s:(1-P_dpa0(A,B))*u/(1-(1-(p/(n-1))*(2.0*A*B/n/(n-1)))**s)
        pairs_from = lambda z: z * (n - z) + z * (z - 1) / 2.0
        pairs_from_both = lambda x, y: x * y
        pairs_from_either = lambda x, y: pairs_from(x) + pairs_from(y) - pairs_from_both(x, y)
        all_pairs = n * (n - 1) / 2.0
        not_in = lambda z: (1 - p / (n - 1)) ** z
        avg_time_till = lambda pairs, u, s: u / (1 - (1 - pairs / all_pairs * p / (n - 1)) ** s)
        # avg_time_dpa_x_then_y = lambda x,y,u,s:(1-p/(n-1))**(y*(n-1))*(1-(1-p/(n-1))**(x*(n-1-y)))*u/(1-(1-2.0*y*(n-y)/n/(n-1)*p/(n-1))**s)
        avg_time_dpa_x_then_y = lambda x, y, u, s: not_in(pairs_from(y)) * (
        1 - not_in(pairs_from(x) - pairs_from_both(x, y))) * avg_time_till(pairs_from(y), u, s)

        # avg_time_till_one_by_one = lambda A,B,u,s:(avg_time_till(pairs_from(A),u,s)+avg_time_till(pairs_from(B),u,s))/2
        join_time = lambda t1, t2: 1 / (1 / t1 + 1 / t2)
        avg_time_till_markov = lambda t1, t2, t12: 1 / (
        (1 / t12) + 1 / join_time(join_time(t1, t12), t2) + 1 / join_time(join_time(t1, t12), t2))
        # avg_time_till_both = lambda A,B,u,s:1/(1/avg_time_till(pairs_from_both(A,B),u,s)+1/avg_time_till_one_by_one(A,B,u,s))
        avg_time_till_both = lambda A, B, u, s: avg_time_till_markov(avg_time_till(pairs_from(A), u, s),
                                                                     avg_time_till(pairs_from(B), u, s),
                                                                     avg_time_till(pairs_from_both(A, B), u, s))
        avg_time_dpa_none_then_both = lambda A, B, u, s: not_in(pairs_from_either(A, B)) * avg_time_till_both(A, B, u,
                                                                                                              s)
        avg_time_dpa = lambda A, B, u, s: avg_time_dpa_none_then_both(A, B, u, s) + avg_time_dpa_x_then_y(A, B, u,
                                                                                                          s) + avg_time_dpa_x_then_y(
            B, A, u, s)

        avg_time_dpa_agg = avg_time_dpa(Aagg, Bagg, update_avg_interval, update_size)
        avg_time_dpa_core = avg_time_dpa(Acore, Bcore, update_avg_interval, update_size)
        print "For inject:"
        print "for agg: avg time", avg_time_dpa_agg, "sec"
        print "for core: avg time", avg_time_dpa_core, "sec"


def plotFormalAnalysis():
    print "plotFormalAnalysis()"
    # Get the sampling ratios
    sampRatios = []
    for i in range(1, 1001):
        sampRatios.append(i/1000.0)
    print sampRatios
    # No. of switches
    totalSwitches = range(20, 40, 20)
    # path length where the attacker is present
    pathLen = 5
    # Lists for before and after switches along the path
    fList = range(1, pathLen)
    bList = range(1, pathLen - 1)
    bList.reverse()
    i = 0
    beforeList = []
    afterList = []
    while i < len(fList) - 2:
        beforeList.append(fList[i])
        afterList.append(bList[i])
        i += 1
    limit = len(beforeList)
    print beforeList, afterList
    # now call the formalanalysis function for each value.
    switchList = []
    for s in totalSwitches:
        beforeAfterList = []
        for i in range(0, limit):
            detectionTimeList = []
            for p in sampRatios:
                detectionTimeList.append(formalAnalysis(p, beforeList[i], afterList[i], s))
            beforeAfterList.append(detectionTimeList)
        switchList.append(beforeAfterList)
    print "for collusion:formalAnalysis(0.0046, 1, 2, 20)=" + str(formalAnalysis(0.0046, 2, 1, 20))
    print "for collusion:formalAnalysis(0.0092, 1, 2, 20)=" + str(formalAnalysis(0.0092, 2, 1, 20))
    print "for collusion:formalAnalysis(0.0139, 1, 2, 20)=" + str(formalAnalysis(0.0139, 2, 1, 20))


    # now to plot it.
    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3', u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3', u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)
    s = 0
    fig = plt.figure(s + 1)
    subplot = 111
    while s < len(totalSwitches):
        ax = plt.subplot(subplot)
        for i in range(0, limit):
            plt.plot(sampRatios, switchList[s][i], color=colorIter.next(),
                     label='N='+str(totalSwitches[s])+', (B, A)='+str(beforeList[i])+','+str(afterList[i]))
            # ax.set_yscale('log')
            ax.set_xscale('log')
        s += 1
    # plt.title('Relationship of $P_{pa}$ with $N$ and $(B,A)$')
    ax.set_xlabel('$P_s$')
    ax.set_ylabel('Packets till detection')
    box = ax.get_position()
    ax.set_position([box.x0 + .05, box.y0 + box.height * 0.11 , box.width * 1.0, box.height * 0.97])
    plt.legend()
    resultsFile = "./results/randomPairAssignment/detectionProbabilityRelationshipPath"+str(pathLen)+".pdf"
    plt.savefig(resultsFile)

def plotAllPsampsSeparately():
    print "plotAllPsampsSeparately()"
    print "Baseline"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggDrop).read()))
    baseAggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0],
                                         attackPositions[0], attacks[0])
    baseAggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
                                          attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggInject).read()))
    baseAggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0],
                                           attackPositions[0], attacks[1])
    baseAggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
                                            attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreDrop).read()))
    baseCoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0],
                                          attackPositions[1], attacks[0])
    baseCoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
                                           attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreInject).read()))
    baseCoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0],
                                            attackPositions[1], attacks[1])
    baseCoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
                                             attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "baseAggDropStatic:" + str(len(baseAggDropStatic))
    print "baseAggDropDynamic:" + str(len(baseAggDropDynamic))
    print "baseAggInjectStatic:" + str(len(baseAggInjectStatic))
    print "baseAggInjectDynamic:" + str(len(baseAggInjectDynamic))
    print "baseCoreDropStatic:" + str(len(baseCoreDropStatic))
    print "baseCoreDropDynamic:" + str(len(baseCoreDropDynamic))
    print "baseCoreInjectStatic:" + str(len(baseCoreInjectStatic))
    print "baseCoreInjectDynamic:" + str(len(baseCoreInjectDynamic))
    print "samplingRate=0.0092"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggDrop).read()))
    psamp2AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0],
                                           attackPositions[0], attacks[0])
    psamp2AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1],
                                            attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggInject).read()))
    psamp2AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0],
                                             attackPositions[0], attacks[1])
    psamp2AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1],
                                              attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreDrop).read()))
    psamp2CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0],
                                            attackPositions[1], attacks[0])
    psamp2CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1],
                                             attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreInject).read()))
    psamp2CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0],
                                              attackPositions[1], attacks[1])
    psamp2CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1],
                                               attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp2AggDropStatic:" + str(len(psamp2AggDropStatic))
    print "psamp2AggDropDynamic:" + str(len(psamp2AggDropDynamic))
    print "psamp2AggInjectStatic:" + str(len(psamp2AggInjectStatic))
    print "psamp2AggInjectDynamic:" + str(len(psamp2AggInjectDynamic))
    print "psamp2CoreDropStatic:" + str(len(psamp2CoreDropStatic))
    print "psamp2CoreDropDynamic:" + str(len(psamp2CoreDropDynamic))
    print "psamp2CoreInjectStatic:" + str(len(psamp2CoreInjectStatic))
    print "psamp2CoreInjectDynamic:" + str(len(psamp2CoreInjectDynamic))
    print "samplingRate=0.0139"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggDrop).read()))
    psamp3AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0],
                                           attackPositions[0], attacks[0])
    psamp3AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1],
                                            attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggInject).read()))
    psamp3AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0],
                                             attackPositions[0], attacks[1])
    psamp3AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1],
                                              attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreDrop).read()))
    psamp3CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0],
                                            attackPositions[1], attacks[0])
    psamp3CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1],
                                             attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreInject).read()))
    psamp3CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0],
                                              attackPositions[1], attacks[1])
    psamp3CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1],
                                               attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp3AggDropStatic:" + str(len(psamp3AggDropStatic))
    print "psamp3AggDropDynamic:" + str(len(psamp3AggDropDynamic))
    print "psamp3AggInjectStatic:" + str(len(psamp3AggInjectStatic))
    print "psamp3AggInjectDynamic:" + str(len(psamp3AggInjectDynamic))
    print "psamp3CoreDropStatic:" + str(len(psamp3CoreDropStatic))
    print "psamp3CoreDropDynamic:" + str(len(psamp3CoreDropDynamic))
    print "psamp3CoreInjectStatic:" + str(len(psamp3CoreInjectStatic))
    print "psamp3CoreInjectDynamic:" + str(len(psamp3CoreInjectDynamic))

    print "psamp3AggInjectStatic:" + str(psamp3AggInjectStatic)
    print "psamp3CoreInjectStatic:" + str(psamp3CoreInjectStatic)
    print "plotAttacks()"
    resultsFile = "pureIndependentPairAssignmentDontAttackSamples/individualPsampsWithInjectDifferentHashDetectionTime.pdf"
    f, axarr = plt.subplots(2, 2)
    data = [baseAggDropStatic, psamp2AggDropStatic, psamp3AggDropStatic,
            baseAggInjectStatic, psamp2AggInjectStatic, psamp3AggInjectStatic,
            baseAggDropDynamic, psamp2AggDropDynamic, psamp3AggDropDynamic,
            baseAggInjectDynamic, psamp2AggInjectDynamic, psamp3AggInjectDynamic,
            baseCoreDropStatic, psamp2CoreDropStatic, psamp3CoreDropStatic,
            baseCoreInjectStatic, psamp2CoreInjectStatic, psamp3CoreInjectStatic,
            baseCoreDropDynamic, psamp2CoreDropDynamic, psamp3CoreDropDynamic,
            baseCoreInjectDynamic, psamp2CoreInjectDynamic, psamp3CoreInjectDynamic,
            ]
    dataStaticDrop=[baseAggDropStatic, psamp2AggDropStatic, psamp3AggDropStatic,
                    baseCoreDropStatic, psamp2CoreDropStatic, psamp3CoreDropStatic]
    dataDynamicDrop=[baseAggDropDynamic, psamp2AggDropDynamic, psamp3AggDropDynamic,
                     baseCoreDropDynamic, psamp2CoreDropDynamic, psamp3CoreDropDynamic]
    dataStaticInject=[baseAggInjectStatic, psamp2AggInjectStatic, psamp3AggInjectStatic,
                      baseCoreInjectStatic, psamp2CoreInjectStatic, psamp3CoreInjectStatic]
    dataDynamicInject=[baseAggInjectDynamic, psamp2AggInjectDynamic, psamp3AggInjectDynamic,
                       baseCoreInjectDynamic, psamp2CoreInjectDynamic, psamp3CoreInjectDynamic]

    aggDrop = [baseAggDropStatic, psamp2AggDropStatic, psamp3AggDropStatic,
               baseAggDropDynamic, psamp2AggDropDynamic, psamp3AggDropDynamic]
    aggInject = [baseAggInjectStatic, psamp2AggInjectStatic, psamp3AggInjectStatic,
                 baseAggInjectDynamic, psamp2AggInjectDynamic, psamp3AggInjectDynamic]
    coreDrop = [baseCoreDropStatic, psamp2CoreDropStatic, psamp3CoreDropStatic,
                baseCoreDropDynamic, psamp2CoreDropDynamic, psamp3CoreDropDynamic]
    coreInject = [baseCoreInjectStatic, psamp2CoreInjectStatic, psamp3CoreInjectStatic,
                  baseCoreInjectDynamic, psamp2CoreInjectDynamic, psamp3CoreInjectDynamic]

    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    medianprops = dict(linestyle='')
    # bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops)
    bps=[]
    bps.append(axarr[0,0].boxplot(aggDrop, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops, medianprops=medianprops))
    bps.append(axarr[1,0].boxplot(aggInject, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops, medianprops=medianprops))
    bps.append(axarr[0,1].boxplot(coreDrop, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops, medianprops=medianprops))
    bps.append(axarr[1,1].boxplot(coreInject, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops, medianprops=medianprops))

    colors = ['#3D9970', '#FF9136', '#FFC51B']
    for bp in bps:
        k = 0
        for patch in bp['boxes']:
            i = k % 3
            patch.set_facecolor(colors[i])
            plt.setp(bp['whiskers'], color='black')
            plt.setp(bp['fliers'], color='black')
            k += 1
    axarr[0,0].set_yscale('log')
    axarr[0,0].set_ylim(1,10000)
    axarr[0,1].set_yscale('log')
    axarr[0,1].set_ylim(1,10000)
    axarr[1,0].set_yscale('log')
    axarr[1,0].set_ylim(1,10000)
    axarr[1,1].set_yscale('log')
    axarr[1,1].set_ylim(1,10000)
    # # plt.xlabel('Attack and Assignment')
    c = 0
    axarr[0,0].text(c + 2, 24120.0, u'Aggregate')
    axarr[0,0].text(c + 10, 24120.0, u'Core')
    offset = 3.5
    axarr[0,0].plot([offset, offset], [-1, 10000], color='#000000')
    axarr[0,1].plot([offset, offset], [-1, 10000], color='#000000')
    axarr[1,0].plot([offset, offset], [-1, 10000], color='#000000')
    axarr[1,1].plot([offset, offset], [-1, 10000], color='#000000')

    baselineP_pa_agg = formalAnalysis(0.004638671875, 1, 3, 20)
    psamp2P_pa_agg = formalAnalysis(0.004638671875 * 2, 1, 3, 20)
    psamp3P_pa_agg = formalAnalysis(0.004638671875 * 3, 1, 3, 20)
    baselineP_pa_core = formalAnalysis(0.004638671875, 2, 2, 20)
    psamp2P_pa_core = formalAnalysis(0.004638671875 * 2, 2, 2, 20)
    psamp3P_pa_core = formalAnalysis(0.004638671875 * 3, 2, 2, 20)

    # # plt.plot(0, baselineP_pa_agg, 'r-', 1, baselineP_pa_agg, 'r-', 3, baselineP_pa_agg, 'r-')
    axarr[0,0].axhline(y=baselineP_pa_agg, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    axarr[1,0].axhline(y=baselineP_pa_agg, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    axarr[0,0].axhline(y=psamp2P_pa_agg, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    axarr[1,0].axhline(y=psamp2P_pa_agg, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    axarr[0,0].axhline(y=psamp3P_pa_agg, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])
    axarr[1,0].axhline(y=psamp3P_pa_agg, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])

    axarr[0,1].axhline(y=baselineP_pa_core, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    axarr[1,1].axhline(y=baselineP_pa_core, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    axarr[0,1].axhline(y=psamp2P_pa_core, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    axarr[1,1].axhline(y=psamp2P_pa_core, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    axarr[0,1].axhline(y=psamp3P_pa_core, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])
    axarr[1,1].axhline(y=psamp3P_pa_core, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])
    # # plt.axhline(y=baselineP_pa_agg, xmin=0, xmax=1.0/8.0, linewidth=.75, linestyle='--', color='red', marker=markerStyles[0])
    # # plt.axhline(y=baselineP_pa_core, xmin=4.0/8.0, xmax=5.0/8.0, linewidth=.75, linestyle='--', color='red', marker=markerStyles[0])
    # # plt.axhline(y=psamp2P_pa_agg, xmin=0, xmax=1.0/8.0, linewidth=.75, linestyle='-', color='red', marker=markerStyles[1])
    # # plt.axhline(y=psamp2P_pa_core, xmin=4.0/8.0, xmax=5.0/8.0, linewidth=.75, linestyle='-', color='red', marker=markerStyles[1])
    # # plt.axhline(y=psamp3P_pa_agg, xmin=0, xmax=1.0/8.0, linewidth=.75, linestyle='-.', color='red', marker=markerStyles[2])
    # # plt.axhline(y=psamp3P_pa_core, xmin=4.0/8.0, xmax=5.0/8.0, linewidth=.75, linestyle='-.', color='red', marker=markerStyles[2])
    #
    # # xmark = ['Drop\n                Static', 'Inject', 'Drop\n                Dynamic', 'Inject',
    # #          'Drop\n                Static', 'Inject', 'Drop\n                Dynamic', 'Inject']
    tickMarks = [2, 4]
    marks = ['', 'Static', '', '', 'Dynamic']
    ytickMarks = [1, 100, 10000]
    # plt.xticks(tickMarks, tuple(marks))
    axarr[1,0].set_xticklabels(tuple(marks))
    axarr[1,1].set_xticklabels(tuple(marks))
    # axarr[0,1].xticks(tickMarks, tuple(marks))
    # axarr[1,0].xticks(tickMarks, tuple(marks))
    # axarr[1,1].xticks(tickMarks, tuple(marks))
    # axarr[0,0].yaxis.set_major_locator(MaxNLocator(steps=[5]))
    # axarr[1,0].yaxis.set_major_locator(MaxNLocator(steps=[5]))
    plt.setp([a.get_xticklabels() for a in axarr[0, :]], visible=False)
    plt.setp([a.get_yticklabels() for a in axarr[:, 1]], visible=False)
    plt.figtext(0.91, 0.750, 'Drop', color='black')
    plt.figtext(0.91, 0.400, 'Inject', color='black')
    plt.figtext(0.030, 0.55, 'Packet sent till detection', ha='center', va='center', rotation='vertical')
    plt.figtext(0.51, 0.1, 'Hash Assignment', ha='center', va='center')
    # plt.figtext(0.58, 0.15, 'Static', color='black')
    # plt.figtext(0.76, 0.15, 'Dynamic', color='black')
    # plt.figtext(0.35, 0.10, 'Attack and Assignment', color='black')
    #
    for ax in axarr[0, :]:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.21, box.width * 1.0, box.height * 0.84])
        ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
        ax.set_axisbelow(True)
    for ax in axarr[1, :]:
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.41, box.width * 1.0, box.height * 0.84])
        ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
        ax.set_axisbelow(True)
    plt.figtext(0.30, 0.018, '$p_s$=0.4\%',
                backgroundcolor=colors[0], color='black')
    plt.figtext(0.50, 0.018, '$p_s$=0.9\%',
                backgroundcolor=colors[1], color='black')
    plt.figtext(0.70, 0.018, '$p_s$=1.3\%',
                backgroundcolor=colors[2], color='black')
    # plt.show()
    plt.savefig(resultsPath + resultsFile)

def plotCollusionTwoAttackersCase1():
    print "plotCollusionCase1"
    print "psamp2AggMirrorCollusion"
    print "Agg: 021_221, Mirror (Inject). Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggMirrorCollusionCase1).read()))
    psamp1AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp1AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggMirrorCollusionCase1).read()))
    psamp2AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp2AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggMirrorCollusionCase1).read()))
    psamp3AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp3AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusionStatic))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusionDynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusionStatic))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusionDynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusionStatic))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusionDynamic))

    # for collusion: formalAnalysis(0.0046, 1, 2, 20) = 1926.72829979
    # for collusion: formalAnalysis(0.0092, 1, 2, 20) = 902.870006964
    # for collusion: formalAnalysis(0.0139, 1, 2, 20) = 561.585977783
    baselineP_pa_agg_collusion = 1.0/formalAnalysisCollusion(0.004638671875, 2, 2, 20)
    psamp2P_pa_agg_collusion = 1.0/formalAnalysisCollusion(0.004638671875*2, 2, 2, 20)
    psamp3P_pa_agg_collusion = 1.0/formalAnalysisCollusion(0.004638671875*3, 2, 2, 20)

    print "plotAttacks()"
    resultsFile = "collusionCase1PureIndependentPairAssignment/allPsampsAggMirrorCollusionDetectionTimeCase1.pdf"
    fig = plt.figure(figCounter)
    # fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    data = [psamp1AggInjectCollusionStatic, psamp2AggInjectCollusionStatic, psamp3AggInjectCollusionStatic,
            psamp1AggInjectCollusionDynamic, psamp2AggInjectCollusionDynamic, psamp3AggInjectCollusionDynamic]
    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops)

    colors = ['#3D9970', '#FF9136', '#FFC51B']
    k = 0
    for patch in bp['boxes']:
        i = k % 3
        patch.set_facecolor(colors[i])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='black')
        k += 1
    plt.plot([3.5, 3.5], [-1, 100000], color='#000000')
    plt.axhline(y=baselineP_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    plt.axhline(y=psamp2P_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    plt.axhline(y=psamp3P_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])

    plt.ylabel('Packet sent till detection.')
    tickMarks = [2, 5]
    marks = ['Static', 'Dynamic']
    plt.xticks(tickMarks, tuple(marks))
    plt.figtext(0.42, 0.150, 'Assignment', color='black')
    # plt.figtext(0.15, 0.95, 'Case:1-Two Colluding Aggregate Switches Mirror Attack')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.21 , box.width * 1.0, box.height * 0.83])
    ax.set_yscale('log')
    ax.set_ylim([1,10000])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.figtext(0.30, 0.018, '$p_s$=0.4\%',
                backgroundcolor=colors[0], color='black')
    plt.figtext(0.50, 0.018, '$p_s$=0.9\%',
                backgroundcolor=colors[1], color='black')
    plt.figtext(0.70, 0.018, '$p_s$=1.3\%',
                backgroundcolor=colors[2], color='black')
 
    # plt.show()
    plt.savefig(resultsPath + resultsFile)

def plotCollusionTwoAttackersCase2():
    print "plotCollusionCase2"
    print "psamp2AggMirrorCollusion"
    print "Agg: 021_221, Mirror (Inject). Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggMirrorCollusionCase2).read()))
    psamp1AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp1AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggMirrorCollusionCase2).read()))
    psamp2AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp2AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggMirrorCollusionCase2).read()))
    psamp3AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp3AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusionStatic))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusionDynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusionStatic))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusionDynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusionStatic))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusionDynamic))

    # for collusion: formalAnalysis(0.0046, 1, 2, 20) = 1926.72829979
    # for collusion: formalAnalysis(0.0092, 1, 2, 20) = 902.870006964
    # for collusion: formalAnalysis(0.0139, 1, 2, 20) = 561.585977783
    baselineP_pa_agg_collusion = 1.0/formalAnalysisCollusion(0.0046, 1, 2, 20, 1)
    psamp2P_pa_agg_collusion = 1.0/formalAnalysisCollusion(0.0092, 1, 2, 20, 1)
    psamp3P_pa_agg_collusion = 1.0/formalAnalysisCollusion(0.0139, 1, 2, 20, 1)

    print "plotAttacks()"
    resultsFile = "randomPairAssignment/allPsampsAggMirrorCollusionDetectionTimeCase2.pdf"
    fig = plt.figure(figCounter)
    # fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    data = [psamp1AggInjectCollusionStatic, psamp2AggInjectCollusionStatic, psamp3AggInjectCollusionStatic,
            psamp1AggInjectCollusionDynamic, psamp2AggInjectCollusionDynamic, psamp3AggInjectCollusionDynamic]
    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops)

    colors = ['#3D9970', '#FF9136', '#FFC51B']
    k = 0
    for patch in bp['boxes']:
        i = k % 3
        patch.set_facecolor(colors[i])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='black')
        k += 1
    plt.plot([3.5, 3.5], [-1, 100000], color='#000000')
    plt.axhline(y=baselineP_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    plt.axhline(y=psamp2P_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    plt.axhline(y=psamp3P_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])

    plt.ylabel('Packet sent till detection.')
    tickMarks = [2, 5]
    marks = ['Static', 'Dynamic']
    plt.xticks(tickMarks, tuple(marks))
    plt.figtext(0.42, 0.150, 'Assignment', color='black')
    plt.figtext(0.15, 0.95, 'Case:2-Two Colluding Aggregate Switches Mirror Attack')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.21 , box.width * 1.0, box.height * 0.83])
    ax.set_yscale('log')
    ax.set_ylim([1,10000])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.figtext(0.25, 0.048, 'p=0.0046',
                backgroundcolor=colors[0], color='black')
    plt.figtext(0.45, 0.048, 'p=0.0092',
                backgroundcolor=colors[1], color='black')
    plt.figtext(0.65, 0.048, 'p=0.0139',
                backgroundcolor=colors[2], color='black')
    # plt.show()
    plt.savefig(resultsPath + resultsFile)

def plotCollusionThreeAttackersCase1():
    print "plotCollusionCase1"
    print "psamp2AggMirrorCollusion"
    print "Agg: 021_221, Mirror (Inject). Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggCoreMirrorCollusionCase1).read()))
    psamp1AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp1AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggCoreMirrorCollusionCase1).read()))
    psamp2AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp2AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggCoreMirrorCollusionCase1).read()))
    psamp3AggInjectCollusionStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp3AggInjectCollusionDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusionStatic))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusionDynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusionStatic))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusionDynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusionStatic))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusionDynamic))

    # for collusion: formalAnalysis(0.0046, 1, 2, 20) = 1926.72829979
    # for collusion: formalAnalysis(0.0092, 1, 2, 20) = 902.870006964
    # for collusion: formalAnalysis(0.0139, 1, 2, 20) = 561.585977783
    baselineP_pa_agg_collusion = 1/formalAnalysisCollusion3Attackers(0.0046, 2, 1, 20, 1)
    psamp2P_pa_agg_collusion = 1/formalAnalysisCollusion3Attackers(0.0046*2, 2, 1, 20, 1)
    psamp3P_pa_agg_collusion = 1/formalAnalysisCollusion3Attackers(0.0046*3, 2, 1, 20, 1)

    # print "collusion with 3 attackers on path=" + str(
    # print "collusion with 3 attackers on path=" + str(1/formalAnalysisCollusion3Attackers(0.0092, 1, 1, 20, 1))
    # print "collusion with 3 attackers on path=" + str(1/formalAnalysisCollusion3Attackers(0.0139, 1, 1, 20, 1))

    print "plotAttacks()"
    resultsFile = "collusionCase1PureIndependentPairAssignment/allPsampsAggCoreMirrorCollusionDetectionTimeCase1.pdf"
    fig = plt.figure(figCounter)
    # fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    data = [psamp1AggInjectCollusionStatic, psamp2AggInjectCollusionStatic, psamp3AggInjectCollusionStatic,
            psamp1AggInjectCollusionDynamic, psamp2AggInjectCollusionDynamic, psamp3AggInjectCollusionDynamic]
    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops)

    colors = ['#3D9970', '#FF9136', '#FFC51B']
    k = 0
    for patch in bp['boxes']:
        i = k % 3
        patch.set_facecolor(colors[i])
        plt.setp(bp['whiskers'], color='black')
        plt.setp(bp['fliers'], color='black')
        k += 1
    plt.plot([3.5, 3.5], [-1, 100000], color='#000000')
    plt.axhline(y=baselineP_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    plt.axhline(y=psamp2P_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    plt.axhline(y=psamp3P_pa_agg_collusion, xmin=0, xmax=3.0 / 6.0, linestyle='-', color=colors[2], marker=markerStyles[2])

    plt.ylabel('Packet sent till detection.')
    tickMarks = [2, 5]
    marks = ['Static', 'Dynamic']
    plt.xticks(tickMarks, tuple(marks))
    plt.figtext(0.42, 0.150, 'Assignment', color='black')
    plt.figtext(0.15, 0.95, 'Three Colluding Switches Mirror Attack')

    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.21 , box.width * 1.0, box.height * 0.83])
    ax.set_yscale('log')
    ax.set_ylim([1,10000])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.figtext(0.25, 0.048, 'p=0.0046',
                backgroundcolor=colors[0], color='black')
    plt.figtext(0.45, 0.048, 'p=0.0092',
                backgroundcolor=colors[1], color='black')
    plt.figtext(0.65, 0.048, 'p=0.0139',
                backgroundcolor=colors[2], color='black')
    # plt.show()
    plt.savefig(resultsPath + resultsFile)

def plotCollusionTwoThreeAttackersCase1():
    print "plotCollusionTwoThreeAttackersCase1"
    print "Agg: 021_221, Mirror (Inject). Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggMirrorCollusionCase1).read()))
    psamp1AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp1AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggMirrorCollusionCase1).read()))
    psamp2AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp2AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggMirrorCollusionCase1).read()))
    psamp3AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp3AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusion2Static))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusion2Dynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusion2Static))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusion2Dynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusion2Static))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusion2Dynamic))

    baselineP_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875, 2, 2, 20)
    psamp2P_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875*2, 2, 2, 20)
    psamp3P_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875*3, 2, 2, 20)

    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggCoreMirrorCollusionCase1).read()))
    psamp1AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp1AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggCoreMirrorCollusionCase1).read()))
    psamp2AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp2AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggCoreMirrorCollusionCase1).read()))
    psamp3AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp3AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusion3Static))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusion3Dynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusion3Static))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusion3Dynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusion3Static))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusion3Dynamic))

    # for collusion: formalAnalysis(0.0046, 1, 2, 20) = 1926.72829979
    # for collusion: formalAnalysis(0.0092, 1, 2, 20) = 902.870006964
    # for collusion: formalAnalysis(0.0139, 1, 2, 20) = 561.585977783
    baselineP_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875, 2, 1, 20, 1)
    psamp2P_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875*2, 2, 1, 20, 1)
    psamp3P_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875*3, 2, 1, 20, 1)

    print "plotAttacks()"
    resultsFile = "collusionCase1PureIndependentPairAssignment/allPsampsCollusionTwoThreeDetectionTimeCase1.pdf"
    fig = plt.figure(figCounter)
    # fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    data = [psamp1AggInjectCollusion2Static, psamp2AggInjectCollusion2Static, psamp3AggInjectCollusion2Static,
            psamp1AggInjectCollusion2Dynamic, psamp2AggInjectCollusion2Dynamic, psamp3AggInjectCollusion2Dynamic,
            psamp1AggInjectCollusion3Static, psamp2AggInjectCollusion3Static, psamp3AggInjectCollusion3Static,
            psamp1AggInjectCollusion3Dynamic, psamp2AggInjectCollusion3Dynamic, psamp3AggInjectCollusion3Dynamic]
    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops)

    colors = ['#3D9970', '#FF9136', '#FFC51B']
    k = 0
    for patch in bp['boxes']:
        i = k % 3
        patch.set_facecolor(colors[i])
        plt.setp(bp['whiskers'], color='black', linestyle='--')
        plt.setp(bp['fliers'], color='black', marker='+')
        k += 1
    plt.plot([3.5, 3.5], [-1, 100000], color='#000000')
    plt.plot([6.5, 6.5], [-1, 100000], color='#000000')
    plt.plot([9.5, 9.5], [-1, 100000], color='#000000')
    plt.axhline(y=baselineP_pa_agg_collusion2, xmin=0, xmax=3.0 / 12.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    plt.axhline(y=psamp2P_pa_agg_collusion2, xmin=0, xmax=3.0 / 12.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    plt.axhline(y=psamp3P_pa_agg_collusion2, xmin=0, xmax=3.0 / 12.0, linestyle='-', color=colors[2], marker=markerStyles[2])
    plt.axhline(y=baselineP_pa_agg_collusion3, xmin=6.0/12.0, xmax=9.0 / 12.0, linestyle='-', color=colors[0],
                marker=markerStyles[0])
    plt.axhline(y=psamp2P_pa_agg_collusion3, xmin=6.0/12.0, xmax=9.0 / 12.0, linestyle='-', color=colors[1],
                marker=markerStyles[1])
    plt.axhline(y=psamp3P_pa_agg_collusion3, xmin=6.0/12.0, xmax=9.0 / 12.0, linestyle='-', color=colors[2],
                marker=markerStyles[2])

    plt.ylabel('Packet sent till detection')
    tickMarks = [2, 5, 8, 11]
    marks = ['Static', 'Dynamic', 'Static', 'Dynamic']
    plt.xticks(tickMarks, tuple(marks))
    plt.figtext(0.42, 0.150, 'Assignment', color='black')
    plt.figtext(0.20, 0.95, 'Two Attackers')
    plt.figtext(0.60, 0.95, 'Three Attackers')

    box = ax.get_position()
    ax.set_position([box.x0 + box.width * .02, box.y0 + box.height * 0.25 , box.width * 1.03, box.height * 0.83])
    ax.set_yscale('log')
    ax.set_ylim([1,10000])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.figtext(0.15, 0.048, '$p_s$=0.4\%',
                backgroundcolor=colors[0], color='black')
    plt.figtext(0.45, 0.048, '$p_s$=0.9\%',
                backgroundcolor=colors[1], color='black')
    plt.figtext(0.75, 0.048, '$p_s$=1.3\%',
                backgroundcolor=colors[2], color='black')
    # plt.show()
    plt.savefig(resultsPath + resultsFile)

def plotCollusionTwoThreeAttackersCase1Scatter():
    print "plotCollusionTwoThreeAttackersCase1"
    print "Agg: 021_221, Mirror (Inject). Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggMirrorCollusionCase1).read()))
    psamp1AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp1AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggMirrorCollusionCase1).read()))
    psamp2AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp2AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggMirrorCollusionCase1).read()))
    psamp3AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp3AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusion2Static))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusion2Dynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusion2Static))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusion2Dynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusion2Static))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusion2Dynamic))

    baselineP_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875, 2, 2, 20)
    psamp2P_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875*2, 2, 2, 20)
    psamp3P_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875*3, 2, 2, 20)

    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggCoreMirrorCollusionCase1).read()))
    psamp1AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp1AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggCoreMirrorCollusionCase1).read()))
    psamp2AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp2AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggCoreMirrorCollusionCase1).read()))
    psamp3AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp3AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusion3Static))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusion3Dynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusion3Static))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusion3Dynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusion3Static))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusion3Dynamic))

    # for collusion: formalAnalysis(0.0046, 1, 2, 20) = 1926.72829979
    # for collusion: formalAnalysis(0.0092, 1, 2, 20) = 902.870006964
    # for collusion: formalAnalysis(0.0139, 1, 2, 20) = 561.585977783
    baselineP_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875, 2, 1, 20, 1)
    psamp2P_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875*2, 2, 1, 20, 1)
    psamp3P_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875*3, 2, 1, 20, 1)

    print "plotAttacks()"
    fig = plt.figure(figCounter)
    # fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)
    data = [psamp1AggInjectCollusion2Static, psamp2AggInjectCollusion2Static, psamp3AggInjectCollusion2Static,
            psamp1AggInjectCollusion2Dynamic, psamp2AggInjectCollusion2Dynamic, psamp3AggInjectCollusion2Dynamic,
            psamp1AggInjectCollusion3Static, psamp2AggInjectCollusion3Static, psamp3AggInjectCollusion3Static,
            psamp1AggInjectCollusion3Dynamic, psamp2AggInjectCollusion3Dynamic, psamp3AggInjectCollusion3Dynamic]

    data = []
    for attack in [psamp1AggInjectCollusion2Static, psamp2AggInjectCollusion2Static, psamp3AggInjectCollusion2Static]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(data, marker='+', linestyle='', color=colorIter.next())
    ax.annotate('Two switches (Experimental)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))
    data = []
    for attack in [psamp1AggInjectCollusion3Static, psamp2AggInjectCollusion3Static, psamp3AggInjectCollusion3Static]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(data, marker='x', linestyle='', color=colorIter.next())
    ax.annotate('Three switches (Experimental)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))

    data = [baselineP_pa_agg_collusion2, psamp2P_pa_agg_collusion2, psamp3P_pa_agg_collusion2]
    plt.plot(data, marker='P', linestyle='', color=colorIter.next())
    ax.annotate('Two switches (theoretical)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-55), arrowprops=dict(arrowstyle="->"))
    data = [baselineP_pa_agg_collusion3, psamp2P_pa_agg_collusion3, psamp3P_pa_agg_collusion3]
    plt.plot(data, marker='X', linestyle='', color=colorIter.next())
    ax.annotate('Three switches (theoretical)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))

    tickMarks = [0, 1, 2]
    marks = ['0.4%', '0.9%', '1.3%']
    plt.xticks(tickMarks, tuple(marks))
    plt.ylabel('Packets sent till detection')
    plt.xlabel('Sampling ratio')
    box = ax.get_position()
    ax.set_position([box.x0 * 1.3, box.y0 + box.height * 0.21 , box.width * 1., box.height * 0.84])
    resultsFile = "collusionCase1PureIndependentPairAssignment/allPsampsCollusionTwoThreeDetectionTimeCase1MeansScatter.pdf"
    plt.savefig(resultsPath + resultsFile)

def getInjectSameHashes():
    print "getInjectDiffHashes()"
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggInjectSameHash).read()))
    baseAggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreInjectSameHash).read()))
    baseCoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggInjectSameHash).read()))
    psamp2AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreInjectSameHash).read()))
    psamp2CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggInjectSameHash).read()))
    psamp3AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreInjectSameHash).read()))
    psamp3CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])

    data = [baseAggInjectDynamic, baseCoreInjectDynamic, psamp2AggInjectDynamic, psamp2CoreInjectDynamic, psamp3AggInjectDynamic, psamp3CoreInjectDynamic]
    print "Order of means are: baseAggInjectDynamic, baseCoreInjectDynamic, psamp2AggInjectDynamic, psamp2CoreInjectDynamic, psamp3AggInjectDynamic, psamp3CoreInjectDynamic"
    for d in data:
        total = 0.0
        for packets in d:
            total += packets
        mean = total/len(d)
        print "mean is:" + str(mean)
        print "len is:" + str(len(d))
    fig = plt.figure(figCounter, figsize=(8.75, 4.6), frameon=True)
    ax = plt.subplot(figSubplot)
    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops)
    ax.set_yscale('log')
    plt.show()


def main():
    print "Parse and plot the results."
    detectionTimeDict = dict(json.loads(open(dataPath + dataFile).read()))
    # pprint.pprint(detectionTimeDict)
    aggregateStaticDrop = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    aggregateDynamicDrop = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + dataFileBaselineCoreDrop).read()))
    coreStaticDrop = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0],  attackPositions[1], attacks[0])
    coreDynamicDrop = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],  attackPositions[1], attacks[0])
    pprint.pprint(aggregateStaticDrop)
    pprint.pprint(aggregateDynamicDrop)
    pprint.pprint(coreStaticDrop)
    pprint.pprint(coreDynamicDrop)
    plotAttack(attacks[0], aggregateStaticDrop, aggregateDynamicDrop, coreStaticDrop, coreDynamicDrop)

    # Carried out the detection for the inject attack again based on the discussion with Stefan
    # Therefore, the inject results have to be collected from different json files.
    # dataFileAggCorrected = 'detectionTimeInjectAggregateCorrectedUpdateRate2.json'
    # detectionTimeDict = dict(json.loads(open(dataPath + dataFileAggCorrected).read()))
    # aggregateStaticInject = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    # aggregateDynamicInject = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    # dataFileCoreCorrected = 'detectionTimeInjectCoreCorrectedUpdateRate2.json'
    # detectionTimeDict = dict(json.loads(open(dataPath + dataFileCoreCorrected).read()))
    # coreStaticInject = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    # coreDynamicInject = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],  attackPositions[1], attacks[1])

    # pprint.pprint(aggregateDynamicInject)
    # pprint.pprint(aggregateStaticInject)
    # pprint.pprint(coreStaticInject)
    # pprint.pprint(coreDynamicInject)
    # plotAttack(attacks[1], [], aggregateDynamicInject, [], coreDynamicInject)
    print "No. of attack data points are:"
    print "aggregateStaticDrop:" + str(len(aggregateStaticDrop))
    print "aggregateDynamicDrop:" + str(len(aggregateDynamicDrop))
    print "coreStaticDrop:" + str(len(coreStaticDrop))
    print "coreDynamicDrop:" + str(len(coreDynamicDrop))
    # print "aggregateStaticInject:" + str(len(aggregateStaticInject))
    # print "aggregateDynamicInject:" + str(len(aggregateDynamicInject))
    # print "coreStaticInject:" + str(len(coreStaticInject))
    # print "coreDynamicInject:" + str(len(coreDynamicInject))
    # plotAttacks(aggregateStaticDrop, aggregateDynamicDrop, coreStaticDrop, coreDynamicDrop,
    #             [], aggregateDynamicInject, coreStaticInject, coreDynamicInject,
    #             resultsFile)

    # The below pieces of commented code are for plotting
    # the changes in update results detections.
    # updateRateFile = 'detectionTimeDropAggCoreUpdate4.json'
    # detectionTimeDict = dict(json.loads(open(dataPath + updateRateFile).read()))
    # aggregateDynamicDropUpdate4 = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[0], updateRate='4')
    # coreDynamicDropUpdate4 = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],  attackPositions[1], attacks[0], updateRate='4')
    # print "aggregateDynamicDrop:" + str(len(aggregateDynamicDropUpdate4))
    # print "coreDynamicDrop:" + str(len(coreDynamicDropUpdate4))
    # # plotAttacks([], aggregateDynamicDropUpdate4, [], coreDynamicDropUpdate4,
    # #             [], [], [], [],
    # #             resultsFileUpdate4)
    #
    # updateRateFile = 'detectionTimeDropAggCoreUpdate1.json'
    # detectionTimeDict = dict(json.loads(open(dataPath + updateRateFile).read()))
    # aggregateDynamicDropUpdate1 = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
    #                                                attackPositions[0], attacks[0], updateRate='1')
    # coreDynamicDropUpdate1 = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
    #                                           attackPositions[1], attacks[0], updateRate='1')
    # print "aggregateDynamicDrop:" + str(len(aggregateDynamicDropUpdate1))
    # print "coreDynamicDrop:" + str(len(coreDynamicDropUpdate1))
    # plotAttacks([], aggregateDynamicDropUpdate1, [], coreDynamicDropUpdate1,
    #             [], [], [], [],
    #             resultsFileUpdate1)

def debugAnalysis():
    def colissions(a, b, T):
        # print "cols =", a * b / T
        return a * b / T

    n = 20
    imp_pairs = lambda A, B: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, D)
    p = 0.0046
    D = (n - 1) / p
    print "psamp1 imp_pairs:" + str(imp_pairs(1, 3))
    p = 0.0092
    D = (n - 1) / p
    print "psamp2 imp_pairs:" + str(imp_pairs(1, 3))
    p = 0.0139
    D = (n - 1) / p
    print "psamp3 imp_pairs:" + str(imp_pairs(1, 3))

def kashyapAnalysis():
    print "kashyap's analysis of detection probability"
    # No. of hash values shared between a pair = x
    # Total no. of hash values assigned to a node = |A(s)|
    # No. of hash values shared before, and after = B, A
    # Total hash values surrounding the attack location = x*B*A
    # Size of hash domain = H
    # Only count the no. of pairs shared between the Before and After nodes.
    H = 4096.0
    # For the drop and report, prob. of detection is the prob. that at least
    # 1 hash value is sampled from the x*B*A values, or, from hash values that are
    # shared with the attacker and A nodes after the attacker.
    # For the drop and no report, prob. of detection is the prob. that at least
    # 1 hash value is sampled from the x*B*A values, or, from hash values that are
    # shared with the attacker and B nodes before the attacker, or from hash values
    # that are shared with the attacker and A nodes after the attacker.
    # For the inject and report, its the same as drop and no report.
    # For the inject and no report, its the same as drop and report.
    # This is because its better for the attacker to not report it, so that
    # it does not caught by switches before it.
    # This analysis so far comes close for collusion case1, i.e., both don't report
    # For collusion, what matters are the values for B and A, their order,
    # and analyzing it 1 attacker at a time, ignoring the attacker nodes, if
    # they do not report.
    # This analysis does not account for the implicit pairs, which is a small improvement.
    P_pa_report_drop = lambda A, B, x: ((x * A * B) + x * A) / H
    P_pa_noreport_drop = lambda A, B, x: ((x * A * B) + x * A + x * B) / H
    P_pa_report_inject = lambda A, B, x: ((x * A * B) + x * A + x * B) / H
    P_pa_noreport_inject = lambda A, B, x: ((x * A * B) + x * A) / H
    print "psamp1 P_pa_report_drop Agg:" + str(1/P_pa_report_drop(1,3,1))
    print "psamp2 P_pa_report_drop Agg:" + str(1/P_pa_report_drop(1,3,2))
    print "psamp3 P_pa_report_drop Agg:" + str(1/P_pa_report_drop(1,3,3))
    print "psamp1 P_pa_report_drop Cor:" + str(1/P_pa_report_drop(2,2,1))
    print "psamp2 P_pa_report_drop Cor:" + str(1/P_pa_report_drop(2,2,2))
    print "psamp3 P_pa_report_drop Cor:" + str(1/P_pa_report_drop(2,2,3))

    print "psamp1 P_pa_noreport_drop Agg:" + str(1/P_pa_noreport_drop(1,3,1))
    print "psamp2 P_pa_noreport_drop Agg:" + str(1/P_pa_noreport_drop(1,3,2))
    print "psamp3 P_pa_noreport_drop Agg:" + str(1/P_pa_noreport_drop(1,3,3))
    print "psamp1 P_pa_noreport_drop Cor:" + str(1/P_pa_noreport_drop(2,2,1))
    print "psamp2 P_pa_noreport_drop Cor:" + str(1/P_pa_noreport_drop(2,2,2))
    print "psamp3 P_pa_noreport_drop Cor:" + str(1/P_pa_noreport_drop(2,2,3))

    print "psamp1 P_pa_report_inject Agg:" + str(1/P_pa_report_inject(1,3,1))
    print "psamp2 P_pa_report_inject Agg:" + str(1/P_pa_report_inject(1,3,2))
    print "psamp3 P_pa_report_inject Agg:" + str(1/P_pa_report_inject(1,3,3))
    print "psamp1 P_pa_report_inject Cor:" + str(1/P_pa_report_inject(2,2,1))
    print "psamp2 P_pa_report_inject Cor:" + str(1/P_pa_report_inject(2,2,2))
    print "psamp3 P_pa_report_inject Cor:" + str(1/P_pa_report_inject(2,2,3))

    print "psamp1 P_pa_noreport_inject Agg:" + str(1/P_pa_noreport_inject(1,3,1))
    print "psamp2 P_pa_noreport_inject Agg:" + str(1/P_pa_noreport_inject(1,3,2))
    print "psamp3 P_pa_noreport_inject Agg:" + str(1/P_pa_noreport_inject(1,3,3))
    print "psamp1 P_pa_noreport_inject Cor:" + str(1/P_pa_noreport_inject(2,2,1))
    print "psamp2 P_pa_noreport_inject Cor:" + str(1/P_pa_noreport_inject(2,2,2))
    print "psamp3 P_pa_noreport_inject Cor:" + str(1/P_pa_noreport_inject(2,2,3))

#     print "psamp1 Collusion2 Case1:" + str(1/(P_pa_noreport_inject(1,2,1)+P_pa_noreport_inject(2,1,1)))
#     print "psamp2 Collusion2 Case1:" + str(1/(P_pa_noreport_inject(1,2,2)+P_pa_noreport_inject(2,1,2)))
#     print "psamp3 Collusion2 Case1:" + str(1/(P_pa_noreport_inject(1,2,3)+P_pa_noreport_inject(2,1,3)))
# 
#     print "psamp1 Collusion3 Case1:" + str(1/(P_pa_noreport_inject(1,1,1)+P_pa_noreport_inject(1,1,1)+P_pa_noreport_inject(1,1,1)))
#     print "psamp2 Collusion3 Case1:" + str(1/(P_pa_noreport_inject(1,1,2)+P_pa_noreport_inject(1,1,2)+P_pa_noreport_inject(1,1,2)))
#     print "psamp3 Collusion3 Case1:" + str(1/(P_pa_noreport_inject(1,1,3)+P_pa_noreport_inject(1,1,3)+P_pa_noreport_inject(1,1,3)))

# Using this instead of kashyapsAnalysis as it includes the implicit pairs
# psamp1 P_dr Agg:660.728418399
# psamp2 P_dr Agg:335.759205892
# psamp3 P_dr Agg:225.064606139
# psamp1 P_dr Cor:653.7002143
# psamp2 P_dr Cor:333.934754483
# psamp3 P_dr Cor:224.243367149
# psamp1 P_inr Agg:660.728418399
# psamp2 P_inr Agg:335.759205892
# psamp3 P_inr Agg:225.064606139
# psamp1 P_inr Cor:653.7002143
# psamp2 P_inr Cor:333.934754483
# psamp3 P_inr Cor:224.243367149
def formalAnalysisWithAttackerSamples():
    def colissions(a, b, T):
#        print "cols =", a * b / T
        return a * b / T

    n = 20.0
    H = 4096.0
    imp_pairs = lambda A, B: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, H)

    print "kashyap's analysis of detection probability"
    P_dr = lambda B, A, c: (((c * A * B) + c * A) + imp_pairs(A, B))/ H
    P_inr = lambda B, A, c: (((c * A * B) + c * A) + imp_pairs(A, B))/ H
    print "psamp1 P_dr Agg:" + str(1/P_dr(1,3,1))
    print "psamp2 P_dr Agg:" + str(1/P_dr(1,3,2))
    print "psamp3 P_dr Agg:" + str(1/P_dr(1,3,3))
    print "psamp1 P_dr Cor:" + str(1/P_dr(2,2,1))
    print "psamp2 P_dr Cor:" + str(1/P_dr(2,2,2))
    print "psamp3 P_dr Cor:" + str(1/P_dr(2,2,3))

    print "psamp1 P_inr Agg:" + str(1/P_inr(1,3,1))
    print "psamp2 P_inr Agg:" + str(1/P_inr(1,3,2))
    print "psamp3 P_inr Agg:" + str(1/P_inr(1,3,3))
    print "psamp1 P_inr Cor:" + str(1/P_inr(2,2,1))
    print "psamp2 P_inr Cor:" + str(1/P_inr(2,2,2))
    print "psamp3 P_inr Cor:" + str(1/P_inr(2,2,3))

def formalAnalysisAttackerSamples(p, B, A, N):
    def colissions(a, b, T):
        return a * b / T

    H = 4096.0
    imp_pairs = lambda A, B, n: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, H)

    n = N
    c = p*H/(n-1)
    P_dr = (((c * A * B) + c * A) + imp_pairs(A, B, n))/ H
    return 1/P_dr

def plotFormal():
    print "Baseline"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggDrop).read()))
    baseAggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    baseAggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggInject).read()))
    baseAggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    baseAggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreDrop).read()))
    baseCoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    baseCoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreInject).read()))
    baseCoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    baseCoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "baseAggDropStatic:" + str(len(baseAggDropStatic))
    print "baseAggDropDynamic:" + str(len(baseAggDropDynamic))
    print "baseAggInjectStatic:" + str(len(baseAggInjectStatic))
    print "baseAggInjectDynamic:" + str(len(baseAggInjectDynamic))
    print "baseCoreDropStatic:" + str(len(baseCoreDropStatic))
    print "baseCoreDropDynamic:" + str(len(baseCoreDropDynamic))
    print "baseCoreInjectStatic:" + str(len(baseCoreInjectStatic))
    print "baseCoreInjectDynamic:" + str(len(baseCoreInjectDynamic))
    print "samplingRate=0.0092"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggDrop).read()))
    psamp2AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp2AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggInject).read()))
    psamp2AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp2AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreDrop).read()))
    psamp2CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp2CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreInject).read()))
    psamp2CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp2CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp2AggDropStatic:" + str(len(psamp2AggDropStatic))
    print "psamp2AggDropDynamic:" + str(len(psamp2AggDropDynamic))
    print "psamp2AggInjectStatic:" + str(len(psamp2AggInjectStatic))
    print "psamp2AggInjectDynamic:" + str(len(psamp2AggInjectDynamic))
    print "psamp2CoreDropStatic:" + str(len(psamp2CoreDropStatic))
    print "psamp2CoreDropDynamic:" + str(len(psamp2CoreDropDynamic))
    print "psamp2CoreInjectStatic:" + str(len(psamp2CoreInjectStatic))
    print "psamp2CoreInjectDynamic:" + str(len(psamp2CoreInjectDynamic))
    print "samplingRate=0.0139"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggDrop).read()))
    psamp3AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp3AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggInject).read()))
    psamp3AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp3AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreDrop).read()))
    psamp3CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp3CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreInject).read()))
    psamp3CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp3CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp3AggDropStatic:" + str(len(psamp3AggDropStatic))
    print "psamp3AggDropDynamic:" + str(len(psamp3AggDropDynamic))
    print "psamp3AggInjectStatic:" + str(len(psamp3AggInjectStatic))
    print "psamp3AggInjectDynamic:" + str(len(psamp3AggInjectDynamic))
    print "psamp3CoreDropStatic:" + str(len(psamp3CoreDropStatic))
    print "psamp3CoreDropDynamic:" + str(len(psamp3CoreDropDynamic))
    print "psamp3CoreInjectStatic:" + str(len(psamp3CoreInjectStatic))
    print "psamp3CoreInjectDynamic:" + str(len(psamp3CoreInjectDynamic))

    print "psamp3AggInjectStatic:" + str(psamp3AggInjectStatic)
    print "psamp3CoreInjectStatic:" + str(psamp3CoreInjectStatic)
    print "plotAttacks()"
    print "plotAttacks()"
    fig = plt.figure(figCounter)
    ax = plt.subplot(figSubplot)
    # First theoretical nos.
    i = 0.0001
    s = 0.0020
    x = 0
    xpoints = []
    x1points = []
    while s <= 0.0140:
        plt.plot(x, formalAnalysis(s, 1, 3, 20),  marker='+', linestyle='', color=u'#8da0cb')
        plt.plot(x, formalAnalysis(s, 2, 2, 20), marker='x', linestyle='', color=u'#e68ac3')
        if x == 6:
            ax.annotate('Agg. switch (theoretical)', xy=(x, formalAnalysis(s, 1, 3, 20)), xycoords='data',
                        xytext=(x + 16, formalAnalysis(s, 1, 3, 20)-100), arrowprops=dict(arrowstyle="->"))
        if x == 2:
            ax.annotate('Core switch (theoretical)', xy=(x, formalAnalysis(s, 2, 2, 20)), xycoords='data',
                        xytext=(x + 20, formalAnalysis(s, 2, 2, 20)-100), arrowprops=dict(arrowstyle="->"))
        # print "s: " + str(s)
        if str(s) == str(0.0046):
            xpoints.append(x)
            # x1points.append(x)
        if str(s) == str(0.0092):
            xpoints.append(x)
            # x1points.append(x)
        if str(s) == str(0.0139):
            xpoints.append(x)
            # x1points.append(x)
        #if str(s) == str(0.0030):
        #    x1points.append(x)
        if str(s) == str(0.0040):
            x1points.append(x)
        #if str(s) == str(0.0050):
        #    x1points.append(x)
        if str(s) == str(0.0060):
            x1points.append(x)
        #if str(s) == str(0.0070):
        #    x1points.append(x)
        if str(s) == str(0.0080):
            x1points.append(x)
        #if str(s) == str(0.0090):
        #    x1points.append(x)
        if str(s) == str(0.0100):
            x1points.append(x)
        #if str(s) == str(0.0110):
        #    x1points.append(x)
        if str(s) == str(0.0120):
            x1points.append(x)
        #if str(s) == str(0.0130):
        #    x1points.append(x)
        if str(s) == str(0.0140):
            x1points.append(x)
        s += i
        x += 1
    print "xlist: " + str(xpoints)

    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)

    data = []
    for attack in [baseAggInjectStatic, psamp2AggInjectStatic, psamp3AggInjectStatic]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(xpoints, data, marker='P', linestyle='', color=colorIter.next())

    ax.annotate('Agg. switch (experimental)', xy=(xpoints[0], data[0]), xycoords='data',
                xytext=(xpoints[0]+15, data[0]), arrowprops=dict(arrowstyle="->"))
    data = []
    for attack in [baseCoreInjectStatic, psamp2CoreInjectStatic, psamp3CoreInjectStatic]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(xpoints, data, marker='X', linestyle='', color=colorIter.next())

    ax.annotate('Core switch (experimental)', xy=(xpoints[0], data[0]), xycoords='data',
                xytext=(xpoints[0]+15, data[0]-105), arrowprops=dict(arrowstyle="->"))

    xpoints.reverse()
    xpoints.append(0)
    xpoints.reverse()
    x1points.reverse()
    x1points.append(0)
    x1points.reverse()
    # tickMarks = xpoints
    # marks = ['~0.2%', '~0.46%', '~0.92%', '~1.3%']
    # plt.xticks(tickMarks, tuple(marks))
    tickMarks = x1points
    marks = ['.2', '.3', '.4', '.46', '.5', '.6', '.7', '.8', '.9', '.92', '1.0', '1.1', '1.2', '1.3', '1.39', '1.4']
    marks = ['0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4']
    marks = ['0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4']
    plt.xticks(tickMarks, tuple(marks))
    plt.ylabel('Packets sent till detection')
    plt.xlabel('Sampling ratio (%)')
    box = ax.get_position()
    ax.set_position([box.x0 * 1.3, box.y0 + box.height * 0.21 , box.width * 1., box.height * 0.84])
    # plt.show()
    # plt.close()
    resultsFile = "pureIndependentPairAssignmentDontAttackSamples/allPsampsWithInjectDifferentHashDetectionTimeMeansScatterMoreTheory.pdf"
    plt.savefig(resultsPath + resultsFile)

if __name__ == "__main__":
    print "Uncomment the function to plot one by one."
    # plotAllPsamps()
    # plotCompareNoEdgeSamplingWithEdgeSampling()

    # plotPathLengthVsDetectionTime()
    # checkSeeds()
    # plotCollusionTwoThreeAttackersCase1()
    # plotCollusionTwoThreeAttackersCase1Scatter()
    # plotAllPsampsScatter()
    # plotCollusionTwoThreeAttackersCase1ScatterMoreTheory()

#####

def plotAllPsampsScatter():
    print "plotAllPsamps()"
    print "Baseline"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggDrop).read()))
    baseAggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    baseAggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggInject).read()))
    baseAggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    baseAggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreDrop).read()))
    baseCoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    baseCoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreInject).read()))
    baseCoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    baseCoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "baseAggDropStatic:" + str(len(baseAggDropStatic))
    print "baseAggDropDynamic:" + str(len(baseAggDropDynamic))
    print "baseAggInjectStatic:" + str(len(baseAggInjectStatic))
    print "baseAggInjectDynamic:" + str(len(baseAggInjectDynamic))
    print "baseCoreDropStatic:" + str(len(baseCoreDropStatic))
    print "baseCoreDropDynamic:" + str(len(baseCoreDropDynamic))
    print "baseCoreInjectStatic:" + str(len(baseCoreInjectStatic))
    print "baseCoreInjectDynamic:" + str(len(baseCoreInjectDynamic))
    print "samplingRate=0.0092"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggDrop).read()))
    psamp2AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp2AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggInject).read()))
    psamp2AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp2AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreDrop).read()))
    psamp2CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp2CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreInject).read()))
    psamp2CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp2CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp2AggDropStatic:" + str(len(psamp2AggDropStatic))
    print "psamp2AggDropDynamic:" + str(len(psamp2AggDropDynamic))
    print "psamp2AggInjectStatic:" + str(len(psamp2AggInjectStatic))
    print "psamp2AggInjectDynamic:" + str(len(psamp2AggInjectDynamic))
    print "psamp2CoreDropStatic:" + str(len(psamp2CoreDropStatic))
    print "psamp2CoreDropDynamic:" + str(len(psamp2CoreDropDynamic))
    print "psamp2CoreInjectStatic:" + str(len(psamp2CoreInjectStatic))
    print "psamp2CoreInjectDynamic:" + str(len(psamp2CoreInjectDynamic))
    print "samplingRate=0.0139"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggDrop).read()))
    psamp3AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp3AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggInject).read()))
    psamp3AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp3AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreDrop).read()))
    psamp3CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp3CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreInject).read()))
    psamp3CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp3CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp3AggDropStatic:" + str(len(psamp3AggDropStatic))
    print "psamp3AggDropDynamic:" + str(len(psamp3AggDropDynamic))
    print "psamp3AggInjectStatic:" + str(len(psamp3AggInjectStatic))
    print "psamp3AggInjectDynamic:" + str(len(psamp3AggInjectDynamic))
    print "psamp3CoreDropStatic:" + str(len(psamp3CoreDropStatic))
    print "psamp3CoreDropDynamic:" + str(len(psamp3CoreDropDynamic))
    print "psamp3CoreInjectStatic:" + str(len(psamp3CoreInjectStatic))
    print "psamp3CoreInjectDynamic:" + str(len(psamp3CoreInjectDynamic))

    print "psamp3AggInjectStatic:" + str(psamp3AggInjectStatic)
    print "psamp3CoreInjectStatic:" + str(psamp3CoreInjectStatic)
    print "plotAttacks()"
    fig = plt.figure(figCounter)
    ax = plt.subplot(figSubplot)
    baselineP_pa_agg=formalAnalysis(0.004638671875, 1, 3, 20)
    psamp2P_pa_agg=formalAnalysis(0.004638671875*2, 1, 3, 20)
    psamp3P_pa_agg=formalAnalysis(0.004638671875*3, 1, 3, 20)
    baselineP_pa_core=formalAnalysis(0.004638671875, 2, 2, 20)
    psamp2P_pa_core=formalAnalysis(0.004638671875*2, 2, 2, 20)
    psamp3P_pa_core=formalAnalysis(0.004638671875*3, 2, 2, 20)
    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)
    xpoints = [0, 1, 2]

    data = []
    for attack in [baseAggInjectStatic, psamp2AggInjectStatic, psamp3AggInjectStatic]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(xpoints, data, marker='+', linestyle='', color=colorIter.next())
    ax.annotate('Agg. switch (experimental)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))
    data = []
    for attack in [baseCoreInjectStatic, psamp2CoreInjectStatic, psamp3CoreInjectStatic]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(xpoints, data, marker='x', linestyle='', color=colorIter.next())
    ax.annotate('Core switch (experimental)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))

    data = [baselineP_pa_agg, psamp2P_pa_agg, psamp3P_pa_agg]
    plt.plot(xpoints, data, marker='P', linestyle='', color=colorIter.next())
    ax.annotate('Agg. switch (theoretical)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))
    data = [baselineP_pa_core, psamp2P_pa_core, psamp3P_pa_core]
    plt.plot(xpoints, data, marker='X', linestyle='', color=colorIter.next())
    ax.annotate('Core switch (theoretical)', xy=(0.025, data[0]), xycoords='data',
                xytext=(0.2, data[0]-25), arrowprops=dict(arrowstyle="->"))

    tickMarks = xpoints
    marks = ['~0.4%', '~0.9%', '~1.3%']
    plt.xticks(tickMarks, tuple(marks))
    plt.ylabel('Packets sent till detection')
    plt.xlabel('Sampling ratio')
    box = ax.get_position()
    ax.set_position([box.x0 * 1.3, box.y0 + box.height * 0.21 , box.width * 1., box.height * 0.84])
    resultsFile = "pureIndependentPairAssignmentDontAttackSamples/allPsampsWithInjectDifferentHashDetectionTimeMeansScatter.pdf"
    plt.savefig(resultsPath + resultsFile)

def plotCollusionTwoThreeAttackersCase1ScatterMoreTheory():
    print "plotCollusionTwoThreeAttackersCase1"
    print "Agg: 021_221, Mirror (Inject). Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggMirrorCollusionCase1).read()))
    psamp1AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp1AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggMirrorCollusionCase1).read()))
    psamp2AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp2AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggMirrorCollusionCase1).read()))
    psamp3AggInjectCollusion2Static = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[0], attacks[1])
    psamp3AggInjectCollusion2Dynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[0], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusion2Static))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusion2Dynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusion2Static))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusion2Dynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusion2Static))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusion2Dynamic))

    baselineP_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875, 2, 2, 20)
    psamp2P_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875*2, 2, 2, 20)
    psamp3P_pa_agg_collusion2 = 1.0/formalAnalysisCollusion(0.004638671875*3, 2, 2, 20)

    detectionTimeDict = dict(json.loads(open(dataPath + psamp1AggCoreMirrorCollusionCase1).read()))
    psamp1AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp1AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])
    # baselineAggInjectCollusionStatic = []
    # baselineAggInjectCollusionDynamic = []

    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggCoreMirrorCollusionCase1).read()))
    psamp2AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp2AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggCoreMirrorCollusionCase1).read()))
    psamp3AggInjectCollusion3Static = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], colludingPositions[1], attacks[1])
    psamp3AggInjectCollusion3Dynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], colludingPositions[1], attacks[1])

    print "Check the data first!"
    print "psamp1AggInjectCollusionStatic:"
    print str(len(psamp1AggInjectCollusion3Static))
    print "psamp1AggInjectCollusionDynamic:"
    print str(len(psamp1AggInjectCollusion3Dynamic))
    print "psamp2AggInjectCollusionStatic:"
    print str(len(psamp2AggInjectCollusion3Static))
    print "psamp2AggInjectCollusionDynamic:"
    print str(len(psamp2AggInjectCollusion3Dynamic))
    print "psamp3AggInjectCollusionStatic:"
    print str(len(psamp3AggInjectCollusion3Static))
    print "psamp3AggInjectCollusionDynamic:"
    print str(len(psamp3AggInjectCollusion3Dynamic))

    # for collusion: formalAnalysis(0.0046, 1, 2, 20) = 1926.72829979
    # for collusion: formalAnalysis(0.0092, 1, 2, 20) = 902.870006964
    # for collusion: formalAnalysis(0.0139, 1, 2, 20) = 561.585977783
    baselineP_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875, 2, 1, 20, 1)
    psamp2P_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875*2, 2, 1, 20, 1)
    psamp3P_pa_agg_collusion3 = 1/formalAnalysisCollusion3Attackers(0.004638671875*3, 2, 1, 20, 1)

    print "plotAttacks()"
    fig = plt.figure(figCounter)
    ax = plt.subplot(figSubplot)

    # First theoretical nos.
    i = 0.0001
    s = 0.0020
    x = 0
    xpoints = []
    x1points = []
    while s <= 0.0140:
        plt.plot(x, 1/formalAnalysisCollusion(s, 2, 2, 20),  marker='+', linestyle='', color=u'#8da0cb')
        plt.plot(x, 1/formalAnalysisCollusion3Attackers(s, 2, 1, 20, 1), marker='x', linestyle='', color=u'#e68ac3')
        if x == 4:
            ax.annotate('Two switches (theoretical)', xy=(x, 1/formalAnalysisCollusion(s, 2, 2, 20)), xycoords='data',
                        xytext=(x + 16, 900), arrowprops=dict(arrowstyle="->"))
        if x == 2:
            ax.annotate('Three switches (theoretical)', xy=(x, 1/formalAnalysisCollusion3Attackers(s, 2, 1, 20, 1)), xycoords='data',
                        xytext=(x + 20, 1300), arrowprops=dict(arrowstyle="->"))
        # print "s: " + str(s)
        if str(s) == str(0.0046):
            xpoints.append(x)
            # x1points.append(x)
        if str(s) == str(0.0092):
            xpoints.append(x)
            # x1points.append(x)
        if str(s) == str(0.0139):
            xpoints.append(x)
            # x1points.append(x)
        #if str(s) == str(0.0030):
        #    x1points.append(x)
        if str(s) == str(0.0040):
            x1points.append(x)
        #if str(s) == str(0.0050):
        #    x1points.append(x)
        if str(s) == str(0.0060):
            x1points.append(x)
        #if str(s) == str(0.0070):
        #    x1points.append(x)
        if str(s) == str(0.0080):
            x1points.append(x)
        #if str(s) == str(0.0090):
        #    x1points.append(x)
        if str(s) == str(0.0100):
            x1points.append(x)
        #if str(s) == str(0.0110):
        #    x1points.append(x)
        if str(s) == str(0.0120):
            x1points.append(x)
        #if str(s) == str(0.0130):
        #    x1points.append(x)
        if str(s) == str(0.0140):
            x1points.append(x)
        s += i
        x += 1
    print "xlist: " + str(xpoints)

    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)

    data = []
    for attack in [psamp1AggInjectCollusion2Static, psamp2AggInjectCollusion2Static, psamp3AggInjectCollusion2Static]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(xpoints, data, marker='P', linestyle='', color=colorIter.next())
    ax.annotate('Two switches (Experimental)', xy=(xpoints[0], data[0]), xycoords='data',
                xytext=(xpoints[0]+15, data[0]-30), arrowprops=dict(arrowstyle="->"))
    data = []
    for attack in [psamp1AggInjectCollusion3Static, psamp2AggInjectCollusion3Static, psamp3AggInjectCollusion3Static]:
        total = 0
        for p in attack:
            total += p
        average = total / len(attack)
        data.append(average)
    plt.plot(xpoints, data, marker='X', linestyle='', color=colorIter.next())
    ax.annotate('Three switches (Experimental)', xy=(xpoints[0], data[0]), xycoords='data',
                xytext=(xpoints[0]+15, data[0]-30), arrowprops=dict(arrowstyle="->"))

    xpoints.reverse()
    xpoints.append(0)
    xpoints.reverse()
    x1points.reverse()
    x1points.append(0)
    x1points.reverse()
    # tickMarks = xpoints
    # marks = ['0.2', '0.46', '0.92', '1.3']
    # plt.xticks(tickMarks, tuple(marks))
    tickMarks = x1points
    marks = ['.2', '.3', '.4', '.46', '.5', '.6', '.7', '.8', '.9', '.92', '1.0', '1.1', '1.2', '1.3', '1.39', '1.4']
    marks = ['0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1.0', '1.1', '1.2', '1.3', '1.4']
    marks = ['0.2', '0.4', '0.6', '0.8', '1.0', '1.2', '1.4']
    plt.xticks(tickMarks, tuple(marks))
    plt.ylabel('Packets sent till detection')
    plt.xlabel('Sampling ratio (%)')
    box = ax.get_position()
    ax.set_position([box.x0 * 1.3, box.y0 + box.height * 0.21 , box.width * 1., box.height * 0.84])
    # plt.show()
    # plt.close()
    resultsFile = "collusionCase1PureIndependentPairAssignment/allPsampsCollusionTwoThreeDetectionTimeCase1MeansScatterMoreTheory.pdf"
    plt.savefig(resultsPath + resultsFile)
 
def formalAnalysis(p, B, A, n):
    # print "formalAnalysis()"
    # print "p=" + str(p)

    def colissions(a, b, T):
        # print "cols =", a * b / T
        return a * b / T

    D = 4096.0
    # print "D =", D
    factorial = lambda x: x * factorial(x - 1)
    exp_pairs = lambda A, B: A * B
    imp_pairs = lambda A, B: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, D)

    P_pa = lambda A, B: 1 - (1 - p / (n - 1)) ** (exp_pairs(A, B) + imp_pairs(A, B))
    P_pa = P_pa(A, B)
    # print "For static drop considering implicit pairs:"
    # print "for agg: P_pa=", P_pa, "avg pkts", 1 / P_pa
    return 1 / P_pa

def formalAnalysisCollusion(p, B, A, n):
    # print "formalAnalysis()"
    # print "p=" + str(p)

    def colissions(a, b, T):
        # print "cols =", a * b / T
        return a * b / T

    D = 4096.0
    # print "D =", D
    factorial = lambda x: x * factorial(x - 1)
    exp_pairs = lambda A, B: A * B
    between_after_pairs = lambda A, B: A * B
    imp_pairs = lambda A, B: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, D)

    P_pa = lambda A, B: 1 - (1 - p / (n - 1)) ** (exp_pairs(A, B) + imp_pairs(A, B))
    P_pa1 = P_pa(A, B)
    P_pa2 = P_pa(A, B)
    collusion_P_pa = P_pa1 + P_pa2
    # collusion_P_pa = P_pa(2,1)
    # print "For static drop considering implicit pairs:"
    # print "for agg: P_pa=", P_pa, "avg pkts", 1 / P_pa
    return collusion_P_pa

def formalAnalysisCollusion3Attackers(p, B, A, n, After):
    # print "formalAnalysis()"
    # print "p=" + str(p)

    def colissions(a, b, T):
        # print "cols =", a * b / T
        return a * b / T

    D = 4096.0
    # print "D =", D
    factorial = lambda x: x * factorial(x - 1)
    exp_pairs = lambda A, B: A * B
    between_after_pairs = lambda A, B: A * B
    imp_pairs = lambda A, B: colissions(A * (n - B - A) + A * (A - 1) / 2, B * (n - B - A) + B * (B - 1) / 2, D)

    P_pa = lambda A, B: 1 - (1 - p / (n - 1)) ** (exp_pairs(A, B) + imp_pairs(A, B))
    P_pa1 = P_pa(A, B)
    P_pa2 = P_pa(A, B)
    P_pa3 = P_pa(A, B)
    collusion_P_pa = P_pa1 + P_pa2 + P_pa3
    # collusion_P_pa = P_pa(1,1)
    # print "For static drop considering implicit pairs:"
    # print "for agg: P_pa=", P_pa, "avg pkts", 1 / P_pa
    return collusion_P_pa

def checkSeeds():
    print "checkSeeds()"
    allSeeds = range(1001, 1101)
    allSeeds = set(allSeeds)
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggDrop).read()))
    psamp1SeedsStatic = getSeeds(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0],
                                 attackPositions[0], attacks[0])
    psamp1SeedsDynamic = getSeeds(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1],
                                 attackPositions[0], attacks[0])
    print "psamp1SeedsStatic Missing seeds are:" + str(allSeeds - psamp1SeedsStatic)
    print "psamp1SeedsDynamic Missing seeds are:" + str(allSeeds - psamp1SeedsDynamic)

#     detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggMirrorCollusionCase1).read()))
#     psamp2SeedsStatic = getSeeds(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0],
#                                  colludingPositions[0], attacks[1])
#     psamp2SeedsDynamic = getSeeds(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1],
#                                   colludingPositions[0], attacks[1])
#     print "psamp2SeedsStatic Missing seeds are:" + str(allSeeds - psamp2SeedsStatic)
#     print "psamp2SeedsDynamic Missing seeds are:" + str(allSeeds - psamp2SeedsDynamic)
# 
#     detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggMirrorCollusionCase1).read()))
#     psamp3SeedsStatic = getSeeds(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0],
#                                  colludingPositions[0], attacks[1])
#     psamp3SeedsDynamic = getSeeds(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1],
#                                   colludingPositions[0], attacks[1])
#     print "psamp3SeedsStatic Missing seeds are:" + str(allSeeds - psamp3SeedsStatic)
#     print "psamp3SeedsDynamic Missing seeds are:" + str(allSeeds - psamp3SeedsDynamic)


def plotAllPsamps():
    print "plotAllPsamps()"
    print "Baseline"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggDrop).read()))
    baseAggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    baseAggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineAggInject).read()))
    baseAggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    baseAggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreDrop).read()))
    baseCoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    baseCoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + baselineCoreInject).read()))
    baseCoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    baseCoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[0], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "baseAggDropStatic:" + str(len(baseAggDropStatic))
    print "baseAggDropDynamic:" + str(len(baseAggDropDynamic))
    print "baseAggInjectStatic:" + str(len(baseAggInjectStatic))
    print "baseAggInjectDynamic:" + str(len(baseAggInjectDynamic))
    print "baseCoreDropStatic:" + str(len(baseCoreDropStatic))
    print "baseCoreDropDynamic:" + str(len(baseCoreDropDynamic))
    print "baseCoreInjectStatic:" + str(len(baseCoreInjectStatic))
    print "baseCoreInjectDynamic:" + str(len(baseCoreInjectDynamic))
    print "samplingRate=0.0092"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggDrop).read()))
    psamp2AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp2AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2AggInject).read()))
    psamp2AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp2AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreDrop).read()))
    psamp2CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp2CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp2CoreInject).read()))
    psamp2CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp2CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[1], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp2AggDropStatic:" + str(len(psamp2AggDropStatic))
    print "psamp2AggDropDynamic:" + str(len(psamp2AggDropDynamic))
    print "psamp2AggInjectStatic:" + str(len(psamp2AggInjectStatic))
    print "psamp2AggInjectDynamic:" + str(len(psamp2AggInjectDynamic))
    print "psamp2CoreDropStatic:" + str(len(psamp2CoreDropStatic))
    print "psamp2CoreDropDynamic:" + str(len(psamp2CoreDropDynamic))
    print "psamp2CoreInjectStatic:" + str(len(psamp2CoreInjectStatic))
    print "psamp2CoreInjectDynamic:" + str(len(psamp2CoreInjectDynamic))
    print "samplingRate=0.0139"
    print "Agg: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggDrop).read()))
    psamp3AggDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[0])
    psamp3AggDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3AggInject).read()))
    psamp3AggInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[0], attacks[1])
    psamp3AggInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[0], attacks[1])
    print "Core: Drop and Inject. Assignment: Static and Dynamic."
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreDrop).read()))
    psamp3CoreDropStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[0])
    psamp3CoreDropDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[0])
    detectionTimeDict = dict(json.loads(open(dataPath + psamp3CoreInject).read()))
    psamp3CoreInjectStatic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[0], attackPositions[1], attacks[1])
    psamp3CoreInjectDynamic = getDetectionData(detectionTimeDict, samplingRatios[2], hashFunctions[0], assignments[1], attackPositions[1], attacks[1])
    print "No. of attack data points are:"
    print "psamp3AggDropStatic:" + str(len(psamp3AggDropStatic))
    print "psamp3AggDropDynamic:" + str(len(psamp3AggDropDynamic))
    print "psamp3AggInjectStatic:" + str(len(psamp3AggInjectStatic))
    print "psamp3AggInjectDynamic:" + str(len(psamp3AggInjectDynamic))
    print "psamp3CoreDropStatic:" + str(len(psamp3CoreDropStatic))
    print "psamp3CoreDropDynamic:" + str(len(psamp3CoreDropDynamic))
    print "psamp3CoreInjectStatic:" + str(len(psamp3CoreInjectStatic))
    print "psamp3CoreInjectDynamic:" + str(len(psamp3CoreInjectDynamic))

    print "psamp3AggInjectStatic:" + str(psamp3AggInjectStatic)
    print "psamp3CoreInjectStatic:" + str(psamp3CoreInjectStatic)
    print "plotAttacks()"
    resultsFile = "pureIndependentPairAssignmentDontAttackSamples/allPsampsWithInjectDifferentHashDetectionTime.pdf"
    fig = plt.figure(figCounter)
    ax = plt.subplot(figSubplot)
    data = [baseAggDropStatic, psamp2AggDropStatic, psamp3AggDropStatic,
            baseAggInjectStatic, psamp2AggInjectStatic, psamp3AggInjectStatic,
            baseAggDropDynamic, psamp2AggDropDynamic, psamp3AggDropDynamic,
            baseAggInjectDynamic, psamp2AggInjectDynamic, psamp3AggInjectDynamic,
            baseCoreDropStatic, psamp2CoreDropStatic, psamp3CoreDropStatic,
            baseCoreInjectStatic, psamp2CoreInjectStatic, psamp3CoreInjectStatic,
            baseCoreDropDynamic, psamp2CoreDropDynamic, psamp3CoreDropDynamic,
            baseCoreInjectDynamic, psamp2CoreInjectDynamic, psamp3CoreInjectDynamic,
            ]
    meanpointprops = dict(marker='*', markeredgecolor='black',
                          markerfacecolor='#2DCDC0')
    medianpointprops = dict(marker='', linestyle='')
    bp = plt.boxplot(data, patch_artist=True, showmeans=True, meanline=False, meanprops=meanpointprops, medianprops=medianpointprops)

    colors = ['#3D9970', '#FF9136', '#FFC51B']
    k = 0
    for patch in bp['boxes']:
        i = k % 3
        patch.set_facecolor(colors[i])
        plt.setp(bp['whiskers'], color='black', linestyle='--')
        plt.setp(bp['fliers'], color='black', marker='+')
        k += 1
    plt.ylabel('Packet sent till detection')
    # plt.xlabel('Attack and Assignment')
    c = 0
    ax.text(c+5, 24120.0, u'Aggregate Switch')
    ax.text(c+17, 24120.0, u'Core Switch')
    offset = 3.5
    for i in range(1, 8):
        plt.plot([offset, offset], [-1, 100000], color='#000000')
        offset += 3
    plt.plot([12.5, 12.5], [-1, 20000], lw=1.5, color='white')
    plt.plot([12.5,12.5], [-1,20000], lw=1.5, color='black')
    plt.plot([12.45,12.45], [-1,20000], lw=.25, color='black')
    baselineP_pa_agg=formalAnalysis(0.004638671875, 1, 3, 20)
    psamp2P_pa_agg=formalAnalysis(0.004638671875*2, 1, 3, 20)
    psamp3P_pa_agg=formalAnalysis(0.004638671875*3, 1, 3, 20)
    baselineP_pa_core=formalAnalysis(0.004638671875, 2, 2, 20)
    psamp2P_pa_core=formalAnalysis(0.004638671875*2, 2, 2, 20)
    psamp3P_pa_core=formalAnalysis(0.004638671875*3, 2, 2, 20)

    plt.axhline(y=baselineP_pa_agg, xmin=0, xmax=2.0/8.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    plt.axhline(y=baselineP_pa_core, xmin=4.0/8.0, xmax=6.0/8.0, linestyle='-', color=colors[0], marker=markerStyles[0])
    plt.axhline(y=psamp2P_pa_agg, xmin=0, xmax=2.0/8.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    plt.axhline(y=psamp2P_pa_core, xmin=4.0/8.0, xmax=6.0/8.0, linestyle='-', color=colors[1], marker=markerStyles[1])
    plt.axhline(y=psamp3P_pa_agg, xmin=0, xmax=2.0/8.0, linestyle='-', color=colors[2], marker=markerStyles[2])
    plt.axhline(y=psamp3P_pa_core, xmin=4.0/8.0, xmax=6.0/8.0, linestyle='-', color=colors[2], marker=markerStyles[2])

    tickMarks = [2, 5, 8, 11, 14, 17, 20, 23]
    marks = ['Drop', 'Inject', 'Drop', 'Inject',
             'Drop', 'Inject', 'Drop', 'Inject',
             'Drop', 'Inject', 'Drop', 'Inject',
             'Drop', 'Inject', 'Drop', 'Inject']
    plt.xticks(tickMarks, tuple(marks))
    plt.figtext(0.16, 0.15, 'Static', color='black')
    plt.figtext(0.38, 0.15, 'Dynamic', color='black')
    plt.figtext(0.61, 0.15, 'Static', color='black')
    plt.figtext(0.825, 0.15, 'Dynamic', color='black')
    plt.figtext(0.44, 0.10, 'Attack and Assignment', color='black')

    box = ax.get_position()
    ax.set_yscale('log')
    ax.set_ylim((0,20000))
    ax.set_position([box.x0 * 0.6, box.y0 + box.height * 0.21 , box.width * 1.15, box.height * 0.84])
    ax.yaxis.grid(True, linestyle='-', which='major', color='grey')
    ax.set_axisbelow(True)
    plt.figtext(0.30, 0.018, '$p_s$=0.4\%',
                backgroundcolor=colors[0], color='black')
    plt.figtext(0.50, 0.018, '$p_s$=0.9\%',
                backgroundcolor=colors[1], color='black')
    plt.figtext(0.70, 0.018, '$p_s$=1.3\%',
                backgroundcolor=colors[2], color='black')
    plt.savefig(resultsPath + resultsFile)


def plotCompareNoEdgeSamplingWithEdgeSampling():
    print "plotCompareNoEdgeSamplingWithEdgeSampling()"
    sampRatios20 = []
    sampRatios36 = []
    for i in range(1, 20):
        sampRatios20.append(i*19.0/4096.0)
        sampRatios36.append(i*35.0/4096.0)
    print sampRatios20
    print sampRatios36
    # No. of switches
    totalSwitches = [20, 36]
    # path lengths where the attacker is present
    pathLengths = [5, 7]
    NpathLengthDict = {20: [5], 36: [7]}
    sampRatioDict = {20: sampRatios20, 36: sampRatios36}
    pairs = range(1, 20)
    switchDict = {}

    # Plot parameters
    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)
    markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
    markerIter = iter(markers)
    s = 0
    fig = plt.figure(s + 1)
    # fig = plt.figure(s + 1, figsize=(3.487/2, 2.15512978986403/2))
    subplot = 111
    ax = plt.subplot(subplot)

    switchDict = {}
    wc20 = []
    bc20 = []
    wc36 = []
    bc36 = []
    for p in sampRatios20:
        wc20.append(formalAnalysis(p, 3, 1, 20))
    	bc20.append(formalAnalysis(p, 2, 2, 20))
    for p in sampRatios36:
    	wc36.append(formalAnalysis(p, 4, 2, 36))
    	bc36.append(formalAnalysis(p, 3, 3, 36))
    switchDict[20] = [wc20, bc20]
    switchDict[36] = [wc36, bc36]
    for n in [36, 20]:
        # best case and worst case for each
        for i in range(0,2):
            if i == 0:
                caseLabel = ' (worst)'
            elif i == 1:
                caseLabel = ' (best)'
            if n == 20:
                nLabel = 'No-ext'
            elif n == 36:
                nLabel = 'Ext'
            color=colorIter.next()
            marker=markerIter.next()
            plt.plot(pairs, switchDict[n][i], color=color,
                    label=nLabel+caseLabel, linestyle='', marker=marker)
    ax.set_yscale('log')
    ax.set_xlabel('Hash assignments shared between a pair of switches')
    ax.set_ylabel('Packets till detection')
    box = ax.get_position()
    plt.legend(ncol=2, bbox_to_anchor=(.97, .97))
    ax.set_position([box.x0 + .05, box.y0 + box.height * 0.11 , box.width * 1.0, box.height * 0.95])
    resultsFile= "randomPairAssignment/detectionProbabilityCompareNoEdgeWithEdgeSampling.pdf"
    plt.savefig (resultsPath+resultsFile)

def plotPathLengthVsDetectionTime():
    print "plotPathLengthVsDetectionTime()"
    sampRatios = []
    for i in range(1, 20):
        sampRatios.append(i/100.0)
    pathLengths = range(3, 11)
    N = 54
    pairs = range(1, 20)
    # Create a dict for the best and worst case for a given path length
    bestCaseWorstCasePathLengthsDict = dict.fromkeys(pathLengths)
    for pathLength in bestCaseWorstCasePathLengthsDict.keys():
        worstCase = [1, pathLength - 2]
        if pathLength % 2 == 0:
            mid = pathLength / 2
            bestCase = [mid - 1, pathLength - mid]
        else:
            mid = (pathLength + 1) / 2
            bestCase = [mid - 1, pathLength - mid]
        bestCaseWorstCasePathLengthsDict[pathLength] = [bestCase, worstCase]
    pprint.pprint(bestCaseWorstCasePathLengthsDict)
    # get the detection time for each case and path length and save in a dict.
    detectionTimeDict = dict.fromkeys(pathLengths)
    for pathLength in detectionTimeDict.keys():
        bestCaseList = []
        worstCaseList = []
        for sampRatio in sampRatios:
            bestCase = formalAnalysis(sampRatio,
                                      bestCaseWorstCasePathLengthsDict[pathLength][0][0],
                                      bestCaseWorstCasePathLengthsDict[pathLength][0][1],
                                      N)
            worstCase = formalAnalysis(sampRatio,
                                      bestCaseWorstCasePathLengthsDict[pathLength][1][0],
                                      bestCaseWorstCasePathLengthsDict[pathLength][1][1],
                                      N)
            bestCaseList.append(bestCase)
            worstCaseList.append(worstCase)
        detectionTimeDict[pathLength] = [bestCaseList, worstCaseList]
    pprint.pprint(detectionTimeDict)

    # now plot it
    colors = [u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63',
              u'#66c2a5', u'#fa8e63', u'#8da0cb', u'#e68ac3', u'#a7d854', u'#ffd92f', u'#e4c494', u'#b3b3b3',
              u'#66c2a5', u'#fa8e63']
    colorIter = iter(colors)
    markers = ['o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X']
    markerIter = iter(markers)
    fig = plt.figure(1)
    ax = plt.subplot(111)
    for pathLength in pathLengths:
        print pathLength
        plt.plot(pairs,
                 detectionTimeDict[pathLength][1],
                 color=colorIter.next(),
                 label = str(pathLength),
                 linestyle='',
                 marker=markerIter.next())
    ax.set_yscale('log')
    ax.set_xlabel('Hash assignments shared between a pair of switches')
    ax.set_ylabel('Packets till detection')
    ticks=ax.get_xticks().tolist()
    count=0
    x=[]
    for tick in ticks:
        x.append(str(5*count))
        count +=1
    ax.set_xticklabels(x)
    plt.legend(ncol=4, title="Path lengths", bbox_to_anchor=(.97, .97))
    box = ax.get_position()
    ax.set_position([box.x0 + .05, box.y0 + box.height * 0.11 , box.width * 1.0, box.height * 0.97])
    resultsFile = "./results/randomPairAssignment/detectionProbabilityPathLengthsWorstCase.pdf"
    plt.savefig(resultsFile)


