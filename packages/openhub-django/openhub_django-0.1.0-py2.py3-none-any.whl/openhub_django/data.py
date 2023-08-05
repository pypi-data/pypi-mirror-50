import json
import logging

import requests
import xmltodict

from openhub_django.variables import OH_TOKEN,ORG_NAME
from openhub_django.outside_projects import get_outside_projects_data
from openhub_django.portfolio_projects import get_portfolio_projects_data
from openhub_django.outside_committers import get_outside_committers_data
from openhub_django.affiliated_committers import get_affiliated_committers_data


def get_data(for_what):
    n = 100
    data_list = []
    logger = logging.getLogger(__name__)
    for i in range(1, n):
        import_url = ('https://www.openhub.net/orgs/'
                      + ORG_NAME + '/' + for_what + '.xml?api_key='
                      + OH_TOKEN + '&page=' + str(i))
        try:
            resp = requests.get(import_url)
            jsonString = json.dumps(xmltodict.parse(resp.content), indent=4)
            json_object = json.loads(jsonString)
        except Exception as ex:
            logger.error(ex)
            break
        if for_what == 'affiliated_committers':
            try:
                data = get_affiliated_committers_data(json_object)
            except Exception as ex:
                logger.error(ex)
                break
        elif for_what == 'outside_committers':
            try:
                data = get_outside_committers_data(json_object)
            except Exception as ex:
                logger.error(ex)
                break
        elif for_what == 'outside_projects':
            try:
                data = get_outside_projects_data(json_object)
            except Exception as ex:
                logger.error(ex)
                break
        elif for_what == 'projects':
            try:
                data = get_portfolio_projects_data(json_object)
            except Exception as ex:
                logger.error(ex)
                break
        data_list = data_list + data
    return data_list
