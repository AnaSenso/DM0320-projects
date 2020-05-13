import pandas as pd
from sklearn.preprocessing import StandardScaler, Normalizer
from process_fun import *

from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge
from sklearn.svm import LinearSVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

stpipelines = [('ScaledLR', Pipeline([('Scaler', StandardScaler()),('LR',LinearRegression())])),
                ('ScaledLASSO', Pipeline([('Scaler', StandardScaler()),('LASSO', Lasso())])),
                ('ScaledRF', Pipeline([('Scaler', StandardScaler()),('RF', RandomForestRegressor())])),
                ('ScaledKNN', Pipeline([('Scaler', StandardScaler()),('KNN', KNeighborsRegressor())])),
                ('ScaledCART', Pipeline([('Scaler', StandardScaler()),('CART', DecisionTreeRegressor())])),
                ('ScaledGBM', Pipeline([('Scaler', StandardScaler()),('GBM', GradientBoostingRegressor())]))]

pipelines = [('LinearRegression', Pipeline([('LR',LinearRegression())])),
                ('Lasso', Pipeline([('LASSO', Lasso())])),
                ('RandomForestRegressor', Pipeline([('RF', RandomForestRegressor())])),
                ('KNeighborsRegressor', Pipeline([('KNN', KNeighborsRegressor())])),
                ('DecisionTreeRegressor', Pipeline([('CART', DecisionTreeRegressor())])),
                ('GradientBoostingRegressor', Pipeline([('GBM', GradientBoostingRegressor())]))]

lpipelines = [('S-LinearSVR', Pipeline([('Scaler', StandardScaler()),('LSVR', LinearSVR())])),
                ('S-Ridge', Pipeline([('Scaler', StandardScaler()),('Ridge', Ridge())]))]

def models(pip, X_train, y_train):
    r_res = []
    m_res = []
    names = []
    ms = []
    for name, model in pip:
        kfold = KFold(n_splits=10, random_state=21, shuffle = True)
        cv_rs = cross_val_score(model, X_train, y_train, cv=kfold, scoring='r2')
        cv_mse = cross_val_score(model, X_train, y_train, cv=kfold, scoring='neg_mean_squared_error')
        r_res.append(cv_rs)
        m_res.append(cv_mse)
        names.append(name)
        msg = ("%s, %f, %f" % (name, cv_rs.mean(), cv_mse.mean()))
        ms.append(msg)
    dft = pd.DataFrame(columns= ['model', 'r2', 'mse'],data=[row.split(',') for row in ms[0:]])
    return dft

def grid(model, params, X_train, y_train):
    clf = GridSearchCV(estimator=model,
             param_grid=params,cv=5, scoring='r2', verbose=3, n_jobs=-1)
    clf.fit(X_train, y_train)
    print('Best params: ', clf.best_params_)
    print('Best estimator: ', clf.best_estimator_)
    return f"Best score: {clf.best_score_}"

def train(modname, X_train, y_train, **params):
    mod = modname()
    model = mod.set_params(params).fit(X_train, y_train)
    score = model.score(X_train, y_train)
    return f"Model: {modname} \n Params: {params} \n Score: {score}"

def final_test(mod, df_test):
    y_pred = mod.predict(df_test)
    columns=['id','price']
    df = pd.DataFrame(y_pred)
    df = df.reset_index(level=0)
    df.columns = columns
    return (df)