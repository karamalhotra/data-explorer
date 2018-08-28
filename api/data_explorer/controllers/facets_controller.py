from data_explorer.models.facet import Facet
from data_explorer.models.facet_value import FacetValue
from data_explorer.models.facets_response import FacetsResponse
from elasticsearch_dsl import HistogramFacet
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

from flask import current_app

from ..dataset_faceted_search import DatasetFacetedSearch
import urllib


def facets_get(filter=None, plot="Age"):  # noqa: E501
    """facets_get

    Returns facets. # noqa: E501

    :param filter: filter represents selected facet values. Elasticsearch query will be run only over selected facet values. filter is an array of strings, where each string has the format \&quot;facetName&#x3D;facetValue\&quot;. Example url /facets?filter&#x3D;Gender&#x3D;female,Region&#x3D;northwest,Region&#x3D;southwest
    :type filter: List[str]

    :rtype: FacetsResponse
    """
    client = Elasticsearch(current_app.config['ELASTICSEARCH_URL'])
    request = Search(index='project_baseline').using(client)
    request = request[0:2000]
    es_response = request.execute()
    print('-----------')
    print(plot)
    es_field_name = current_app.config['ELASTICSEARCH_FACETS'][plot]._params['field'].split('.keyword')[0]
    print(es_field_name)
    all_weights = []
    for hit in es_response['hits']['hits']:
        p = hit.to_dict()
        try:
            all_weights.append(p['_source'][es_field_name])
        except:
            continue

    plot_name = plot
    # print('KB')
    # print(plot)
    # print(all_weights)
    # print('in get facets now')
    # #return FacetsResponse(facets=all_weights)
    # print('the filter is')
    # print(filter)
    search = DatasetFacetedSearch(deserialize(filter))
    es_response = search.execute()
    es_response_facets = es_response.facets.to_dict()
    facets = []
    for name, description in current_app.config['UI_FACETS'].iteritems():
        print(name)
        es_facet = current_app.config['ELASTICSEARCH_FACETS'][name]
        values = []
        for value_name, count, _ in es_response_facets[name]:
            if isinstance(es_facet, HistogramFacet):
                # For histograms, Elasticsearch returns:
                #   name 10: count 15     (There are 15 people aged 10-19)
                #   name 20: count 33     (There are 33 people aged 20-29)
                # Convert "10" -> "10-19".
                range_str = _number_to_range(value_name,
                                             es_facet._params['interval'])
                values.append(FacetValue(name=range_str, count=count))
            else:
                values.append(FacetValue(name=value_name, count=count))
        facets.append(Facet(name=name, description=description, values=values))

    return FacetsResponse(
        facets=facets,
        count=es_response._faceted_search.count(),
        datak=all_weights,
        plot_name=plot_name)


def deserialize(filter_arr):
    """
    :param filter_arr: an array of strings with format "facet_name=facet_value".
    A facet_name may be repeated if multiple filters are desired.
    :return: A dict of facet_name:[facet_value] mappings.
    """
    if not filter_arr or filter_arr == [""]:
        return {}
    parsed_filter = {}
    print(filter_arr)
    # filter_str looks like "Gender=male"
    for facet_filter in filter_arr:
        print(facet_filter)
        filter_str = urllib.unquote(facet_filter).decode('utf8')
        key_val = filter_str.split('=')
        name = key_val[0]

        es_facet = current_app.config['ELASTICSEARCH_FACETS'][name]
        if isinstance(es_facet, HistogramFacet):
            value = _range_to_number(key_val[1])
        else:
            value = key_val[1]

        if not name in parsed_filter:
            parsed_filter[name] = [value]
        else:
            parsed_filter[name].append(value)
    return parsed_filter


def _number_to_range(bucket_number, interval_size):
    """Converts "X" -> "X-Y"."""
    return '%d-%d' % (bucket_number, bucket_number + interval_size - 1)


def _range_to_number(bucket_string):
    """Converts "X-Y" -> "X"."""
    return int(bucket_string.split('-')[0])
