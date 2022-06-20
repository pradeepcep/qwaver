import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import sqlalchemy
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from pandas.api.types import is_numeric_dtype
from sqlalchemy import create_engine

from . import user_can_access_query
from ..models import Query, Parameter

max_table_rows = 50
image_encoding = 'jpg'


def execute(request, id):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    query = get_object_or_404(Query, pk=id)
    user_can_access_query(request.user, query)
    params = Parameter.objects.filter(query=query)
    db = query.database
    is_dark = request.user.is_authenticated and request.user.profile.display_mode == 2
    if is_dark:
        plt.style.use('dark_background')
    else:
        # https://www.geeksforgeeks.org/style-plots-using-matplotlib/
        plt.style.use('fast')

    # creating context for params data
    sql = query.query
    title = query.title
    param_values = {}
    is_easter = False
    for param in params:
        param_value = request.GET.get(param.name)
        if param_value is None:
            param_value = param.default
        elif param_value == 'dml':
            is_easter = True
        param_values[param.name] = param_value
        sql = sql.replace(f"{{{param.name}}}", param_value)
        title = title.replace(f"{{{param.name}}}", param_value)
    # formatting the text to avoid problems with the % character in queries
    sql = sqlalchemy.text(sql)
    # https://www.rudderstack.com/guides/access-and-query-your-amazon-redshift-data-using-python-and-r/
    if db.title == "Aurora":
        connection = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    else:
        connection = create_engine(f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    if is_easter:
        return render(request, 'queries/easter.html', {})
        # return redirect("http://synthblast.com")
    else:
        try:
            df = pd.read_sql(sql, connection)
            # df_reduced = df.head(max_table_rows)
            df_reduced = df
            is_chart = df.columns.size == 2 and len(df.index) > 1 and is_numeric_dtype(df.iloc[:, 1])
            is_single = df.columns.size == 1 and len(df.index) == 1
            single = df.iat[0, 0]
            chart = None
            if is_chart:
                chart = get_chart(df_reduced)
            table_style = ""
            if is_dark:
                table_style = "table-dark"
            context = {
                'title': title,
                'table': df_reduced,
                'tableHtml': df_reduced.to_html(classes=[f"table {table_style} table-sm table-responsive"],
                                                table_id="results",
                                                index=False),
                'query': query,
                'image_encoding': image_encoding,
                'chart': chart,
                'is_chart': is_chart,
                'is_single': is_single,
                'single': single,
                'param_values': param_values,
                'params': params
            }
            return render(request, 'queries/result.html', context)
        except Exception as err:
            context = {
                'title': title,
                'query': query,
                'error': err,
                'params': params
            }
            return render(request, 'queries/result_error.html', context)


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

    dataframe.plot(x=columns[0], y=columns[1], kind='bar', figsize=(7, 4))
    plt.locator_params(axis='x', nbins=10)  # reduce the number of ticks
    plt.tight_layout()
    # plt.switch_backend('AGG')
    # plt.axis('off')
    chart = get_graph()
    return chart
