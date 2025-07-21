import pandas as pd
import numpy as np
import ast
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.decomposition import PCA
from xgboost import XGBClassifier
from imblearn.over_sampling import SMOTE

def parse_csi_array(csi_str):
    try:
        return np.array(ast.literal_eval(csi_str.strip('"')))
    except:
        return np.zeros(128)

def load_and_label(file, label):
    df = pd.read_csv(file, encoding="utf-16")
    csi_col = df.columns[-1]
    df["zone"] = label
    df["parsed_csi"] = df[csi_col].apply(parse_csi_array)
    return df

# Load datasets
df1 = load_and_label("ZONE1.csv", "ZONE1")
df2 = load_and_label("ZONE2.csv", "ZONE2")
df3 = load_and_label("ZONE3.csv", "ZONE3")
df4 = load_and_label("ZONE4.csv", "ZONE4")

# Merge
full_df = pd.concat([df1, df2, df3, df4], ignore_index=True)

# Features & labels
X = np.stack(full_df["parsed_csi"].values)
y = full_df["zone"].values

# Label encoding
le = LabelEncoder()
y_encoded = le.fit_transform(y)  # Zone1 => 0, Zone2 => 1, etc.

# Apply SMOTE on confusing classes (Zone1 vs Zone3)
confused_mask = (y_encoded == 0) | (y_encoded == 2)
X_confused = X[confused_mask]
y_confused = y_encoded[confused_mask]

smote = SMOTE(random_state=42)
X_conf_res, y_conf_res = smote.fit_resample(X_confused, y_confused)

# Combine resampled confused data with the rest
X_rest = X[~confused_mask]
y_rest = y_encoded[~confused_mask]

X_final = np.vstack([X_rest, X_conf_res])
y_final = np.hstack([y_rest, y_conf_res])

# 📉 Optional: PCA to denoise
pca = PCA(n_components=60)
X_final_pca = pca.fit_transform(X_final)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_final_pca, y_final, test_size=0.2, random_state=42)

# Train XGBoost Classifier
clf = XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='mlogloss')
clf.fit(X_train, y_train)

#  Evaluate
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)

print(f"\n✅ Accuracy: {acc:.4f}")
print("\n📊 Confusion Matrix:\n", cm)
print("\n📋 Classification Report:\n", report)

# Plot confusion matrix
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", xticklabels=le.classes_, yticklabels=le.classes_)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

# 💾 Save model and encoder
joblib.dump(clf, "csi_zone_model.pkl")
joblib.dump(pca, "csi_zone_pca.pkl")
joblib.dump(le, "csi_zone_label_encoder.pkl")

print("\n✅ Model, PCA, and LabelEncoder saved successfully!")
