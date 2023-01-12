# -*- coding: utf-8 -*-
"""HS22_BigData_Final_Project_JM_Euler.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11uFPJh6JtC3wx6jIWivrRvwA1TC8a3T0

# General Instructions

**PLEASE DO NOT SHARE THE DATASETS and NOTEBOOK with other people!!!!**

You have the option to analyze one of two datasets for the endterm and: 

*   Predict diabetes (current status or future onset) from clinical imaging data or molecular parameters; or
*   Predict COVID death or intensive care unit (ICU) admission from lifestyle and clinical parameters.

## Required final project components
### Part 1
Describe the population with regards to the outcome you chose (e.g. comparison of age distribution for patients who died vs patients who didn't die, comparison of gender vs diabetes status, comparison ) with at least three plots, which are accurately labeled and interpreted. In this part, also consider pre-processing and describing your data with regards to the missing data.

### Part 2
#### For the COVID analysis
The first COVID cases were discovered in Mexico on February 28th 2020. Using pd.to_datetime to convert the date of death into a datetime object, then using the deltatime object of time elapsed from the first COVID cases (pd.to_datetime('28.02.2020')) until death as the time to event, plot a Kaplan-Meier curve for the people who have died of COVID, subgrouped by any variable of your choosing (e.g. males vs females, younger/older than 65, with/without pneumonia, smokers yes/no).

#### For the Diabetes analysis
Use any clustering algorithm of your chosing to cluster the individuals in the dataset based on either clinical imaging or metabolomics data. 
Then choose the visualization method that you prefer to visualize the different clusters (variable 1 vs variable 2, diabetes vs age, PC1 vs PC2, tSNE, etc). 

### Part 3
* Predict your outcome of interest according to 2 distinct machine learning methods that we have learnt.

* For each prediction, show confusion plot of the train and test dataset and indicate:
  1.  accuracy;
  2.  precision;
  3.  recall.

* Interpret the results from each ML method, and comment how the predictions could be improved.


**Examples**

*Use Random Forest classifier and K-NN classifier to predict whether a patient will die of COVID.*

or

*Use Gradient Boosting classifier and logistic regression to predict with clinical imaging data (and patients info) whether someone currently has diabetes.*

## Extra points (ordered from most to least rewarded) 

You can get extra points (in addition to the max points of the endterm) if you:

* Run the analysis on Euler using the entire dataset (for that option you would also to upload your code as a .py file, the command used to run the script on Euler and the output of your code, i.e. the slurm file and any figure/table saved as part of your analysis).
* Fine tune the methods parameters using GridSearchCV;
* Show which covariate(s) contributes the most to the prediction (from one method is sufficient);
* Plot the covariate(s) that contributes the most to the prediction as a function of the outcome.

## Analysis notes

* Remember to drop NAs if necessary and standardize the data where relevant. 

* Some covariates might strongly correlate with each other. If so, show a representative plot and drop the rendundant ones.

* This are a real-world datasets. It is normal that the predictions won't have very high accuracy/precision/recall.

* Provide visualisation and interpretation of your results.

## Submission method

Same as for the midterm. Please do not copy/paste from each other.

## Deadline

The deadline is in approximately one month and 10 days from now, on January 15th. If you need more time, let us know.

# Dataset 1: COVID outcomes
For this final project, you will work with real-world COVID patients data. 

You can decide on the outcome that you want to study:
* whether a patient died;
* whether a patient was admitted to the intensive care unit (ICU)

You can decide on the dataset you want to use:
* the reduced version (n = 100'000)
* the entire dataset (n = 1'048'576) --> Euler becomes essential

## Dataset

You can choose to use the subset we provide or the entire dataset that you can access from [Kaggle](https://www.kaggle.com/datasets/meirnizri/covid19-dataset).
"""

import pandas as pd

import numpy as np

covid = pd.read_csv('CovidData.csv')

import warnings
warnings.filterwarnings("ignore")

