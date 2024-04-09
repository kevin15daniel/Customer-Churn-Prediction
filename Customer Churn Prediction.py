# -*- coding: utf-8 -*-
"""CUSTOMER CHURN PREDICTION USING MLT.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1P16Pjpcn7CuLS8nawD_uUpCFqbpYgcik

### **// Import necessary libraries**
"""

import pandas as pd # pd is used for data manipulation and analysis.
import numpy as np # np is used for numerical computations.
import matplotlib.pyplot as plt # plt is used for creating visualizations.
import seaborn as sns # sns is used for statistical data visualization.
import plotly.express as px # px is used for creating interactive visualizations.
import plotly.graph_objects as go # go is used for creating interactive graphs and visualizations.

from plotly.subplots import make_subplots # It allows you to create subplots within the plotly figures.
# Suppress(es) unnecessary warning messages.
import warnings
warnings.filterwarnings('ignore')

from sklearn.preprocessing import LabelEncoder # It is used to convert categorical labels into numeric form.
from sklearn.preprocessing import StandardScaler # It is used to remove the mean and scale the unit variance, ensuring all features are on the same scale.

from sklearn.model_selection import train_test_split # It is used to split a dataset into training and testing sets for evaluation and validation purposes.
from sklearn.neighbors import KNeighborsClassifier # It is used for classification tasks based on similarity to neighboring data points.

from sklearn.tree import DecisionTreeClassifier # It is used to create decision tree-based models for classification tasks.
from sklearn.ensemble import RandomForestClassifier # It is used to create a MLM that combines multiple decision trees to make predictions.

from sklearn.naive_bayes import GaussianNB # It is used for classification tasks based on bayes' theorem.
from sklearn.svm import SVC # It is used for classification tasks by constructing hyperplanes in a high-dimensional space to separate different classes.

from sklearn.neural_network import MLPClassifier # It is capable of learning complex relationships in data, often used for classification tasks.
from sklearn.ensemble import AdaBoostClassifier # It is used to combine multiple weak classifiers to build a strong classifier.

from sklearn.ensemble import GradientBoostingClassifier # It is used for implementing the gradient boosting ensemble learning method from the scikit-learn library.
from sklearn.ensemble import ExtraTreesClassifier # It is used to create and use an extra trees classifier for machine learning tasks.

from sklearn.linear_model import LogisticRegression # It is used to create and train logistic regression models for classification tasks.
from sklearn.model_selection import train_test_split # It is used to split a dataset into training and testing sets for evaluation and validation purposes.

from sklearn.metrics import accuracy_score # It is used to compute the accuracy of a classification model's predictions.
from xgboost import XGBClassifier # It enables us to utilize xgboost's gradient boosting algorithm for classification tasks.

from sklearn import metrics # It provides various functions for evaluating the performance of a MLM.
from sklearn.metrics import roc_curve # It is used to compute Receiver Operating Characteristic (ROC) curve points for a BCM.

from sklearn.metrics import recall_score, confusion_matrix, precision_score, f1_score, accuracy_score, classification_report # It is used for evaluating the performance of a MLM.
from sklearn.ensemble import VotingClassifier # It is used to create an ensemble classifier that combines predictions from multiple individual classifiers using various voting strategies for improved performance.

# Common libraries used in data visualization:
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.metrics import f1_score, precision_score, recall_score, fbeta_score

from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import cross_val_score

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import ShuffleSplit

from sklearn.model_selection import KFold
from sklearn import feature_selection

from sklearn import model_selection
from sklearn import metrics

from sklearn.metrics import classification_report, precision_recall_curve
from sklearn.metrics import auc, roc_auc_score, roc_curve

from sklearn.metrics import make_scorer, recall_score, log_loss
from sklearn.metrics import average_precision_score

"""### **// Import the dataset**"""

# Import the "Telecommunication.csv" file into a pandas DF
data = pd.read_csv('Telecommunication.csv')

"""### **// Data preparation**

The process of preparing raw data so that it is suitable for further processing and analysis is called as **Data preparation**.
"""

# Check if there are any missing values in the DF
data.isnull().any().any()

# Display information about the DF
data.info()

# Check the shape of the DF
data.shape

import missingno as msno # msno is used for visualizing missing data.

# Display a matrix visualization of missing values in the DF
msno.matrix(data)

# Remove the 'customerID' column from the DF
data = data.drop(["customerID"], axis=1)

# Display the first few rows of the updated DF
data.head()

# Filter rows where 'TotalCharges' column has an empty string
data[data["TotalCharges"] == ' ']

# Convert 'TotalCharges' column to numeric, handling errors by converting them to NaN
data['TotalCharges'] = pd.to_numeric(data.TotalCharges, errors='coerce')

# Calculate the number of missing values in each column of the DF
data.isnull().sum()

