# Big_data_analysis_endterm
There are two versions of the file, the difference is in the machine learning data processing. Please refer to the the normal version (HS22_BigData_Final_Project_JM.ipynb) for the correction. In one file medical unit is kept as is, in the hot encoded version it is divided into the various numbers (0,1,3,4 in the google collab version, where each number has a column with 1 or 0). Age was not normalised, as it is the only continous variable in the data set.
One the google collab file, with the smaller datat set, in the RFC model and KNN there isn't a significant difference between the two data filtering methods (accuracy on test data set, approx. RFC=0.85 and KNN=0.84 in both models).
The comments in the two version are identical besides some extra comments added in the hot encoded version to explain a few things.

The hot encoding version wasn't necessary, as CARTs can handle multiple variables, but I uploaded them for fun :)  
# Euler notes:
The outcome used was death of the patient, when a date of death was present the patient was assumed to have died. No number (9999-999-999) was assumed to still be alive.
When analysing the data with euler, it can be noted that the accuracy of the models diminish, which is intresting as I previously thought they would increase (more data, better prediction). 
For example the Random Forest classifier model, with Search CV for parameter optimization, had an accuarcy of 0.72 (test data) with the bigger data set compared to 0.85 (also with search CV, test data, not hot encoded) with the smaller data set. This could be because the data set used in google collab (100'000 rows), was somehow "better data", where the models were able to have better accuracy. 
In euler more patient data is available, and most likley the model wasn't able to create/find good predictors for the model. 

The KNN model has an accuracy of 0.69 with the euler data set compared to 0.84 on the smaller data set. 

The feature importance in the larger data set compared to the smaller one also changes, where in the search cv model, intubated, age, pneumonia and USMR gain importance and medical unit decreases. 
When looking at all of the confusion matrixes, there is a tendency that the model predicts the patient as dead even if they are alive and has more difficult predicting if the patient is alive. 

As mentioned in the google collab script, it would be interesting to add more parameters, such as genetic ones, or even BMI,... to see if the model can be improved. Alternativley other machine learning methods could be used or other ways of filtering the data. 
