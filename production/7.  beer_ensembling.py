
# coding: utf-8

# # Ensembling

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, roc_auc_score, roc_curve, auc
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier 
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

import pickle
with open('beer_df_formodel.pickle','rb') as read_file:
    beer_df = pickle.load(read_file)
beer_df.head(1)


X = beer_df.iloc[:,4:-13].drop(columns = 'brewmethod')
y = beer_df.style_num

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 4444)

#Gradient Boost

gbdt_model = GradientBoostingClassifier(n_estimators = 500, random_state = 4444) #Max Depth Default = 3

gbdt_model.fit(X_train, y_train)

print('Gradient Boost Model Train Score:', gbdt_model.score(X_train, y_train))
print('Gradient Boost Model Test Score:', gbdt_model.score(X_test, y_test ))


#Random Forest

rf_model = RandomForestClassifier(n_estimators = 500, max_depth = 10, random_state=4444)

rf_model.fit(X_train, y_train)

print('Random Forest Model Test Score:', rf_model.score(X_test, y_test))


#Ensemble Model - Voting Classifer

ensemble_classifier = VotingClassifier(estimators = [('Gradient Boost Decision Tree', gbdt_model), ('Random Forest Model', rf_model)],voting = 'soft') 

ensemble_classifier = ensemble_classifier.fit(X_train, y_train)

ensemble_pred = ensemble_classifier.predict(X_test)

print('Ensemble Model Accuracy Score:',accuracy_score(y_test, ensemble_pred))


with open ('ensemble_model.pickle', 'wb') as to_write:
    pickle.dump(ensemble_classifier, to_write)

# make a prediction
list(X.columns)

# Replace with own inputs in order from above
input_list = ['size',
              'og',
              'fg',
              'abv',
              'ibu',
              'color', 
              'boilsize',
              'boiltime',
              'boilgravity',
              'efficiency',
              'allgrain',
              'biab',
              'partialmash',
              'extract']

inputs = [10,2,1,6,100,20,30,20,3,65,1,0,0,0] 

try:
    if len (inputs) == 14:
        True
except:
    print("Need 14 inputs")
    
prediction = ensemble_classifier.predict(inputs).reshape(-1, 1)


""" Did not use the Parent Model -->

#Ensemble Model - Parent Model

#IPA, Stout, Ale, APA, Wheat, Pilsner performed best using Gradient Boosted Decision Trees
#Style numbers 1, 3, 7, 8, 9, 10
GBDT_styles = [1,3,7,8,9,10]

#Lager, Porter, Saison, Kolsch performed better using Random Forest than GBDT
#Style numbers 2, 4, 5, 6

beer_df['GBDT_styles'] = 1 * beer_df.style_num.isin(GBDT_styles)

#Logistic Regression Model


'''

Using Logistic Regression to determine if I want to use Gradient Boosted Decision Trees
or Random Forest.

Add classifiers to training and testing sets.

Split on classifiers to determine which model to perform.

Train each model on its own training set and test on its own testing set.

'''

log_model = LogisticRegression(C = 10, random_state = 4444)

y_parentmodel = beer_df.GBDT_styles

X_parentmodel = X

X_train_parent, X_test_parent, y_train_parent, y_test_parent = train_test_split(X_parentmodel, y_parentmodel, test_size = 0.3, random_state = 4444)

log_model.fit(X_train_parent, y_train_parent)

log_model.score(X_test_parent, y_test_parent)

classifier_preds_train = log_model.predict(X_train_parent)
classifier_preds_test = log_model.predict(X_test_parent)

beer_training_data = X_train.join(y_train)
beer_testing_data = X_test.join(y_test)

beer_training_data['classifier_preds_train'] = classifier_preds_train
beer_testing_data['classifier_preds_test'] = classifier_preds_test

#Gradient Boost

gbdt_train = beer_training_data[beer_training_data['classifier_preds_train'] == 1]
gbdt_test = beer_testing_data[beer_testing_data['classifier_preds_test'] == 1]


gbdt_y_train = gbdt_train['style_num']
gbdt_y_test = gbdt_test['style_num']

gbdt_X_train = gbdt_train.iloc[:,:14]
gbdt_X_test = gbdt_test.iloc[:,:14]

gbdt_model.fit(gbdt_X_train, gbdt_y_train)

print("Gradient Boost Train Accuracy:", gbdt_model.score(gbdt_X_train, gbdt_y_train))

print("Gradient Boost Test Accuracy:",gbdt_model.score(gbdt_X_test, gbdt_y_test)


#Random Forest

rf_model_parent = RandomForestClassifier(max_depth = 10, random_state=4444)

rf_train = beer_training_data[beer_training_data['classifier_preds_train'] == 0]
rf_test = beer_testing_data[beer_testing_data['classifier_preds_test'] == 0]

rf_y_train = rf_train['style_num']
rf_y_test = rf_test['style_num']


rf_X_train = rf_train.iloc[:,:14]
rf_X_test = rf_test.iloc[:,:14]


rf_model_parent.fit(rf_X_train, rf_y_train)

print("Random Forest Train Accuracy:", rf_model.score(rf_X_train, rf_y_train))

print("Random Forest Test Accuracy:", rf_model.score(rf_X_test, rf_y_test))

"""
