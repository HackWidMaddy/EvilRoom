# predict_zone.py
import numpy as np
import ast
import joblib

def parse_csi_array(csi_str):
    try:
        return np.array(ast.literal_eval(csi_str.strip('"')))
    except:
        return np.zeros(128)

# Load the trained model
clf = joblib.load("csi_zone_model.pkl")

# Input CSI string
csi_input = input("Enter CSI array (e.g. [83,-80,4,0,...]):\n")
parsed_csi = parse_csi_array(csi_input)

# Predict zone
if parsed_csi.shape[0] != 128:
    print("Invalid CSI array length! Must be 128 values.")
else:
    zone = clf.predict([parsed_csi])[0]
    print(f"Predicted Zone: {zone}")