"""## Dataset dictionary

The dataset was provided by the Mexican government. This dataset contains an enormous number of anonymized patient-related information including pre-conditions. The raw dataset consists of 21 unique features and 1'048'576 unique patients. In the Boolean features, 1 means "yes" and 2 means "no". Values encoded as 97 and 99 are missing data.

* sex: female or male.
* age: of the patient.
* patient type: type of care the patient received in the unit. 1 for returned home and 2 for hospitalization..
* pneumonia: whether the patient already have air sacs inflammation or not.
* pregnancy: whether the patient is pregnant or not.
* diabetes: whether the patient has diabetes or not.
* copd: Indicates whether the patient has Chronic obstructive pulmonary disease or not.
* asthma: whether the patient has asthma or not.
* inmsupr: whether the patient is immunosuppressed or not.
* hypertension: whether the patient has hypertension or not.
* cardiovascular: whether the patient has heart or blood vessels related disease.
* renal chronic: whether the patient has chronic renal disease or not.
* other disease: whether the patient has other disease or not.
* obesity: whether the patient is obese or not.
* tobacco: whether the patient is a tobacco user.
* usmr: Indicates whether the patient treated medical units of the first, second or third level.
* medical unit: type of institution of the National Health System that provided the care.
* intubed: whether the patient was connected to the ventilator.
* icu: Indicates whether the patient had been admitted to an Intensive Care Unit.
* death: indicates whether the patient died or recovered.

Note: you can ignore the column "CLASIFFICATION_FINAL"

Source: [Kaggle](https://www.kaggle.com/datasets/meirnizri/covid19-dataset)
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import pylab as pl
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

import scipy as sp
from scipy import stats
# %pylab inline

"""# Graphical analysis + data filtering"""

len(covid)

covid.drop_duplicates(inplace=True)
covid.dropna(inplace=True)

covid.dtypes

covid_died1 = covid[covid.DATE_DIED.str.contains("9999-99-99") == False]
covid_alive=covid[covid.DATE_DIED.str.contains("9999-99-99") == True]
covid_alive["died"]="alive" #0 means ALIVE
covid_died1["died"]="dead"  #1 means DEAD
# divided the data sets based on dead or not, later gave 1 and 2

df= pd.merge(covid_died1, covid_alive, how="outer")
len(df)

df["died"].value_counts(normalize=True)

df= df.dropna(subset=['AGE'])

print("patients 99 age:", df[df['AGE']==99].value_counts().sum())

dict1=["Under 50", "between 50 and 59", "between 60 and 69", "between 70 and 79","between 80 and 89", "Over 90 "]
dict2= [df[df['AGE']< 50],
        df[(df['AGE']>= 50.0) & (df['AGE']<60.0)],
        df[(df['AGE']>= 60.0) & (df['AGE']<70.0)],
        df[(df['AGE']>= 70.0) & (df['AGE']<80.0)],
        df[(df['AGE']>= 80.0) & (df['AGE']<90.0)],
        df[df['AGE']>=90]]

value_alive=[]
value_dead=[]

for i in range(6):
  a=(dict2[i]['died'].value_counts(normalize=True).sort_index(ascending=False)["alive"]) 
  value_alive = np.append(value_alive, a)
  b=(dict2[i]['died'].value_counts(normalize=True).sort_index(ascending=False)["dead"]) 
  value_dead = np.append(value_dead, b)

value_dead

value_alive

# want to compare patients who died to patients who didn't die 
n=6
r = np.arange(6)
width = 0.25  

plt.bar(r, value_alive*100, color = ['blue'], width = width, edgecolor = 'black', label='% of alive in age group when positive to COVID')
plt.bar(r + width, value_dead*100, color = ['orange'],width = width, edgecolor = 'black',label='% of dead in age group when positive to COVID')

plt.xticks(r + width/2,["Under 50", "between 50 and 59", "between 60 and 69", "between 70 and 79","between 80 and 89", "Over 90 "])
plt.xlabel('Age Groups')
plt.xticks(rotation=90) 
plt.ylabel('% of alive vs dead in the age group')
plt.title('Covid patients, alive/dead % in age groups') 
plt.legend(loc='center left', bbox_to_anchor=(1,0.5), title= "Legend")  
plt.savefig("DiedvsAlive_age.png", bbox_inches='tight')
plt.close()

"""With increasing age the percentage of people who die from covid increase. (not done with statistical analysis but by observing the graph)"""

df["DIABETES"].value_counts()
# Here we have the 98 value, however we are looking if the person is affected by the disease, =1 no need to remove the 98

# pneumonia patients vs non pneumonia patients outcome 2 --> means not obese 
# 1 means has pneumonia (YES), 2 means (NO)
# taking patients with diesease and seeing outcome, dead or alive--> making graph to compare the different conditions 
disease=("HIPERTENSION","PNEUMONIA","DIABETES","CARDIOVASCULAR", "TOBACCO","OBESITY", "RENAL_CHRONIC")

