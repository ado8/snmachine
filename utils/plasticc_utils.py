"""
Utility script for calculating the log loss
"""

from sklearn.metrics import confusion_matrix
import sys
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(font_scale=1.3, style="ticks")


def plot_confusion_matrix(y_true, y_pred, title, target_names, normalize=False):
    cm = confusion_matrix(y_true, y_pred, labels=target_names)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)

    annot = np.around(cm, 2)
    
    dict_label_to_real = {15:'TDE', 42:'SNII', 52:'SNIax', 62:'SNIbc', 64:'KN', 67:'SNIa-91bg',
                          88:'AGN', 90:'SNIa', 95:'SLSN-I'} # to erase later; This is just for de-bug
    target_names = np.vectorize(dict_label_to_real.get)(target_names)

    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(cm, xticklabels=target_names,
                yticklabels=target_names, cmap='Blues',
                annot=annot, lw=0.5, vmin=0, vmax=1)

    ax.set_xlabel('Predicted Label')
    ax.set_ylabel('True Label')
    ax.set_aspect('equal')
    plt.title(title)

    return cm, fig


def plasticc_log_loss(y_true, probs):
    """
    Implementation of weighted log loss used for the Kaggle challenge
    
    Parameters:
    -------
    probs : np.array of shape (# samples, # features)
    """
    predictions = probs.copy()
    labels = np.unique(y_true) # assumes the probabilities are also ordered in the same way
    weights_dict = {6:1/18, 15:1/9, 16:1/18, 42:1/18, 52:1/18, 53:1/18, 62:1/18, 64:1/9, 
                    65:1/18, 67:1/18, 88:1/18, 90:1/18, 92:1/18, 95:1/18, 99:1/19}

    # sanitize predictions
    epsilon = sys.float_info.epsilon  # this is machine dependent but essentially prevents log(0)
    predictions = np.clip(predictions, epsilon, 1.0 - epsilon)
    predictions = predictions / np.sum(predictions, axis=1)[:, np.newaxis]

    predictions = np.log(predictions)
    # multiplying the arrays is equivalent to a truth mask as y_true only contains zeros and ones
    class_logloss = []
    weights = []
    for i in range(predictions.shape[1]): # for each class
        # average column wise log loss with truth mask applied
        current_label = labels[i]
        result = np.average(predictions[y_true==current_label, i]) 
        class_logloss.append(result)
        weights.append(weights_dict[current_label])
    return -1 * np.average(class_logloss, weights=weights)