# Select rows where the 'tenure' column equals 0
data[data["tenure"] == 0]

# Drop rows from the DF where the 'tenure' column equals 0
data.drop(labels=data[data["tenure"] == 0].index, axis=0, inplace=True)

# Fill missing values in the 'TotalCharges' column with the mean value
data.fillna(data["TotalCharges"].mean())

# Convert 'TotalCharges' column to numeric, handling errors by converting them to NaN
data['TotalCharges'] = pd.to_numeric(data.TotalCharges, errors='coerce')

# Calculate the number of missing values in each column of the DF
data.isnull().sum()

# Display unique values of the 'SeniorCitizen' column in the DF
data.SeniorCitizen.unique()

# Transform 'SeniorCitizen' column values from 0 and 1 to "No" and "Yes"
data.SeniorCitizen = data.SeniorCitizen.map({0: "No", 1: "Yes"})

# Display the first few rows of the updated DF
data.head()

# Describe the 'InternetService' column including object and boolean types
data.InternetService.describe(include=["object", "bool"])

"""### **// Exploratory Data Analysis (EDA)**

It is a common task performed by business analysts to discover patterns, understand relationships, validate assumptions, and identify anomalies in their data. This method is called as **Exploratory Data Analysis**.
"""

# Define the categories
type_ = ["No", "Yes"]

# Create a subplot figure
fig = make_subplots(rows=1, cols=1)

# Add a pie chart trace to the figure
fig.add_trace(go.Pie(labels=type_, values=data['Churn'].value_counts(), name="Churn"))

# Update the style of the pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name", textfont_size=16)

# Update the overall layout of the figure
fig.update_layout (
    title_text = 'CHURN DISTRIBUTION', annotations=[dict(text='CHURN', x=0.5, y=0.5, font_size=20, showarrow=False)])

# Display the figure
fig.show()

# Calculate the number of customers who did not churn, grouped by gender
data.Churn[data.Churn == "No"].groupby(by=data.gender).count()

# Calculate the number of customers who churn, grouped by gender
data.Churn[data.Churn == "Yes"].groupby(by=data.gender).count()

# Set up data
plt.figure(figsize=(6, 6))
labels =["Churn: Yes", "Churn: No"]
values = [1869, 5163]
labels_gender = ["F", "M", "F", "M"]
sizes_gender = [939, 930, 2544, 2619]
colors = ['#ff6666', '#66b3ff']
colors_gender = ['#c2c2f0', '#ffb3e6', '#c2c2f0', '#ffb3e6']
explode = (0.3, 0.3)
explode_gender = (0.1, 0.1, 0.1, 0.1)
textprops = {"fontsize": 15}

# Create pie chart for churn distribution
plt.pie(values, labels=labels, autopct='%1.1f%%', pctdistance=1.08, labeldistance=0.8, colors=colors, startangle=90, frame=True, explode=explode, radius=10, textprops=textprops, counterclock=True, )
plt.pie(sizes_gender, labels=labels_gender, colors=colors_gender, startangle=90, explode=explode_gender, radius=7, textprops=textprops, counterclock=True, )

# Adding a white circle in the middle
centre_circle = plt.Circle((0, 0), 5, color='black', fc='white', linewidth=0)
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

# Add title and adjust layout
plt.title('CHURN DISTRIBUTION', fontsize=15, y=1.1)
plt.axis('equal')
plt.tight_layout()

# Display the figure
plt.show()

# Create a histogram for customer contract distribution
fig = px.histogram(data, x="Churn", color="Contract", barmode="group", title="CUSTOMER CONTRACT DISTRIBUTION")

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.2)

# Display the figure
fig.show()

# Extract unique payment methods and their counts
labels = data['PaymentMethod'].unique()
values = data['PaymentMethod'].value_counts()

# Create pie chart for payment method distribution
fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])

# Update layout
fig.update_layout(title_text="PAYMENT METHOD DISTRIBUTION")

# Display the figure
fig.show()

# Create a histogram for customer payment method distribution
fig = px.histogram(data, x="Churn", color="PaymentMethod", title="CUSTOMER PAYMENT METHOD DISTRIBUTION")

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Count the occurrences of 'InternetService' and 'Churn' columns for male
data[data["gender"]=="Male"][["InternetService", "Churn"]].value_counts()

# Count the occurrences of 'InternetService' and 'Churn' columns for female
data[data["gender"]=="Female"][["InternetService", "Churn"]].value_counts()

# Create a new plotly figure
fig = go.Figure()

# Add data for 'DSL' internet service
fig.add_trace(go.Bar(
  x = [['Churn:No', 'Churn:No', 'Churn:Yes', 'Churn:Yes'],
       ["Female", "Male", "Female", "Male"]],
  y = [965, 992, 219, 240],
  name = 'DSL',
))

