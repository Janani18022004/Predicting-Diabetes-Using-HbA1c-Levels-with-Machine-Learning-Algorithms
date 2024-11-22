import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt  # data visualization
import seaborn as sns  # data visualization
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

import pickle
df = pd.read_csv('Dataset/diabetes_prediction_dataset.csv')

print(df.head())

print(df.shape)

# preprocessing
df.drop_duplicates(inplace=True)
print(df.shape)
df.isnull().sum()

print(df['diabetes'].value_counts())

plt.figure(figsize=(6, 6))
sns.histplot(df['age'])
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

categorical_vars = ['gender', 'hypertension', 'heart_disease', 'smoking_history', 'HbA1c_level', 'blood_glucose_level']
# defining the categorical variables to create multiple plots using one code
nrows = 2  # plotting the graphs on the same page
ncols = 3

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(20, 10))
axs = axs.flatten()

for i, var in enumerate(categorical_vars):  # creating for loop for all the variables
    ax = axs[i]
    sns.countplot(x=var, data=df, hue='diabetes', ax=ax)
    ax.set_title(f'Distribution of {var}')

plt.tight_layout()  # prevents overlapping
plt.show()

print("COM")
X = df[["age", "hypertension", "heart_disease", "bmi", "HbA1c_level", "blood_glucose_level" ]]
y = df['diabetes']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape)
rf = RandomForestClassifier(n_estimators=100, random_state=0)
rf.fit(X_train, y_train)

filename = 'model.pkl'
pickle.dump(rf, open(filename, 'wb'))

print("Training Accuracy :" + str(rf.score(X_train, y_train)))

print("Testing Accuracy :" + str(rf.score(X_test, y_test)))

y_pred = rf.predict(X_test)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, y_pred)
print('Confusion Matrix:\n', cm)

import seaborn as sns
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()
