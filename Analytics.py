import pandas as pd

# Load the dataset
data = pd.read_csv("C:\\Users\\nabil\\Downloads\\owid-energy-data.csv")

# Filter relevant years and ensure no 'World' double counting
world_data = data[(data['year'] >= 2015) & (data['year'] <= 2022) & (data['country'] != 'World')].copy()

# ------------------------------------------------
# 1. Global Distribution Loss Over Time
# ------------------------------------------------
# Calculate Total Production and Consumption
world_data['total_production'] = world_data[['coal_consumption', 'oil_consumption', 'gas_consumption',
                                             'hydro_consumption', 'renewables_consumption',
                                             'nuclear_consumption']].sum(axis=1)

world_data['total_consumption'] = world_data[['fossil_fuel_consumption', 'renewables_consumption',
                                              'nuclear_consumption']].sum(axis=1)

# Group by year to get totals
distribution_loss = world_data.groupby('year').agg({
    'total_production': 'sum',
    'total_consumption': 'sum'
})

# Calculate Distribution Loss
distribution_loss['net_loss'] = distribution_loss['total_production'] - distribution_loss['total_consumption']

print("\nGlobal Distribution Loss Over Time (TWh):")
print(distribution_loss)

# ------------------------------------------------
# 2. Net Difference by Energy Type (2015-2022)
# ------------------------------------------------
# Group by year and calculate net difference for key energy types
net_difference = world_data.groupby('year').agg({
    'coal_consumption': 'sum',
    'gas_consumption': 'sum',
    'oil_consumption': 'sum',
    'hydro_consumption': 'sum'
})

# Subtract global consumption from production
net_difference['Coal Net Difference'] = net_difference['coal_consumption']
net_difference['Gas Net Difference'] = net_difference['gas_consumption']
net_difference['Oil Net Difference'] = net_difference['oil_consumption']
net_difference['Hydro Net Difference'] = net_difference['hydro_consumption']

# Drop redundant columns
net_difference = net_difference[['Coal Net Difference', 'Gas Net Difference',
                                 'Oil Net Difference', 'Hydro Net Difference']]

print("\nNet Difference Between Production and Consumption (2015-2022):")
print(net_difference)

# ------------------------------------------------
# 3. Additional Insights
# ------------------------------------------------
# Total cost of net energy losses (assuming $40,000 per GWh)
distribution_loss['cost_of_loss'] = distribution_loss['net_loss'] * 40

print("\nCost of Global Energy Loss (in $):")
print(distribution_loss[['net_loss', 'cost_of_loss']])





# ------------------------------------------------
# 1. Energy Distribution Overview: Fossil, Renewables, Nuclear
# ------------------------------------------------
global_energy = data[(data['year'] >= 1965) & (data['year'] <= 2022)].copy()  # Explicit copy

# Group energy types over time
energy_trends = global_energy.groupby('year')[[
    'fossil_fuel_consumption', 'renewables_consumption', 'nuclear_consumption'
]].sum()

print("\nEnergy Distribution Over Time (TWh):")
print(energy_trends.tail())

# ------------------------------------------------
# 2. Breakdown of Renewables and Fossil Fuels (2022)
# ------------------------------------------------
latest_year = global_energy[global_energy['year'] == 2022]

# Sum up renewables and fossil fuel breakdown
renewables_2022 = latest_year[['hydro_consumption', 'solar_consumption', 'wind_consumption', 'biofuel_consumption']].sum()
fossil_fuels_2022 = latest_year[['coal_consumption', 'oil_consumption', 'gas_consumption']].sum()

print("\nRenewable Energy Breakdown (2022):")
print(renewables_2022)
print("\nFossil Fuel Energy Breakdown (2022):")
print(fossil_fuels_2022)

# ------------------------------------------------
# 3. Energy Consumption Per Capita Trends
# ------------------------------------------------
global_energy = global_energy.copy()  # Ensure we're working with a copy

# Use .loc to add calculated columns
global_energy.loc[:, 'total_energy'] = global_energy['fossil_fuel_consumption'] + \
                                       global_energy['renewables_consumption'] + \
                                       global_energy['nuclear_consumption']

global_energy.loc[:, 'energy_per_capita'] = global_energy['total_energy'] / global_energy['population']

per_capita_trends = global_energy.groupby('year')['energy_per_capita'].mean()
print("\nEnergy Consumption Per Capita (TWh per person):")
print(per_capita_trends.tail())

# ------------------------------------------------
# 4. Electricity Production Analysis
# ------------------------------------------------
electricity_trends = global_energy.groupby('year')[[
    'coal_consumption', 'oil_consumption', 'gas_consumption',
    'hydro_consumption', 'nuclear_consumption', 'renewables_consumption'
]].sum()

print("\nElectricity Production Trends (TWh):")
print(electricity_trends.tail())

# ------------------------------------------------
# 5. Monthly Data (If Available)
# ------------------------------------------------
if 'month' in global_energy.columns:
    monthly_trends = global_energy.groupby('month')['electricity_demand'].mean()
    print("\nMonthly Electricity Consumption (TWh):")
    print(monthly_trends)
else:
    print("\nMonthly data is not available in the current dataset.")

print(global_energy.columns)


