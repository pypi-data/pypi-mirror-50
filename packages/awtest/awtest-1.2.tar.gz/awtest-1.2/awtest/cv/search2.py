import pandas as pd
import numpy as np
from sklearn.metrics import silhouette_score, f1_score, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier as RFC
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from .utilities import unique_array, isiter

class grid_search_cluster2:

    def __init__(self):
        self.gs_complete = False

    def grid_search_cluster(self, model, model_name, params, X, return_model = False, metric = 'silhouette', verbose = 5):
        X_df = X.copy()
        from sklearn.preprocessing import StandardScaler
        X = StandardScaler().fit_transform(X)
        import itertools as it
        keys = sorted(params)
        combinations = list(it.product(*(params[key] for key in keys)))
        param_grid = []
        for combo in combinations:
            combo_dict = {}
            for i in range(len(combo)):
                combo_dict[keys[i]] = combo[i]
            param_grid.append(combo_dict)
        print('Number of parameter sets: {:,}'.format(len(param_grid)))
        labels_df = X_df.copy()
        s_scores = []
        models = []
        if model_name == 'KMeans':
            cluster_centers = []
        for i in range(len(param_grid)):
            param_set = param_grid[i]
            if i % verbose == 0:
                print('\nNow working on param set {:,}'.format(i))
                print(param_set)
            model_test = model(**param_set).fit(X)
            labels = model_test.labels_
            n_labels = len(unique_array(labels))
            labels_df['labels_{}'.format(i)] = labels
            # Calculate Silhouette Score
            if n_labels > 1 and n_labels < len(labels):
                s_score = silhouette_score(X, model_test.labels_)
            else:
                s_score = -1
            s_scores.append(s_score)
            models.append(model_test)
            if model_name == 'KMeans':
                cluster_centers.append(model_test.cluster_centers_)
        output_df = pd.DataFrame({'param set': param_grid, 'silhouette score': s_score})
        if model_name == 'KMeans':
            output_df['cluster centers'] = cluster_centers
        return labels_df, output_df, models

