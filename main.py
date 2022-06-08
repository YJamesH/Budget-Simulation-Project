from random import randrange



# # INPUTS 
# # Contract Inputs
# contractTerm = int(input("Contract Term (years): ")) # Contract Term/Life of Bus
# contractEsc = .03                                    # 3%/year
# contractPrice = 30000                                # 30k bus/year

# # User Info Inputs
# annualBudget = int(input("Annual budget: "))          # Total Annual Budget ~60m
# fleetSize = int(input("Total Fleet Size: "))          # Total Fleet Size 
# annualMiles = int(input("Annual mileage with gas: ")) # Annual miles driven
# weightedMPG = float(input("MPG with gas: "))          # Average mpg
# fuelPrice = float(input("Fuel price $/gal: "))        # $/gallon fuel average
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



# --------------- coded inputs for testing --------------- #
# Contract Inputs
contractTerm = 15                                    # Contract Term/Life of Bus
contractEsc = .03                                    # 3%/year
contractPrice = 30000                                # 30k bus/year
# User Info Inputs
annualBudget = 60000000                               # Total Annual Budget ~60m
fleetSize = 200                                       # Total Fleet Size 
annualMiles = 9000                                    # Annual miles driven
weightedMPG = 6                                       # Average mpg
fuelPrice = 2.5                                       # $/gallon fuel
MRCost = 6000                                         # M&R base cost
# Diesel Info Inputs
dieselPrice = 120000                                  # Price of 1 Diesel Bus ~120k
dieselRate = .03                                      # _%/year ~2%/year
dieselTerm = 5                                        # Years to Finance Bus
dieselPriceEsc = .05                             # Diesel Price escalator 5%
overheadAllocation = .15                         # Overhead Cost Allocation 15%
costEsc = .02                                    # Other costs escalator (M&R, fuel, overhead,...)
MREsc1 = .06                                     # M&R escalator in first half-life
MREsc2 = .08                                     # M&R escalator in second half-life

annualDeployed = [10,20,30,40,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67] # subject to change
annualContract = [22000,22000,22000,22000,27000,27000,27000,27000,20000,20000,20000,20000,24000,24000,24000,24000,24000,24000,24000,24000]
# ------------- end coded inputs for testing ------------- #


# --------------------------------------------------- #
# Example Highland Contract Illustration




# --------------------------------------------------- #
# Diesel Total Cost of Ownership (TCO)

purchaseTCO = []
mrTCO = []
fuelTCO = []
overheadTCO = []

# WIP @@@@@
# Purchase price with financing
pmtDieselPrice = 0
rateAccumulated = pow((1+dieselRate),dieselTerm)
if dieselRate==0:
    pmtDieselPrice = int(dieselPrice/dieselTerm)
else:
    pmtDieselPrice = int((dieselRate*dieselPrice*rateAccumulated) / (rateAccumulated-1))
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
    fuelTCO.append(int((annualMiles/weightedMPG)*fuelPrice*pow((1+costEsc),i)))


# Overhead
for i in range(contractTerm):
    overheadTCO.append(int((mrTCO[i]+fuelTCO[i])*overheadAllocation))


print("TCO", purchaseTCO)
print("TCO", mrTCO)
print("TCO", fuelTCO)
print("TCO", overheadTCO)

# --------------------------------------------------- #
# Diesel Costs avoided  - Break down

purchaseDCA = []
mrDCA = []
fuelDCA = []
overheadDCA = []

# Purchase costs avoided


# M&R costs avoided


# Fuel costs avoided


# Overhead costs avoided


# --------------------------------------------------- #
# Carbon Reduction

CO2DieselConstant = .01018      # Equivalent CO2 emissions per gal of diesel (metric tons)
CO2GasConstant = .008887        # Equivalent CO2 emissions per gal of gas (metric tons)

totalDeployed = []
totalGalAvoided = []
annualCarbonReduced = []
cumulCarbonReduced = []

totalDeployed.append(annualDeployed[0])
for i in range(1,20):
    totalDeployed.append(totalDeployed[i-1]+annualDeployed[i])
for i in range(20):
    totalGalAvoided.append((totalDeployed[i]*annualMiles)/weightedMPG)
for i in range(20):
    annualCarbonReduced.append(CO2DieselConstant*totalGalAvoided[i])
cumulCarbonReduced.append(annualCarbonReduced[0])
for i in range(1,20):
    cumulCarbonReduced.append(annualCarbonReduced[i]+cumulCarbonReduced[i-1])

print(cumulCarbonReduced) # MAKE PRINT 1 DECIMAL PLACE
# --------------------------------------------------- #


# Statistics summary
print("\n Summary Statistics")
print("Annual Budget is ", annualBudget)
print("Total Fleet Size is ", fleetSize)
print("Annual mileage with gas is ", annualMiles)
print("Gas Bus MPG is ", weightedMPG)
print("Diesel Bus Purchase Price is ", dieselPrice)
print("Diesel Bus Financing Rate is ", dieselRate)
print("Diesel Bus Financing Term is ", dieselTerm)


