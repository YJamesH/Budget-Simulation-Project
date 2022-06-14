from random import randrange
import matplotlib.pyplot as plt
import numpy as np

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

# --------------------------------------------------- #

if __name__ == '__main__':

    # --------------------------------------------------- #
    # # INPUTS 

    # # Contract Inputs
    # deploymentYear = int(input("Deployment Year: "))
    # contractTerm = int(input("Contract Term (years): ")) # Contract Term/Life of Bus
    # contractEsc = .03                                    # 3%/year
    # contractPrice = 30000                                # 30k bus/year

    # # User Info Inputs
    # annualBudget = int(input("Annual budget: "))          # Total Annual Budget ~60m
    # fleetSize = int(input("Total Fleet Size: "))          # Total Fleet Size 
    # annualMiles = int(input("Annual mileage with gas: ")) # Annual miles driven
    # weightedMPG = float(input("MPG with gas: "))          # Average mpg
    # fuelPriceGal = float(input("Fuel price $/gal: "))        # $/gallon fuel average
    # MRCost = int(input("Maintenance & Repair Year 1 Base Cost: ")) # M&R base cost
    
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
    contractTerm = 15                                    # Contract Term/Life of Bus
    contractEsc = .03                                    # 3%/year
    contractPrice = 30000                                # 30k bus/year
    # User Info Inputs
    annualBudget = 59893990                               # Total Annual Budget ~60m
    fleetSize = 200                                       # Total Fleet Size 
    annualMiles = 9000                                    # Annual miles driven
    weightedMPG = 6                                       # Average mpg
    fuelPriceGal = 2.5                                    # $/gallon fuel
    MRCost = 6000                                         # M&R base cost
    # Diesel Info Inputs
    dieselPrice = 120000                                  # Price of 1 Diesel Bus ~120k
    dieselRate = .03                                      # _%/year ~2%/year
    dieselTerm = 3                                        # Years to Finance Bus
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

    print("Contract", contractYearPrice)

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
    print("TCO", overheadTCO)

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
    print("DCA", overheadDCA)

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
    for simDepYear in range(20):
        budgetStaQuo.append(int(annualBudget * pow(1+costEsc, simDepYear)))

    # Prints
    print("Total DCA", totalDCA)
    print("Budget Diff", budgetDiffRBN)

    print("budget Status Quo", budgetStaQuo)

    # --------------------------------------------------- #
    # bottom-up budget analysis



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

    print("CCR", cumulCarbonReduced) 


    # Graph Creation 
    yearsADep = []
    for years in range(deploymentYear, deploymentYear+20):
        yearsADep.append(years)

    plt.plot(yearsADep, cumulCarbonReduced, '-b', label='Carbon Reduced')
    plt.xticks(yearsADep)
    yStep = 25000
    CCRyMax = round((cumulCarbonReduced[-1]+ yStep)/yStep) *25000
    plt.yticks(np.arange(0, CCRyMax, yStep))
    plt.ylabel('metric tons')
    plt.xlabel('Year')
    plt.legend(loc='upper left')
    plt.title('Cumulative Metric Tons of CO2 Reduced since Deployment Year')
    # plt.grid()
    # plt.show()

    # --------------------------------------------------- #


    # Statistics summary
    print("\n Summary ")
    print("Annual Budget is ", annualBudget)
    print("Total Fleet Size is ", fleetSize)
    print("Annual mileage with gas is ", annualMiles)
    print("Gas Bus MPG is ", weightedMPG)
    print("Diesel Bus Purchase Price is ", dieselPrice)
    print("Diesel Bus Financing Rate is ", dieselRate)
    print("Diesel Bus Financing Term is ", dieselTerm)