for i in range(len(disease)):
  df= df.dropna(subset=[disease[i]])

alive_disease=[]
dead_disease=[]

for i in range(len(disease)):
  a=df[df[disease[i]]==1]['died'].value_counts().sort_index(ascending=False)["dead"]
  dead_disease = np.append(dead_disease, a)
  b=df[df[disease[i]]==1]["died"].value_counts().sort_index(ascending = False)["alive"] 
  alive_disease = np.append(alive_disease, b)

df[df["DIABETES"]==1]['died'].value_counts().sort_index(ascending=False)

df[df["DIABETES"]==1]['died'].value_counts().sort_index(ascending=False)["alive"]  # to check if the results are correct

alive_disease

n=(len(disease))
r = np.arange(len(disease))
width = 0.25

plt.bar(r,alive_disease, width=width,label='positive to covid and disease, alive') 
plt.bar(r+width,dead_disease, width=width,label='postive to covid and disease, dead')

plt.xticks(r + width/2,disease)
plt.ylabel("absolute number of patients")
plt.xlabel('Various diseases of the patients')
plt.title("Covid patients with disease, alive or dead")
plt.legend()
plt.xticks(rotation=90) 
plt.legend(loc='center left', bbox_to_anchor=(1,0.5), title= "Legend") 
plt.savefig('Covid_disease_dead_alive.png', bbox_inches='tight')
plt.close()

"""With this graph, I wanted to see the effect of a disease on patient death. In the graph all patients have the disease on the x axis and are positive to covid. Additionally one can see if the patient with the disease and positive to covid, is dead or alive. 
For example when one is diagnosed with Pneumonia, the "chances" of dying are much higher, as most patients die. Obestity instead doesn't seem to be so influencial.
These observations are done by observing the graph, not by statistical analysis 
"""

covid_died1[covid_died1["RENAL_CHRONIC"]==1]["SEX"].value_counts().sort_index(ascending = False)

#gender, died with disease, how is the distribution with gender 
# 1 means has pneumonia (YES), 2 means (NO)
covid_died1 #data set with people who died, sex female 1, male 2
disease=("HIPERTENSION","PNEUMONIA","DIABETES","CARDIOVASCULAR", "TOBACCO","OBESITY", "RENAL_CHRONIC")
male=[]
female=[]
#1 - female  2 - male
for i in range(len(disease)):
  a=covid_died1[covid_died1[disease[i]]==1]["SEX"].value_counts().sort_index(ascending = False)[2] #2 is male
  male = np.append(male, a)
  b=covid_died1[covid_died1[disease[i]]==1]["SEX"].value_counts().sort_index(ascending = False)[1] # 1 is female 
  female = np.append(female, b)

male

female

covid_died1[covid_died1["RENAL_CHRONIC"]==1]["SEX"].value_counts().sort_index(ascending = False) # 1 is female , 2 is male

covid_died1[covid_died1["RENAL_CHRONIC"]==1]["SEX"].value_counts().sort_index(ascending = False)[1] # gives you the value of the one

covid_died1[covid_died1["RENAL_CHRONIC"]==1]["SEX"].value_counts().sort_index(ascending = False).values[1] #position 0, then 1 (second)

n=(len(disease))
r = np.arange(len(disease))
width = 0.25

plt.bar(r,male, width=width,label='positive to covid, with disease, dead, male', color="blue") 
plt.bar(r+width,female, width=width,label='postive to covid with disease, dead, female', color="red")

plt.xticks(r + width/2,disease)
plt.ylabel("absolute number of patients")
plt.xlabel('Various diseases of the patients')
plt.title(" Dead covid patients with disease, male vs female")
plt.legend()
plt.xticks(rotation=90) 
plt.legend(loc='center left', bbox_to_anchor=(1,0.5), title= "Legend") 
plt.savefig('Covid_dead_male_female.png', bbox_inches='tight')
plt.close()

print("covid died data set")
print(covid_died1["SEX"].value_counts(normalize=True))

print("covid data set")
print(df["SEX"].value_counts(normalize=True))

