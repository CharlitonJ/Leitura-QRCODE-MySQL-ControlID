# QRCode-MySQL-ControlID Reader

This application aims to control the exit of vehicles and people through barcode or QR Code reading. It was initially developed to validate invoice access keys and integrates with Control ID devices and a MySQL database.

## Technologies Used

- Python 3.8 or higher  
- Control ID APIs  
- MySQL (or compatible database)  
- Barcode/QR Code Reader (keyboard input mode)

## Requirements

Before running the application, make sure you have:

- Python 3.8 or higher installed  
- Barcode or QR Code reader connected to the machine (keyboard mode)  
- Access to Control ID device  
- Access to Control ID API  
- Access to the database for validation  
- A machine/VM where the application will run  
- Dependencies listed in `requirements.txt`

## How It Works

1. The application stays in listening mode, waiting for code input via the QR/Barcode reader.  
2. When input is detected, it queries the database to validate the data.  
3. If the data is valid, the application triggers the Control ID device via API to allow the person or vehicle to exit.

## Installation

Clone this repository:

```bash
git clone https://github.com/CharlitonJ/Leitura-QRCODE-MySQL-ControlID.git
cd Leitura-QRCODE-MySQL-ControlID
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Use

1. Configure the `config.ini` file with your environment credentials (database and Control ID).  
2. Run the main script:

```bash
python script.py
```

## Private Project

This is a private project and does not have a public license.  
Usage or redistribution without the author's permission is prohibited.

## Author

- Charliton Junior  
- GitHub: https://github.com/CharlitonJ  
- LinkedIn: https://www.linkedin.com/in/charliton-junior/
