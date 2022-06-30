# Reading an excel file using Python
from kiwisolver import Expression
import pandas as pd
 
# Give the location of the file
excelVars = pd.read_excel(r'./Settings/Budget Simulation - Admin.xlsx', usecols= "E", header=2, nrows=7)
# excelDeploy = pd.read_excel('Budget Simulation - Admin.xlsx', usecols= "I", header=4, nrows=20)
# excelPrice = pd.read_excel('Budget Simulation - Admin.xlsx', usecols= "J", header=4, nrows=20)

# data = excelPrice.columns.values[18]

test = pd.read_excel(r'./Settings/Budget Simulation - Admin.xlsx', usecols= "I,J", header=3, nrows=20)

print(excelVars.iat[6,0])


# print(excelVars)
# print(excelDeploy)
# print(excelPrice)
# print(data)
