import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs("output", exist_ok=True)

# ============================================================
# LOAD DATASET
# ============================================================

df = pd.read_csv("All_Diets.csv")

# ============================================================
# DATA CLEANING
# ============================================================

# Nutritional columns used throughout the analysis
nutrition_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]

# ------------------------------------------------------------
# PERFORMANCE ENHANCEMENT
# Convert all nutritional columns to numeric in one operation
# using vectorized Pandas functions. Invalid values become NaN.
# ------------------------------------------------------------

df[nutrition_cols] = df[nutrition_cols].apply(
    pd.to_numeric,
    errors="coerce"
)

# ------------------------------------------------------------
# PERFORMANCE ENHANCEMENT
# Fill all missing nutritional values at once using the mean
# of each column. This avoids repeated loops and ensures the
# dataset is clean before performing calculations.
# ------------------------------------------------------------

df[nutrition_cols] = df[nutrition_cols].fillna(
    df[nutrition_cols].mean()
)

# Fill missing categorical values
if "Diet_type" in df.columns:
    df["Diet_type"] = df["Diet_type"].fillna("Unknown")

if "Cuisine_type" in df.columns:
    df["Cuisine_type"] = df["Cuisine_type"].fillna("Unknown")

# ============================================================
# PERFORMANCE ENHANCEMENT
# Group the dataset once and reuse it throughout the script.
# This avoids repeatedly scanning the DataFrame with groupby().
# ============================================================

diet_groups = df.groupby("Diet_type")

# ============================================================
# AVERAGE MACRONUTRIENTS
# ============================================================

avg_macros = (
    diet_groups[nutrition_cols]
    .mean()
    .round(2)
)

print("\n===== Average Macronutrients =====")
print(avg_macros)

avg_macros.to_csv("output/average_macros.csv")

# ============================================================
# TOP 5 PROTEIN-RICH RECIPES
# ============================================================

# ------------------------------------------------------------
# PERFORMANCE ENHANCEMENT
# nlargest() retrieves only the five highest protein recipes
# for each diet group instead of sorting the entire dataset.
# ------------------------------------------------------------

top5 = (
    diet_groups.apply(
        lambda x: x.nlargest(5, "Protein(g)")
    )
    .reset_index(drop=True)
)

print("\n===== Top 5 Protein-rich Recipes =====")
print(top5)

top5.to_csv("output/top5_protein.csv", index=False)

# ============================================================
# DIET TYPE WITH HIGHEST AVERAGE PROTEIN
# ============================================================

average_protein = diet_groups["Protein(g)"].mean()

highest_protein_diet = average_protein.idxmax()
highest_protein_value = average_protein.max()

print("\n===== Diet Type with Highest Average Protein =====")
print(f"Diet Type: {highest_protein_diet}")
print(f"Average Protein: {highest_protein_value:.2f} g")

# ============================================================
# HIGHEST PROTEIN RECIPE
# ============================================================

highest_recipe = df.loc[df["Protein(g)"].idxmax()]

print("\n===== Highest Protein Recipe =====")
print(highest_recipe)

# ============================================================
# MOST COMMON CUISINE
# ============================================================

common_cuisine = (
    diet_groups["Cuisine_type"]
    .agg(lambda x: x.mode().iat[0] if not x.mode().empty else np.nan)
)

print("\n===== Most Common Cuisine by Diet Type =====")
print(common_cuisine)

common_cuisine.to_csv("output/cuisine_counts.csv")

# ============================================================
# CREATE NEW METRICS
# ============================================================

# ------------------------------------------------------------
# PERFORMANCE ENHANCEMENT
# Prepare denominator columns once to avoid repeating the
# replace() operation and safely prevent division by zero.
# ------------------------------------------------------------

safe_carbs = df["Carbs(g)"].replace(0, np.nan)
safe_fat = df["Fat(g)"].replace(0, np.nan)

df["Protein_to_Carbs_ratio"] = (
    df["Protein(g)"] / safe_carbs
)

df["Carbs_to_Fat_ratio"] = (
    safe_carbs / safe_fat
)

# ============================================================
# SAVE CLEANED DATASET
# ============================================================

df.to_csv("output/cleaned_dataset.csv", index=False)

# ============================================================
# BAR CHART
# ============================================================

avg_macros.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Average Macronutrients by Diet Type")
plt.xlabel("Diet Type")
plt.ylabel("Grams")
plt.tight_layout()

plt.savefig("output/average_macros.png")
plt.show()

# ============================================================
# HEATMAP
# ============================================================

plt.figure(figsize=(8, 5))

sns.heatmap(
    avg_macros,
    annot=True,
    cmap="YlGnBu",
    fmt=".1f"
)

plt.title("Macronutrient Heatmap")
plt.tight_layout()

plt.savefig("output/heatmap.png")
plt.show()

# ============================================================
# SCATTER PLOT
# ============================================================

plt.figure(figsize=(12, 7))

sns.scatterplot(
    data=top5,
    x="Cuisine_type",
    y="Protein(g)",
    hue="Diet_type",
    s=120
)

plt.xticks(rotation=45)

plt.title("Top 5 Protein-rich Recipes by Cuisine")

plt.tight_layout()

plt.savefig("output/protein_scatter.png")

plt.show()

# ============================================================
# ANALYSIS COMPLETE
# ============================================================

print("\n===== Analysis Complete =====")
print("Outputs saved inside the output/ folder.")

print("- cleaned_dataset.csv")
print("- average_macros.csv")
print("- top5_protein.csv")
print("- cuisine_counts.csv")
print("- average_macros.png")
print("- heatmap.png")
print("- protein_scatter.png")
