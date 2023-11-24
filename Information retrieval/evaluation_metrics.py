import numpy as np
from process_files import *

'''
NDCG to measure the overall ranking quality and Precision@k to measure the quality of the top-k results.
NDCG is used as the official metric for the TREC Deep Learning Track, which is based on the MS MARCO dataset.
Therefore, NDCG is a reasonable choice for evaluating systems that use the MS MARCO dataset, regardless of the retrieval model used.
'''


def precision(query_relevancy_labels, k):
  """Computes the precision at k for a given query.

  Args:
    query_relevancy_labels: A numpy array of relevancy labels for the query.
    k: The number of top results to consider.

  Returns:
    The precision at k for the given query.
  """

  # Get the top k results.
  top_k_results = query_relevancy_labels[:k]

  # Count the number of relevant results in the top k results.
  num_relevant_results = np.sum(top_k_results)

  # Compute the precision at k.
  precision_at_k = num_relevant_results / k

  return precision_at_k


def DCG(query_relevancy_labels):
    i = len(query_relevancy_labels)
    return np.sum(query_relevancy_labels / np.log2(1 + np.arange(1, i + 1)))

def NDCG(query_relevancy_labels):
  """Computes the Normalized Discounted Cumulative Gain (NDCG) for a given query.

  Args:
    query_relevancy_labels: A numpy array of relevancy labels for the query.
    k: The number of top results to consider.

  Returns:
    The NDCG for the given query.
  """

  # Compute the DCG.
  DCG_score = DCG(query_relevancy_labels)

  ideal_relevancy_labels = np.sort(query_relevancy_labels)[::-1]
  IDCG = DCG(ideal_relevancy_labels)

  # If the IDCG is 0, then the NDCG is undefined.
  if IDCG == 0:
    return 0.0

  return DCG_score / IDCG

def evaluate(qrel_path, results_path):
    results_per_query = {
        'precision@1': [],
        'precision@5': [],
        'precision@10': [],
        'precision@25': [],
        'NDCG': [],
    }
    for labels in process_files(qrel_path, results_path):
        print(labels)
        results_per_query['precision@1'].append(precision(labels, 1))
        results_per_query['precision@5'].append(precision(labels, 5))
        results_per_query['precision@10'].append(precision(labels, 10))
        results_per_query['precision@25'].append(precision(labels, 25))
        results_per_query['NDCG'].append(NDCG(labels))

    results = {}
    for key, values in results_per_query.items():
        results[key] = np.mean(values)
    return results
