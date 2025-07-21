# 📡 EvilRoom - Wi-Fi CSI-Based Real-Time Human Zone Detection

> Detect human presence and location in real-time using Wi-Fi Channel State Information (CSI) with ESP32 and Machine Learning - no cameras or wearables required!

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![ESP32](https://img.shields.io/badge/ESP32-Compatible-red.svg)](https://www.espressif.com/en/products/socs/esp32)

## 🎯 Overview

This project uses **Channel State Information (CSI)** from an ESP32 device to detect and classify human presence into **four predefined zones** within a room using machine learning techniques. The system operates entirely through Wi-Fi signal analysis, making it a non-intrusive privacy-friendly solution.

## 🧠 What is CSI?

Channel State Information (CSI) represents how Wi-Fi signals propagate from transmitter to receiver, capturing fine-grained information about the wireless channel. When humans move through the environment, they cause changes in signal propagation that can be detected and analyzed to determine location and movement patterns.

## ✨ Features

* ❌ **No cameras or wearables** - completely privacy-friendly
* 📍 **Real-time zone detection** with 80.5% accuracy
* 🔄 **Live monitoring** with terminal-based visualization
* 🤖 **Machine learning** powered by XGBoost with PCA and SMOTE
* 📊 **Data balancing** to handle uneven zone occupancy
* ⚡ **Low latency** predictions via serial communication

## 🛠️ Tech Stack

| Component         | Technology                       |
| ----------------- | -------------------------------- |
| **Hardware**      | ESP32 in AP mode                 |
| **Language**      | Python 3.8+                      |
| **ML Model**      | XGBoost Classifier               |
| **Preprocessing** | PCA + SMOTE                      |
| **Communication** | Serial (PySerial)                |
| **UI**            | Terminal-based real-time display |

## 🗂️ Project Structure

```
Seefromwall/
├── ZONE1.csv                 # Training data for Zone 1
├── ZONE2.csv                 # Training data for Zone 2
├── ZONE3.csv                 # Training data for Zone 3
├── ZONE4.csv                 # Training data for Zone 4
├── trainmodel.py             # Model training script
├── live_predict.py           # Real-time prediction script
├── csi_zone_model.pkl        # Trained XGBoost model
├── csi_zone_pca.pkl          # PCA transformer
├── csi_label_encoder.pkl     # Label encoder
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## 📊 Model Performance

Our trained model achieves impressive results:

* **🎯 Accuracy**: 80.5%
* **📈 F1-Score**: 0.80 (macro average)

### Confusion Matrix

|            | Pred Zone 1 | Pred Zone 2 | Pred Zone 3 | Pred Zone 4 |
| ---------- | ----------- | ----------- | ----------- | ----------- |
| **Zone 1** | **151**     | 10          | 24          | 9           |
| **Zone 2** | 6           | **180**     | 10          | 22          |
| **Zone 3** | 20          | 23          | **130**     | 9           |
| **Zone 4** | 2           | 6           | 7           | **150**     |

## 🚀 Quick Start

### Prerequisites

* ESP32 development board
* Python 3.8 or higher
* USB cable for ESP32 connection

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install numpy pandas scikit-learn xgboost joblib imbalanced-learn pyserial
```

### 2. Flash ESP32 with CSI Firmware

Use a CSI-enabled firmware (ESP32 CSI tool or modified ESP-IDF example). This project uses:

> [https://github.com/espressif/esp-csi](https://github.com/espressif/esp-csi) — specifically `csi_recv_router`

The ESP32 was flashed with this to capture CSI data, which was then transmitted via serial to Python.

### 3. Collect Training Data (Optional)

If you want to retrain the model for your specific environment:

```bash
python collect_csi.py  # Collect data for each zone
```

### 4. Train the Model

```bash
python trainmodel.py
```

This generates:

* `csi_zone_model.pkl` - Trained XGBoost classifier
* `csi_zone_pca.pkl` - PCA transformer
* `csi_label_encoder.pkl` - Label encoder

### 5. Run Live Prediction

```bash
python live_predict.py
```

## 📺 Live Monitoring Interface

The system provides a real-time terminal interface showing current zone detection:

```
## 📡 Real-Time CSI Zone Monitor

⚪ ZONE 1
🟢 ZONE 2 ← Active
⚪ ZONE 3  
⚪ ZONE 4
--------
⏱ Updated at: 01:42:01
```

## 📡 Sample CSI Data Format

```
CSI_DATA,0,ee:8a:c6:a9:19:f4,-67,11,1,7,0,0,1,0,0,0,1,-96,0,6,0,8162657,0,126,0,128,1,"[126,96,7,0,28,...,30,17]"
```

The CSI array contains 128 complex values representing the channel response across different subcarriers.

## 🔧 Configuration

### Serial Port Configuration

Update the COM port in `live_predict.py`:

```python
SERIAL_PORT = 'COM5'  # Windows
# SERIAL_PORT = '/dev/ttyUSB0'  # Linux
# SERIAL_PORT = '/dev/cu.usbserial-*'  # macOS
```

### Zone Mapping

Modify zone definitions in your training data collection phase to match your room layout.

## 🧪 How It Works

1. **Data Collection**: ESP32 in AP mode captures CSI packets from Wi-Fi signals
2. **Preprocessing**: Raw CSI data is parsed into 128-element arrays
3. **Feature Engineering**: PCA reduces dimensionality while preserving important features
4. **Data Balancing**: SMOTE handles class imbalance across different zones
5. **Classification**: XGBoost classifier predicts the most likely zone
6. **Real-time Inference**: Live CSI packets are processed and displayed instantly

## 🔮 Future Enhancements

* 🧠 **Deep Learning**: Implement LSTM/CNN for temporal sequence modeling
* 👥 **Multi-person Tracking**: Detect and track multiple individuals
* 🌐 **3D Visualization**: Web-based room visualization with real-time avatars
* 📱 **Mobile Dashboard**: WebSocket-based mobile/web interface
* 🏠 **Smart Home Integration**: MQTT integration for home automation
* 🎯 **Improved Accuracy**: Advanced feature extraction techniques

## 📊 Research Applications

This project has applications in:

* **Smart Buildings**: Occupancy detection and space utilization
* **Healthcare**: Elderly monitoring and fall detection
* **Security**: Intrusion detection systems
* **IoT**: Context-aware smart home automation
* **Research**: Human-computer interaction studies

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

* ESP32 community for CSI extraction tools
* scikit-learn and XGBoost developers
* Research papers on CSI-based human detection

## 👨‍💻 Author

**Madhav Shah**

---

## 🛡️ Disclaimer

This project is for **educational and research purposes only**. Ensure proper privacy compliance and obtain consent when deploying in real environments.

---

⭐ **If you found this project helpful, please give it a star!** ⭐
