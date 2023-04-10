"""Metrics and plots for comparing networks.
"""
import numpy as np
import matplotlib.pyplot as plt

def compare_adj_plot(
        adj: np.ndarray,
        pred_adj: np.ndarray,
        title: str= None,
):
    """Compares two zero-one adjacency matrixes in a true-positive,
    false-positive and false-negative plot.
     
    Parameters
    ----------
    adj: A square numpy array that describes the true network.
    pred_adj: A numpy array with the same dimensions as `adj` that
        contains the predicted network.
    title: A title for the plot. (Defaults to None)

    Returns:
        A plot of a true vs predicted adjacency matrix.
    """
    n = pred_adj.shape[0]
    
    true_pos = (adj == 1) & (pred_adj == 1)
    false_pos = (adj == 0) & (pred_adj == 1)
    false_neg = (adj == 1) & (pred_adj == 0)


    plt.scatter(*np.where(true_pos), marker = "o", s=8, c='green', label="Correct Prediction")
    plt.scatter(*np.where(false_pos), marker = "o", s=5, c='red', label="False Positives")
    plt.scatter(*np.where(false_neg), marker = "o", s=5, c='gray', label="False Negatives")

    plt.axis("off")
    plt.legend(loc=(1, .8))
    plt.ylim((n+1, -1))
    plt.title(title)
    plt.show()

def compare_adj_f1_score(
        true_adj: np.ndarray,
        pred_adj: np.ndarray,
        verbose: bool = False,
):
    """Compares two zero-one adjacency matrixes and returns the F1
    score based on precision and recall of edges.
     
    When `verbose=True`, prints the confusion matrix and detailed metrics.

    Parameters
    ----------
    adj: A square numpy array that describes the true network.
    pred_adj: A numpy array with the same dimensions as `adj` that
        contains the predicted network.
    verbose: Determines if metrics should be displayed (Defaults to False)

    Returns:
        The F1 score computed based on the precision and recall of edges in
        the network.
    """
    num_edges = np.sum(true_adj)
    n = pred_adj.shape[0]

    true_pos = (true_adj == 1) & (pred_adj == 1)
    true_neg = (true_adj == 0) & (pred_adj == 0)
    false_pos = (true_adj == 0) & (pred_adj == 1)
    false_neg = (true_adj == 1) & (pred_adj == 0)
    precision = np.sum(true_pos) / (np.sum(true_pos) + np.sum(false_pos))
    recall = np.sum(true_pos) / num_edges

    f1_den = (precision + recall)
    if f1_den < 1e-11:
        f1 =  0.0
    else:
        f1 = 2 * precision * recall / f1_den

    if verbose:
        print(
            f"Predicted Adj Shape {pred_adj.shape} \n"
            f"True Adj Shape {true_adj.shape} \n"
            f"Number of edges: {num_edges} \n"
            f"True Pos: {np.sum(true_pos)} \t False Pos: {np.sum(false_pos)} \n"
            f"False Neg: {np.sum(false_neg)} \t True Neg: {np.sum(true_neg)} \n"
            f"Precision: {precision} \n"
            f"Recall: {recall} \n"
            f"F1 Score: {f1}"
        )
    return f1