import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Titanic dataset
data = pd.read_csv("titanic.csv")

# Fill missing values in Age column with median age
data["Age"].fillna(data["Age"].median(), inplace=True)

# Fill missing values in Embarked column with mode
data["Embarked"].fillna(data["Embarked"].mode()[0], inplace=True)

# Fill missing values in Fare column with median fare for each Pclass
data["Fare"].fillna(data.groupby("Pclass")["Fare"].transform("median"), inplace=True)

# Combine SibSp and Parch columns to create FamilySize
data["FamilySize"] = data["SibSp"] + data["Parch"]

# Create IsAlone column
data["IsAlone"] = (data["FamilySize"] == 0).astype(int)

# Extract deck information from Cabin column
data["Deck"] = data["Cabin"].apply(lambda x: x[0] if pd.notnull(x) else "Unknown")

# Extract title from Name column
data["Title"] = data["Name"].str.extract(" ([A-Za-z]+)\.", expand=False)

# Replace rare titles with more common ones
title_mapping = {"Mr": "Mr", "Miss": "Miss", "Mrs": "Mrs", "Master": "Master", "Dr": "Rare", "Rev": "Rare", "Col": "Rare", "Major": "Rare", "Mlle": "Miss", "Countess": "Rare", "Ms": "Miss", "Lady": "Rare", "Jonkheer": "Rare", "Don": "Rare", "Dona": "Rare", "Mme": "Mrs", "Capt": "Rare", "Sir": "Rare"}
data["Title"] = data["Title"].map(title_mapping)

# Drop unnecessary columns
data.drop(["PassengerId", "Name", "Ticket", "Cabin", "SibSp", "Parch"], axis=1, inplace=True)

# One-hot encode categorical variables
data = pd.get_dummies(data, columns=["Pclass", "Sex", "Embarked", "Deck", "Title"], drop_first=True)

# Visualize the correlation between features and the target variable
plt.figure(figsize=(12, 10))
sns.heatmap(data.corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.show()