class grid_search2:

    def __init__(self):
        self.name = 'hello'

    def print_title(self, string):
        string = str(string)
        lines = '#' * (10 + len(string))
        print(lines)
        print('#### {} ####'.format(string))
        print(lines)

    def grid_search_kfold(self, X, y, model_name, param_grid, decision_prob = 0.5, scoring = 'accuracy', num_folds = 5, ids = 'None', return_all = True):
        import itertools as it
        multi_class = len(unique_array([x[0] for x in y.values]).tolist()) >= 3
        keys = sorted(param_grid)
        combinations = list(it.product(*(param_grid[key] for key in keys)))
        param_sets = []
        for combo in combinations:
            combo_dict = {}
            for i in range(len(combo)):
                combo_dict[keys[i]] = combo[i]
            param_sets.append(combo_dict)
        score_best = -2
        print_title(string = 'Working on {:,} parameter sets'.format(len(param_sets)), title = 'full')
        i = 0
        if return_all:
            output_all = pd.DataFrame()
        for param_set in param_sets:
            print()
            print_title('Working on parameter set {:,} ({})'.format(i, str(param_set)))
            classifier, output_df = self.kfold_model(X, y, model_name, param_set, num_folds = num_folds, ids = ids)
            if scoring == 'accuracy':
                score = accuracy_score(output_df['true_value'], output_df['prediction'])
            elif scoring == 'f1':
                if multi_class:
                    print('Using accuracy because "f1" was selected and this problem has multiple classes...')
                    score = accuracy_score(output_df['true_value'], output_df['prediction'])
                else:
                    score = f1_score(output_df['true_value'], output_df['prediction'])
            elif scoring == 'f1_micro':
                score = f1_score(output_df['true_value'], output_df['prediction'], average = 'micro')
            elif scoring == 'f1_macro':
                score = f1_score(output_df['true_value'], output_df['prediction'], average = 'macro')
            elif scoring == 'f1_weighted':
                score = f1_score(output_df['true_value'], output_df['prediction'], average = 'weighted')
            if score > score_best:
                max_score = score
                classifier_best = classifier
                output_best = output_df.copy()
            if return_all:
                output_df['params'] = str(param_set)
                output_all = pd.concat([output_all, output_df], axis = 0)
            i += 1
        print("The overall {} score is: {}%".format(scoring, round(score_best * 100, 2)))
        if not return_all:
            return classifier_best, output_best
        else:
            return classifier_best, output_best, output_all

    def kfold_model(self, X, y, model_name, params = 'None', param_grid = 'None', scoring = 'f1', num_folds = 5, ids = 'None'):
        kfold = KFold(num_folds, True)
        trns = []
        tests = []
        logit_q_df = pd.DataFrame()
        rfr_q_df = pd.DataFrame()
        fold_num = 0
        predictions_all = [] 
        predict_probas_all = []
        folds = []
        y_tests = []
        multi_class = len(unique_array([x[0] for x in y.values]).tolist()) >= 3
        if str(ids) != 'None':
            ids_output = []
        for trn, test in kfold.split(X):
            if type(X) == pd.core.frame.DataFrame:
                X_trn = X.iloc[trn, :]
                X_test = X.iloc[test, :]
            else:
                X_trn = X[trn, :]
                X_test = X[test, :]   
            if type(y) in (pd.core.series.Series, pd.core.frame.DataFrame):
                y_trn = y.iloc[trn]
                y_test = y.iloc[test]
                y_trn.index = range(len(y_trn))    
                y_test.index = range(len(y_test))    
            else:
                y_trn = y[trn]
                y_test = y[test]          
            y_tests.append([x[0] for x in y_test.values])
            if str(ids) != 'None':
                ids_output.append(pd.Series(ids).iloc[test])

            # model training
            if model_name.lower() == 'logit':
                if param_grid != 'None':
                    classifier = GridSearchCV(LogisticRegression(), param_grid, cv = 5, scoring = scoring, verbose = 1)
                else:
                    if params != 'None':
                        classifier = LogisticRegression(**params)
                    else:
                        classifier = LogisticRegression()
            elif model_name.lower() == 'rfc':
                if param_grid != 'None':
                    classifier = GridSearchCV(RFC(), param_grid, cv = 5, scoring = scoring, verbose = 1)
                else:
                    if params != 'None':
                        classifier = RFC(**params)
                    else:
                        classifier = RFC()
            if model_name.lower() == 'random':
                predict_probas = np.random.random_sample((len(X_test),))
                predictions = [1 if x > .5 else 0 for x in predict_probas]
                predictions_all.append(predictions)
                predict_probas_all.append(predict_probas)
                classifier = 'random_classifier'
            else:
                classifier.fit(X_trn, y_trn)
                # prediction
                predictions = classifier.predict(X_test)
                if not multi_class:
                    predict_probas = [x[1] for x in classifier.predict_proba(X_test)]
                else:
                    predict_probas = classifier.predict_proba(X_test)
                predictions_all.append(predictions)
                predict_probas_all.append(predict_probas)
            # model evaluation
            score = accuracy_score(y_test, predictions)
            print("\nThe accuracy score for fold {} is: {}%".format(fold_num, round(score * 100, 2)))
            if not multi_class:
                f_score = f1_score(y_test, predictions)
                print("The F1 score for fold {} is: {}%".format(fold_num, round(f_score * 100, 2)))
            folds.append([fold_num] * len(y_test))
            fold_num += 1

        y_tests = pd.Series(flatten(y_tests))
        predictions_all = pd.Series(flatten(predictions_all))
        predict_probas_all = pd.Series(flatten(predict_probas_all))
        score = accuracy_score(y_tests, predictions_all)
        folds = pd.Series(flatten(folds))
        if str(ids) != 'None':
            ids_output = pd.Series(flatten(ids_output))
        print("\nThe overall accuracy score is: {}%".format(round(score * 100, 2)))
        if not multi_class:
            f_score = f1_score(y_tests, predictions_all)
            print("The overall F1 score is: {}%".format(round(f_score * 100, 2)))

        if str(ids) != 'None':
            output_df = pd.DataFrame({'id': ids_output, 'prediction': predictions_all, 'predict_proba': predict_probas_all, 'true_value': y_tests, 'fold': folds})
        else:
            output_df = pd.DataFrame({'prediction': predictions_all, 'predict_proba': predict_probas_all, 'true_value': y_tests, 'fold': folds})
            
        return classifier, output_df