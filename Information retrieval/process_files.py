import csv
import numpy as np
from relevancy import relevancy_lookup

def parse_qrel_line(line):
    #query_id, _, document_id, relevance
    line = line[0].split()
    return int(line[0]), line[2], int(line[3])

def process_qrel_file(qrel_path):
    relevancies = relevancy_lookup()

    with open(qrel_path) as file:
        qrel_file = csv.reader(file, delimiter="\t")
        for line in qrel_file:
            query, document, relevancy = parse_qrel_line(line)
            relevancies.add(query, document, relevancy)
    return relevancies

###########################


def parse_results_line(line):
  """Parses a single line from the results file and outputs the query ID, the document ID and the rank at which the document is placed by the ranking system.

  Args:
    line: A string containing a single line from the results file.

  Returns:
    A tuple containing the query ID, the document ID and the rank at which the document is placed by the ranking system.
  """

  # Split the line into its components.
  components = line.split()

  # Get the query ID, the document ID and the rank at which the document is placed by the ranking system.
  query = int(components[0])
  document = "D" + components[2]
  rank = int(components[3])
  # query, relevancy, doc, rank, score, run
  # Return the query ID, the document ID and the rank at which the document is placed by the ranking system.
  return query, document, rank

def get_ranked_labels(rel_lookup, query, doc_rank_list):
    result = np.zeros(len(doc_rank_list), dtype=int)
    for x in doc_rank_list:
        result[x[1]-1] = rel_lookup.get(query, x[0])
    return result

def process_results_file(results_path):
    with open(results_path, 'r') as results_file:
        current_query, document, rank = parse_results_line(next(results_file))
        doc_rank_list = [(document, rank)]
        for line in results_file:
            query, document, rank = parse_results_line(line)
            if query != current_query:
                yield get_ranked_labels(relevancies, current_query, doc_rank_list)
                current_query = query
                doc_rank_list = [(document, rank)]
            else:
                doc_rank_list.append((document, rank))
        yield get_ranked_labels(relevancies, current_query, doc_rank_list)

def process_files(qrel_path, results_path):
    relevancies = process_qrel_file(qrel_path)
    with open(results_path, 'r') as results_file:
        current_query, document, rank = parse_results_line(next(results_file))
        doc_rank_list = [(document, rank)]
        for line in results_file:
            query, document, rank = parse_results_line(line)
            if query != current_query:
                yield get_ranked_labels(relevancies, current_query, doc_rank_list)
                current_query = query
                doc_rank_list = [(document, rank)]
            else:
                doc_rank_list.append((document, rank))
        yield get_ranked_labels(relevancies, current_query, doc_rank_list)