"""In this graph I looked at all of the dead patients with the disease, and differentiated them by sex. In all of the diseases, the death rate is higher in the male group. It should be noted that in the initial data set, with alive and dead patients, there are 62% males and 38% females. This could be due to bad sampling in the smaller data set, or males have a higher chance of becoming infected by covid thus having a higher percentage in the within the data sets.

# Kepler Meier Diagram
"""

covid_died = covid[covid.DATE_DIED.str.contains("9999-99-99") == False]

'''
!pip install lifelines
'''

from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
from lifelines import KaplanMeierFitter

kmf = KaplanMeierFitter()

pd.to_datetime(covid_died["DATE_DIED"])
day1=pd.to_datetime('28.02.2020')
covid_died["time_elapsed"]=pd.to_datetime(covid_died["DATE_DIED"])-day1
covid_died["died"]=1

covid_died["time_elapsed"].min()

covid_died["DATE_DIED"].min()
covid_died.drop(covid_died[covid_died['time_elapsed'] < "0 days"].index, inplace = True)
# there a few dates that slipped in that are before the 28 of feb.--> give a negative result

covid_died["time_elapsed"].min()

covid_died['time_elapsed_int'] = covid_died['time_elapsed'].dt.days.astype('int16')

"""First on how the death rate evolved over tie, comparing died (in this data set all the patints died), with time elapsed """

kmf = KaplanMeierFitter()

kmf.fit(covid_died['time_elapsed_int'],covid_died['died'])
kmf.plot_survival_function()
plt.ylabel('Survival probability')
plt.xlabel('Days since first covid diagnosis')
plt.title("Kepler Meier graph of patients who died of Covid")

plt.close()

covid_died.drop(covid_died[covid_died['PNEUMONIA'] == 99].index, inplace = True)

covid_died['PNEUMONIA'].value_counts()

kmf = {}
legend=["","positive to pneumonia", "negative to pneumonia"]
#1 means "yes" and 2 means "no"
for i in covid_died['PNEUMONIA'].unique():
  print(i)
  kmf[i] = KaplanMeierFitter()
  df1 = covid_died[covid_died['PNEUMONIA'] == i]
  kmf[i].fit(df1['time_elapsed_int'], event_observed=df1['died'])
  kmf[i].plot_survival_function(label = legend[i])

plt.ylabel('Survival probability')  
plt.title("Kepler Meier graph of patients who died of Covid with or without pneumonia")
plt.xlabel('Days since first covid diagnosis')
plt.savefig('KeplerMeier_pneumonia.png', bbox_inches='tight')
plt.close()

"""In this data set all the people have died, and the difference between people with or without on death outcome is minimal. This is also seen later in the modelling part, where pneumonia does play a role but is not very important."""

covid_died["time_elapsed_int"].max()

"""# ML

Predict your outcome of interest according to 2 distinct machine learning methods that we have learnt.
For each prediction, show confusion plot of the train and test dataset and indicate:
accuracy;
precision;
recall.
Interpret the results from each ML method, and comment how the predictions could be improved.
Examples
Use Random Forest classifier and K-NN classifier to predict whether a patient will die of COVID.

Random Forest classifier:

1.   Initial ML
2.   Optimisation with searchCV
"""

covid_alive["died"]=0 #0 means ALIVE
covid_died1["died"]=1  #1 means DEAD
# divided the data sets based on dead or not
df1= pd.merge(covid_died1, covid_alive, how="outer")

"""Used the data set, without the time elapsed or date died. Want to look at only the diseases intially. 



In this version of the code, all the other parameters were used (can be seen in the variable features)
"""

df1

df1["PATIENT_TYPE"].value_counts()

df1[df1["SEX"]==1]["PREGNANT"].value_counts()
# 1 is female, there are 98 non values--> delete

df1.drop(df1[(df1["SEX"]==1) & (df1["PREGNANT"]==98)].index, inplace = True)
# Dropping all of the females with 98, as we don't know if they are pregnant or not 
# 1 means "yes" and 2 means "no"

df1[df1["SEX"]==2]["PREGNANT"].value_counts()
# these are all males, can change the value to 2, not pregnant

# changing the values for all males to 2, not pregnant 
df1['PREGNANT'] = df['PREGNANT'].replace([97], [2])

df1["ICU"].value_counts()

features_filter = list(df1.columns)
print("len of all features", len(features_filter))
features_filter.remove("AGE")
features_filter.remove("DATE_DIED")
features_filter.remove("CLASIFFICATION_FINAL")

