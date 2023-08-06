#!/usr/bin/env python

from prometheus_client import start_http_server, Summary, Gauge
from elasticsearch import Elasticsearch
import random, time, os
from functools import reduce  # forward compatibility for Python 3
import operator

# Create a metric to track time spent and requests made.
ELASTICSEARCH_QUERY_RESULTS = Gauge(os.getenv('ELASTICSEARCH_QUERY_RESULTS_NAME', 'elasticsearch_query_results'), 
                                    os.getenv('ELASTICSEARCH_QUERY_RESULTS_TEXT', 'Results from Elasticsearch query'))
# Create a metric to track time spent and requests made.
ES_QUERY_TIME = Summary(os.getenv('ES_QUERY_TIME_NAME', 'es_query_time_seconds'), 
                        os.getenv('ES_QUERY_TIME_TEXT', 'Time spent Querying Elasticsearch'))

es = Elasticsearch(os.getenv('ES_HOST_LIST', 'http://elasticsearch.jamiehouse:9200').split(','), 
                   maxsize=os.getenv('ES_MAX_CONNECTIONS', 25))

def get_by_path(root, items):
  """Access a nested object in root by item sequence."""
  return reduce(operator.getitem, items, root)

@ES_QUERY_TIME.time()
def query_elasticsearch():
  search_results = es.search(
            index=os.getenv('ES_SEARCH_INDEX', 'tempsensor-*'),
            # https://jsonlint.com/?reformat=compress
            body=os.getenv('ES_SEARCH_BODY', '{"query":{"range":{"@timestamp":{"gt":"now-15m"}}},"aggs":{"avg_temp":{"avg":{"field":"temp"}}}}'))
  query_results = get_by_path(search_results, os.getenv('ES_SEARCH_RESULT_FIELD_PATH', 'aggregations.avg_temp.value').split('.'))
  ELASTICSEARCH_QUERY_RESULTS.set(query_results)
  print("%s: %s" % (os.getenv('ELASTICSEARCH_QUERY_RESULTS_NAME', 'elasticsearch_query_results'), query_results))

if __name__ == '__main__':
  # Start up the server to expose the metrics.
  start_http_server(8000)
  # Generate some requests.
  while True:
    query_elasticsearch()
    time.sleep(os.getenv('SLEEP_TIME', 10))

