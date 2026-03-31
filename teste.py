import pandas as pd

dados = pd.read_csv('/home/julio/dev/fiapAurora/household_power_consumption.txt', sep=';')

print(dados.head())

print(dados.describe())

