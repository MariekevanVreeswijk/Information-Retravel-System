class relevancy_lookup(object):
  def __init__(self):
    self.relevancies = {}

  def add(self, query, document, relevancy):
    """Adds a new document-query pair to the relevancy lookup.

    Args:
      query: The query ID.
      document: The document ID.
      relevancy: The relevancy of the document to the query.
    """

    if query not in self.relevancies:
      self.relevancies[query] = {}
    self.relevancies[query][document] = relevancy

  def get(self, query, document):
    """Gets the relevancy of a document to a query from the relevancy lookup.

    Args:
      query: The query ID.
      document: The document ID.

    Returns:
      The relevancy of the document to the query, or 0 if the document is not relevant to the query.
    """

    if query not in self.relevancies or document not in self.relevancies[query]:
      return 0
    return self.relevancies[query][document]
