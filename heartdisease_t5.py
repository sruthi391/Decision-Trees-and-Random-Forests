# -*- coding: utf-8 -*-
"""HeartDisease_T5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D536fGxUudiRpJUNBxB2sHeYkw9aI9ca
"""

# Run this only once in Colab to install necessary packages
!pip install graphviz --quiet

from google.colab import files

uploaded = files.upload()  # Upload your CSV file

import pandas as pd

# Replace 'heart.csv' with your actual filename after upload
df = pd.read_csv("heart.csv")

# Show first few rows of data
df.head()

from sklearn.model_selection import train_test_split

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Train features shape:", X_train.shape)
print("Test features shape:", X_test.shape)
print("Train labels count:\n", y_train.value_counts())
print("Test labels count:\n", y_test.value_counts())

from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import graphviz

dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(X_train, y_train)

y_pred_dt = dt.predict(X_test)

print("Decision Tree Accuracy:", accuracy_score(y_test, y_pred_dt))
print("\nClassification Report:\n", classification_report(y_test, y_pred_dt))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_dt))

dot_data = export_graphviz(dt, out_file=None,
                           feature_names=X.columns,
                           class_names=["No Disease", "Disease"],
                           filled=True, rounded=True)

graph = graphviz.Source(dot_data)
graph.render("decision_tree")  # Save to file
print("Decision tree saved as 'decision_tree.pdf'")
graph

from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)  # ✅ Fixed here: fit(X_train, y_train), NOT X_test

y_pred_rf = rf.predict(X_test)

print("Random Forest Accuracy:", accuracy_score(y_test, y_pred_rf))
print("\nClassification Report:\n", classification_report(y_test, y_pred_rf))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))

from google.colab import drive

# Mounting the drive
drive.mount('/content/drive')
print("Drive mounted successfully.")

import matplotlib.pyplot as plt
import os

# Get feature importances
importances = rf.feature_importances_
features = X.columns

# Plot feature importances
plt.figure(figsize=(10, 6))
plt.barh(features, importances)
plt.xlabel('Importance')
plt.title('Feature Importances from Random Forest')
plt.tight_layout()
plt.savefig("/content/feature_importances.png")  # Save locally in Colab


# Save to Google Drive
output_path = "/content/drive/My Drive/AI_ML_Internship_Task5"

# Create folder if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Save figure to Drive
plt.savefig(f"{output_path}/feature_importances.png")
print("Feature importance plot saved to Google Drive at:")
print(f"{output_path}/feature_importances.png")
plt.show()

from sklearn.model_selection import cross_val_score

# Decision Tree CV
dt_scores = cross_val_score(dt, X, y, cv=5)
print("\nDecision Tree Cross-Validation Score:", dt_scores.mean())

# Random Forest CV
rf_scores = cross_val_score(rf, X, y, cv=5)
print("Random Forest Cross-Validation Score:", rf_scores.mean())

import seaborn as sns
import matplotlib.pyplot as plt

# Compute correlation matrix
corr = df.corr()

# Plot heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.tight_layout()
plt.savefig("/content/correlation_heatmap.png")

# Save to Google Drive
drive_path = "/content/drive/My Drive/AI_ML_Internship_Task5"
os.makedirs(drive_path, exist_ok=True)
plt.savefig(f"{drive_path}/correlation_heatmap.png")
print("✅ Correlation heatmap saved to Google Drive.")
plt.show()

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# For Decision Tree
cm_dt = confusion_matrix(y_test, y_pred_dt)
disp_dt = ConfusionMatrixDisplay(confusion_matrix=cm_dt, display_labels=["No Disease", "Disease"])
disp_dt.plot(cmap=plt.cm.Blues)
plt.title("Decision Tree - Confusion Matrix")
plt.savefig("/content/confusion_matrix_dt.png")
plt.savefig(f"{drive_path}/confusion_matrix_decision_tree.png")
plt.show()

# For Random Forest
cm_rf = confusion_matrix(y_test, y_pred_rf)
disp_rf = ConfusionMatrixDisplay(confusion_matrix=cm_rf, display_labels=["No Disease", "Disease"])
disp_rf.plot(cmap=plt.cm.Greens)
plt.title("Random Forest - Confusion Matrix")
plt.savefig("/content/confusion_matrix_rf.png")
plt.savefig(f"{drive_path}/confusion_matrix_random_forest.png")
plt.show()
print("Confusion matrices saved to Google Drive.")

from sklearn.model_selection import learning_curve
import matplotlib.pyplot as plt
import numpy as np

train_sizes, train_scores, test_scores = learning_curve(
    dt, X, y, cv=5, scoring='accuracy', n_jobs=-1,
    train_sizes=np.linspace(0.1, 1.0, 10))

train_mean = np.mean(train_scores, axis=1)
test_mean = np.mean(test_scores, axis=1)

plt.plot(train_sizes, train_mean, label="Training score")
plt.plot(train_sizes, test_mean, label="Cross-validation score")
plt.title("Learning Curve")
plt.xlabel("Training Set Size")
plt.ylabel("Accuracy")
plt.legend()
plt.grid()
plt.savefig("/content/learning_curve_dt.png")
plt.savefig(f"{drive_path}/learning_curve_decision_tree.png")
print("✅ Learning curve saved to Google Drive.")
plt.show()

import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("heart.csv")

# Prepare features and target
X = df.drop("target", axis=1)
y = df["target"]

# Create and train model
dt = DecisionTreeClassifier(max_depth=3, random_state=42)

# Cross-validation
scores = cross_val_score(dt, X, y, cv=5)

# Plot results
plt.boxplot(scores, vert=False)
plt.title("Cross-Validation Scores (Decision Tree)")
plt.xlabel("Accuracy")
plt.yticks([])
plt.savefig("/content/cross_validation_scores_dt.png")
plt.savefig(f"{drive_path}/cross_validation_scores_decision_tree.png")
plt.show()

print("Mean CV Accuracy:", scores.mean())