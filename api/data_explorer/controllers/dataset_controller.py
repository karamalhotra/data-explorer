import connexion
import six

from flask import current_app

from data_explorer.models.dataset_response import DatasetResponse  # noqa: E501


def dataset_get():  # noqa: E501
    """dataset_get

    Gets dataset information, such as name. # noqa: E501

    :rtype: DatasetResponse
    """
    return DatasetResponse(
        name=current_app.config['DATASET_NAME'],
        table_names=current_app.config['TABLE_NAMES'])
