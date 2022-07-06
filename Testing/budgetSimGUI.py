# Plotting 
from calendar import c
from csv import excel
from this import s
from webbrowser import BackgroundBrowser
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter
import numpy
import numpy as np
import math

# GUI 
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

# Read Excel
from kiwisolver import Expression
import pandas as pd


def create_budget_graphs(inputs):

    # --------------------------------------------------- #
    # FUNCTIONS

    # PMT 
    def pmtCalc(rate, term, price):
        result = 0
        rateAcc = pow((1+rate),term)
        if rate==0:
            if term==0:
                result = int(price)
            else:
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
    # User Inputs 

    # Contract Inputs
    deploymentYear = inputs[0]
    contractTerm = inputs[1]                         # Contract Term/Life of Bus

    # User Info Inputs  **CHANGE TO PERCENTAGES**
    annualBudget = inputs[2]                         # Total Annual Budget ~60m
    annualBudgetSal = inputs[3]*annualBudget         # ~67% Annual Budget -> Salaries    
    annualBudgetCap = inputs[4]*annualBudget         # ~17% Annual Budget -> Capital Cost
    annualBudgetOp = inputs[5]*annualBudget          # ~17% Annual Budget -> Operating Costs

    fleetSize = inputs[6]                            # Total Fleet Size 
    annualMiles = inputs[7]                          # Annual miles driven
    weightedMPG = inputs[8]                          # Average mpg
    fuelPriceGal = inputs[9]                         # $/gallon fuel
    MRCost = inputs[10]                               # M&R base cost
    
    # Diesel Info Inputs
    dieselPrice = inputs[11]                          # Price of 1 Diesel Bus ~120k
    dieselRate = inputs[12]                           # _%/year ~2%/year
    dieselTerm = inputs[13]                          # Years to Finance Bus


    # --------------------------------------------------- #
    # Admin Inputs   **Read from excel sheet "Budget Simulation - Admin.xlsx"
    
    # Read from excel sheet
    excelVars = pd.read_excel(r'./Settings/Budget Simulation - Admin.xlsx', usecols= "E", header=2, nrows=7)
    excelContract = pd.read_excel(r'./Settings/Budget Simulation - Admin.xlsx', usecols= "I,J", header=3, nrows=20)

    # Admin Variables
    contractPrice = excelVars.iat[0,0]          # 30k bus/year
    contractEsc = excelVars.iat[1,0]            # 3%/year
    dieselPriceEsc = excelVars.iat[2,0]         # Diesel Price escalator 5%
    overheadAllocation = excelVars.iat[3,0]     # Overhead Cost Allocation 15%
    costEsc = excelVars.iat[4,0]                # Other costs escalator (M&R, fuel, overhead,...)
    MREsc1 = excelVars.iat[5,0]                 # M&R escalator in first half-life
    MREsc2 = excelVars.iat[6,0]                 # M&R escalator in second half-life


    # Highland Contract
    annualDeployed = [0]
    annualContract = [0]
    for i in range(20):
        annualDeployed.append(excelContract.iat[i,0]) 
        annualContract.append(excelContract.iat[i,1])


    # --------------------------------------------------- #
    # Highland Contract Total Price per Year Cumulative

    contractYearPrice = [0]*21

    for simDepYear in range(21):
        CYPPrice = annualDeployed[simDepYear] * annualContract[simDepYear]
        for simAddYear in range(simDepYear, simDepYear+contractTerm):
            if simAddYear == 21:
                break
            contractYearPrice[simAddYear] = int(contractYearPrice[simAddYear] + CYPPrice)
            CYPPrice = CYPPrice * (1+contractEsc)

    # --------------------------------------------------- #

    # Statistics summary
    print("\n Summary ")
    print("Deployment Year              ", deploymentYear)
    print("Contract Term                ", deploymentYear)
    print("Annual Budget                ", annualBudget)
    print("Annual Budget Salary         ", annualBudgetSal)
    print("Annual Budget Capital        ", annualBudgetCap)
    print("Annual Budget Operating      ", annualBudgetOp)

    print("Total Fleet Size is          ", fleetSize)
    print("Annual mileage with gas is   ", annualMiles)
    print("Gas Bus MPG is               ", weightedMPG)
    print("Fuel Price per Gallon        ", fuelPriceGal)
    print("Maintenance & Repair Cost    ", MRCost)

    print("Diesel Bus Purchase Price is ", dieselPrice)
    print("Diesel Bus Financing Rate is ", dieselRate)
    print("Diesel Bus Financing Term is ", dieselTerm)

    print("\n ")
    print("Contract Bus Price/Year      ", contractPrice)
    print("Contract Bus Escalator       ", contractEsc)
    print("Diesel Bus Escalator         ", dieselPriceEsc)
    print("Overhead Allocation Cost     ", overheadAllocation)
    print("Other Costs Escaltor         ", costEsc)
    print("M&R first half-life          ", MREsc1)
    print("M&R second half-life         ", MREsc2)

    print("Annual Deploy", annualDeployed)
    print("Annual Contract Price", annualContract)
    print("Contract Year Price", contractYearPrice, "\n")


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

    purchaseDCA = [0]*contractTerm
    mrDCA = [0]*contractTerm
    fuelDCA = [0]*contractTerm
    overheadDCA = []

    # Purchase costs avoided
    for simDepYear in range(contractTerm):
        currPrice = int(dieselPrice * pow(1+dieselPriceEsc, simDepYear))
        simCost = annualDeployed[simDepYear] * pmtCalc(dieselRate, dieselTerm, currPrice)
        for simAddYear in range(dieselTerm):
            if (simDepYear+simAddYear) < (contractTerm):
                purchaseDCA[simDepYear+simAddYear] = purchaseDCA[simDepYear+simAddYear] + simCost
    purchaseDCA.insert(0,0)

    # M&R costs avoided
    for simDepYear in range(contractTerm):
        currMRCost = MRCost * pow(1+costEsc, simDepYear)
        yearlyMR = currMRCost * annualDeployed[simDepYear]
        for simAddYear in range(simDepYear, simDepYear+contractTerm):
            if simAddYear == contractTerm:
                break
            mrDCA[simAddYear] = int(mrDCA[simAddYear] + yearlyMR)
            if (simAddYear+1-simDepYear) < (contractTerm-1)/2:
                yearlyMR = yearlyMR * (1+MREsc1)
            else:
                yearlyMR = yearlyMR * (1+MREsc2)
    mrDCA.insert(0,0)
    

    # Fuel costs avoided
    for simDepYear in range(contractTerm):
        currFuelCost = fuelTCO[0] * pow(1+costEsc, simDepYear)
        yearlyFuel = currFuelCost * annualDeployed[simDepYear]
        for simAddYear in range(simDepYear, simDepYear+contractTerm):
            if simAddYear == contractTerm:
                break
            fuelDCA[simAddYear] = int(fuelDCA[simAddYear] + yearlyFuel)
            yearlyFuel = yearlyFuel * (1+costEsc)
    fuelDCA.insert(0,0)

    # Overhead costs avoided
    for simDepYear in range(contractTerm):
        overheadDCA.append(int(overheadAllocation*(fuelDCA[simDepYear] + mrDCA[simDepYear])))
    overheadDCA.insert(0,0)

    # Prints
    print("DCA", purchaseDCA)
    print("DCA", mrDCA)
    print("DCA", fuelDCA)
    print("DCA", overheadDCA, "\n")

    # --------------------------------------------------- #
    # Relative Budget Neutrality

    # Total Diesel Costs Avoided
    totalDCA = []
    for i in range(contractTerm+1):
        totalDCA.append(purchaseDCA[i] + mrDCA[i] + fuelDCA[i] + overheadDCA[i])

    ### Budget Difference ###
    budgetStaQuo = []
    for simDepYear in range(contractTerm+1):
        budgetStaQuo.append(int(annualBudget * pow(1+costEsc, simDepYear)))

    budgetDiffRBN = []
    for i in range(contractTerm+1):
        tempSub = totalDCA[i]-contractYearPrice[i]
        budgetDiffRBN.append(tempSub)

    ### Total Budget With Highland ###
    finalRBudget = []
    for simDepYear in range(contractTerm+1):
        tempSub = budgetStaQuo[simDepYear]-budgetDiffRBN[simDepYear]
        if tempSub<0:
            tempSub=0
        finalRBudget.append(tempSub)

    # Prints
    print("Total DCA", totalDCA)
    print("Budget Diff RBN", budgetDiffRBN)

    print("Budget Status Quo", budgetStaQuo)
    print("Final Relative Budget", finalRBudget, "\n")

    # --------------------------------------------------- #
    # bottom-up budget analysis
    evCostReduction = []
    evCostReduction.append(annualDeployed[0]/fleetSize)
    for simDepYear in range(1,contractTerm+1):
        tempPerc = round(evCostReduction[simDepYear-1] + annualDeployed[simDepYear]/fleetSize,3)
        if tempPerc > 100:
            tempPerc = 100
        evCostReduction.append(tempPerc)

    ## Starts one year before deploy (i.e. 2022) ##
    buOperatingSQ = []
    for simDepYear in range(contractTerm+1):      
        buOperatingSQ.append(int(annualBudgetOp * pow(1+costEsc, simDepYear))) 

    buOperatingCosts = []
    buOperatingCosts.append(buOperatingSQ[0])
    for simDepYear in range(contractTerm+1):   
        tempOpCost = int(buOperatingSQ[simDepYear] * (1-evCostReduction[simDepYear]))
        if tempOpCost < 0:
            tempOpCost = 0
        buOperatingCosts.append(tempOpCost)

    buPersonnelCosts = []
    for simDepYear in range(contractTerm+1):   
        buPersonnelCosts.append(int(annualBudgetSal * pow(1+costEsc, simDepYear)))

    # total minus diesel buses
    buTotalPrice = []
    for i in range(contractTerm+1):
        buTotalPrice.append(int(buOperatingCosts[i] + buPersonnelCosts[i]))
    # total with highland contract
    buTotalPrice[0] = buTotalPrice[0]+annualBudgetCap
    for simDepYear in range(1,contractTerm+1):
        buTotalPrice[simDepYear] = buTotalPrice[simDepYear] + contractYearPrice[simDepYear-1]


    # print("Bottom-up Operating Status Quo", buOperatingSQ)
    # print("Bottom-up Operating Costs", buOperatingCosts)
    # print("Bottom-up Personnel Costs", buPersonnelCosts)

    # print("Bottom-up Total", buTotalPrice, "\n")




    # --------------------------------------------------- #
    # Carbon Reduction

    CO2DieselConstant = .01018      # Equivalent CO2 emissions per gal of diesel (metric tons)
    CO2GasConstant = .008887        # Equivalent CO2 emissions per gal of gas (metric tons)

    totalDeployed = []              # Cumulative count of EV's deployed
    totalGalAvoided = []            # Total gallons avoided given # of EV's deployed
    annualCarbonReduced = []        # Carbon reduced per specific year
    cumulCarbonReduced = []         # Cumulative Carbon reduced since deployment year

    totalDeployed.append(annualDeployed[0])
    for i in range(1,contractTerm+1):
        totalDeployed.append(totalDeployed[i-1]+annualDeployed[i])
    for i in range(contractTerm+1):
        totalGalAvoided.append((totalDeployed[i]*annualMiles)/weightedMPG)
    for i in range(contractTerm+1):
        annualCarbonReduced.append(CO2DieselConstant*totalGalAvoided[i])
    cumulCarbonReduced.append(round(annualCarbonReduced[0],1))
    for i in range(1,contractTerm+1):
        cumulCarbonReduced.append(round(annualCarbonReduced[i]+cumulCarbonReduced[i-1],1))

    # print("Cumulative Carbon Reduced", cumulCarbonReduced, "\n") 

    # --------------------------------------------------- #
    # Graphs and Plots

    fig, axes = plt.subplots(nrows = 2, ncols = 2)

    yearsWDep = []
    for years in range(deploymentYear-1, deploymentYear+contractTerm):
        yearsWDep.append(years)


    # X Axis Formatting
    def xAxisCalculator(term, xAxisTemp):
        if term == 5:
            for i in range(5):
                xAxisTemp.append(xAxisTemp[-1]+1)
        elif term>=6 and term<=11:
            divTemp = math.floor(term/2)-1
            for i in range(divTemp):
                xAxisTemp.append(xAxisTemp[-1]+2)
            xAxisTemp.append(xAxisTemp[0]+term)
        # elif term>=12 and term<=14:
        #     for i in range(3):
        #         xAxisTemp.append(xAxisTemp[-1]+3)
        #     xAxisTemp.append(xAxisTemp[0]+term)
        else:
            xCalcDiv = math.floor(term/5)
            xCalcMod = (term)%5
            for i in range(5-xCalcMod):
                xAxisTemp.append(xAxisTemp[-1]+xCalcDiv)
            for i in range(xCalcMod):
                xAxisTemp.append(xAxisTemp[-1]+(xCalcDiv+1))

        return xAxisTemp


    xAxisShown = [deploymentYear-1]
    xAxisShown = xAxisCalculator(contractTerm, xAxisShown)

    xAxisFig4 = np.arange(deploymentYear-1, deploymentYear+5, 1)

    # formatting
    formatMillions = FuncFormatter(millions)
    formatThousands = FuncFormatter(thousands)


    # Figure 1 - Budget Neutral Transition
    plt.sca(axes[0,0])
    plt.plot(yearsWDep, budgetStaQuo[0:contractTerm+1], 'r', label='Budget SQ')
    plt.plot([], [], 'b', linewidth=5)     # Houston ISD Budget
    plt.plot([], [], 'y', linewidth=5)     # Budget with Highland
    plt.stackplot(yearsWDep, finalRBudget[0:contractTerm+1], budgetDiffRBN[0:contractTerm+1], colors=['b','y'])

    # Figure Y Max
    Fig1YMax = round(budgetStaQuo[contractTerm]+10000000,-7)

    # Figure 1 Graph Labeling
    plt.ticklabel_format(style = 'plain')
    axes[0,0].yaxis.set_major_formatter(formatMillions)
    plt.xticks(xAxisShown)
    plt.yticks(np.arange(0, Fig1YMax, round(Fig1YMax+50000000,-8)/10))
    plt.ylabel('Millions')
    plt.xlabel('Year')
    # plt.legend(["Budget Status Quo", "Budget with Highland", "Budget saved"], loc='lower right')
    plt.title('Budget Neutral Transition')


    # Figure 2 - Bottom Up Budget Analysis
    plt.sca(axes[0,1])

    plt.plot(yearsWDep, budgetStaQuo[0:contractTerm+1], 'r', label='Budget SQ') ##############################
    plt.bar(yearsWDep, buOperatingCosts[0:contractTerm+1], color='m',)
    plt.bar(yearsWDep, buPersonnelCosts[0:contractTerm+1], bottom=buOperatingCosts[0:contractTerm+1], color='b')
    # Since operating costs and personnel costs are not arrays, need to combine lists
    CYPFormat = contractYearPrice.copy()
    CYPFormat.insert(0,0)
    OpPerSum = []
    for i in range(contractTerm+1):
        OpPerSum.append(buOperatingCosts[i]+buPersonnelCosts[i])
    plt.bar(yearsWDep, CYPFormat[0:contractTerm+1], bottom=OpPerSum[0:contractTerm+1], color='c')
    plt.bar(deploymentYear-1, annualBudgetCap, bottom=CYPFormat[0]+buOperatingCosts[0]+buPersonnelCosts[0], color='k')

    # Figure 2 Y Max
    comp1 = budgetStaQuo[contractTerm]
    comp2 = buOperatingCosts[contractTerm]+buPersonnelCosts[contractTerm]+CYPFormat[contractTerm]
    Fig2YMax = 0
    if comp1 < comp2:
        Fig2YMax = round(comp2+10000000,-7)
    else:
        Fig2YMax = round(comp1+10000000,-7)

    # Figure 2 Graph Labeling
    plt.ticklabel_format(style = 'plain')
    axes[0,1].yaxis.set_major_formatter(formatMillions)
    plt.xticks(xAxisShown)
    plt.yticks(np.arange(0, Fig2YMax, round(Fig2YMax+50000000,-8)/10))
    plt.ylabel('Millions')
    plt.xlabel('Year')
    # plt.legend(["Budget Status Quo", "Operating Costs", "Personnel Costs", "Highland Contract", "Budget Capital Cost"], bbox_to_anchor=(1, 1))
    plt.title('Bottom Up Analysis')


    # Figure 3 - Carbon Reduction Line Graph 
    plt.sca(axes[1,0])
    plt.plot(yearsWDep, cumulCarbonReduced[0:contractTerm+1], 'r', label='Expected Carbon Reduction')

    # Figure 3 Y Max
    Fig3YMax = round((cumulCarbonReduced[contractTerm]+10000), -4)

    # Figure 3 Graph Labeling
    plt.ticklabel_format(style = 'plain')
    axes[1,0].yaxis.set_major_formatter(formatThousands)
    plt.xticks(xAxisShown)
    plt.yticks(np.arange(0, Fig3YMax, Fig3YMax/5))
    plt.ylabel('Metric Tons (Thousand)')
    plt.xlabel('Year')
    # plt.legend(loc='upper left')
    plt.title('Cumulative CO2 (M.Ton) Reduced')


    # Figure 4 - Short Term Bottom Up analysis
    fiveYearSim = []
    for i in range(-1,5):
        fiveYearSim.append(deploymentYear+i)
    plt.sca(axes[1,1])

    fiveBudgetStaQuo = []
    fiveBuOperatingCosts = []
    fiveBuPersonnelCosts = []
    fiveCYPFormat = []
    for i in range(6):
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
    for i in range(6):
        fiveOpPerSum.append(fiveBuOperatingCosts[i]+fiveBuPersonnelCosts[i])    
    plt.bar(fiveYearSim, fiveCYPFormat, bottom=fiveOpPerSum, color='c')
    plt.bar(deploymentYear-1, annualBudgetCap, bottom=CYPFormat[0]+buOperatingCosts[0]+buPersonnelCosts[0], color='k')

    # Figure 4 Y max
    comp1 = budgetStaQuo[5]
    comp2 = buOperatingCosts[5]+buPersonnelCosts[5]+CYPFormat[5]
    Fig4YMax = 0
    if comp1 < comp2:
        Fig4YMax = round(comp2+10000000,-7)
    else:
        Fig4YMax = round(comp1+10000000,-7)

    # Figure 4 Graph Labeling
    plt.ticklabel_format(style = 'plain')
    axes[1,1].yaxis.set_major_formatter(formatMillions)
    plt.xticks(xAxisFig4)
    plt.yticks(np.arange(0, Fig4YMax, round(Fig4YMax+50000000,-8)/10))
    plt.ylabel('Millions')
    plt.xlabel('Year')
    # plt.legend(["Budget Status Quo", "Operating Costs", "Personnel Costs", "Highland Contract"], bbox_to_anchor=(1, 1))
    plt.title('Short Term Bottom Up Analysis')

    # Plot configuration
    fig.tight_layout()
    fig.set_figheight(6)
    fig.set_figwidth(8)

    # background color
    fig.set_facecolor('#fffeea')
    axes[0,0].set_facecolor('#fffeea')
    axes[0,1].set_facecolor('#fffeea')
    axes[1,0].set_facecolor('#fffeea')
    axes[1,1].set_facecolor('#fffeea')

    return plt.gcf()

