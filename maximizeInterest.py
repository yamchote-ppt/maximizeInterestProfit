import pyomo.environ as pyo
import re

def getWeightName(inputDict):
    nameVars = []
    for bankName in inputDict:
        for i in range(len(inputDict[bankName][1])):
            nameVars.append(bankName+str(i+1))
    return nameVars

def getDeltaName(inputDict):
    nameVars = []
    for bankName in inputDict:
        for i in range(len(inputDict[bankName][1])+1):
            nameVars.append(bankName+str(i+1))
    return nameVars

def getDeltaLast(inputDict,principle):
    nameVars = []
    for bankName in inputDict:
        nameVars.append((bankName+str(len(inputDict[bankName][1])+1),principle))
    return nameVars

def getBankConstraint(inputDict):
    nameVars = []
    bounds   = []
    for bankName in inputDict:
        for i in range(len(inputDict[bankName][1])):
            nameVars.append(bankName+str(i+1))
        bounds += [x[0]-x[1] for x in zip(inputDict[bankName][1],[0] + inputDict[bankName][1][:-1])]
    return list(zip(nameVars, bounds))

def rule_lower(m, c, bound):
    return m.w[c]*bound <= m.delta[c]

def rule_upper(m, c, bound):
    if int(c[-1])-1 == 0:
        return m.delta[c] <= bound
    else:
        return m.delta[c] <= bound*m.w[c[:-1] + str(int(c[-1])-1)]
    
def rule_upper_last(m, c, principle):
    if int(c[-1])-1 == 0:
        return m.delta[c] <= principle
    else:
        return m.delta[c] <= principle*m.w[c[:-1] + str(int(c[-1])-1)]

def getInterestRate(inputDict):
    rate = []
    for bankName in inputDict:
        rate += inputDict[bankName][0]
    return rate

def printReport(m,principle,inputDict):
    print(f"Maximum interest = {pyo.value(m.interest)}")
    print(f"Average interest rate = {pyo.value(m.interest)/principle *100:.2f}%")
    print(':==============================:')
    asset_value = {}
    interest = {}
    for rate, bankName in zip(getInterestRate(inputDict),getDeltaName(inputDict)):
        key = re.match(r'(.+)(\d+)',bankName).group(1)
        asset_value[key] = asset_value.get(key,0) + pyo.value(m.delta[bankName])
        interest[key] = interest.get(key,0) + pyo.value(rate*m.delta[bankName])
    # print(asset_value)
    # print(interest)
    print(f'{"":10s} {"amount":^12s} {"interest":^12s}')
    for key in asset_value:
        print(f'{key:>10s}:{asset_value[key]:^12.0f} {interest[key]:^12.0f}')
    print(':==============================:')
    
def optimize(principle,inputDict,verbose=False):
    m = pyo.ConcreteModel()
    m.w     = pyo.Var(getWeightName(inputDict),
                    initialize=0,within=pyo.Binary)
    m.delta = pyo.Var(getDeltaName(inputDict),
                    bounds=(0,principle))
    m.lower  = pyo.Constraint(getBankConstraint(inputDict),rule = rule_lower)
    m.upper  = pyo.Constraint(getBankConstraint(inputDict),rule = rule_upper)
    m.last   = pyo.Constraint(getDeltaLast(inputDict,principle),rule = rule_upper_last)
    m.principle   = pyo.Constraint(expr = sum(m.delta[x] for x in getDeltaName(inputDict)) == principle)
    m.interest = pyo.Objective(expr=sum(x[0]*m.delta[x[1]] for x in zip(getInterestRate(inputDict),getDeltaName(inputDict))),sense = pyo.maximize)
    pyo.SolverFactory("glpk").solve(m)
    
    if verbose:
        printReport(m,principle,inputDict)
        
    return m


if __name__ == "__main__":
    inputDict = {
        'LH':([0.0025, 0.0175,0.0555,0.015,0.0025,0],[100000, 900000, 1000000, 3000000, 100000000]),
        'KPP':([0.02,0.04,0.02,0.0155,0.005],[5000,10000,50000,1500000]),
        'Dime':([0.03,0.015,0.005],[10000,1000000]),
        'CIMBChill': ([0.005,0.018,0.0288,0.002],[10000,50000,100000]),
        'Kept':([0.0175],[]),
        'TTB':([0.022,0.016,0.012],[100000,1000000]),
        'Alpha':([0.02,0.007],[500000]),
        'CIMBSpeed':([0.008,0.0188],[100000]),
    }
    
    m = optimize(5000000,inputDict,True)