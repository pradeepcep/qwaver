import base64
import datetime
import numbers
from io import BytesIO

import matplotlib.pyplot
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy
from dateutil.parser import parse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView
from django.conf import settings
from pandas.api.types import is_numeric_dtype
from sqlalchemy import create_engine
from django.utils import timezone

from . import user_can_access_query
from ..common.components import users_recent_results
from ..models import Query, Parameter, Result, Value

max_table_rows = settings.MAX_TABLE_ROWS
image_encoding = 'jpg'

# So that server does not create (and then destroy) GUI windows that will never be seen
matplotlib.pyplot.switch_backend('Agg')


class ResultDetailView(LoginRequiredMixin, DetailView):
    model = Result
    context_object_name = 'result'

    def get_object(self, queryset=None):
        user = self.request.user
        result = get_object_or_404(Result, id=self.kwargs.get('pk'))
        user_can_access_query(user, result.query)
        result.last_view_timestamp = timezone.now()
        result.view_count = result.view_count + 1
        result.save()
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
        # getting historic results
        context['results'] = users_recent_results(query=self.object.query, user=self.request.user)
        context['selected_result'] = self.object
        context['has_valid_parameters'] = has_valid_parameters
        return context


# 1. Getting the user, query and parameters
# 2. Creating a connection to the db
# 3. Replacing placeholder parameters with their values
# 4. Executing the query
# 5. Saving the result to the DB
def execute(request, query_id):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('login'))
    query = get_object_or_404(Query, pk=query_id)
    user_can_access_query(user, query)
    params = Parameter.objects.filter(query=query)
    is_dark = user.is_authenticated and user.profile.display_mode != 1
    if is_dark:
        plt.style.use('dark_background')
    else:
        # https://www.geeksforgeeks.org/style-plots-using-matplotlib/
        plt.style.use('fast')

    # creating context for params data
    sql = query.query
    title = query.title
    param_values = {}
    for param in params:
        param_value = request.POST.get(param.name)
        if param_value is None:
            param_value = param.default
        param_values[param.name] = param_value
        # if there are results, save the param value as default
        sql = sql.replace(f"{{{param.name}}}", param_value)
        title = f"{title};\n {param.name}: {param_value}"
    # formatting the text to avoid problems with the % character in queries
    sql = sqlalchemy.text(sql)
    # https://www.rudderstack.com/guides/access-and-query-your-amazon-redshift-data-using-python-and-r/
    db = query.database
    if db.platform == db.MYSQL:
        connection = create_engine(f"mysql+pymysql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    elif db.platform == db.ORACLE:
        connection = create_engine(f"oracle://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    elif db.platform == db.MICROSOFT_SQL_SERVER:
        connection = create_engine(f"mssql+pymssql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    elif db.platform == db.SQLITE:
        connection = create_engine(f"sqlite://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    else:
        connection = create_engine(f"postgresql://{db.user}:{db.password}@{db.host}:{db.port}/{db.database}")
    try:
        df_full = pd.read_sql(sql, connection)
        df = df_full.head(max_table_rows)
        row_count = len(df.index)
        column_count = df.columns.size
        chart = get_chart(df, title)
        if chart is None:
            print("noooooooooooooooo")
        if row_count == 1 and column_count == 1:
            single = df.iat[0, 0]
        else:
            # single = str(list(df.columns.values))
            single = None
        result = Result(
            user=user,
            query=query,
            title=title,
            dataframe=df.to_json(),
            table=get_table(df),
            single=single,
            image_encoding=image_encoding,
            chart=chart,
            last_view_timestamp=timezone.now(),
            version_number=query.get_version_number(),
            query_text=sql
        )
        result.save()
        # update query with latest result
        query.run_count += 1
        query.last_run_date = timezone.now()
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


def get_chart(df, title):
    header = df.head()
    columns = list(header.columns.values)
    row_count = len(df.index)
    col_count = len(columns)
    if row_count < 2 or col_count < 2:
        return None
    first_value = df[columns[0]].iat[0]
    second_value = df[columns[1]].iat[0]
    third_value = None
    if col_count >= 3:
        third_value = df[columns[2]].iat[0]
    is_bar_or_pie = len(columns) == 2 and row_count > 1 and is_numeric_dtype(df.iloc[:, 1])
    is_pivot = (len(columns) == 3
                and row_count > 1
                and first_value is not None
                and second_value is not None
                and third_value is not None
                and isinstance(first_value, datetime.date)
                and isinstance(second_value, str)
                and isinstance(third_value, numbers.Number))
    if not is_bar_or_pie and not is_pivot:
        return None
    # if first_value is number or date, assume this is a bar chart
    is_bar = (first_value is not None
              and isinstance(first_value, (datetime.date, numbers.Number)))

    if is_pivot:
        # https://stackoverflow.com/a/48799804/2595659
        df.groupby([columns[0], columns[1]])[columns[2]] \
            .sum() \
            .unstack(level=1) \
            .plot.area()
        # .plot.bar(stacked=True)


    elif is_bar:
        df.plot(x=columns[0], y=columns[1], kind='bar', figsize=(7, 4), legend=False, title=title)
        plt.locator_params(axis='x', nbins=10)  # reduce the number of ticks
    # Else, pie chart
    else:
        # converting first column to a string
        df[columns[0]] = df[columns[0]].astype(str)
        grouped = df.groupby([columns[0]]).sum().sort_values([columns[1]], ascending=False)

        # row count:
        row_count = len(grouped.index)
        max_rows = 49
        if row_count > max_rows:
            # splitting dataframe by row index
            df1 = grouped.iloc[:max_rows, :]
            # summing the remainder
            df2 = grouped.iloc[max_rows:, :].sum()
            # adding sum of remainder columns as final row
            df1.loc['Remaining Values', :] = df2.sum(axis=0)
            grouped = df1
        grouped.plot(y=columns[1], autopct='%1.1f%%', kind='pie', figsize=(7, 4), legend=False, title=title)
        plt.axis('off')
    plt.tight_layout()
    chart = get_graph()
    return chart


def get_table(df):
    css_classes = "table table_dark table-sm table-responsive"
    table_id = "results"
    row_count = len(df.index)
    if row_count == 0:
        columns = list(df.columns.values)
        table = f"<table id={table_id} class='{css_classes}'"
        for column in columns:
            table += f"<tr><td>{column}</td></tr>"
        table += "</table>"
        return table
    else:
        return df.to_html(classes=[css_classes],
                          table_id=table_id,
                          index=False)


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
