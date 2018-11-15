import json

from django.db import connection
from django.conf import settings
from rest_framework.response import Response


class MetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not settings.DEBUG:
            return response

        response = self.add_metrics_to_response(response)

        return response

    @staticmethod
    def add_metrics_to_response(response):
        queries_count = len(connection.queries)
        sql_time = 0

        sql_queries = []
        duplicate_queries = []
        for index, query in enumerate(connection.queries):
            sql_query = str(query["sql"])
            sql_query = sql_query.replace("\"", "'")
            
            if sql_query in sql_queries:
                duplicate_queries.append(sql_query)

            sql_queries.append(sql_query)

            sql_time += float(query["time"])

        if isinstance(response, Response) and hasattr(response, "data"):
            try:
                response.data["metrics"] = {
                    "number_of_queries": queries_count,
                    "sql_queries": sql_queries,
                    "duplicate_queries": duplicate_queries,
                    "sql_total_time": sql_time
                }
                response.content = json.dumps(response.data)
            except TypeError:
                return response

        return response