# Add data for 'Fiber optic' internet service
fig.add_trace(go.Bar(
  x = [['Churn:No', 'Churn:No', 'Churn:Yes', 'Churn:Yes'],
       ["Female", "Male", "Female", "Male"]],
  y = [889, 910, 664, 633],
  name = 'Fiber optic',
))

# Add data for 'No Internet' service
fig.add_trace(go.Bar(
  x = [['Churn:No', 'Churn:No', 'Churn:Yes', 'Churn:Yes'],
       ["Female", "Male", "Female", "Male"]],
  y = [690, 717, 56, 57],
  name = 'No Internet',
))

# Update layout
fig.update_layout(title_text="CHURN DISTRIBUTION w.r.t. INTERNET SERVICE & GENDER")

# Display the figure
fig.show()

# Define a color map for the 'Dependents' column
color_map = {"Yes": "#FF97FF", "No": "#AB63FA"}

# Create a histogram for dependents distribution
fig = px.histogram(data, x="Churn", color="Dependents", barmode="group", title="DEPENDENTS DISTRIBUTION", color_discrete_map=color_map)

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Define a color map for the 'Partner' column
color_map = {"Yes": '#FFA15A', "No": '#00CC96'}

# Create a histogram for churn distribution w.r.t. partners
fig = px.histogram(data, x="Churn", color="Partner", barmode="group", title="CHURN DISTRIBUTION w.r.t. PARTNER", color_discrete_map=color_map)

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Define a color map for the 'SeniorCitizen' column
color_map = {"Yes": '#00CC96', "No": '#B6E880'}

# Create a histogram for churn distribution w.r.t. senior citizen
fig = px.histogram(data, x="Churn", color="SeniorCitizen", title="CHURN DISTRIBUTION w.r.t. SENIOR CITIZEN", color_discrete_map=color_map)

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Define a color map for the 'OnlineSecurity' column
color_map = {"Yes": "#FF97FF", "No": "#AB63FA"}

# Create a histogram for churn distribution w.r.t. online security
fig = px.histogram(data, x="Churn", color="OnlineSecurity", barmode="group", title="CHURN DISTRIBUTION w.r.t. ONLINE SECURITY", color_discrete_map=color_map)

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Define a color map for the 'PaperlessBilling' column
color_map = {"Yes": '#FFA15A', "No": '#00CC96'}

# Create a histogram for churn distribution w.r.t. paperless billing
fig = px.histogram(data, x="Churn", color="PaperlessBilling",  title="CHURN DISTRIBUTION w.r.t. PAPERLESS BILLING", color_discrete_map=color_map)

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Create a histogram for churn distribution w.r.t. tech support
fig = px.histogram(data, x="Churn", color="TechSupport", barmode="group", title="CHURN DISTRIBUTION w.r.t. TECH SUPPORT")

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Define a color map for the 'PhoneService' column
color_map = {"Yes": '#00CC96', "No": '#B6E880'}

# Create a histogram for churn distribution w.r.t. phone service
fig = px.histogram(data, x="Churn", color="PhoneService", title="CHURN DISTRIBUTION w.r.t. PHONE SERVICE", color_discrete_map=color_map)

# Customize layout settings such as width, height, and gap between bars
fig.update_layout(width=700, height=500, bargap=0.1)

# Display the figure
fig.show()

# Set the context and font scale for seaborn
sns.set_context("paper", font_scale=1.1)

# Create a kernel density estimate plot for MonthlyCharges
ax = sns.kdeplot(data.MonthlyCharges[(data["Churn"] == 'No')], color="Red", shade=True);

# Overlay another kernel density estimate plot for Churn
ax = sns.kdeplot(data.MonthlyCharges[(data["Churn"] == 'Yes')], ax=ax, color="Blue", shade=True);

# Add a legend indicating the meaning of the plotted lines
ax.legend(["Not Churn", "Churn"], loc='upper right');

# Set the x-axis label
ax.set_xlabel("MonthlyCharges (x)");

# Set the y-axis label
ax.set_ylabel("Density (y)");

# Set the title of the plot
ax.set_title("DISTRIBUTION OF MONTHLY CHARGES BY CHURN");

# ---------------------------------------------------------- #

# Customers with high MonthlCharges are more likely to Churn #

# ---------------------------------------------------------- #

# Create a kernel density estimate plot for TotalCharges
ax = sns.kdeplot(data.TotalCharges[(data["Churn"] == 'No')], color="Gold", shade=True);

# Overlay another kernel density estimate plot for Churn
ax = sns.kdeplot(data.TotalCharges[(data["Churn"] == 'Yes')], ax=ax, color="Green", shade=True);

# Add a legend indicating the meaning of the plotted lines
ax.legend(["Not Churn", "Churn"], loc='upper right');

# Set the x-axis label
ax.set_xlabel("TotalCharges (x)");

