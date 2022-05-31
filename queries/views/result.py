import pandas as pd
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from django.shortcuts import render
from sqlalchemy import create_engine
from io import BytesIO
from pandas.api.types import is_numeric_dtype

from ..models import Query

max_table_rows = 50
image_encoding = 'jpg'


def execute(request, id):
    query = Query.objects.get(pk=id)
    db = query.database
    # https://www.rudderstack.com/guides/access-and-query-your-amazon-redshift-data-using-python-and-r/
    engine = create_engine(f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    df = pd.read_sql(query.query, engine)
    df_reduced = df.head(max_table_rows)
    is_chart = df.columns.size > 1 and is_numeric_dtype(df.iloc[:, 1])
    chart = None
    if is_chart:
        chart = get_chart(df_reduced)
    context = {
        'title': query.title,
        'table': df_reduced,
        'tableHtml': df_reduced.to_html(classes=["table table-dark table-sm table-responsive"]),
        'query': query,
        'image_encoding': image_encoding,
        'chart': chart,
        'is_chart': is_chart
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

    dataframe.plot(x=columns[0], y=columns[1], kind='bar', figsize=(8, 6))
    plt.locator_params(axis='x', nbins=10)  # reduce the number of ticks
    plt.tight_layout()
    # plt.switch_backend('AGG')
    # plt.axis('off')
    chart = get_graph()
    return chart
