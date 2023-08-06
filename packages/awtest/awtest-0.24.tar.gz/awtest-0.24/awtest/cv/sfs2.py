import pandas as pd
import numpy as np
from eli5.sklearn import PermutationImportance
import eli5
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier as RFC
import datetime
from .utilities import checkpoint, isiter

class sfs2:

    def __init__(self):

    def kfold_model_perm(self, X, y, params, cols, indices, folds = 5, model = 'logit'):

        kfold = KFold(folds, True)
        best_model_output = pd.DataFrame()
        fold_num = 0
        perm_df = pd.DataFrame()
        for trn, test in kfold.split(X):
            print('Working on fold', fold_num)
            X_trn = X[trn, :]
            X_test = X[test, :]
            print('y.shape:', y.shape)
            y_trn = y[trn]
            y_test = y[test]
            if type(model) == str:
                if model.lower() == 'logit':
                    model = LogisticRegression()
                elif model.lower() == 'rfc':
                    model = RFC(**params)
            model.fit(X_trn, y_trn)
            preds = model.predict(X_test)
            accuracy = sum([preds[i] == y_test[i] for i in range(y_test.shape[0])]) / y_test.shape[0]
            df_dict = {
                       'pred': preds,
                       'actual': y_test,
                       'test_ind': test,
                       'fold_num': pd.Series([fold_num for i in range(y_test.shape[0])]),
                       'accuracy': pd.Series([accuracy for i in range(y_test.shape[0])])
                      }
            perm = PermutationImportance(model).fit(X_test, y_test)
            best_model_output_temp = pd.DataFrame(df_dict)        
            best_model_output = pd.concat([best_model_output, best_model_output_temp])
            
            perm_df_temp = pd.DataFrame({
                                         'importance':perm.feature_importances_,
                                         'feature': cols,
                                         'index': indices,
                                         'fold': [fold_num for i in range(len(cols))]
                                        })
            perm_df_temp = perm_df_temp.sort_values('importance', ascending = False)
            
            perm_df = pd.concat([perm_df, perm_df_temp])

            fold_num += 1

        return best_model_output, perm_df

    def backwards_elimination(self, X, y, params, param_grid = 'None', model = 'logit', cols = [], verbose = 0):

        # Format X
        isiter(X, 'X')
        if len(X.shape) != 2:
            raise TypeError('X is not a 2D array')
        if cols == []:
            try:
                cols = list(X.columns)
            except:
                cols = ['feature_{}'.format(i) for i in range(X.shape[1])]
        else:
            isiter(cols, 'cols')
        X = np.array(X)
        # Format y
        isiter(y, 'y')
        if len(y.shape) > 2:
            raise TypeError('y has too many dimensions')
        elif len(y.shape) == 2:
            y = np.array([x[0] for x in y])
        else:
            y = np.array(y)
        accuracy_df = pd.DataFrame()
        cols_l = []
        indices = list(range(X.shape[1]))
        removed_features = []
        removed_indices = []
        begin_all = datetime.datetime.today()
        for i in range(X.shape[1]):
            print('\n#### Working on step {:,} ####'.format(i))
            cols_l.append(cols.copy())
            # Getting permutation importances
            begin = datetime.datetime.today()
            print(begin)
            df_perm, perm_df = self.kfold_model_perm(X[:, indices], y, cols = cols, indices = indices, params = params, model = model)
            df_perm.insert(0, 'step', i)
            df_perm.insert(1, 'features used', [cols for i in range(df_perm.shape[0])])
            current = datetime.datetime.today()
            checkpoint(current, begin)
            print(current)
            # Ranking features by importances and determining which to remove
            print('Ranking features by importances and determining which to remove...')
            worst_feature = perm_df.groupby(['feature', 'index']).mean()['importance'].reset_index().rename(columns = {'importance': 'mean importance'}).sort_values('mean importance').iloc[0]
            feature_to_remove = worst_feature['feature']
            index_to_remove = worst_feature['index']
            print('Removing {}'.format(feature_to_remove))
            cols.remove(feature_to_remove)
            indices.remove(index_to_remove)
            removed_features.append(feature_to_remove)
            df_perm.insert(2, 'feature to remove', feature_to_remove)
            # Determining accuracy for the set
            print('Determining accuracy for the set...')
            iter_accuracy = df_perm.groupby('fold_num').first()['accuracy'].reset_index().T
            iter_accuracy.columns = ['fold {} accuracy'.format(iteration) for iteration in range(iter_accuracy.shape[1])]
            overall_accuracy = df_perm.groupby('fold_num').first()['accuracy'].mean()
            print('Overall Accuracy: {}%'.format(round(overall_accuracy * 100, 2)))
            iter_accuracy.insert(0, 'overall accuracy', overall_accuracy)
            iter_accuracy.insert(0, 'step', i)
            accuracy_df = pd.concat([accuracy_df, iter_accuracy])
            print('Finished iteration. Total time elapsed:')
            current = datetime.datetime.today()
            checkpoint(current, begin_all)

        print('\nPrepping final output...')

        self.be_results = df_perm

        accuracy_df_original = accuracy_df.copy()
        accuracy_df = accuracy_df_original.copy()
        accuracy_df = accuracy_df.reset_index()
        accuracy_df = accuracy_df[accuracy_df['index'] != 'fold_num']
        accuracy_df.insert(2, 'features used', cols_l)
        accuracy_df.insert(3, 'feature to remove', removed_features)
        accuracy_df = accuracy_df.drop('index', axis = 1)
        accuracy_df.index = list(range(len(accuracy_df)))

        self.be_summary = accuracy_df

    def get_be_summary(self):
        try:
            return self.be_summary
        except:
            raise Exception('`backwards_elimination` has not yet been run')

    def get_be_results(self):
        try:
            return self.be_results
        except:
            raise Exception('`backwards_elimination` has not yet been run')