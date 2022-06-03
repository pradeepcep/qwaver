import pandas as pd
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import sqlalchemy
from django.shortcuts import render
from sqlalchemy import create_engine
from io import BytesIO
from pandas.api.types import is_numeric_dtype

from ..models import Query, Parameter

max_table_rows = 50
image_encoding = 'jpg'


def execute(request, id):
    query = Query.objects.get(pk=id)
    params = Parameter.objects.filter(query=query)
    db = query.database

    # creating context for params data
    sql = query.query
    title = query.title
    param_values = {}
    for param in params:
        param_value = request.GET.get(param.name)
        if param_value is None:
            param_value = param.default
        param_values[param.name] = param_value
        sql = sql.replace(f"{{{ param.name }}}", param_value)
        title = title.replace(f"{{{param.name}}}", param_value)
    # formatting the text to avoid problems with the % character in queries
    sql = sqlalchemy.text(sql)
    # https://www.rudderstack.com/guides/access-and-query-your-amazon-redshift-data-using-python-and-r/
    engine = create_engine(f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    df = pd.read_sql(sql, engine)
    df_reduced = df.head(max_table_rows)
    is_chart = df.columns.size > 1 and is_numeric_dtype(df.iloc[:, 1])
    chart = None
    if is_chart:
        chart = get_chart(df_reduced)
    context = {
        'title': title,
        'table': df_reduced,
        'tableHtml': df_reduced.to_html(classes=["table table-dark table-sm table-responsive"]),
        'query': query,
        'image_encoding': image_encoding,
        'chart': chart,
        'is_chart': is_chart,
        'param_values': param_values,
        'params': params
    }
    return render(request, 'queries/result.html', context)


# https://www.section.io/engineering-education/representing-data-in-django-using-matplotlib/
# possible idea for returning only image from endpoint: https://groups.google.com/g/pydata/c/yxKcJI4Y7e8
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format=image_encoding)
    buffer.seek(0)
    image_data = buffer.getvalue()
    graph = base64.b64encode(image_data)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(dataframe):
    # ax = plt.axes()
    # ax.xaxis.set_major_locator(ticker.MaxNLocator(3))
    # plt.locator_params(nbins=4)
    header = dataframe.head()
    columns = list(header.columns.values)

    dataframe.plot(x=columns[0], y=columns[1], kind='bar', figsize=(6, 4))
    plt.locator_params(axis='x', nbins=10)  # reduce the number of ticks
    plt.tight_layout()
    # plt.switch_backend('AGG')
    # plt.axis('off')
    chart = get_graph()
    return chart
