import base64
import datetime
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
import pymysql
import sqlalchemy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from pandas.api.types import is_numeric_dtype
from sqlalchemy import create_engine
from dateutil.parser import parse

from . import user_can_access_query
from ..models import Query, Parameter, Result, Value

max_table_rows = 500
image_encoding = 'jpg'


class ResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
    context_object_name = 'result'

    def get_object(self, queryset=None):
        user = self.request.user
        result = get_object_or_404(Result, id=self.kwargs.get('pk'))
        user_can_access_query(user, result.query)
        return result

    def get_context_data(self, **kwargs):
        context = super(ResultDetailView, self).get_context_data(**kwargs)
        values = Value.objects.filter(result=self.object)
        current_parameters = Parameter.objects.filter(query=self.object.query)

        has_valid_parameters = True
        for value in values:
            # if the value of this result does not match any of the current parameters of the query
            if not any(parameter.name == value.parameter_name for parameter in current_parameters):
                has_valid_parameters = False
        for parameter in current_parameters:
            # if a current parameter for the query doesn't match any of the saved values
            if not any(parameter.name == value.parameter_name for value in values):
                has_valid_parameters = False
        context['params'] = values
        context['has_valid_parameters'] = has_valid_parameters
        return context


# 1. Getting the user, query and parameters
# 2. Creating a connection to the db
# 3. Replacing placeholder parameters with their values
# 4. Executing the query
# 5. Saving the result to the DB
def execute(request, id):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login'))
    query = get_object_or_404(Query, pk=id)
    user_can_access_query(user, query)
    params = Parameter.objects.filter(query=query)
    is_dark = user.is_authenticated and user.profile.display_mode != 1
    table_style = ""
    if is_dark:
        table_style = "table-dark"
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
        param_value = request.POST.get(param.name)
        if param_value is None:
            param_value = param.default
        elif param_value == 'dml':
            is_easter = True
        param_values[param.name] = param_value
        # if there are results, save the param value as default
        sql = sql.replace(f"{{{param.name}}}", param_value)
        title = title.replace(f"{{{param.name}}}", param_value)
    # formatting the text to avoid problems with the % character in queries
    sql = sqlalchemy.text(sql)
    # https://www.rudderstack.com/guides/access-and-query-your-amazon-redshift-data-using-python-and-r/
    db = query.database
    if db.platform == db.MYSQL:
        connection = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    else:
        connection = create_engine(f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    if is_easter:
        return render(request, 'queries/easter.html', {})
        # return redirect("http://synthblast.com")
    else:
        try:
            df_full = pd.read_sql(sql, connection)
            df = df_full.head(max_table_rows)
            row_count = len(df.index)
            column_count = df.columns.size
            chart = None
            single = None
            if row_count > 0:
                is_chart = column_count == 2 and row_count > 1 and is_numeric_dtype(df.iloc[:, 1])
                is_single = column_count == 1 and row_count == 1
                if is_single:
                    single = df.iat[0, 0]
                if is_chart:
                    chart = get_chart(df)
            else:
                single = "no results"
            result = Result(
                user=user,
                query=query,
                title=title,
                dataframe=df.to_json(),
                table=df.to_html(classes=[f"table {table_style} table-sm table-responsive"],
                                                table_id="results",
                                                index=False),
                single=single,
                image_encoding=image_encoding,
                chart=chart
            )
            result.save()
            # update query with latest result
            query.run_count += 1
            query.last_run_date = datetime.datetime.now()
            query.latest_result = result
            query.save()
            # save parameter values
            for param_name, param_value in param_values.items():
                value = Value(
                    parameter_name=param_name,
                    value=param_value,
                    result=result
                )
                value.save()
            return redirect(reverse('result-detail', args=[result.pk]))
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


def get_svg_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='svg')
    buffer.seek(0)
    image_data = str(buffer.getvalue())
    image_data = image_data.replace('\\n', '\n')
    buffer.close()
    return image_data


def get_chart(dataframe):
    header = dataframe.head()
    columns = list(header.columns.values)
    first_value = dataframe[columns[0]].iat[0]
    # if first_value is number or date, assume this is a bar chart
    if first_value is not None and isinstance(first_value, datetime.date):
        dataframe.plot(x=columns[0], y=columns[1], kind='bar', figsize=(7, 4), legend=False)
        plt.locator_params(axis='x', nbins=10)  # reduce the number of ticks
    else:
        # converting first column to a string
        dataframe[columns[0]] = dataframe[columns[0]].astype(str)
        grouped = dataframe.groupby([columns[0]]).sum().sort_values([columns[1]], ascending=False)
        grouped.plot(y=columns[1], kind='pie', figsize=(7, 4), legend=False)
        plt.axis('off')
    plt.tight_layout()
    chart = get_graph()
    return chart


# https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format
def is_date(string):
    try:
        parse(string, fuzzy=False)
        return True
    except ValueError:
        return False


# https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?page=1&tab=scoredesc#tab-top
def is_number(s):
    try:
        float(s)
        return True
    except Exception:
        return False
