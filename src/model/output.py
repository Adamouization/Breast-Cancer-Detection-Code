import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import accuracy_score, auc, classification_report, confusion_matrix, roc_curve
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical


def plot_roc_curve(y_true: list, y_pred: list) -> None:
    """
    Plot ROC curve for binary classification.
    :param y_true: Ground truth of the data in one-hot-encoding type.
    :param y_pred: Prediction result of the data in one-hot-encoding type.
    :return: None.
    """
    # calculate fpr, tpr, and area under the curve(auc)
    fpr, tpr, _ = roc_curve(argmax(y_ture, axis=1), argmax(y_pred,
                                                           axis=1))  # transform y_true and y_pred from one-hot-encoding to the label-encoding.
    roc_auc = auc(fpr, tpr)

    # plot
    plt.figure(figsize=(8, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)  # plot roc curve
    plt.plot([0, 1], [0, 1], 'k--', color='navy', lw=2)  # plot random guess line

    # set labels, title, ticks, legend, axis range and annotation
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.annotate('Random Guess', (.53, .48), color='navy')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plot_name = 'Receiver Operating Characteristic.png'
    plt.savefig("../output/{}".format(plot_name))
    plt.show()


# ref: https://github.com/DeepmindHub/python-/blob/master/ROC%20Curve%20Multiclass.py
def plot_roc_curve_multiclasses(y_true: list, y_pred: list, label_encoder) -> None:
    """
    Plot ROC curve for multi classification.
    :param y_true: Ground truth of the data in one-hot-encoding type.
    :param y_pred: Prediction result of the data in one-hot-encoding type.
    :return: None.
    """
    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    # calculate fpr, tpr, area under the curve(auc) of each class
    for i in range(len(label_encoder.classes_)):
        fpr[i], tpr[i], _ = roc_curve(y_true[:, i], y_pred[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    # calculate macro fpr, tpr and area under the curve(auc)
    all_fpr = np.unique(np.concatenate([fpr[i] for i in range(len(label_encoder.classes_))]))

    mean_tpr = np.zeros_like(all_fpr)
    for i in range(len(label_encoder.classes_)):
        mean_tpr += np.interp(all_fpr, fpr[i], tpr[i])

    mean_tpr /= len(label_encoder.classes_)

    fpr['macro'] = all_fpr
    tpr['macro'] = mean_tpr
    roc_auc['macro'] = auc(fpr['macro'], tpr['macro'])

    # calculate micro fpr, tpr and area under the curve(auc)
    fpr['micro'], tpr['micro'], _ = roc_curve(y_true.ravel(), y_pred.ravel())
    roc_auc['micro'] = auc(fpr['micro'], tpr['micro'])

    # plot
    plt.figure(figsize=(8, 5))

    # plot micro roc curve
    plt.plot(fpr['micro'], tpr['micro'],
             label='micro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc["micro"]),
             color='deeppink', linestyle=':', lw=4)

    # plot macro roc curve
    plt.plot(fpr['macro'], tpr['macro'],
             label='macro-average ROC curve (area = {0:0.2f})'
                   ''.format(roc_auc['macro']),
             color='black', linestyle=':', lw=4)

    # plot roc curve of each class
    colors = ['#3175a1', '#e1812b', '#39923a', '#c03d3e', '#9372b2']
    for i, color in zip(range(len(label_encoder.classes_)), colors):
        plt.plot(fpr[i], tpr[i], color=color, lw=2,
                 label='ROC curve of class {0} (area = {1:0.2f})'
                       ''.format(label_encoder.classes_[i], roc_auc[i]))

    plt.plot([0, 1], [0, 1], 'k--', color='red', lw=2)  # plot random guess line

    # set labels, title, ticks, legend, axis range and annotation
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.annotate('Random Guess', (.53, .48), color='red')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plot_name = 'Receiver Operating Characteristic.png'
    plt.savefig("../output/{}".format(plot_name))
    plt.show()


def plot_confusion_matrix(cm: np.ndarray, title: str, fmt: float, label_encoder) -> None:
    """
    Plot confusion matrix.
    :param cm: Confusion matrix array.
    :param title: The title of the figure.
    :param fmt: The formatter for numbers in confusion matrix.
    :return: None.
    """
    # plot
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(cm, annot=True, ax=ax, fmt=fmt, cmap=plt.cm.Blues)  # annot=True to annotate cells

    # set labels, title, ticks and axis range
    ax.set_xlabel('Predicted classes')
    ax.set_ylabel('True classes')
    ax.set_title(title)
    ax.xaxis.set_ticklabels(label_encoder.classes_)
    ax.yaxis.set_ticklabels(label_encoder.classes_)
    plt.tight_layout()
    bottom, top = ax.get_ylim()
    # ax.set_ylim(bottom + 0.5, top - 0.5)
    plot_name = title + '.png'
    plt.savefig("../output/{}".format(plot_name))
    plt.show()


def plot_comparison_chart(df: pd.DataFrame, comp_type: str) -> None:
    """
    Plot comparison bar chart.
    :param df: Compare data from json file.
    :param comp_type: Compare column.
    :return: None.
    """
    # plot
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.barplot(x='paper', y=comp_type, data=df)

    # add number at the top of the bar
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., height + 0.01, height, ha='center')

    # set title
    plt.title(comp_type.capitalize() + ' Comparison')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=60, ha='right', rotation_mode='anchor')
    plot_name = comp_type.capitalize() + ' Comparison.png'
    plt.savefig("../output/{}".format(plot_name), bbox_inches = 'tight')
    plt.show()


def evaluate(y_true: list, y_pred: list, label_encoder: LabelEncoder, dataset: str, classification_type: str):
    """
    Evaluate model performance with accuracy, confusion matrix, ROC curve and compare with other papers' results.
    :param y_true: Ground truth of the data in one-hot-encoding type.
    :param y_pred: Prediction result of the data in one-hot-encoding type.
    :param label_encoder: The label encoder for y value (label).
    :param dataset: The dataset to use.
    :param classification_type: The classification type. Ex: N-B-M: normal, benign and malignant; B-M: benign and malignant.
    :return: None.
    """
    # inverse transform y_true and y_pred from one-hot-encoding to original label
    y_true_inv = label_encoder.inverse_transform(np.argmax(y_true, axis=1))
    y_pred_inv = label_encoder.inverse_transform(np.argmax(y_pred, axis=1))

    y_pred_one_hot = to_categorical(np.argmax(y_pred, axis=1))

    accuracy = float('{:.4f}'.format(accuracy_score(y_true_inv, y_pred_inv)))  # calculate accuracy

    print('accuracy = ', accuracy)
    print()
    print(classification_report(y_true_inv, y_pred_inv,
                                target_names=label_encoder.classes_))  # print classification report for precision, recall and f1

    # plot confusion matrix
    cm = confusion_matrix(y_true_inv, y_pred_inv)  # calculate confusion matrix with original label of classes
    plot_confusion_matrix(cm, 'Confusion Matrix', 'd', label_encoder)

    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:,
                                         np.newaxis]  # calculate normalized confusion matrix with original label of classes
    cm_normalized[np.isnan(cm_normalized)] = 0
    plot_confusion_matrix(cm_normalized, 'Normalized Confusion Matrix', '.2f', label_encoder)

    # plot roc curve
    if len(label_encoder.classes_) == 2:  # binary classification
        plot_roc_curve(y_true, y_pred_one_hot)

    elif len(label_encoder.classes_) >= 2:  # multi classification
        plot_roc_curve_multiclasses(y_true, y_pred_one_hot, label_encoder)

    # compare with other papers' result
    with open('other/other_results.json') as config_file:  # load other papers' result from json file
        data = json.load(config_file)

    df = pd.DataFrame.from_records(data[dataset][classification_type],
                                   columns=['paper', 'accuracy'])  # filter data by dataset and classification type

    new_row = pd.DataFrame({'paper': 'Dissertation', 'accuracy': accuracy},
                           index=[0])  # add model result into dataframe to compare
    df = pd.concat([new_row, df]).reset_index(drop=True)

    df['accuracy'] = pd.to_numeric(df['accuracy'])  # digitize the accuracy column

    plot_comparison_chart(df, 'accuracy')