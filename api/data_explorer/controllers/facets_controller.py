from data_explorer.models.facet import Facet
from data_explorer.models.facet_value import FacetValue
from data_explorer.models.facets_response import FacetsResponse
from elasticsearch_dsl import HistogramFacet
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from flask import current_app
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import numpy as np
from scipy import stats
from ..dataset_faceted_search import DatasetFacetedSearch
import urllib
import pandas as pd
import time

def process_response_for_correlations(es_response, plot, plot2):
    get_all_data = False
    datak = {}
    if True:#not 'all_data' in locals():
        print('redoing full processing')
        participants = []
        for hit in es_response['hits']['hits']:
            p = hit.to_dict()
            participants.append(p['_id'])

        facets = []
        for name, description in current_app.config['UI_FACETS'].iteritems():
            facets.append(name)

        all_data = pd.DataFrame(index=participants, columns=facets)

        for hit in es_response['hits']['hits']:
            p = hit.to_dict()
            participant_id = p['_id']
            for name, description in current_app.config['UI_FACETS'].iteritems():
                if (not get_all_data) and (name!=plot and name!=plot2):
                    continue
                try:
                    es_field_name = current_app.config['ELASTICSEARCH_FACETS'][
                        name]._params['field'].split('.keyword')[0]
                    weight = p['_source'][es_field_name]
                    all_data.loc[all_data.index == participant_id, name] = weight
                except:
                    continue
        all_data = all_data.convert_objects(convert_numeric=True)
        print(all_data[plot])
        print(all_data[plot].dtype)
        def is_numeric(type_):
            if (type_ == 'int64') or (type_ == 'float64'):
                return True
            else:
                return False

        correlation_matrix = pd.DataFrame(index=facets, columns=facets)
        for facet_1 in facets:
            for facet_2 in facets:
                if not get_all_data and (facet_1!=plot or facet_2!=plot2):
                    continue
                if (is_numeric(all_data[facet_1].dtype) and is_numeric(all_data[facet_2].dtype)):
                    answer = stats.pearsonr(all_data[facet_1].values, all_data[facet_2].values)
                    response = 'peasonr coeff = %0.2f' % (answer[0])
                elif (is_numeric(all_data[facet_1].dtype) and is_numeric(all_data[facet_2].dtype)==False):
                    data = {}
                    for rc in np.unique(all_data[facet_2]):
                        if rc is None or pd.isnull(rc):
                            continue
                        data[rc] = all_data[all_data[facet_2] == rc][facet_1].dropna().values

                    answer = stats.f_oneway(*[data[k] for k in data.keys()])
                    response = 'anova F value= %0.2f' % (answer[0])
                elif (is_numeric(all_data[facet_1].dtype)==False and is_numeric(all_data[facet_2].dtype)):
                    data = {}
                    for rc in np.unique(all_data[facet_1]):
                        if rc is None or pd.isnull(rc):
                            continue
                        print(rc)
                        print(type(rc))
                        data[rc] = all_data[all_data[facet_1] == rc][facet_2].dropna().values

                    print('---------------')
                    print(data['yes'])
                    print((data['no']))
                    print(data.keys())
                    print(len(data.keys()))
                    answer = stats.f_oneway(*[data[k] for k in data.keys()])
                    response = 'anova F value= %0.2f' % (answer[0])
                else:
                    # Cross tab shows the distributionsof each category with respect to each other
                    ct1 = pd.crosstab(all_data[facet_1], all_data[facet_2])
                    cs1 = stats.chi2_contingency(ct1)
                    response = 'Chi2 test stat= %0.2f' % (cs1[0])
                correlation_matrix.loc[facet_1, facet_2] = response
        print(correlation_matrix)

    if get_all_data:
        for name in facets:
            datak[name] = list(all_data[name].values)

        for facet_1 in facets:
            for facet_2 in facets:
                datak[facet_1+'_'+facet_2] = correlation_matrix.loc[facet_1, facet_2]
    else:
        datak[plot] = list(all_data[plot].values)
        datak[plot2] = list(all_data[plot2].values)
        datak[plot + '_' + plot2] = correlation_matrix.loc[plot, plot2]

        datak['highest_correlation'] = correlation_matrix.loc[plot, plot2]
    return datak

def facets_get(filter=None, plot="Age", plot2="Age"):  # noqa: E501
    """facets_get

    Returns facets. # noqa: E501

    :param filter: filter represents selected facet values. Elasticsearch query will be run only over selected facet values. filter is an array of strings, where each string has the format \&quot;facetName&#x3D;facetValue\&quot;. Example url /facets?filter&#x3D;Gender&#x3D;female,Region&#x3D;northwest,Region&#x3D;southwest
    :type filter: List[str]

    :rtype: FacetsResponse
    """
    print('called facets_controller')
    # client = Elasticsearch(current_app.config['ELASTICSEARCH_URL'])
    # request = Search(index='project_baseline').using(client)
    # request = request[0:200]
    # es_response = request.execute()
    plot_name = plot
    plot_name2 = plot2
    print('about to start faceted search')
    print(time.time())
    search = DatasetFacetedSearch(deserialize(filter))
    es_response = search.execute()
    print('finished faceted search')
    print(time.time())
    print(len(es_response['hits']['hits']))
    datak = process_response_for_correlations(es_response, plot, plot2)
    print('finished correlations')
    print(time.time())
    es_response_facets = es_response.facets.to_dict()
    facets = []
    for name, description in current_app.config['UI_FACETS'].iteritems():
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
        datak=datak,
        plot_name=plot_name,
        plot_name2=plot_name2)


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
