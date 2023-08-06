import os
from django.http import HttpResponse
from django.db import connection
import pandas as pd


def generate_excel_from_sql(sql, columns):
    response = HttpResponse(content_type="application/xls")
    response['Content-Disposition'] = 'attachment; filename=Relatório de Guias.xls'
    try:
        df = pd.read_sql(sql, connection)
        df.to_excel("output.xls", header=columns, index=False)
        with open("output.xls", 'rb') as f:
            excel = f.read()
        response.write(excel)
        os.remove("output.xls")
    finally:
        pass
    return response