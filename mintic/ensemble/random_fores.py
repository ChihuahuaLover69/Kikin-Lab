import numpy as np
import random
import math
import pandas as pd

def boostrap_sample(x,y,seed=0):
    data = pd.concat([y, x], axis=1)

    random.seed(a=seed)
    newdf=[]
    
    for i in range(len(data)-1):
        newdf.append(data.iloc[random.randint(0,len(data)-1)])
    df=pd.DataFrame(newdf)
    x=df.iloc[:,1:]
    y=df.iloc[:,0]
    return x,y
    
#boostrap_sample(x,y,42)

def calculate_entropy(y):
    total_rows = len(y)
    target_values = y.unique()
    entropy = 0
    for value in target_values:
        # Calculate the proportion of instances with the current value
        value_count = len(y[y == value])
        proportion = value_count / total_rows
        entropy-=proportion*math.log2(proportion)
    return entropy

def calculate_information_gain(x,y,feature):
    # Calculate weighted average entropy for the feature
    unique_values = x[feature].unique()
    weighted_entropy = 0
    for value in unique_values:
        subset = x[x[feature] == value]
        subset_y = y[x[feature] == value]

        proportion = len(subset) / len(x)
        weighted_entropy += proportion * calculate_entropy(subset_y)

    # Calculate information gain
    information_gain = calculate_entropy(y) - weighted_entropy

    return information_gain

#https://www.geeksforgeeks.org/machine-learning/sklearn-iterative-dichotomiser-3-id3-algorithms/
#TQM geeksforgeeks
def build_id3_tree(x,y):
    features=x.columns
    if len(y.unique()) == 1:
        return y.iloc[0]
    if len(features) == 0:
        return y.mode().iloc[0]

    best_feature = max(features,key=lambda feature: calculate_information_gain(x, y, feature))
    tree = {best_feature: {}}

    features = [f for f in features if f != best_feature]
    for value in x[best_feature].unique():
        subset = x[x[best_feature] == value]
        subset_y = y[x[best_feature] == value]
        tree[best_feature][value] = id3(subset[features],subset_y)

    return tree


#build_id3_tree(x,y)

def build_random_forest(x,y,n_trees=10, random_state=0):
    random.seed(a=random_state)
    arboles=[]
    for i in range(n_trees):
        x1,y2=boostrap_sample(x,y)
        arboles.append(build_id3_tree(x1,y2))
    return arboles
#build_random_forest(x,y)

def predict_tree(tree, row):
    while isinstance(tree, dict):
        feature = next(iter(tree))
        value = row[feature]
        tree = tree[feature][value]

    return tree


def predict_ensemble(trees, X):
    predictions = []
    for tree in trees:
        tree_predictions = []

        for row in X.to_numpy():
            tree_predictions.append(predict_tree(tree, row))

        predictions.append(tree_predictions)

    predictions = np.array(predictions)

    final_predictions = []

    for i in range(X.shape[0]):
        classes, counts = np.unique(predictions[:, i], return_counts=True)
        max_count = counts.max()

        final_predictions.append(classes[counts == max_count][0])

    return np.array(final_predictions)


#predict_ensemble(build_random_forest(x,y),x.iloc[1:10])
