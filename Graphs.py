import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load and Clean the Dataset

data = pd.read_csv("C:\\Users\\nabil\\Downloads\\owid-energy-data.csv")

# Remove 'World' as a country to avoid double-counting global data
data = data[data['country'] != 'World']

# Ensure Relevant Columns Are Numeric
data.iloc[:, 3:] = data.iloc[:, 3:].apply(pd.to_numeric, errors='coerce')

# Drop Rows with Missing Critical Values
data = data.dropna(subset=['fossil_fuel_consumption', 'renewables_consumption', 'nuclear_consumption', 'electricity_generation'])

# Group Data by Year for Aggregation
global_energy = data.groupby('year').sum()

# ----------------------------------------------------
# 1. Global Distribution Loss Over Time
# ----------------------------------------------------
global_energy['net_loss'] = global_energy['electricity_generation'] - global_energy['electricity_demand']

plt.figure(figsize=(10, 6))
plt.plot(global_energy.index, global_energy['net_loss'], marker='o', linestyle='-', color='red')
plt.title('Global Distribution Loss Over Time (2015-2022)')
plt.xlabel('Year')
plt.ylabel('Net Energy Loss (TWh)')
plt.grid(axis='y')
plt.show()

# ----------------------------------------------------
# 2. Net Difference Between Production and Consumption by Energy Type
# ----------------------------------------------------
energy_types = ['coal_consumption', 'gas_consumption', 'oil_consumption', 'hydro_consumption']
net_differences = global_energy[energy_types].copy()
net_differences.columns = ['Coal', 'Gas', 'Oil', 'Hydro']

plt.figure(figsize=(10, 6))
bar_width = 0.2
years = np.arange(len(global_energy.index))

plt.bar(years - bar_width*1.5, net_differences['Coal'], bar_width, label='Coal', color='navy')
plt.bar(years - bar_width/2, net_differences['Gas'], bar_width, label='Gas', color='red')
plt.bar(years + bar_width/2, net_differences['Oil'], bar_width, label='Oil', color='pink')
plt.bar(years + bar_width*1.5, net_differences['Hydro'], bar_width, label='Hydro', color='lightblue')

plt.xticks(years, global_energy.index, rotation=45)
plt.title('Net Difference Between Production and Consumption by Energy Type')
plt.xlabel('Year')
plt.ylabel('Net Difference (TWh)')
plt.legend(title='Energy Source')
plt.tight_layout()
plt.show()

# ----------------------------------------------------
# 3. Share of Renewables in Total Energy Production (Pie Chart)
# ----------------------------------------------------
latest_year = global_energy.loc[2022]
renewables_share = {
    'Hydro': latest_year['hydro_consumption'],
    'Solar': latest_year['solar_consumption'],
    'Wind': latest_year['wind_consumption'],
    'Biofuel': latest_year['biofuel_consumption']
}

plt.figure(figsize=(8, 8))
plt.pie(renewables_share.values(), labels=renewables_share.keys(), autopct='%1.1f%%', startangle=140, colors=sns.color_palette('viridis'))
plt.title('Share of Renewables in Total Energy Production (2022)')
plt.show()

# ----------------------------------------------------
# 4. Trends in Renewable Energy Sources Over Time
# ----------------------------------------------------
plt.figure(figsize=(10, 6))
plt.stackplot(global_energy.index,
              global_energy['hydro_consumption'],
              global_energy['solar_consumption'],
              global_energy['wind_consumption'],
              labels=['Hydro', 'Solar', 'Wind'],
              alpha=0.8, colors=sns.color_palette('viridis', 3))
plt.title('Trends in Renewable Energy Sources Over Time')
plt.xlabel('Year')
plt.ylabel('Energy Consumption (TWh)')
plt.legend(loc='upper left')
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt

import matplotlib.pyplot as plt

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# ----------------------------------------------------
# Energy Consumption Per Capita (World vs. Canada) (Excluding 2023)
# ----------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Prepare data
world_energy = data.groupby('year').sum()
canada_energy = data[data['country'] == 'Canada'].groupby('year').sum()

# Remove 2023 from the dataset
world_energy = world_energy[world_energy.index < 2023]
canada_energy = canada_energy[canada_energy.index < 2023]

