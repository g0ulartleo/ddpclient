import datetime


class Selector(object):
    def __init__(self):
        # https://fedorahosted.org/suds/wiki/TipsAndTricks#TypesNamesContaining
        # client.factory.separator('/')
        self.selector_data = {}
        self.selector_data['fields'] = []
        self.selector_data['predicates'] = []
        self.selector_data['ordering'] = []

    def build(self, soap_client):
        return self._build_type(soap_client, ('Selector', self.selector_data))

    def _build_type(self, soap_client, data):

        if type(data) is tuple:
            t, d = data
            type_obj = soap_client.factory.create(t)

            if type(d) is dict:
                for sub_k, sub_data in d.iteritems():
                    type_obj[sub_k] = self._build_type(soap_client, sub_data)

                return type_obj
            else:
                return type_obj[d]
        elif type(data) is list:

            return [self._build_type(soap_client, sub_data)
                    for sub_data in data]

        else:
            return data

    def select_fields(self, *args):
        self.selector_data['fields'] = list(args)
        return self

    # filter criteria
    def filter_by(self, field, values, operator='=='):
        self.selector_data['predicates'].append(
            ('Predicate', {'field': field,
                           'operator':
                           self._create_predicate_operator(operator),
                           'values': values}))

        return self

    def order_by(self, field, desc=False):
        '''sortting a field by either 'ASCENDING' or 'DESCENDING' order.'''

        sort_order = ('SortOrder', 'DESCENDING' if desc else 'ASCENDING')
        self.selector_data['ordering'].append(('OrderBy', {'field': field,
                                                           'sortOrder':
                                                           sort_order}))

        return self

    def at_page(self, start_index=0, page_size=100):
        self.selector_data['paging'] = ('Paging', {'startIndex': start_index,
                                                   'numberResults': page_size})

        return self

    def _create_predicate_operator(self, short_operator_name):
        operatorr_map = {'!=': 'NOT_EQUALS',
                         '<>': 'NOT_EQUALS',
                         '==': 'EQUALS',
                         '>': 'GREATER_THAN',
                         '>=': 'GREATER_THAN_EQUALS',
                         '<': 'LESS_THAN',
                         '<=': 'LESS_THAN_EQUALS',
                         '[]': 'IN',
                         '][': 'NOT_IN'}

        match_operator = operatorr_map[
            short_operator_name] if operatorr_map.has_key(
                short_operator_name) else short_operator_name

        return ('Predicate.Operator', match_operator)
