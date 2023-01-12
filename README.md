# Big_data_analysis_endterm
Euler notes:
The outcome used was death of the patient, when a date of death was present the patient was assumed to have died. No number (9999-999-999) was assumed to still be alive.
When analysing the data with euler, it can be noted that the accuracy of the models diminish, which is intresting as I previously thought they would increase (more data, better prediction). For example the Random Forest classifier model, with Search CV for parameter optimization, had an accuarcy of 0.72 (test data) with the bigger data set compared to 0.85 (also with search CV, test data) with the smaller data set. This could be because the data set used in google collab (100'000 rows), was somehow "better data", where the models were able to have better accuracy. 
In euler more patient data is available, and most likley the model wasn't able to create/find good predictors for the model. 
The KNN model has an accuracy of 0.69 with the euler data set compared to 0.84 on the smaller data set. 
When looking at all of the confusion matrixes, there is a tendency that the model predicts the patient as dead even if they are alive and has more difficult predicting if the patient is alive. 
As mentioned in the google collab script, it would be interesting to add more parameters, such as genetic ones, or even BMI,... to see if the model can be improved. Alternativley other machine learning methods could be used.