# Convert TWh to kWh per Person
world_energy['per_capita'] = (world_energy['fossil_fuel_consumption'] / world_energy['population']) * 1e6
canada_energy['per_capita'] = (canada_energy['fossil_fuel_consumption'] / canada_energy['population']) * 1e6

# Custom y-axis formatter
def format_y(value, _):
    return f"{int(value)}"  # Format ticks as integers

# Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(world_energy.index, world_energy['per_capita'],
        label='World', color='slateblue', linewidth=2)
ax.plot(canada_energy.index, canada_energy['per_capita'],
        label='Canada', color='darkolivegreen', linewidth=2)

# Titles and labels
ax.set_title('Energy Consumption Per Capita (World vs. Canada)', fontsize=16, weight='bold', pad=20)
ax.set_xlabel('Year', fontsize=14, weight='bold')
ax.set_ylabel('kWh per Person', fontsize=14, weight='bold')

# Remove unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Format ticks
ax.tick_params(axis='both', which='major', labelsize=12)
ax.yaxis.set_major_formatter(FuncFormatter(format_y))

# Add annotations with boxed text
bbox_props = dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3')

ax.text(1988, 60,
        "1988: A significant increase\nin Canada's energy use.",
        fontsize=11, color='darkolivegreen', bbox=bbox_props)

ax.text(2008, 77,
        "Canada's per capita energy consumption\nremains consistently high over the decades.",
        fontsize=11, color='darkolivegreen', bbox=bbox_props)

ax.text(1995, 50,
        "Canada consumes 139% more energy per capita\nthan the global average.",
        fontsize=11, color='dimgray', bbox=bbox_props)

ax.text(2006, 37,
        "Global consumption grows slowly,\nwith much lower per capita use.",
        fontsize=11, color='slateblue', bbox=bbox_props)

# Legend
ax.legend(fontsize=12, frameon=False, loc='upper left')

# Show plot
plt.tight_layout()
plt.show()



# ----------------------------------------------------
# 6. Cost of Energy Loss Over Time (2000+)
# ----------------------------------------------------
COST_PER_TWH = 40_000  # USD per GWh

# Filter data for years >= 2000
global_energy_post_2000 = global_energy[global_energy.index >= 2000]
global_energy_post_2000['cost_of_loss'] = global_energy_post_2000['net_loss'] * COST_PER_TWH / 1e9  # Convert to billions

plt.figure(figsize=(12, 7))
bars = plt.bar(global_energy_post_2000.index, global_energy_post_2000['cost_of_loss'], color='steelblue')

# Format the graph
plt.title('Cost of Global Energy Loss Over Time (2000+)', fontsize=15, weight='bold')
plt.xlabel('Year', fontsize=12, weight='bold')
plt.ylabel('Cost (USD, billions)', fontsize=12, weight='bold')

# Remove boxing (spines) except x and y axes
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

# Adjust tick parameters for better clarity
plt.tick_params(axis='both', which='major', labelsize=10)

# Adjusted Annotations
plt.annotate('In 2000, energy losses cost $1.24B,\nmarking the lowest point\nin recent history.',
             xy=(2000, 1.20), xytext=(2002, 2.1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1),
             fontsize=10, ha='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

plt.annotate('Between 2010 and 2015,\nannual costs grew steadily\nby an average of $0.05B per year.',
             xy=(2012, 1.88), xytext=(2010, 2.3),
             arrowprops=dict(arrowstyle='->', color='black', lw=1),
             fontsize=10, ha='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))

plt.annotate('By 2022, energy loss costs\nreached $2.44B, reflecting\na 96% increase since 2000.',
             xy=(2022, 2.44), xytext=(2021, 2.6),
             arrowprops=dict(arrowstyle='->', color='black', lw=1),
             fontsize=10, ha='center', bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round,pad=0.3'))


# Highlight the mean cost with a dashed line
mean_cost = global_energy_post_2000['cost_of_loss'].mean()
plt.axhline(mean_cost, color='gray', linestyle='--', linewidth=1)
plt.text(2002, mean_cost + 0.05, f"Mean Cost: {mean_cost:.2f}B", fontsize=10, color='gray', weight='bold')

plt.tight_layout()
plt.show()




print("\nGraphs generated successfully.")