def create_empty_graph():
    fig, axes = plt.subplots(nrows = 2, ncols = 2)
    
    # background color
    fig.set_facecolor('#fffeea')
    axes[0,0].set_facecolor('#fffeea')
    axes[0,1].set_facecolor('#fffeea')
    axes[1,0].set_facecolor('#fffeea')
    axes[1,1].set_facecolor('#fffeea')

    fig.set_figheight(6)
    fig.set_figwidth(8)
    return plt.gcf()

def delete_prev_graph(curr_fig):
    curr_fig.get_tk_widget().forget()
    plt.close('all')

if __name__ == '__main__':

    # Window Colors and background  
    # #fffeea                         tan yellow
    # #338165                         green
    # #3d4043                         gray
    # #f0bf4c                         bus yellow
    # #fdbd1c                         button yellow

    # Background Colors and Theme
    sg.theme_background_color(color = '#b9b9b9')
    sg.theme_button_color(color = ('#3d4043', '#fdbd1c'))          # button text, button background
    sg.theme_input_background_color(color='#ffffff')
    sg.theme_input_text_color(color='#3d4043')
    sg.theme_text_color(color='#3d4043')    
    sg.theme_text_element_background_color(color='#fffeea')

    # sg.theme_element_background_color(color='#6a0dad')   
    # sg.theme_element_text_color(color='#6a0dad')



    # Get last inputted -- file is formatted in same order as displayed inputs
    savedInputs = []
    with open(r'./Settings/previousInputs.txt', 'r') as inputFile:
        for line in inputFile:
            for input in line.split():
                savedInputs.append(input)

    layoutCol1 = [
        # [sg.T('', background_color='#fffeea')],
        [sg.VP()],
        [sg.P(), sg.T('Deployment Year (Y)', font='_ 17 bold'), 
                    sg.I(default_text=savedInputs[0], key='-DEPLOY-YEAR-', font='_ 12', do_not_clear=True, size=(11, 0))],
        [sg.P(), sg.T('Contract Term (Y)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[1]):,}", key='-CONTRACT-TERM-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Annual Budget ($)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[2]):,}", key='-ANNUAL-BUDGET-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Annual Budget - Salary (%)', font='_ 17 bold'), 
                    sg.I(default_text=savedInputs[3], key='-BUDGET-SALARY-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Annual Budget - Capital Cost (%)', font='_ 17 bold'), 
                    sg.I(default_text=savedInputs[4], key='-BUDGET-CAPITAL-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Annual Budget - Operating Cost (%)', font='_ 17 bold'), 
                    sg.I(default_text=savedInputs[5], key='-BUDGET-OPERATING-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Fleet Size (#)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[6]):,}", key='-FLEET-SIZE-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Annual Mileage (#)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[7]):,}", key='-ANNUAL-MILES-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Average MPG (#)', font='_ 17 bold'), 
                    sg.I(default_text=f"{float(savedInputs[8]):,}", key='-WEIGHTED-MPG-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Fuel Cost per Gallon ($)', font='_ 17 bold'), 
                    sg.I(default_text=f"{float(savedInputs[9]):,}", key='-FUEL-PRICE-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Maintenance & Repairs Cost ($)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[10]):,}", key='-MR-COST-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Diesel Bus Purchase Price ($)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[11]):,}", key='-DIESEL-PRICE-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Diesel Bus Financing Rate (%)', font='_ 17 bold'), 
                    sg.I(default_text=savedInputs[12], key='-DIESEL-RATE-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.P(), sg.T('Diesel Bus Financing Term (Y)', font='_ 17 bold'), 
                    sg.I(default_text=f"{int(savedInputs[13]):,}", key='-DIESEL-TERM-', font='_ 12', do_not_clear=True, size=(11, 1))],
        [sg.VP()],
        [sg.P(), 
                    sg.B('Plot!', font='_ 16 bold'), 
                    sg.B('Reset Inputs', font='_ 16 bold'), 
                    sg.B('Save', font='_ 16 bold', disabled=True)
        ]
    ]
    
    layoutCol2 = [
        [sg.Canvas(key='canvas')]
    ]

    layoutTopRow = [    
        [sg.P(background_color='#338165'), 
            sg.T('Highland Fleets Budget Simulation', font='_ 28 bold', text_color='#FFFFFF', background_color='#338165'),
        sg.P(background_color='#338165')]
    ]

    layout = [
        [sg.Column(layoutTopRow, expand_x=True, pad=((0,0),(0,0)), background_color='#338165')],
        [sg.VP()], 
            [sg.P(), 
                sg.Column(layoutCol1, key='-COLUMN-ONE-', expand_y=True, expand_x=True, background_color='#fffeea'),
                sg.Column(layoutCol2, key = '-COLUMN-TWO-', expand_y=True, expand_x=True, background_color='#fffeea'), 
            sg.P()
            ],
        [sg.VP()]
    ]


    def draw_figure(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(fill='both', expand=1, side='right')
        return figure_canvas_agg



    window = sg.Window('Budget Simulation', layout, element_justification='right', finalize=True, margins=(0,0))

    # Set minimum window resizable size
    window.TKroot.minsize(1250, 650)

    # Keep track of window size
    window.bind('<Configure>',"Event")


    curr_fig = draw_figure(window['canvas'].TKCanvas, create_empty_graph())
    

    while (True):
        event, values = window.read()

        # Mouse over options
        # mouse = values['-MOUSE-']
        # if event == '-MOUSE-':
        #     if mouse == (None, None):
        #         print("I CLICKED!!!")

        # Resizable graph and inputs based on window size?
        # if event == "Event":
        #     print(window.size)

        if event == sg.WINDOW_CLOSED:
            break
        if event=="Plot!":
            
            # User Error Checking
            someError = False

            # Grab bounds for Deploy Year and Contract Term
            excelBounds = pd.read_excel(r'./Settings/Budget Simulation - Admin.xlsx', usecols= "E", header=9, nrows=3)
            DYLowerBound = excelBounds.iat[0,0]
            CTLowerBound = excelBounds.iat[1,0]
            CTUpperBound = excelBounds.iat[2,0]

            # Deployment Year - integer, 2021<X
            text = values['-DEPLOY-YEAR-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(num >= DYLowerBound)
                window['-DEPLOY-YEAR-'].update(background_color='#ffffff')
            except:
                window['-DEPLOY-YEAR-'].update(background_color='red')
                someError = True

            # Contract Term - integer, 5<X<=20
            text = values['-CONTRACT-TERM-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(CTLowerBound <= num <= CTUpperBound)
                window['-CONTRACT-TERM-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-CONTRACT-TERM-'].update(background_color='red')
                someError = True

            # Annual Budget Total - integer, 0<X
            text = values['-ANNUAL-BUDGET-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(0 < num)
                window['-ANNUAL-BUDGET-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-ANNUAL-BUDGET-'].update(background_color='red')
                someError = True

            # Budget Salary Cost Percentage - float, 0<=X<=1
            text = values['-BUDGET-SALARY-']
            try:
                text = text.replace(',','')
                num = float(text)
                assert(0 <= num <= 1)
                window['-BUDGET-SALARY-'].update(background_color='#ffffff')
            except:
                window['-BUDGET-SALARY-'].update(background_color='red')
                someError = True

            # Budget Capital Cost Percentage - float, 0<=X<=1
            text = values['-BUDGET-CAPITAL-']
            try:
                text = text.replace(',','')
                num = float(text)
                assert(0 <= num <= 1)
                window['-BUDGET-CAPITAL-'].update(background_color='#ffffff')
            except:
                window['-BUDGET-CAPITAL-'].update(background_color='red')
                someError = True
 
            # Budget Operating Cost Percentage - float, 0<=X<=1
            text = values['-BUDGET-OPERATING-']
            try:
                text = text.replace(',','')
                num = float(text)
                assert(0 <= num <= 1)
                window['-BUDGET-OPERATING-'].update(background_color='#ffffff')
            except:
                window['-BUDGET-OPERATING-'].update(background_color='red')
                someError = True

            # Total Fleet Size - integer, 0<X
            text = values['-FLEET-SIZE-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(0 < num)
                window['-FLEET-SIZE-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-FLEET-SIZE-'].update(background_color='red')
                someError = True

            # Annual Mileage - integer, 0<=X
            text = values['-ANNUAL-MILES-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(0 <= num)
                window['-ANNUAL-MILES-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-ANNUAL-MILES-'].update(background_color='red')
                someError = True

            # Weighted MPG - float, 0<X
            text = values['-WEIGHTED-MPG-']
            try:
                text = text.replace(',','')
                num = float(text)
                assert(0 < num)
                window['-WEIGHTED-MPG-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-WEIGHTED-MPG-'].update(background_color='red')
                someError = True

            # Fuel Price - float, 0<=X
            text = values['-FUEL-PRICE-']
            try:
                text = text.replace(',','')
                num = float(text)
                assert(0 <= num)
                window['-FUEL-PRICE-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-FUEL-PRICE-'].update(background_color='red')
                someError = True

            # Maintenance and Repairs Year 1 Cost - integer, 0<=X
            text = values['-MR-COST-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(0 <= num)
                window['-MR-COST-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-MR-COST-'].update(background_color='red')
                someError = True

            # Diesel Bus Total Price - integer, 0<=X
            text = values['-DIESEL-PRICE-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(0 <= num)
                window['-DIESEL-PRICE-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-DIESEL-PRICE-'].update(background_color='red')
                someError = True
            
            # Diesel Finance Rate - float, 0<=X<=1
            text = values['-DIESEL-RATE-']
            try:
                text = text.replace(',','')
                num = float(text)
                assert(0 <= num <= 1)
                window['-DIESEL-RATE-'].update(background_color='#ffffff')
            except:
                window['-DIESEL-RATE-'].update(background_color='red')
                someError = True

            # Diesel Finance Term - integer, 0<=X
            text = values['-DIESEL-TERM-']
            try:
                text = text.replace(',','')
                num = int(text)
                assert(0 <= num)
                window['-DIESEL-TERM-'].update(f"{num:,}", background_color='#ffffff')
            except:
                window['-DIESEL-TERM-'].update(background_color='red')
                someError = True

            if someError:
                continue

            # Get the user input information
            userInputs = []
            userInputs.append(int(values['-DEPLOY-YEAR-'].replace(',','')))
            userInputs.append(int(values['-CONTRACT-TERM-'].replace(',','')))
            userInputs.append(int(values['-ANNUAL-BUDGET-'].replace(',','')))
            userInputs.append(float(values['-BUDGET-SALARY-'].replace(',','')))
            userInputs.append(float(values['-BUDGET-CAPITAL-'].replace(',','')))
            userInputs.append(float(values['-BUDGET-OPERATING-'].replace(',','')))
            userInputs.append(int(values['-FLEET-SIZE-'].replace(',','')))
            userInputs.append(int(values['-ANNUAL-MILES-'].replace(',','')))
            userInputs.append(float(values['-WEIGHTED-MPG-'].replace(',','')))
            userInputs.append(float(values['-FUEL-PRICE-'].replace(',','')))
            userInputs.append(int(values['-MR-COST-'].replace(',','')))
            userInputs.append(int(values['-DIESEL-PRICE-'].replace(',','')))
            userInputs.append(float(values['-DIESEL-RATE-'].replace(',','')))
            userInputs.append(int(values['-DIESEL-TERM-'].replace(',','')))

            # Update Previous Inputs file
            with open(r'./Settings/previousInputs.txt', 'w') as inputFile:
                for input in userInputs:
                    inputFile.write(str(input)) 
                    inputFile.write(' ')

            # Delete old graph and replace with updated graph
            delete_prev_graph(curr_fig)
            tempGraph = create_budget_graphs(userInputs)
            # tempGraph.subplots_adjust(right=1.2)

            window['Save'].update(disabled=False)
            curr_fig = draw_figure(window['canvas'].TKCanvas, tempGraph)

        if event=="Reset Inputs":
            # Get inputs from backup file
            newInputs = []
            with open(r'./Settings/backupInputs.txt', 'r') as inputFile:
                for line in inputFile:
                    for input in line.split():
                        newInputs.append(input)

            # Update User Window
            window['-DEPLOY-YEAR-'].update(newInputs[0])
            window['-CONTRACT-TERM-'].update(f"{int(newInputs[1]):,}")
            window['-ANNUAL-BUDGET-'].update(f"{int(newInputs[2]):,}")
            window['-BUDGET-SALARY-'].update(newInputs[3])
            window['-BUDGET-CAPITAL-'].update(newInputs[4])
            window['-BUDGET-OPERATING-'].update(newInputs[5])
            window['-FLEET-SIZE-'].update(f"{int(newInputs[6]):,}")
            window['-ANNUAL-MILES-'].update(f"{int(newInputs[7]):,}")
            window['-WEIGHTED-MPG-'].update(f"{float(newInputs[8]):,}")
            window['-FUEL-PRICE-'].update(f"{float(newInputs[9]):,}")
            window['-MR-COST-'].update(f"{int(newInputs[10]):,}")
            window['-DIESEL-PRICE-'].update(f"{int(newInputs[11]):,}")
            window['-DIESEL-RATE-'].update(newInputs[12])
            window['-DIESEL-TERM-'].update(f"{int(newInputs[13]):,}")

            # Write to previous Inputs
            with open(r'./Settings/previousInputs.txt', 'w') as inputFile:
                for input in newInputs:
                    inputFile.write(str(input)) 
                    inputFile.write(' ')

        if event=="Save":
            pass

    window.close()