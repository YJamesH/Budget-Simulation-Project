from random import randrange
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

# --------------------------------------------------- #
# FUNCTIONS

# PMT 
def pmtCalc(rate, term, price):
    result = 0
    rateAcc = pow((1+rate),term)
    if rate==0:
        result = int(price/term)
    else:
        result = int((rate*price*rateAcc) / (rateAcc-1))
    return result

# Millions simplifier for graphing
def millions(x, pos):
    # x = value and pos = tick position
    return '$%1.1f' % (x * 1e-6)

# Thousands simplifier for graphing
def thousands(x, pos):
    return '%1.1f' % (x * 1e-3)

# --------------------------------------------------- #

if __name__ == '__main__':

    # --------------------------------------------------- #
    # INPUTS 

    # # Contract Inputs
    # deploymentYear = int(input("Deployment Year: "))
    # contractTerm = int(input("Contract Term (years): ")) # Contract Term/Life of Bus
    # contractEsc = .03                                    # 3%/year
    # contractPrice = 30000                                # 30k bus/year

    # # User Info Inputs
    # annualBudget = int(input("Annual budget: "))              # Total Annual Budget ~60m
    # annualBudgetSal = 46255860                                # ~67% Annual Budget -> Salaries    
    # annualBudgetCap = 3000000                                 # ~17% Annual Budget -> Capital Cost
    # annualBudgetOp = 10638130                                 # ~17% Annual Budget -> Operating Costs
    # fleetSize = int(input("Total Fleet Size: "))              # Total Fleet Size 
    # annualMiles = int(input("Annual mileage: "))              # Annual miles driven
    # weightedMPG = float(input("MPG: "))                       # Average mpg
    # fuelPriceGal = float(input("Fuel price $/gal: "))         # $/gallon fuel average
    # MRCost = int(input("Maintenance & Repair Year 1 Cost: ")) # M&R base cost
    
    # # Diesel Info Inputs
    # dieselPrice = int(input("Diesel Bus Purchase Price: "))  # Price of 1 Diesel Bus ~120k
    # dieselRate = float(input("Diesel Bus Financing Rate: ")) # _%/year ~2%/year
    # dieselTerm = int(input("Diesel Bus Financing Term: "))   # Years to Finance Bus

    # dieselPriceEsc = .05                             # Diesel Price escalator 5%
    # overheadAllocation = .15                         # Overhead Cost Allocation 15%
    # costEsc = .02                                    # Other costs escalator (M&R, fuel, overhead,...)
    # MREsc1 = .06                                     # M&R escalator in first half-life
    # MREsc2 = .08                                     # M&R escalator in second half-life

    # --------------------------------------------------- #
    # Coded Inputs for Testing 

    # Contract Inputs
    deploymentYear = 2023
    contractTerm = 15                                # Contract Term/Life of Bus
    contractEsc = .03                                # 3%/year
    contractPrice = 30000                            # 30k bus/year
    # User Info Inputs  **CHANGE TO PERCENTAGES**
    annualBudget = 59893990                          # Total Annual Budget ~60m
    annualBudgetSal = 46255860                       # ~67% Annual Budget -> Salaries    
    annualBudgetCap = 3000000                        # ~17% Annual Budget -> Capital Cost
    annualBudgetOp = 10638130                        # ~17% Annual Budget -> Operating Costs

    fleetSize = 800                                  # Total Fleet Size 
    annualMiles = 9000                               # Annual miles driven
    weightedMPG = 6                                  # Average mpg
    fuelPriceGal = 2.5                               # $/gallon fuel
    MRCost = 6000                                    # M&R base cost
    # Diesel Info Inputs
    dieselPrice = 120000                             # Price of 1 Diesel Bus ~120k
    dieselRate = .03                                 # _%/year ~2%/year
    dieselTerm = 3                                   # Years to Finance Bus
    dieselPriceEsc = .05                             # Diesel Price escalator 5%
    overheadAllocation = .15                         # Overhead Cost Allocation 15%
    costEsc = .02                                    # Other costs escalator (M&R, fuel, overhead,...)
    MREsc1 = .06                                     # M&R escalator in first half-life
    MREsc2 = .08                                     # M&R escalator in second half-life

    # --------------------------------------------------- #
    # Example Highland Contract Illustration  
    #
    #   ***subject to change***
    annualDeployed = [10,20,30,40,
                    67,67,67,67,
                    67,67,67,67,
                    67,67,67,67,
                    67,67,67,67] 
    annualContract = [22000,22000,22000,22000,
                    27000,27000,27000,27000,
                    20000,20000,20000,20000,
                    24000,24000,24000,24000,
                    24000,24000,24000,24000]

    # --------------------------------------------------- #
    # Example Highland Contract Total Budget
    
    contractYearPrice = [0]*20

    for simDepYear in range(20):
        contractPrice = annualDeployed[simDepYear] * annualContract[simDepYear]
        for simAddYear in range(simDepYear, simDepYear+contractTerm):
            if simAddYear == 20:
                break
            contractYearPrice[simAddYear] = int(contractYearPrice[simAddYear] + contractPrice)
            contractPrice = contractPrice * (1+contractEsc)

    print("Contract", contractYearPrice, "\n")

    # --------------------------------------------------- #
    # Diesel Total Cost of Ownership (TCO)

    purchaseTCO = []
    mrTCO = []
    fuelTCO = []
    overheadTCO = []

    # Purchase price with financing
    pmtDieselPrice = pmtCalc(dieselRate, dieselTerm, dieselPrice)
    for i in range(dieselTerm):
        purchaseTCO.append(pmtDieselPrice)


    # Maintenance and Repair
    for i in range(contractTerm):
        # M&R differs in different half lifes
        if i < (contractTerm-1)/2:
            mrTCO.append(int(MRCost*(pow(1+MREsc1,i))))
        else:
            mrTCO.append(int(mrTCO[i-1]*(1+MREsc2)))


    # Fuel
    for i in range(contractTerm):
        fuelTCO.append(int((annualMiles/weightedMPG)*fuelPriceGal*pow((1+costEsc),i)))


    # Overhead
    for i in range(contractTerm):
        overheadTCO.append(int((mrTCO[i]+fuelTCO[i])*overheadAllocation))

    # Prints
    print("TCO", purchaseTCO)
    print("TCO", mrTCO)
    print("TCO", fuelTCO)
    print("TCO", overheadTCO, "\n")

    # --------------------------------------------------- #
    # Diesel Costs avoided  - Break down

    purchaseDCA = [0]*20
    mrDCA = [0]*20
    fuelDCA = [0]*20
    overheadDCA = []

    # Purchase costs avoided
    for simDepYear in range(20):
        currPrice = int(dieselPrice * pow(1+dieselPriceEsc, simDepYear))
        simCost = annualDeployed[simDepYear] * pmtCalc(dieselRate, dieselTerm, currPrice)
        for simAddYear in range(dieselTerm):
            if simDepYear+simAddYear < 20:
                purchaseDCA[simDepYear+simAddYear] = purchaseDCA[simDepYear+simAddYear] + simCost

    # M&R costs avoided
    for simDepYear in range(20):
        currMRCost = MRCost * pow(1+costEsc, simDepYear)
        yearlyMR = currMRCost * annualDeployed[simDepYear]
        for simAddYear in range(simDepYear, simDepYear+contractTerm):
            if simAddYear == 20:
                break
            mrDCA[simAddYear] = int(mrDCA[simAddYear] + yearlyMR)
            if (simAddYear+1-simDepYear) < (contractTerm-1)/2:
                yearlyMR = yearlyMR * (1+MREsc1)
            else:
                yearlyMR = yearlyMR * (1+MREsc2)

    # Fuel costs avoided
    for simDepYear in range(20):
        currFuelCost = fuelTCO[0] * pow(1+costEsc, simDepYear)
        yearlyFuel = currFuelCost * annualDeployed[simDepYear]
        for simAddYear in range(simDepYear, simDepYear+contractTerm):
            if simAddYear == 20:
                break
            fuelDCA[simAddYear] = int(fuelDCA[simAddYear] + yearlyFuel)
            yearlyFuel = yearlyFuel * (1+costEsc)

    # Overhead costs avoided
    for simDepYear in range(20):
        overheadDCA.append(int(overheadAllocation*(fuelDCA[simDepYear] + mrDCA[simDepYear])))

    # Prints
    print("DCA", purchaseDCA)
    print("DCA", mrDCA)
    print("DCA", fuelDCA)
    print("DCA", overheadDCA, "\n")

    # --------------------------------------------------- #
    # Relative Budget Neutrality
    totalDCA = []
    for i in range(20):
        totalDCA.append(purchaseDCA[i] + mrDCA[i] + fuelDCA[i] + overheadDCA[i])

    ### Budget Difference ###
    budgetDiffRBN = []
    for i in range(20):
        budgetDiffRBN.append(totalDCA[i]-contractYearPrice[i])

    ### Total Budget With Highland ###
    budgetStaQuo = []
    finalRBudget = []
    for simDepYear in range(20):
        budgetStaQuo.append(int(annualBudget * pow(1+costEsc, simDepYear)))
    for simDepYear in range(20):
        finalRBudget.append(budgetStaQuo[simDepYear]-budgetDiffRBN[simDepYear])
    
    # maybe make one for individual
    #   budget w/ highland     \
    #   budget w/o highland   --- compare


    # Prints
    print("Total DCA", totalDCA)
    print("Budget Diff", budgetDiffRBN)

    print("Budget Status Quo", budgetStaQuo)
    print("Relative Budget", finalRBudget, "\n")

    # --------------------------------------------------- #
    # bottom-up budget analysis
    evCostReduction = []
    evCostReduction.append(annualDeployed[0]/fleetSize)
    for simDepYear in range(1,20):
        tempPerc = round(evCostReduction[simDepYear-1] + annualDeployed[simDepYear]/fleetSize,3)
        if tempPerc > 100:
            tempPerc = 100
        evCostReduction.append(round(evCostReduction[simDepYear-1] + annualDeployed[simDepYear]/fleetSize,3))
    
    ## Starts one year before deploy (i.e. 2022) ##
    buOperatingSQ = []
    for simDepYear in range(0,21):      
        buOperatingSQ.append(int(annualBudgetOp * pow(1+costEsc, simDepYear))) 
   
    buOperatingCosts = []
    buOperatingCosts.append(buOperatingSQ[0])
    for simDepYear in range(20):   
        tempOpCost = int(buOperatingSQ[simDepYear] * (1-evCostReduction[simDepYear]))
        if tempOpCost < 0:
            tempOpCost = 0
        buOperatingCosts.append(tempOpCost)

    buPersonnelCosts = []
    for simDepYear in range(21):   
        buPersonnelCosts.append(int(annualBudgetSal * pow(1+costEsc, simDepYear)))

    # total minus diesel buses
    buTotalPrice = []
    for i in range(21):
        buTotalPrice.append(int(buOperatingCosts[i] + buPersonnelCosts[i]))
    # total with highland contract
    buTotalPrice[0] = buTotalPrice[0]+annualBudgetCap
    for simDepYear in range(1,21):
        buTotalPrice[simDepYear] = buTotalPrice[simDepYear] + contractYearPrice[simDepYear-1]


    print("Bottom-up Operating Status Quo", buOperatingSQ)
    print("Bottom-up Operating Costs", buOperatingCosts)
    print("Bottom-up Personnel Costs", buPersonnelCosts)

    print("Bottom-up Total", buTotalPrice, "\n")


    

    # --------------------------------------------------- #
    # Carbon Reduction

    CO2DieselConstant = .01018      # Equivalent CO2 emissions per gal of diesel (metric tons)
    CO2GasConstant = .008887        # Equivalent CO2 emissions per gal of gas (metric tons)

    totalDeployed = []              # Cumulative count of EV's deployed
    totalGalAvoided = []            # Total gallons avoided given # of EV's deployed
    annualCarbonReduced = []        # Carbon reduced per specific year
    cumulCarbonReduced = []         # Cumulative Carbon reduced since deployment year

    totalDeployed.append(annualDeployed[0])
    for i in range(1,20):
        totalDeployed.append(totalDeployed[i-1]+annualDeployed[i])
    for i in range(20):
        totalGalAvoided.append((totalDeployed[i]*annualMiles)/weightedMPG)
    for i in range(20):
        annualCarbonReduced.append(CO2DieselConstant*totalGalAvoided[i])
    cumulCarbonReduced.append(round(annualCarbonReduced[0],1))
    for i in range(1,20):
        cumulCarbonReduced.append(round(annualCarbonReduced[i]+cumulCarbonReduced[i-1],1))

    print("Cumulative Carbon Reduced", cumulCarbonReduced, "\n") 

    # --------------------------------------------------- #
    # Graphs and Plots
    
    fig, axes = plt.subplots(nrows = 2, ncols = 2)
    yearsADep = []
    for years in range(deploymentYear, deploymentYear+20):
        yearsADep.append(years)
    yearsWDep = yearsADep.copy()
    yearsWDep.insert(0, deploymentYear-1)
    yearsShown = []
    for years in range(0,21,4):
        yearsShown.append(yearsWDep[years])

    # formatting
    formatMillions = FuncFormatter(millions)
    formatThousands = FuncFormatter(thousands)

    # Figure 1 - Budget Neutral Transition
    plt.sca(axes[0,0])
    plt.plot(yearsADep, budgetStaQuo, 'r', label='Budget SQ')
    plt.plot([], [], 'b', linewidth=5)     # Houston ISD Budget
    plt.plot([], [], 'y', linewidth=5)     # Budget with Highland
    plt.stackplot(yearsADep, finalRBudget, budgetDiffRBN, colors=['b','y'])

    plt.ticklabel_format(style = 'plain')
    axes[0,0].yaxis.set_major_formatter(formatMillions)
    plt.xticks(yearsShown)
    plt.yticks(np.arange(0, 100000000, 10000000))
    plt.ylabel('Millions')
    plt.xlabel('Year')
    plt.legend(["Budget Status Quo", "Budget with Highland", "Budget saved"], loc='lower right')
    plt.title('Budget Neutral Transition')

    # Figure 2 - Bottom Up Budget Analysis
    plt.sca(axes[0,1])
    budgetStaQuo1 = budgetStaQuo.copy()
    budgetStaQuo1.append(int(annualBudget*pow(1+costEsc, 20)))
    plt.plot(yearsWDep, budgetStaQuo1, 'r', label='Budget SQ') ##############################
    plt.bar(yearsWDep, buOperatingCosts, color='m',)
    plt.bar(yearsWDep, buPersonnelCosts, bottom=buOperatingCosts, color='b')
    # Since operating costs and personnel costs are not arrays, need to combine lists
    CYPFormat = contractYearPrice.copy()
    CYPFormat.insert(0,0)
    OpPerSum = []
    for i in range(21):
        OpPerSum.append(buOperatingCosts[i]+buPersonnelCosts[i])
    plt.bar(yearsWDep, CYPFormat, bottom=OpPerSum, color='c')
    plt.bar(deploymentYear-1, annualBudgetCap, bottom=CYPFormat[0]+buOperatingCosts[0]+buPersonnelCosts[0], color='k')

    plt.ticklabel_format(style = 'plain')
    axes[0,1].yaxis.set_major_formatter(formatMillions)
    plt.xticks(yearsShown)
    plt.yticks(np.arange(0, 110000000, 10000000))
    plt.ylabel('Millions')
    plt.xlabel('Year')
    plt.legend(["Budget Status Quo", "Operating Costs", "Personnel Costs", "Highland Contract", "Budget Capital Cost"], bbox_to_anchor=(1, 1))
    plt.title('Bottom Up Analysis')

    # Figure 3 - Carbon Reduction Line Graph 
    plt.sca(axes[1,0])
    plt.plot(yearsADep, cumulCarbonReduced, 'c', label='Expected Carbon Reduction')
    
    plt.ticklabel_format(style = 'plain')
    axes[1,0].yaxis.set_major_formatter(formatThousands)
    plt.xticks(yearsShown)
    yStep = 25000
    CCRyMax = round((cumulCarbonReduced[-1]+ yStep)/yStep) *25000
    plt.yticks(np.arange(0, CCRyMax, yStep))
    plt.ylabel('Metric Tons')
    plt.xlabel('Year')
    plt.legend(loc='upper left')
    plt.title('Cumulative CO2 (M.Ton) Reduced')

    # Figure 4 - Short Term Bottom Up analysis
    

    fiveYearSim = [deploymentYear-1]
    for i in range(6):
        fiveYearSim.append(deploymentYear+i)
    plt.sca(axes[1,1])

    fiveBudgetStaQuo = []
    fiveBuOperatingCosts = []
    fiveBuPersonnelCosts = []
    fiveCYPFormat = []
    for i in range(7):
        fiveBudgetStaQuo.append(budgetStaQuo[i])
        fiveBuOperatingCosts.append(buOperatingCosts[i])
        fiveBuPersonnelCosts.append(buPersonnelCosts[i])
        fiveCYPFormat.append(CYPFormat[i])
    # Insert data into bar graph
    plt.plot(fiveYearSim, fiveBudgetStaQuo, 'r', label='Budget SQ')
    plt.bar(fiveYearSim, fiveBuOperatingCosts, color='m',)
    plt.bar(fiveYearSim, fiveBuPersonnelCosts, bottom=fiveBuOperatingCosts, color='b')

    # Since operating costs and personnel costs are not arrays, need to combine lists
    fiveOpPerSum = []
    for i in range(7):
        fiveOpPerSum.append(fiveBuOperatingCosts[i]+fiveBuPersonnelCosts[i])    
    plt.bar(fiveYearSim, fiveCYPFormat, bottom=fiveOpPerSum, color='c')

    plt.ticklabel_format(style = 'plain')
    axes[1,1].yaxis.set_major_formatter(formatMillions)
    plt.xticks(np.arange(deploymentYear-1, deploymentYear+6, 1))
    plt.yticks(np.arange(0, 100000000, 10000000))
    plt.ylabel('Millions')
    plt.xlabel('Year')
    plt.legend(["Budget Status Quo", "Operating Costs", "Personnel Costs", "Highland Contract"], bbox_to_anchor=(1, 1))
    plt.title('Short Term Bottom Up Analysis')

    
    fig.tight_layout()
    plt.show()

    # --------------------------------------------------- #


    # Statistics summary
    print("\n Summary ")
    print("Annual Budget is ", annualBudget)
    print("Total Fleet Size is ", fleetSize)
    print("Annual mileage with gas is ", annualMiles)
    print("Gas Bus MPG is ", weightedMPG)
    print("Diesel Bus Purchase Price is ", dieselPrice)
    print("Diesel Bus Financing Rate is ", dieselRate)
    print("Diesel Bus Financing Term is ", dieselTerm, "\n")