# Set the y-axis label
ax.set_ylabel("Density (y)");

# Set the title of the plot
ax.set_title("DISTRIBUTION OF TOTAL CHARGES BY CHURN");

# Plot a box plot of 'tenure' against 'Churn'
fig = px.box(data, x='Churn', y='tenure')

# Change the title of the x-axis
fig.update_xaxes(title_text='Churn (x)', row=1, col=1)

# Change the title of the y-axis
fig.update_yaxes(title_text='Tenure (y)', row=1, col=1)

# # Customize layout settings such as autosize, width, height, and title
fig.update_layout(autosize=True, width=750, height=600, title="TENURE vs CHURN", )

# Display the figure
fig.show()

# ---------------------------------------------------------- #

#           New customers are more likely to Churn           #

# ---------------------------------------------------------- #

# Initializing LabelEncoder
le = LabelEncoder()
values

# Label encoding categorical columns with only two unique values
le_count = 0
for col in data.columns[1:]:
    if data[col].dtype == 'object':
        if len(list(data[col].unique())) <= 2:
            le.fit(data[col])
            data[col] = le.transform(data[col])
            le_count += 1

# Print the number of columns label encoded
print('{} columns were label encoded.'.format(le_count))

# Select specific columns from the DF
data2 = data[['SeniorCitizen', 'Partner', 'Dependents', 'tenure', 'PhoneService', 'PaperlessBilling', 'MonthlyCharges', 'TotalCharges']]

# Calculate correlations of selected columns with the 'Churn' column
correlations = data2.corrwith(data.Churn)

# Filter out correlations that are not equal to 1
correlations = correlations[correlations != 1]

# Separate positive and negative correlations
positive_correlations = correlations[correlations>0].sort_values(ascending=False)
negative_correlations = correlations[correlations<0].sort_values(ascending=False)

# Plot correlations as a bar chat
correlations.plot.bar(figsize=(7, 5), fontsize=15, color='grey', rot=45, grid=True)
plt.title("CORRELATION WITH CHURN RATE")

# Set the seaborn style to 'white'
sns.set(style="white")

# Create a heatmap of correlation matrix
plt.figure(figsize=(18, 15))
corr = data.apply(lambda x: pd.factorize(x)[0]).corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
ax = sns.heatmap(corr, mask=mask, xticklabels=corr.columns, yticklabels=corr.columns, annot=True, linewidths=.2, cmap='coolwarm', vmin=0.3, vmax=1)

# Set the seaborn style to 'white'
sns.set(style="white")

# Compute the correlation matrix
corr = data2.corr()

# Create a mask for the upper triangle of the correlation matrix
mask = np.zeros_like(corr, dtype=bool)
mask[np.triu_indices_from(mask)] = True

# Create a matplotlib figure and axes
f, ax = plt.subplots(figsize=(18, 15))

# Define a color palette for the heatmap
cmap = sns.diverging_palette(220, 10, as_cmap=True)

# Create a heatmap of correlation matrix
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, annot=True, linewidths=.5, cbar_kws={"shrink":.5})

# Define a function to encode categorical data
def encode_data(dataframe):
    if dataframe.dtype == "object":
        dataframe = LabelEncoder().fit_transform(dataframe)
    return dataframe

# Apply the 'encode_data' function to all columns in the DF
data = data.apply(lambda x: encode_data(x))

# Display the first few rows of the updated DF
data.head()

# Assign features to X by dropping the 'Churn' column
X = data.drop(columns="Churn")

# Assign the target variable 'Churn' to y as an array
y = data["Churn"].values

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=4, stratify=y)

# Define a function to create a distribution plot for the given feature(s) in a DF
def distplot(feature, frame, color='r'):
    plt.figure(figsize=(8, 3))
    plt.title("Distribution for {}".format(feature))
    ax = sns.distplot(frame[feature], color=color)

col = ["tenure", 'MonthlyCharges', 'TotalCharges']
for features in col :distplot(features, data)

# Standardize the data
data_std = pd.DataFrame(StandardScaler().fit_transform(data[col]).astype('float64'), columns=col)

# Plot the distribution of each feature
for feat in col: distplot(feat, data_std, color='c')

# Display column names in a DF
data.columns

# Display unique values for each column in the DF
for i in data.columns:
    print(i, ":", data[i].unique())

# Identify categorical columns for label encoding
cat_cols_ohe = ['PaymentMethod', 'Contract', 'InternetService']

# Identify categorical columns for label encoding by excluding specific columns
cat_cols_le = list(set(X_train.columns) - set(col) - set(cat_cols_ohe))

# Print the list of categorical columns
print(cat_cols_le)

# Scale the features
scaler = StandardScaler()
X_train[col] = StandardScaler().fit_transform(X_train[col])
X_test[col] = StandardScaler().fit_transform(X_test[col])

