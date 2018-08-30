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


def facets_get(filter=None, plot="Age", plot2="Age"):  # noqa: E501
    """facets_get

    Returns facets. # noqa: E501

    :param filter: filter represents selected facet values. Elasticsearch query will be run only over selected facet values. filter is an array of strings, where each string has the format \&quot;facetName&#x3D;facetValue\&quot;. Example url /facets?filter&#x3D;Gender&#x3D;female,Region&#x3D;northwest,Region&#x3D;southwest
    :type filter: List[str]

    :rtype: FacetsResponse
    """
    print('called facets_controller')
    client = Elasticsearch(current_app.config['ELASTICSEARCH_URL'])
    request = Search(index='project_baseline').using(client)
    request = request[0:30]
    es_response = request.execute()
    datak = {}

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
            try:
                es_field_name = current_app.config['ELASTICSEARCH_FACETS'][
                    name]._params['field'].split('.keyword')[0]
                weight = p['_source'][es_field_name]
                all_data.loc[all_data.index == participant_id, name] = weight
            except:
                continue
    all_data = all_data.convert_objects(convert_numeric=True)
    #
    # all_data_with_indicators = pd.get_dummies(all_data).dropna().copy()
    #
    # select = SelectKBest(score_func=chi2, k='all')
    # current_es_plot_name = current_app.config['ELASTICSEARCH_FACETS'][plot]._params[
    #                 'field'].split('.keyword')[0]
    # associated_var_columns = [i for i in all_data_with_indicators.columns if plot in i]
    # use_as_correlated = associated_var_columns[0]
    #
    # y = all_data_with_indicators[use_as_correlated].values
    # y = y.astype('float64')
    #
    # cols = all_data_with_indicators[[col for col in all_data_with_indicators.columns if col != use_as_correlated]].columns
    #
    # input_data = all_data_with_indicators[[col for col in all_data_with_indicators.columns if col != use_as_correlated]].values
    # input_data = input_data.astype('float64')
    #
    # print(' y is ')
    # print(y.dtype)
    # print('input data')
    # print(input_data.dtype)

    # fit = select.fit(input_data, y)
    # highest_correlated= cols[np.argmax(fit.scores_)]
    # print('highest correlated')
    # print(highest_correlated)

    # for each facet, what is the best score?

    for name, description in current_app.config['UI_FACETS'].iteritems():
        es_field_name = current_app.config['ELASTICSEARCH_FACETS'][
            name]._params['field'].split('.keyword')[0]
        all_weights = []
        for hit in es_response['hits']['hits']:
            p = hit.to_dict()
            try:
                all_weights.append(p['_source'][es_field_name])
            except:
                continue
        datak[name] = all_weights

    def is_numeric(type_):
        if (type_ == 'int64') or (type_ == 'float64'):
            return True
        else:
            return False

    print('type is here')
    print(all_data[plot].dtype)
    if is_numeric(all_data[plot].dtype) and is_numeric(all_data[plot2].dtype):
        answer = stats.pearsonr(all_data[plot].values, all_data[plot2].values)
        response = 'peasonr coeff for %s and %s is %0.2f' % (plot, plot2,
                                                             answer[0])
        print(response)

    else:
        response = 'nope: %s is type %s, %s is type %s'%(plot, is_numeric(all_data[plot].dtype), plot2, all_data[plot2].dtype)
    print(response)
    # test = pd.DataFrame(datak)
    #print(test.head())
    datak['highest_correlation'] = response
    datak['highest_correlation_name'] = ''
    # data_to_correlate = pd.Series(datak[plot])
    # if data_to_correlate.dtypes == 'O':
    #     data_to_correlate = data_to_correlate.astype('category').cat.codes
    #
    # for name, description in current_app.config['UI_FACETS'].iteritems():
    #     if name != plot:
    #         data_var2 = pd.Series(datak[name])
    #         if data_var2.dtypes == 'O':
    #             data_var2 = data_var2.astype('category').cat.codes
    #         correlation = data_to_correlate.corr(data_var2)
    #         if correlation > datak['highest_correlation']:
    #             datak['highest_correlation'] = correlation
    #             datak['highest_correlation_name'] = name

    plot_name = plot
    plot_name2 = plot2

    search = DatasetFacetedSearch(deserialize(filter))
    es_response = search.execute()
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