for i in range(len(features_filter)):
  df1.drop(df1[df1[features_filter[i]] == 97].index, inplace = True)
  df1.drop(df1[df1[features_filter[i]] == 99].index, inplace = True)
  df1.drop(df1[df1[features_filter[i]] == 98].index, inplace = True)

features_filter = list(df1.columns)
features_filter.remove("DATE_DIED")
features_filter.remove("CLASIFFICATION_FINAL")
len(features_filter)

'''
Initial features that were analysed, in this analysis all the features beside date died and classification were analysed
features = df1[["MEDICAL_UNIT","SEX","AGE","PATIENT_TYPE","INTUBED","PNEUMONIA","DIABETES","CARDIOVASCULAR", "TOBACCO","OBESITY", "RENAL_CHRONIC"]]
values that we want to see how the correlation is 
features = np.array(features)
'''
features= df1[features_filter] #date died and classification final are already removed 
features= df1[[i for i in features if "died" not in i]]# need to remove died as this is what we are trying to predict
labels = df1['died']# value that we want to predict

"""Check if there is a high correlation with the variables"""

plt.figure(figsize=(20,20))
sns.heatmap(features.corr(),annot=True, cmap='RdBu', vmin=-1, vmax=1)
plt.title('Correlation Matrix')
plt.savefig('Correlation_matrix.png', bbox_inches='tight')
plt.close()

df1["PATIENT_TYPE"].value_counts()

"""As patient type now only has 2, it could be removed from features, but i left it in in case that in the euler data set something changes. In the feature importance for this model, as expected the result is 0."""

from sklearn.model_selection import train_test_split
# splitting data set into training and testing
train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42, stratify = labels)
# died, date died and classification final are removed from the feature data sets (22-3)=19

print('Training Features Shape:', train_features.shape)
print('Training Labels Shape:', train_labels.shape)
print('Testing Features Shape:', test_features.shape)
print('Testing Labels Shape:', test_labels.shape)

"""For the first model I choose a Random Forest Classifier """

# Here the model was fitted with the TRAIN data set 
from sklearn import ensemble
from sklearn.ensemble import RandomForestClassifier
from sklearn import tree
prediction_model =  ensemble.RandomForestClassifier(max_depth=3, criterion="gini", random_state=2021).fit(train_features,train_labels)
print ("score %.2f"%prediction_model.score(train_features.values, train_labels))
# run the train model and see the score

from sklearn.metrics import plot_confusion_matrix
# see the confusion matrix for the model on TRAIN data set
plot_confusion_matrix(prediction_model,train_features, train_labels, cmap='inferno',values_format='g')
plt.title("Confusion matrix, train data set")
plt.show()
plt.savefig('RFC_confusion_matrix_train_data.png')
plt.close()

# calculate the predicted survival rate, with the TRAIN features 
predicted_survival_train = prediction_model.predict(train_features)

#function to print results with TRAIN set and prediction variable
from sklearn import metrics
def getresults(test,pred_variable):
    return 'Precision:', metrics.precision_score(test,pred_variable), 'Recall: ', metrics.recall_score(test,pred_variable),"Accuracy:", metrics.accuracy_score(test,pred_variable), "F1:", metrics.f1_score(test,pred_variable)
print("Outcomes with RandomForestClassifier model with train set")
print(getresults(train_labels,predicted_survival_train)) #need to have the labels here

#see the matrix with the TEST features 
from sklearn.metrics import plot_confusion_matrix

plot_confusion_matrix(prediction_model,test_features, test_labels, cmap='inferno',values_format='g')
plt.title("Confusion matrix, test data set")
plt.show()
plt.savefig('RFC_confusion_matrix_test_data.png')
plt.close()
# train_prediction is the model in question, here done with the testing data set

# calculate the predicted survival, with the TEST features (divided above)
predicted_survival = prediction_model.predict(test_features)
#function to print results with test set and prediction variable
print("Outcomes with RandomForestClassifier model with test set")
print(getresults(test_labels,predicted_survival)) #need to have the labels here

"""After testing the model with the testing data set, it can be seen that there are a few errors present within the labelling of the outcome (alive or dead). It should be noted that this is a real data set, where 100% accuracy isn't always a given.

Show which covariate(s) contributes the most to the prediction (from one method is sufficient)
"""

#feature importance, done with TEST data set here
print("Random Forest feature importance, with test set")
for f,fi in zip (test_features.columns, prediction_model.feature_importances_):
  print (f, fi.round(2))

