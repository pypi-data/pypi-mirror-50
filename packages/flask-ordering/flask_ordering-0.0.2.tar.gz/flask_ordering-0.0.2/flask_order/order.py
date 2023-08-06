import logging

from flask import request
from sqlalchemy import desc, asc
from flask_rest_api import abort
from http import HTTPStatus

def ordering_response(Model): 
    def gen_function(func):
        def set_order(self, *args, **kwargs):
            query = func(self, *args, **kwargs)

            """
            ean --> ascending order of ean
            -ean --> descending order of ean
            
            if `query_parms_ordering` is None or empty value,
            set it's default value as '-id'
            """

            query_parms_ordering = request.args.get('ordering')
            if not query_parms_ordering or query_parms_ordering == '':
                query_parms_ordering = '-id'

            # return error when ordering value doesn't exist in the database
            if not query_parms_ordering.replace('-', '') in dir(Model):
                logging.info('ordering value not in the database as a column')
                raise abort(HTTPStatus.NOT_FOUND, message=f"your ordering value {query_parms_ordering} doesn't exist")

            # checking whether ordering is ascending or descending
            val = desc(query_parms_ordering[1:]) if query_parms_ordering[0] == '-' else asc(query_parms_ordering)
            return query.order_by(val)

        return set_order
    return gen_function 


def searching(field_list):
    def gen_function(func):
        def set_seraching(self, *args, **kwargs):
            query = func(self, *args, **kwargs)

            query_parms_q = request.args.get('q')
            if query_parms_q and query_parms_q != '':
                return query.msearch(query_parms_q, fields=field_list)
            return query
        return set_seraching
    return gen_function