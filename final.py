import serial
import re
import ast
import joblib
import numpy as np
from time import sleep, strftime
from collections import deque
from sklearn.preprocessing import LabelEncoder

# Load model components
model = joblib.load("csi_zone_model.pkl")
pca = joblib.load("csi_zone_pca.pkl")
le = joblib.load("csi_zone_label_encoder.pkl")

# Serial config
ser = serial.Serial("COM5", 921600, timeout=1)
print("✅ Connected to COM5")

# CSI pattern regex
csi_array_regex = re.compile(r'CSI_DATA.*?"(\[[^\]]+\])"')

# Smooth zone detection
zone_buffer = deque(maxlen=10)

def parse_csi_array(csi_str):
    try:
        return np.array(ast.literal_eval(csi_str.strip('"')))
    except:
        return np.zeros(128)

def predict_zone(csi_vector):
    reduced = pca.transform([csi_vector])
    pred_encoded = model.predict(reduced)[0]
    return le.inverse_transform([pred_encoded])[0]

def display_zone(active_zone):
    print("\033c", end="")  # Clear terminal
    print("📡 Real-Time CSI Zone Monitor")
    print("-----------------------------------")
    for i in range(1, 5):
        symbol = "🟢" if active_zone == f"ZONE{i}" else "⚪"
        print(f"{symbol} ZONE {i}")
    print("-----------------------------------")
    print(f"⏱ Updated at: {strftime('%H:%M:%S')}")

sample_counter = 0

try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if "CSI_DATA" in line:
            sample_counter += 1
            if sample_counter % 20 != 0:
                continue  # Drop unnecessary samples

            match = csi_array_regex.search(line)
            if match:
                csi_raw = match.group(1)
                csi_vector = parse_csi_array(csi_raw)

                if len(csi_vector) == 128:
                    zone = predict_zone(csi_vector)
                    zone_buffer.append(zone)

                    # Majority voting in buffer
                    if len(zone_buffer) == zone_buffer.maxlen:
                        stable_zone = max(set(zone_buffer), key=zone_buffer.count)
                        display_zone(stable_zone)

except KeyboardInterrupt:
    print("\n🛑 Stopped by user")
    ser.close()
