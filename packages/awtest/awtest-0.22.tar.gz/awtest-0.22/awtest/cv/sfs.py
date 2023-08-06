import pandas as pd
import numpy as np
from eli5.sklearn import PermutationImportance
import eli5
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier as RFC
import datetime
from .utilities import checkpoint, isiter

class sfs:

    def __init__(self):
        self.name = 'hello'

    def print_title(self, string):
        string = str(string)
        lines = '#' * (10 + len(string))
        print(lines)
        print('#### {} ####'.format(string))
        print(lines)

    def kfold_model_perm(self, X, y, params, folds = 5, model = 'logit', use_true_values = False, true_values = 'None'):

        kfold = KFold(folds, True)
        best_model_output = pd.DataFrame()
        fold_num = 0
        perm_df = pd.DataFrame()
        if str(type(y)) == "<class 'pandas.core.frame.DataFrame'>":
            y = pd.Series([x[0] for x in y.values])
        elif type(y) == list:
            y = pd.Series(y)
        for trn, test in kfold.split(X):
            print('Working on fold', fold_num)
            X_trn = X.iloc[trn, :]
            X_trn.index = range(len(X_trn))
            X_test = X.iloc[test, :]  
            X_test.index = range(len(X_test))
            y_trn = pd.Series(y.iloc[trn].values)
            y_trn.index = range(len(y_trn))
            y_test = pd.Series(y.iloc[test].values)
            y_test.index = range(len(y_test))
            # true_values_temp.index = range(len(true_values_temp))
            #### Best model predicting class #### 
            if type(model) == str:
                if model.lower() == 'logit':
                    model = LogisticRegression()
                elif model.lower() == 'rfc':
                    model = RFC(**params)
            try:
                model.fit(X_trn, y_trn)
            except Exception as e:
                raise ValueError('There was a problem with your input data:\n{}'.format(str(e)))
            preds = model.predict(X_test)
            accuracy = sum([preds[i] == y_test.iloc[i] for i in range(len(y_test))]) / len(y_test)
            df_dict = {'pred': preds, 'actual': y_test,
                          'test_ind': test,
                         'fold_num': pd.Series([fold_num for i in range(len(y_test))]), 'accuracy': pd.Series([accuracy for i in range(len(y_test))])}
            perm = PermutationImportance(model).fit(X_test, y_test)
            eli5.show_weights(perm, feature_names = X_test.columns.tolist())        
            if use_true_values:
                true_values_temp = true_values.copy().iloc[test]
                true_values_temp.index = range(len(true_values_temp))            
                df_dict['true_value'] = true_values_temp
            best_model_output_temp = pd.DataFrame(df_dict)        
            # best_model_output_temp = run_model_best(X_trn, X_test, y_trn, y_test, trn, test, true_values, parameters_qual_rfc_rnd, model = 'RFC')
            best_model_output = pd.concat([best_model_output, best_model_output_temp])
            fold_num += 1
            
            perm_df_temp = pd.DataFrame({'importance':perm.feature_importances_, 'feature': X_test.columns, 'fold': [fold_num for i in range(len(X_test.columns))]})
            perm_df_temp = perm_df_temp.sort_values('importance', ascending = False)
            
            perm_df = pd.concat([perm_df, perm_df_temp])

        return best_model_output, perm_df

    def backwards_elimination(self, X, y, params, param_grid = 'None', model = 'logit', verbose = 0):
        accuracy_df = pd.DataFrame()
        cols = list(X.columns)
        cols_l = []
        removed_features = list()
        begin_all = datetime.datetime.today()
        for i in range(len(X.columns)):
            print('\n#### Working on step {:,} ####'.format(i))
            cols_l.append(cols.copy())
            # Getting permutation importances
            begin = datetime.datetime.today()
            print(begin)
            df_perm, perm_df = self.kfold_model_perm(X[cols], y, params = params, model = model)
            current = datetime.datetime.today()
            checkpoint(current, begin)
            print(current)
            # Ranking features by importances and determining which to remove
            print('Ranking features by importances and determining which to remove...')
            perm_df_group_temp = perm_df.groupby('feature').mean()['importance'].reset_index().rename(columns = {'importance': 'mean importance'})
            feature_to_remove = perm_df_group_temp.sort_values('mean importance').iloc[0, 0]
            print('Removing {}'.format(feature_to_remove))
            cols.remove(feature_to_remove)
            removed_features.append(feature_to_remove)
            # Determining accuracy for the set
            print('Determining accuracy for the set...')
            iter_accuracy = df_perm.groupby('fold_num').first()['accuracy'].reset_index().T
            iter_accuracy.columns = ['fold {} accuracy'.format(iteration) for iteration in range(len(iter_accuracy.columns))]
            overall_accuracy = df_perm.groupby('fold_num').first()['accuracy'].mean()
            print('Overall Accuracy: {}%'.format(round(overall_accuracy * 100, 2)))
            iter_accuracy.insert(0, 'overall accuracy', overall_accuracy)
            iter_accuracy.insert(0, 'step', i)
            accuracy_df = pd.concat([accuracy_df, iter_accuracy])
            print('Finished iteration. Total time elapsed:')
            current = datetime.datetime.today()
            checkpoint(current, begin_all)
        print('\nPrepping final output...')
        accuracy_df_original = accuracy_df.copy()
        accuracy_df = accuracy_df_original.copy()
        accuracy_df = accuracy_df.reset_index()
        accuracy_df = accuracy_df[accuracy_df['index'] != 'fold_num']
        accuracy_df.insert(2, 'variables used', cols_l)
        accuracy_df.insert(3, 'feature to remove', removed_features)
        accuracy_df = accuracy_df.drop('index', axis = 1)
        accuracy_df.index = list(range(len(accuracy_df)))
        print('\n\nDone!!!\n')
        return accuracy_df