# Compare feature importance in the models above
# use model.feature_importances_ to determine the importance of each feature
# also create a plot with the variance of the feature importance in each of the estimators

# Model 1 --> prediction_model
# done with the train data set, larger, more interesting with the variance
fistd = np.std([tree.feature_importances_ for tree in prediction_model.estimators_],
             axis=0)

print("Random Forest feature importance")
for f, fi, s in zip (train_features.columns, prediction_model.feature_importances_, fistd):
  print (f, fi.round(2), "+/-", s.round(2))

indices = np.argsort(prediction_model.feature_importances_)
plt.figure(figsize= (10,8))
plt.title("Feature importance")
plt.barh(np.arange(prediction_model.feature_importances_.shape[0]), 
        prediction_model.feature_importances_[indices],
       xerr=fistd[indices], align="center")
plt.yticks(range(prediction_model.feature_importances_.shape[0]), 
          labels=train_features.columns[indices])
plt.xlim(0, 1)
plt.xlabel('Importance')
plt.show()  
plt.savefig('RFC_feature_importance.png', bbox_inches='tight')
plt.close()

"""The initial machine learning was done (with these features: "MEDICAL_UNIT","SEX","AGE","PATIENT_TYPE","INTUBED","PNEUMONIA","DIABETES","CARDIOVASCULAR", "TOBACCO","OBESITY", "RENAL_CHRONIC", which resulted in an accuracy of 0.70. Most likley by adding more parameters the accruacy of the model could be further increased. 



This was done, and in this version the other parameters can be seen. By increasing the parameters the model becomes more and more accurate.
This can be seen in this version of the code, here the accuarcy has risen to 0.82 with the testing data set. This is because some parameters that were initially excluded have a high feature importance 


The main variable that influence the outcome, death, are medical unit, intubated, and age. Followed by pregnancy, Hypertension and ICU. 
The accuracy between the testing and train is very similar (0.83 vs 0.84), which is good. This also indicated that most likley there isn't any overfitting.

Grid-search CV, to optmise the hyperparameters of the model
"""

from sklearn.model_selection import GridSearchCV

# determine the classifier and basic parameters of the classifier
grid_cv =  RandomForestClassifier(random_state=2021)

# decide the hyperparameters to be tested
min_samples_split = [2,3,4]                                      
max_depth=[3,4,5,6,8, None]
criterion= ['gini','entropy']
parameters_rf=dict(min_samples_split=min_samples_split,criterion=criterion,max_depth=max_depth)

#training random forest model with combinations of all hyperparameters above using GridSearchCV
# GridSearchCV will find the hyperparameters that will give you the best predictions in cross validation according to the scoring method chosen

gridrf=GridSearchCV(grid_cv,parameters_rf,cv=10, scoring = 'accuracy')
gridrf.fit(train_features,train_labels)
#gridrf.fit(train_df[ml_features],train_df['diagnosis'])

def examinebestmodel(model_name):
    print(model_name.best_score_)
    print(model_name.best_params_)
    print(model_name.best_estimator_)

print("Search CV model parameters with random forest classifier")
examinebestmodel(gridrf)

# various results for the model on TRAIN set
train_prediction_cv_train=gridrf.best_estimator_.predict(train_features)
print("Outcomes with model, with parameters from grid search CV, with train set")
print(getresults(train_labels,train_prediction_cv_train))

#confusion matrix for the optimised model with grid search CV with TRAIN data set
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(gridrf.best_estimator_,train_features,train_labels,cmap='inferno',values_format='g')
plt.title("Confusion matrix S.CV, train data set")
plt.show()
plt.savefig('RFC_searchCV_confusion_matrix_train_data.png')
plt.close()

# various results for the model on TEST set
test_prediction_cv=gridrf.best_estimator_.predict(test_features)
print("Outcomes with model, with parameters from grid search CV, with test set")
print(getresults(test_labels,test_prediction_cv))

#confusion matrix for the optimised model with grid search CV with TEST data set
from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(gridrf.best_estimator_,test_features,test_labels,cmap='inferno',values_format='g')
plt.title("Confusion matrix, test data set")
plt.show()
plt.savefig('RFC_searchCV_confusion_matrix_test_data.png')
plt.close()

