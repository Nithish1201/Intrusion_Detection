import pandas as pd
import numpy as np
from imblearn.under_sampling import RandomUnderSampler
import hashlib
from collections import defaultdict
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import RobustScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
import json 


def drop_timestamp_column(df): 
    df.drop(columns="Timestamp", inplace=True)
    print (df.shape)
    return df


## https://www.researchgate.net/figure/Attack-Types-in-CSE-CIC-IDS2018-dataset_tbl1_333894962
mapping= {'SSH-Bruteforce': 'Brute-force',
          'FTP-BruteForce': 'Brute-force',
          ################ Brute-force 
          
          'Brute Force -XSS': 'Web attack',
          'Brute Force -Web': 'Web attack',
          'SQL Injection': 'Web attack',
          ################ Web attack 
          
          'DoS attacks-Hulk': 'DoS attack',
          'DoS attacks-SlowHTTPTest': 'DoS attack',
          'DoS attacks-Slowloris': 'DoS attack',
          'DoS attacks-GoldenEye': 'DoS attack',
          ################ DoS attack 
          
          'DDOS attack-HOIC': 'DDoS attack',
          'DDOS attack-LOIC-UDP': 'DDoS attack',
          'DDoS attacks-LOIC-HTTP': 'DDoS attack',
          ################ DDoS attack 
          
          'Benign': 'Benign',
          'Label': 'Benign',
          ################ Benign 
    }

def transform_multi_label(df):
    print(df['Label'].value_counts())
    df['Label'] = df['Label'].map(mapping) 
    return df


def balance_data(df):
    X=df.drop(["Label"], axis=1)
    y=df["Label"]

    rus = RandomUnderSampler()
    X_balanced, y_balanced = rus.fit_resample(X, y) 

    df = pd.concat([X_balanced, y_balanced], axis=1)
    del X, y, X_balanced, y_balanced
    print (df.shape)
    print(df['Label'].value_counts())
    
    return df



def hash_series(s):
    return hashlib.md5(pd.util.hash_pandas_object(s, index=False).values).hexdigest()



def main():
    # Read Data
    print('Reading data\n')
    data = pd.read_csv('reduced_combined_data.csv')
    print('Finished reading data')

    print('droping NAs\n')
    print('before: ', data.shape, '\n')
    data = data.dropna()
    print('after: ', data.shape, '\n')

    # Drop Timestamp Cols
    data = drop_timestamp_column(data)


    # Narrow down multi-labels(8) to 4 labels -> ['Benign', 'Brute-force', 'DDoS attack', 'DoS attack']
    data = transform_multi_label(data)


    # Undersample all of the available data for better modelling results
    print('Balancing data\n')
    data = balance_data(data)
    print('Finished balancing data\n')

    # Drop rows with unwanted categories
    unwanted_categories = ['Botnet', 'Infiltration', 'Web attack']
    data = data[~data['Label'].isin(unwanted_categories)]


    # Eliminate Constant columns
    variances = data.var(numeric_only=True)
    constant_columns = variances[variances == 0].index
    data = data.drop(constant_columns, axis=1)


    # Remove columns with entirely same values (duplicates column wise)
    # Hash all columns
    col_hashes = {col: hash_series(data[col]) for col in data.columns}
    hash_map = defaultdict(list)
    # Invert the dict to find duplicates
    for col, h in col_hashes.items():
        hash_map[h].append(col)
    # Get all groups with duplicates
    duplicate_cols = [cols[1:] for cols in hash_map.values() if len(cols) > 1]
    duplicate_cols = [item for sublist in duplicate_cols for item in sublist]
    # Remove those duplicates
    data = data.drop(columns=duplicate_cols)


    # Removing Columns (X Variables) where there is high correlation among X variables
    # pearson correlation heatmap
    plt.figure(figsize=(70, 70))
    corr = data.corr(numeric_only=True)
    # sns.heatmap(corr, annot=True, cmap='RdBu', vmin=-1, vmax=1, square=True) # annot=True
    # plt.show()

    correlated_col = set()
    is_correlated = [True] * len(corr.columns)
    threshold = 0.92
    # Loop over to find columns with higher correlation based on the threshold
    for i in range (len(corr.columns)):
        if(is_correlated[i]):
            for j in range(i):
                if (np.abs(corr.iloc[i, j]) >= threshold) and (is_correlated[j]):
                    colname = corr.columns[j]
                    is_correlated[j]=False
                    correlated_col.add(colname)
    # Drop highly correlated cols
    data.drop(correlated_col, axis=1, inplace=True)


    # TRAIN TEST SPLIT
    label_col = 'Label'
    feature_cols = list(data.columns)
    feature_cols.remove(label_col)

    train_df, test_df = train_test_split(data, test_size=0.2, random_state=2, shuffle=True, stratify=data[label_col])
    del data 


    # Scaling the features (MinMax Scalar)
    minmax_scaler = MinMaxScaler()
    train_df[feature_cols] = minmax_scaler.fit_transform(train_df[feature_cols])
    test_df[feature_cols] = minmax_scaler.transform(test_df[feature_cols])

    # Create and export label mappings for testing
    order_label_list = list(np.unique(train_df[label_col]))
    label_dict = {v:v for v in order_label_list}
    with open("label_dict.json", "w") as outfile: 
        json.dump(label_dict, outfile)

    # Create y_TRAIN and y_TEST data
    y_train = pd.Series([order_label_list.index(k) for k in train_df[label_col]])
    y_test = pd.Series([order_label_list.index(k) for k in test_df[label_col]])

    # Export all data
    y_train.to_csv('data/y_train.csv', index = False, header=['Label'])
    y_test.to_csv('data/y_test.csv', index = False, header=['Label'])
    train_df[feature_cols].to_csv('data/X_train.csv', index = False)
    test_df[feature_cols].to_csv('data/X_test.csv', index = False)


if __name__ == "__main__":
    main()