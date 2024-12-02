"""
This script generates radar plots for the Sri Lankan districts based on their ranks in different indexes.

Author: Fulvio D. Lopnae
Centre for Advanced Spatial Anlaysis
University College London
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# File paths
input_file = "./data/radar_graphs_data.csv"
output_file = "./outputs/radar_charts.png"

# Read the CSV file
data = pd.read_csv(input_file)

# Ensure required columns are present
required_columns = ["District", "Supply_rank", "Demand_rank", "SD_rank", "SD-GWR_rank", "Tanks_rank", "ADP_rank"]
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The CSV file must contain the following columns: {required_columns}")

# Clean column names for display
categories = [col.replace("_rank", "") for col in
              ["Supply_rank", "Demand_rank", "SD_rank", "SD-GWR_rank", "Tanks_rank", "ADP_rank"]]
num_vars = len(categories)

# Extract unique districts
districts = data["District"].unique()


# Function to create radar plot
def create_radar_plot(ax, values, label):
    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    # Complete the loop
    values += values[:1]
    angles += angles[:1]

    # Plot data
    ax.fill(angles, values, alpha=0.25, color='mediumaquamarine')
    ax.plot(angles, values, linewidth=2, color='mediumaquamarine', label=label)

    # Inverse axis limits
    ax.set_ylim(1, 17)
    ax.set_yticks([1, 5, 9, 13, 17])
    ax.invert_yaxis()

    # Add category labels with increased offset
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=8, ha='center', color='dimgrey')
    for label, angle in zip(ax.get_xticklabels(), angles[:-1]):
        x_offset = 0.1 * np.cos(angle)
        y_offset = 0.1 * np.sin(angle)
        label.set_position((x_offset, y_offset))

    # Add radial axis tick labels
    ax.set_yticklabels([str(tick) for tick in [1, 5, 9, 13, 17]], fontsize=7, color="gray")


# Create subplots
fig, axes = plt.subplots(6, 3, subplot_kw=dict(polar=True), figsize=(8.27, 11.69))
axes = axes.flatten()

# Plot radar chart for each district
for i, district in enumerate(districts):
    district_data = data[data["District"] == district].iloc[0]
    values = district_data[[col for col in required_columns if col != "District"]].values.tolist()

    ax = axes[i]
    create_radar_plot(ax, values, district)
    ax.set_title(district, size=10, color='black')

# Remove extra subplots
for j in range(len(districts), len(axes)):
    fig.delaxes(axes[j])

# Adjust layout to prevent overlaps
plt.tight_layout()

# Save the figure as a PNG file
plt.savefig(output_file, dpi=300, bbox_inches='tight')

# Show the figure
plt.show()