models = []

models.append(('Logistic Regression', LogisticRegression(solver='liblinear', random_state=0, class_weight='balanced')))
models.append(('Support Vector Classifier', SVC(kernel='linear', random_state=0)))
models.append(('Kernel SVM', SVC(kernel='rbf', random_state=0)))
models.append(('K-Nearest Neighbour', KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)))
models.append(('Gaussian Naive Bayes', GaussianNB()))
models.append(('Decision Tree Classifier', DecisionTreeClassifier(criterion='entropy', random_state=0)))
models.append(('Random Forest', RandomForestClassifier(n_estimators=100, criterion='entropy', random_state=0)))
models.append(('AdaBoost', AdaBoostClassifier()))
models.append(('Gradient Boosting Classifier', GradientBoostingClassifier()))
models.append(('Voting Classifier', VotingClassifier(estimators=[('gbc', GradientBoostingClassifier()), ('lr', LogisticRegression()), ('abc', AdaBoostClassifier())], voting='soft')))

"""### **// Evaluating the model results**"""

acc_results = [] # List to store accuracy results
auc_results = [] # List to store ROC AUC results
names = [] # List to store model names

# Define columns for the result DF
result_col = ["Algorithm", "ROC AUC Mean", "ROC AUC STD", "Accuracy Mean", "Accuracy STD"]

# Create an empty DF to store model results
model_results = pd.DataFrame(columns = result_col)

i = 0 # Initialize index counter

# Iterate over models list
for name, model in models:
    # Append model name to names list
    names.append(name)

    # Define KFold cross-validator
    kfold = model_selection.KFold(n_splits=10, shuffle=True, random_state=0)

    # Perform cross-validation for accuracy
    cv_acc_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring="accuracy")

    # Perform cross-validation for ROC AUC
    cv_auc_results = model_selection.cross_val_score(model, X_train, y_train, cv=kfold, scoring="roc_auc")

    # Append accuracy and ROC AUC results to respective lists
    acc_results.append(cv_acc_results)
    auc_results.append(cv_auc_results)

    # Add results to the model_results DF
    model_results.loc[i] = [name,
                            round(cv_auc_results.mean() * 100, 2),
                            round(cv_auc_results.std() * 100, 2),
                            round(cv_acc_results.mean() * 100, 2),
                            round(cv_acc_results.std() * 100, 2)]
    i += 1 # Increment index counter

# Sort model_results DF by 'ROC AUC Mean' column in descending order
model_results.sort_values(by=['ROC AUC Mean'], ascending=False)

# Create a boxplot for accuracy results
fig = plt.figure(figsize=(25, 15))
ax = fig.add_subplot(111)
plt.boxplot(acc_results)
ax.set_xticklabels(names)

# Set the x-axis label
plt.xlabel("Baseline Classification Algorithms (x)")

# Set the y-axis label
plt.ylabel("ROC AUC Score (y)")

# Set the title of the plot
plt.title("ACCURACY SCORE COMPARISON")

# Display the plot
plt.show()

# Create a boxplot for accuracy results
fig = plt.figure(figsize=(25, 15))
ax = fig.add_subplot(111)
plt.boxplot(auc_results)
ax.set_xticklabels(names)

# Set the x-axis label
plt.xlabel("Baseline Classification Algorithms (x)")

# Set the y-axis label
plt.ylabel("ROC AUC Score (y)")

# Set the title of the plot
plt.title("ROC AUC COMPARISON")

# Display the plot
plt.show()

"""### **// K-Nearest Neighbour**"""

# Initialize an empty list to store scores
score_array = []

# Loop through values of k from 1 to 24
for each in range(1, 25):
    # Initialize a KNeighborsClassifier with current value of k
    knn_loop = KNeighborsClassifier(n_neighbors=each)

    # Train the classifier
    knn_loop.fit(X_train, y_train)

    # Calculate and append the accuracy score to the list
    score_array.append(knn_loop.score(X_test, y_test))

# Display the list
score_array

# Create a figure with specified size
fig = plt.figure(figsize=(15, 7))

# Plot data with specified color
plt.plot(range(1, 25), score_array, color='#ec838a')

# Set the x-axis label
plt.xlabel("Score (x)")

# Set the y-axis label
plt.ylabel("Range (y)")

# Set the title of the plot
plt.title("OPTIMAL NUMBER OF K-NEAREST NEIGHBOUR")

# plt.legend(loc='top right', fontsize="medium")

# Display the plot
plt.show()

"""### **// Random Forest**"""

# Initialize an empty list to store scores
score_array = []

