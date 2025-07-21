import serial
import re

ser = serial.Serial("COM5", 921600, timeout=1)

# Extract the array inside double quotes after CSI_DATA
csi_array_regex = re.compile(r'CSI_DATA.*?"(\[[^\]]+\])"')

print("Reading CSI data and extracting CSI array only...")
try:
    while True:
        line = ser.readline().decode(errors='ignore').strip()
        if "CSI_DATA" in line:
            match = csi_array_regex.search(line)
            if match:
                csi_array_str = match.group(1)  # includes the square brackets
                print(csi_array_str)
except KeyboardInterrupt:
    print("Stopped.")
    ser.close()