from sklearn.metrics import classification_report
report_CV = classification_report(test_labels, test_prediction_cv, output_dict = True)
print("RandomForestClassifier_Grid_search_CV_report, with test data")
print(classification_report(test_labels, test_prediction_cv))

# You can also save this report as a .csv file
report_dataframe_CV = pd.DataFrame.from_dict(report_CV)
report_dataframe_CV.to_csv('RandomForestClassifier_searchCV_report.csv')
#report_dataframe_CV.to_csv(output_path + 'class-prediction-CV_report.csv') for euler

fistd = np.std([tree.feature_importances_ for tree in gridrf.best_estimator_],
             axis=0)

print("Random Forest feature importance")
for f, fi, s in zip (test_features.columns, gridrf.best_estimator_.feature_importances_, fistd):
  print (f, fi.round(2), "+/-", s.round(2))

indices = np.argsort(gridrf.best_estimator_.feature_importances_)
plt.figure(figsize= (10,8))
plt.title("Feature importance")
plt.barh(np.arange(gridrf.best_estimator_.feature_importances_.shape[0]), 
        gridrf.best_estimator_.feature_importances_[indices],
       xerr=fistd[indices], align="center")
plt.yticks(range(gridrf.best_estimator_.feature_importances_.shape[0]), 
          labels=test_features.columns[indices])
plt.xlim(0, 1)
plt.xlabel('Importance')
plt.show()  
plt.savefig('RFC_searchCV_feature_importance.png', bbox_inches='tight')
plt.close()

"""By optimising the parameters there is a slight change in accuracy, from 0.83 to 0.85. Which is slighlty better, this idicates that the initil hyperparameters were already pretty good. The feature importance of the first three features remains similar, however in the cv search model the importance of an ICU, Pneumonia, Obesity and sex increases and pregnancy decreases.

One ways of increasing the accuarcy could be to have more variable such as genetics.

K-NN
"""

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier()
neighbors=[3,5,9,13]
metric=['manhattan','euclidean', 'chebyshev']
algorithm=['ball_tree', 'brute','auto', 'kd_tree']
parameters_knn=dict(n_neighbors=neighbors,metric=metric,algorithm=algorithm)

#training KNN model, finding best params
gridknn=GridSearchCV(knn,parameters_knn,cv=10,verbose=1, scoring = 'accuracy')
gridknn.fit(train_features,train_labels)

print("Search CV parameters with KNN model")
examinebestmodel(gridknn)

# confusion matrix with the TRAIN features 
ConfusionMatrixDisplay.from_estimator(gridknn.best_estimator_,train_features,train_labels,cmap='inferno',values_format='g')
plt.title("Confusion matrix, train data set, KNN")
plt.show()
plt.savefig('KNN_searchCV_confusion_matrix_train_data.png')
plt.close()

# calculate the predicted survival rate, with the TRAIN features 
predicted_survival_knn_train = gridknn.predict(train_features)
#function to print results with TRAIN set and prediction variable
print("Outcomes with KNN Grid search CV model, on train set")
print(getresults(train_labels,predicted_survival_knn_train)) #need to have the labels here

#predicting on test set, after finding the optimal parameters from the CV optimisation 
test_prediction_knn=gridknn.best_estimator_.predict(test_features)
print("Outcomes with KNN Grid search CV model, on test set")
print(getresults(test_labels,test_prediction_knn))

#confusion matrix for KNN on TEST set
ConfusionMatrixDisplay.from_estimator(gridknn.best_estimator_,test_features,test_labels,cmap='inferno',values_format='g')
plt.title("Confusion matrix, test data set, KNN")
plt.savefig('KNN_searchCV_confusion_matrix_test_data.png')
plt.close()
plt.show()

report_CV = classification_report(test_labels, test_prediction_knn, output_dict = True)
print("Outcomes with KNN Grid search CV model, on test set")
print(classification_report(test_labels, test_prediction_knn))

# You can also save this report as a .csv file
report_dataframe_CV = pd.DataFrame.from_dict(report_CV)
report_dataframe_CV.to_csv('KNN_searchCV_report.csv')

"""With the KNN model the accuracy is slightly worse than with the random forest classifier (0.84 vs 0.85 with the same test data set).
Here the hyperparameters are already optimised as the model was created with seach CV. As mentioned above, this is real world data were it isn't always so eays to predict with higher accuracy scores. 
It would be interesting to add more predictors for the death outcome, such as genetic factors (might have stronger correlations).
"""