# Loop through values of k from 1 to 99
for each in range(1, 100):
    # Initialize a RandomForestClassifier with current value of k
    rf_loop = RandomForestClassifier(n_estimators=each, random_state=1)

    # Train the classifier
    rf_loop.fit(X_train, y_train)

    # Calculate and append the accuracy score to the list
    score_array.append(rf_loop.score(X_test, y_test))

# Display the list
score_array

# Iterate over 'score_array' and print each element along with its index
for i, j in enumerate(score_array):
    print(i+1, ":", j)

# Create a figure with specified size
fig = plt.figure(figsize=(15, 7))

# Plot data with specified color
plt.plot(range(1, 100), score_array, color='#ec838a')

# Set the x-axis label
plt.xlabel("Score (x)")

# Set the y-axis label
plt.ylabel("Range (y)")

# Set the title of the plot
plt.title("OPTIMAL NUMBER OF TREES FOR RANDOM FOREST MODEL")

# plt.legend(loc='top right', fontsize="medium")

# Display the plot
plt.show()

"""### **// Iteration - 2**"""

# Define a function for model evaluation metrics
def model_evaluation(y_test, y_pred, model_name):
    # Calculate evaluation metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    f2 = fbeta_score(y_test, y_pred, beta=2.0)

    # Create a DF to store results
    results = pd.DataFrame([[model_name, acc, prec, rec, f1, f2]], columns=["Model", "Accuracy", "Precision", "Recall", "F1 Score", "F2 Score"])

    # Sort results based on precision, recall, and F2 score
    results = results.sort_values(["Precision", "Recall", "F2 Score"], ascending=False)
    return results

