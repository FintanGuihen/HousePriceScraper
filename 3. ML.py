
#Machine learning

#******************************************************************************
#***************************run 1. Munging.py first ***************************
#******************************************************************************

#REMOVE BLANK ASKING PRICE
DS_CleanDependantVariable = deduplicatedDataset[(deduplicatedDataset.currentAskingPrice.notnull()) & (deduplicatedDataset.currentAskingPrice <= 800000)]

#reorder columns
DS_CleanDependantVariable = DS_CleanDependantVariable[[

 'beds',
 'bathrooms',
 'size',
 'ber lower',
 'CountyOrPostcode',
 'County',
 'PropertyType',
 'price bin',
  'currentAskingPrice']]

independent = DS_CleanDependantVariable.iloc[:, 0:7]
independent = DS_CleanDependantVariable.iloc[:, 0:7].values
dependent = DS_CleanDependantVariable.iloc[:, 8].values

from sklearn.preprocessing import LabelEncoder, OneHotEncoder
labelencoder_X  = LabelEncoder()



#ber
berVariables = independent[:,3]
berVariables = labelencoder_X.fit_transform(berVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
berVariables = onehotencoder.fit_transform(berVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
berVariables = berVariables[:,1:]

#countryOrPostcode
countryOrPostcodeVariables = independent[:,4]
countryOrPostcodeVariables = labelencoder_X.fit_transform(countryOrPostcodeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
countryOrPostcodeVariables = onehotencoder.fit_transform(countryOrPostcodeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
countryOrPostcodeVariables = countryOrPostcodeVariables[:,1:]

#county
countyVariables = independent[:,5]
countyVariables = labelencoder_X.fit_transform(countyVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
countyVariables = onehotencoder.fit_transform(countyVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
countyVariables = countyVariables[:,1:]

#PropertyType
PropertyTypeVariables = independent[:,6]
PropertyTypeVariables = labelencoder_X.fit_transform(PropertyTypeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
PropertyTypeVariables = onehotencoder.fit_transform(PropertyTypeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
PropertyTypeVariables = PropertyTypeVariables[:,1:]

#concatenate all encoded categorical variable arrays
catVariables = np.concatenate((berVariables,countryOrPostcodeVariables),axis = 1)
catVariables = np.concatenate((catVariables,countyVariables),axis = 1)
catVariables = np.concatenate((catVariables,PropertyTypeVariables),axis = 1)


AllVariables = np.append(catVariables, independent[:,[0]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[1]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[2]], axis = 1)



#taken care of by the library


from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(AllVariables, dependent, test_size = 0.2, random_state = 0)



from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X_train, y_train)


y_pred = regressor.predict(X_test)

from sklearn.metrics import mean_squared_error
from math import sqrt

rms = sqrt(mean_squared_error(y_test, y_pred))
# = RMSE 583,206. very high, not accurate at all.


#----------------------------just dublin------------------------------------------





DS_CleanDependantVariable
DS_CleanDependantVariable = deduplicatedDataset[deduplicatedDataset.currentAskingPrice.notnull()& (deduplicatedDataset.currentAskingPrice <= 800000)]
DS_CleanDependantVariable = DS_CleanDependantVariable[(DS_CleanDependantVariable['County'] == 'dublin') ]
#reorder columns
DS_CleanDependantVariable = DS_CleanDependantVariable[[

 'beds',
 'bathrooms',
 'size',
 'ber lower',
 'CountyOrPostcode',
 'PropertyType',
 'price bin',
  'currentAskingPrice']]



independent = DS_CleanDependantVariable.iloc[:, 0:6]
independent = DS_CleanDependantVariable.iloc[:, 0:6].values
dependent = DS_CleanDependantVariable.iloc[:, 7].values

                                          
                                          
                                          


#ber
berVariables = independent[:,3]
berVariables = labelencoder_X.fit_transform(berVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
berVariables = onehotencoder.fit_transform(berVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
berVariables = berVariables[:,1:]

#countryOrPostcode
countryOrPostcodeVariables = independent[:,4]
countryOrPostcodeVariables = labelencoder_X.fit_transform(countryOrPostcodeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
countryOrPostcodeVariables = onehotencoder.fit_transform(countryOrPostcodeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
countryOrPostcodeVariables = countryOrPostcodeVariables[:,1:]



#PropertyType
PropertyTypeVariables = independent[:,5]
PropertyTypeVariables = labelencoder_X.fit_transform(PropertyTypeVariables[:])
onehotencoder = OneHotEncoder(categorical_features=[0])
PropertyTypeVariables = onehotencoder.fit_transform(PropertyTypeVariables.reshape(-1,1)).toarray()
#Avoid dummy variable trap
PropertyTypeVariables = PropertyTypeVariables[:,1:]

#concatenate all encoded categorical variable arrays
catVariables = np.concatenate((berVariables,countryOrPostcodeVariables),axis = 1)
catVariables = np.concatenate((catVariables,PropertyTypeVariables),axis = 1)


AllVariables = np.append(catVariables, independent[:,[0]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[1]], axis = 1)
AllVariables = np.append(AllVariables, independent[:,[2]], axis = 1)

AllVariables = AllVariables.astype(float)

#taken care of by the library


from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(AllVariables, dependent, test_size = 0.2, random_state = 0)



from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X_train, y_train)


y_pred = regressor.predict(X_test)

from sklearn.metrics import mean_squared_error
from math import sqrt

rms = sqrt(mean_squared_error(y_test, y_pred))
#344697 . very bad.



# backward elimination to see which variables to remove

import statsmodels.formula.api as sm

AllVariables = np.append(arr = np.ones((2877,1)).astype(int), values = AllVariables, axis = 1)

#X_opt will only contain optimal variables for the model. initialized with the index of all vaiables
X_opt = AllVariables[:, range(0,63)]


regressor_OLS = sm.OLS(endog = dependent, exog = X_opt).fit()

regressor_OLS.summary()


