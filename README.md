# 🚨 Intrusion Detection System using Machine Learning

This project leverages machine learning to build an efficient **Intrusion Detection System (IDS)** capable of detecting and classifying different types of cyberattacks using the **CSE-CIC-IDS2018** dataset.

## 📁 Project Structure

```
intrusion-detection-ml/
│
├── 📄 data_reduce.py                  # Python script to optimize data types & reduce memory usage
├── 📄 preprocessing_modelling.ipynb   # Jupyter notebook for end-to-end ML pipeline
├── 📄 preprocessing_modelling.pdf     # Exported PDF version of the notebook
│
├── 📄 Project_Proposal.pdf            # Initial project proposal
├── 📄 PPT.pptx                        # Final presentation slides
├── 📁 data/                           # Folder containing original and processed data files
│   ├── *.csv                          # Raw daily network flow data
│   ├── reduced_combined_data.parquet # Optimized dataset used in modeling
│
└── 📄 README.md                       # Project documentation (this file)
```


## 🔍 Project Overview

In today's cybersecurity landscape, real-time detection of malicious traffic is essential. This project builds a **multi-class classification model** that classifies network flow as one of:

- `Benign`
- `DoS attack`
- `DDoS attack`
- `Brute-force attack`

It addresses major challenges in big data processing, such as high dimensionality, imbalanced classes, and memory constraints.

## 🎯 Objectives

- Efficiently load and preprocess >10M records of network flow data.
- Optimize feature space and memory footprint using custom scripts.
- Handle label imbalance using undersampling.
- Build and evaluate multiple ML models including:
  - Decision Tree
  - Random Forest
  - XGBoost

## 🗂️ File Descriptions

### `reduce_data_types.py`
- **Purpose**: Optimizes memory by converting columns to minimal data types.
- **Functionality**:
  - Converts `float64` → `float32`, `int64` → `int16/uint8`, etc.
  - Handles `NaN`, `'Infinity'`, and other inconsistent values.
  - Outputs a lightweight Parquet file for fast loading.

### `preprocessing_modelling.ipynb`
- **Purpose**: Full ML pipeline from raw data to model evaluation.
- **Highlights**:
  - Drops irrelevant, constant, and duplicate columns.
  - Maps granular attack types into 4 broader categories.
  - Balances data using `RandomUnderSampler`.
  - Feature scaling using `MinMaxScaler`.
  - Trains and evaluates 3 classifiers (DT, RF, XGBoost).
  - Evaluates via confusion matrix, accuracy, F1-score.

## 📊 Dataset: CSE-CIC-IDS2018

- **Rows**: ~16 million  
- **Columns**: ~80 features  
- **Source**: [CIC Official Website](https://www.unb.ca/cic/datasets/ids-2018.html)  
- **Attack Types**: Brute Force, DoS, DDoS, Botnet, Web, Infiltration, etc.  
- **Challenge**: 78% of the data is benign — addressed via sampling & harmonization.

## 🧪 Modeling Results

| Model         | Accuracy | Comments                            |
|---------------|----------|-------------------------------------|
| Decision Tree | ~94%     | Simple and interpretable baseline   |
| Random Forest | ~94%     | Robust to noise and overfitting     |
| XGBoost       | **96%**  | Best performance across all metrics |

Final model used **XGBoost**, with:
- No false positives for benign traffic (critical for real-world systems)
- High F1 scores across all categories

## 📌 Key Challenges

- **Data Size**: Colab memory limitations
- **Label Granularity**: Merging similar attack types
- **Feature Redundancy**: Eliminated 20+ highly correlated features
- **Imbalanced Classes**: Balanced using undersampling techniques

## 🚀 How to Run

### Step 1: Run `data_reduce.py`
```
python data_reduce.py
```
This script will output a reduced `.parquet` file.

### Step 2: Open the Notebook
Run all cells in `preprocessing_modelling.ipynb` (or refer to the `preprocessing_modelling.pdf` for results).

---

## 📚 References

- [CSE-CIC-IDS2018 Dataset](https://www.unb.ca/cic/datasets/ids-2018.html)
- `imbalanced-learn`, `xgboost`, `scikit-learn`, `pandas`, `matplotlib`

---

## 👥 Team

- **Nithish Kumar Senthil Kumar**  
- **Subhiksha Murugesan**  
- **Rishi Manohar Manoharan**  
- **Kunal Ahirrao**