# Logistic Regression
classifier = LogisticRegression(random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

# Support Vector Classifier
classifier2 = SVC(kernel='linear', random_state=0)
classifier2.fit(X_train, y_train)
y_pred2 = classifier2.predict(X_test)

# K-Nearest Neighbour
classifier3 = KNeighborsClassifier(n_neighbors=22, metric="minkowski", p=2)
classifier3.fit(X_train, y_train)
y_pred3 = classifier3.predict(X_test)

# Kernel SVM
classifier4 = SVC(kernel="rbf", random_state=0)
classifier4.fit(X_train, y_train)
y_pred4 = classifier4.predict(X_test)

# Gaussian Naive Bayes
classifier5 = GaussianNB()
classifier5.fit(X_train, y_train)
y_pred5 = classifier5.predict(X_test)

# Decision Tree Classifier
classifier6 = DecisionTreeClassifier(criterion="entropy", random_state=0)
classifier6.fit(X_train, y_train)
y_pred6 = classifier6.predict(X_test)

# Random Forest
classifier7 = RandomForestClassifier(n_estimators=72, criterion="entropy", random_state=0)
classifier7.fit(X_train, y_train)
y_pred7 = classifier7.predict(X_test)

# AdaBoost
classifier8 = AdaBoostClassifier()
classifier8.fit(X_train, y_train)
y_pred8 = classifier8.predict(X_test)

# Gradient Boosting Classifier
classifier9 = GradientBoostingClassifier()
classifier9.fit(X_train, y_train)
y_pred9 = classifier9.predict(X_test)

# Voting Classifier
classifier10 = VotingClassifier(estimators=[('gbc', GradientBoostingClassifier()), ('lr', LogisticRegression()), ('abc', AdaBoostClassifier())], voting='soft')
classifier10.fit(X_train, y_train)
y_pred10 = classifier10.predict(X_test)

# Evaluate different models
lr = model_evaluation(y_test, y_pred, "Logistic Regression")
svm = model_evaluation(y_test, y_pred2, "Support Vector Classifier")
knn = model_evaluation(y_test, y_pred3, "K-Nearest Neighbour")
k_svm = model_evaluation(y_test, y_pred4, "Kernel SVM")
nb = model_evaluation(y_test, y_pred5, "Gaussian Naive Bayes")
dt = model_evaluation(y_test, y_pred6, "Decision Tree Classifier")
rf = model_evaluation(y_test, y_pred7, "Random Forest")
ab = model_evaluation(y_test, y_pred8, "AdaBoost")
gb = model_evaluation(y_test, y_pred9, "Gradient Boosting Classifier")
vc = model_evaluation(y_test, y_pred10, "Voting Classifier")

# Concatenate and sort evaluation metrics DF
eval_ = pd.concat([lr, svm, knn, k_svm, nb, dt, rf, ab, gb, vc]).sort_values(["Precision", "Recall", "F2 Score"], ascending=False).reset_index(drop=True)
eval_

# Create a list of predictions
predictions = [y_pred, y_pred2, y_pred3, y_pred4, y_pred5, y_pred6, y_pred7, y_pred8, y_pred9, y_pred10]

# Iterate over predictions and corresponding model names
for i, j in zip(predictions, eval_.Model.values):
    # Create a figure for each confusion matrix
    plt.figure(figsize=(4, 3))

    # Plot heatmap of confusion matrix
    sns.heatmap(confusion_matrix(y_test, i), annot=True, fmt="d", linecolor="k", linewidths=3)

    # Set the title of the plot
    plt.title(j, fontsize=14)

    # Display the plot
    plt.show()

"""### **// Model evaluation**"""

# Define a function for k-fold cross-validation
def k_fold_cross_validation(classifier_name, name):
    accuracies = cross_val_score(estimator=classifier_name, X=X_train, y=y_train, cv=10)
    print(name, "Accuracy: %0.2f (+/- %0.2f)" % (accuracies.mean(), accuracies.std() * 2))

# Call the 'k_fold_cross_validation' function for each classifier
k_fold_cross_validation(classifier, "Logistic regression")
k_fold_cross_validation(classifier2, "Support Vector Classifier")
k_fold_cross_validation(classifier3, "K-Nearest Neighbour")
k_fold_cross_validation(classifier4, "Kernel SVM")
k_fold_cross_validation(classifier5, "Gaussian Naive Bayes")
k_fold_cross_validation(classifier6, "Decision Tree Classifier")
k_fold_cross_validation(classifier7, "Random Forest")
k_fold_cross_validation(classifier8, "AdaBoost")
k_fold_cross_validation(classifier9, "Gradient Boosting Classifier")
k_fold_cross_validation(classifier10, "Voting Classifier")

# Define a ROC curve function
def ROC_curve(classifier_, name, y_pred_):
    # Fit the classifier model on training data
    classifier_.fit(X_train, y_train)

    # Get predicted probabilities for the test data
    probs = classifier_.predict_proba(X_test)
    probs = probs[:, 1]

    # Calculate the ROC AUC score
    classifier_roc_auc = roc_auc_score(y_test, probs)

    # Calculate ROC curve values
    rf_fpr, rf_tpr, rf_thresholds = roc_curve(y_test, classifier_.predict_proba(X_test)[:,1])

    # Plot the ROC curve
    plt.figure(figsize=(14, 6))
    label_ = name + '(area = %0.2f)' % classifier_roc_auc
    plt.plot(rf_fpr, rf_tpr, label=label_)

    # Plot the base rate line
    plt.plot([0, 1], [0, 1], label='Base Rate' 'k--')

    # Set plot limits and labels
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate (x)')
    plt.ylabel('True Positive Rate (y)')
    plt.title('ROC GRAPH')

    # Display legend and show the plot
    # plt.legend(loc="lower right", fontsize="medium")
    plt.show()

# Define lists of predictions, classifiers, and model names
preds = [y_pred, y_pred3, y_pred5, y_pred6, y_pred7, y_pred8, y_pred9, y_pred10]
classifiers = [classifier, classifier3, classifier5, classifier6, classifier7, classifier8, classifier9, classifier10]
model_names_ = ["Logistic Regression", "K-Nearest Neighbour", "Gaussian Naive Bayes", "Decision Tree Classifier", "Random Forest", "AdaBoost", "Gradient Boosting Classifier", "Voting Classifier"]

# Loop through each classifiers, model names, and predictions
for i, j, k in zip(classifiers, model_names_, predictions):
    # Call the ROC_curve function with classifier, model name, and prediction as arguments
    ROC_curve(i, j, k)

# Import necessary libraries
from sklearn.model_selection import cross_val_score

# Define a cross-validation Dictionary Generator function
def cvDictGen(functions, scr, X_train=X, y_train=y, cv=5):
    # Initialize a cross-validation Dictionary
    cvDict = {}
    # Loop through each function
    for func in functions:
        # Compute cross-validation Score
        cvScore = cross_val_score(func, X_train, y_train, cv=cv, scoring=scr)
        # Store mean and standard deviation in cvDict
        cvDict[str(func).split('(')[0]] = [cvScore.mean(), cvScore.std()]
    # Return the cross-validation Dictionary
    return cvDict

# Generate the cross-validated scores Dictionary
cvD = cvDictGen(classifiers, scr='roc_auc')

# Print the result
cvD

"""### **// Feature importance**"""

# AdaBoost Classifier:
# Sort the feature_importances
feature_importances = pd.concat([pd.DataFrame(data.columns, columns=["features"]), pd.DataFrame(np.transpose(classifier8.feature_importances_), columns=["coef"])], axis=1)

# Print 'feature_importances.sort_values' in descending order
feature_importances.sort_values(by="coef", ascending=False)

# Gradient Boosting Classifier:
# Sort the feature_importances
feature_importances = pd.concat([pd.DataFrame(data.columns, columns=["features"]), pd.DataFrame(np.transpose(classifier9.feature_importances_), columns=["coef"])], axis=1)

# Print 'feature_importances.sort_values' in descending order
feature_importances.sort_values(by="coef", ascending=False)

"""### **// Hyperparameter tuning:**

### **// AdaBoost Classifier (RandomizedSearchCV)**
"""

# Import necessary libraries
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

# Define hyperparameters for AdaBoost classifier
adaHyperParams = {"n_estimators": [10, 50, 100, 200, 420],
                  "learning_rate": [0.001, 0.01, 0.1, 0.3]}

# Initialize RandomizedSearchCV with AdaBoost classifier, hyperparameters, and scoring metric
gridSearchAda = RandomizedSearchCV(estimator=classifier8, param_distributions=adaHyperParams, n_iter=5, scoring='roc_auc')

# Fit the RandomizedSearchCV on training data
gridSearchAda.fit(X_train, y_train)

gridSearchAda.best_params_, gridSearchAda.best_score_

# Fit the best estimator found by 'gridSearchAda' on the training data
bestAdaModFitted = gridSearchAda.best_estimator_.fit(X_train, y_train)

# Predict probabilities for the test data
test_labels = bestAdaModFitted.predict_proba(np.array(X_test.values))[:,1]

# Calculate the ROC AUC score using the predicted probabilities and actual test labels
roc_auc_score(y_test, test_labels, average='macro', sample_weight=None)

"""### **// Gradient Boosting Classifier (RandomizedSearchCV)**"""

# Define hyperparameters for Gradient Boosting Classifier
gbHyperParams = {'loss': ['deviance', 'exponential'],
                 'n_estimators': randint(10, 500),
                 'max_depth': randint(1, 10)}

# Initialize RandomizedSearchCV with Gradient Boosting classifier, hyperparameters, and scoring metric
gridSearchGB = RandomizedSearchCV(estimator=classifier9, param_distributions=gbHyperParams, n_iter=10, scoring='roc_auc')

# Fit the RandomizedSearchCV on training data
gridSearchGB.fit(X_train, y_train)

gridSearchGB.best_params_, gridSearchGB.best_score_

# Fit the best estimator found by 'gridSearchGB' on the training data
bestGBModFitted = gridSearchGB.best_estimator_.fit(X_train, y_train)

# Predict probabilities for the test data
test_labels_GB = bestGBModFitted.predict_proba(np.array(X_test.values))[:,1]

# Calculate the ROC AUC score using the predicted probabilities and actual test labels
roc_auc_score(y_test, test_labels_GB, average='macro', sample_weight=None)

"""### **// AdaBoost Classifier (GridSearchCV)**"""

ABC = AdaBoostClassifier()

# Define parameter grid for GridSearchCV
ABC_param_grid = {
    "n_estimators": [10, 50, 100, 200, 420],
    "learning_rate": [0.001, 0.01, 0.1, 0.3]
    }

# Initialize GridSearchCV with AdaBoost classifier, parameter grid, and other settings
gsABC = GridSearchCV(ABC, param_grid=ABC_param_grid, cv=10, scoring="roc_auc", n_jobs=6, verbose=1)

# Fit the GridSearchCV to training data
gsABC.fit(X_train, y_train)

# Get the best estimator
ada_best = gsABC.best_estimator_

# Print the best estimator and its score
print(ada_best)
print(gsABC.best_score_)

# Fit the 'GridSearchCV' to find the best ABC model
bestAdaModFitted2 = gsABC.best_estimator_.fit(X_train, y_train)

# Predict probabilities for the test data
test_labels = bestAdaModFitted2.predict_proba(np.array(X_test.values))[:,1]

# Calculate the ROC AUC score using the predicted probabilities and actual test labels
roc_auc_score(y_test, test_labels, average='macro', sample_weight=None)

"""### **// Gradient Boosting Classifier (GridSearchCV)**"""

# Define parameter grid for GridSearchCV
gb_param_grid = {'loss': ['deviance'],
                 'n_estimators': [10, 100, 200, 300],
                 'max_depth': [1, 2, 4, 6, 8]}

# Initialize GridSearchCV with Gradient Boosting classifier, parameter grid, and other settings
gsGB = GridSearchCV(classifier9, param_grid=gb_param_grid, cv=10, scoring="roc_auc", n_jobs=6, verbose=1)

# Fit the GridSearchCV to training data
gsGB.fit(X_train, y_train)

# Get the best estimator
gb_best = gsGB.best_estimator_

# Print the best estimator and its score
print(gb_best)
print(gsGB.best_score_)

# Fit the 'GridSearchCV' to find the best GBC model
bestGBModFitted2 = gsGB.best_estimator_.fit(X_train, y_train)

# Predict probabilities for the test data
test_labels_gb2 = bestGBModFitted2.predict_proba(np.array(X_test.values))[:,1]

# Calculate the ROC AUC score using the predicted probabilities and actual test labels
roc_auc_score(y_test, test_labels_gb2, average='macro', sample_weight=None)