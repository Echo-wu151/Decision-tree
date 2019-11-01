from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

#data = pd.read_csv("C:\Users\S\OneDrive\wine.csv")
data = pd.read_csv("iris.csv")
#x, y = data.iloc[:, 1:], data.iloc[:, 0]
x, y = data.iloc[:, 0:4], data.iloc[:, [4]]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)
print(len(x_train))
# 124
print(len(x_test))
    # 54
x_train.to_csv("iris_train.csv")
x_test.to_csv("iris_test.csv")
y_train.to_csv("iris_trainy.csv")
y_test.to_csv("iris_testy.csv")