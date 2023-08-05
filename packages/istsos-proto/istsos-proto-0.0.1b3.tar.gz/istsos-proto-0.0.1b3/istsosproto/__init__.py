# -*- coding: utf-8 -*-

from .query_pb2 import (Query, Id, Where)


def qry(fields = {}):

    class Qry():

        def __init__(self, fields = {}):
            self._idx = 0
            self.fields = fields

        def __dir__(self):
            keys = ['to_pg']
            keys.sort()
            return keys

        def getIdx(self):
            self._idx += 1
            return "$%s" % self._idx

        def get_field(self, field):
            if field in self.fields.keys():
                if isinstance(self.fields[field], dict):
                    return self.fields[field]['column']
                return self.fields[field]
            else:
                return field
                # raise Exception("Field %s unknown" % field)

        def get_operator(self, operator):
            if operator == Where.GREATER_THAN:
                return '>'

            elif operator == Where.GREATER_THAN_OR_EQUAL_TO:
                return '>='

            elif operator == Where.LESS_THAN_OR_EQUAL_TO:
                return '<'

            elif operator == Where.LESS_THAN_OR_EQUAL_TO:
                return '<='

            elif operator == Where.EQUALS:
                return '='

            elif operator == Where.NOT_EQUALS:
                return '<>'

            elif operator == Where.LIKE:
                return 'IS LIKE'

            else:
                raise Exception("Operator %s unknown" % operator)

        def get_conditions(self, where, prepend = None):
            sql, p = self.prepare(where)

            if prepend is not None:
                return f"{prepend} {sql}", p
            
            return sql, p

        def prepare(self, where):

            sql = ''
            params = []

            # Nested conditions
            if where.operator in [Where.AND, Where.OR]:
                w = []
                for f in where.where:
                    sql, p = self.prepare(f)
                    params += p
                    w.append(sql)

                if where.operator == Where.AND:
                    return "(%s)" % " AND ".join(w), params

                else:
                    return "(%s)" % " OR ".join(w), params

            elif where.operator > 0:
                value = where.WhichOneof('value')

                if where.operator == Where.NOT_NULL:

                    sql = '%s IS NOT NULL' % (
                        self.get_field(where.property)
                    )

                else:
                    sql = '%s %s ' % (
                        self.get_field(where.property),
                        self.get_operator(where.operator)
                    )
                    if value == 'timestamp':
                        params.append(where.timestamp.ToDatetime())
                        sql += "%s" % self.getIdx()

                    elif value == 'count':
                        params.append(where.count)
                        sql += "%s" % self.getIdx()

                    elif value == 'measure':
                        params.append(where.measure)
                        sql += "%s" % self.getIdx()

                    elif value == 'text':
                        params.append(where.text)
                        sql += "%s" % self.getIdx()

                    elif value == 'bool':
                        params.append(where.bool)
                        sql += "%s" % self.getIdx()

                return sql, params

            else:
                if where.function == Where.ST_INTERSECTS:
                    params.append(where.ewkt)
                    sql = f"""
ST_Intersects(
    {self.get_field(where.property)},
    ST_GeomFromEWKT({self.getIdx()})
)
"""
                elif where.function == Where.ST_DWITHIN:
                    params.append(where.ewkt)
                    params.append(where.xmeasure)
                    sql = f"""
ST_DWithin(
    {self.get_field(where.property)},
    ST_GeomFromEWKT({self.getIdx()}),
    {self.getIdx()}
)
"""
                elif where.function == Where.ST_CONTAINS:
                    params.append(where.ewkt)
                    sql = f"""
ST_Contains(
    {self.get_field(where.property)},
    ST_GeomFromEWKT({self.getIdx()})
)
"""

                return sql, params

    return Qry(fields)
