from evaluation_metrics import *

qrel_path = "msmarco-docdev-qrels.tsv"
results_path = "BM25_eval.txt"
#relevancies = process_qrel_file(qrel_path)
#print(relevancies.relevancies)
# all 1 because only the relevant documents are present in the qrel file

results = evaluate(qrel_path, results_path)
print(results)
