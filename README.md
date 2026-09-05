# AI-Based Signature Verification System

An automated signature verification system using Deep Learning (CNN) and Image Processing.

## Features

- ✅ Smart Image Quality Checker
- ✅ CNN-based Signature Classification
- ✅ Confidence Score Display
- ✅ PDF Verification Report
- ✅ SQLite Database Logging
- ✅ Tkinter GUI

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Train the model:
```bash
python -c "from src.train import train_model; train_model()"
```

2. Run the application:
```bash
python app.py
```

## Dataset Structure
dataset/
  |-- train/
      |-- genuine/
      |-- forged/
  |-- val/
      |-- genuine/
      |-- forged/
  |-- test/
      |-- genuine/
      |-- forged/

## Technologies
- Python
- TensorFlow/Keras
- OpenCV
- Tkinter
- SQLite
- ReportLab
