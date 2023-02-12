import re

import openai
import sqlparse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from queries.common.access import get_users_most_recent_database
from queries.common.database import get_column_list
from queries.forms import QueryAiCreateForm
from queries.models import Query
from qwaver.settings import config


@login_required
def query_ai_create(request):
    if request.method == 'POST':
        form = QueryAiCreateForm(request.POST)
        if form.is_valid():
            tables = split_string(form.cleaned_data['tables'])
            description = form.cleaned_data['description']
            user = request.user
            database = get_users_most_recent_database(user)
            prompt = f"{database.platform} tables (and columns):"
            for table in tables:
                columns = get_column_list(
                    database=database,
                    user=user,
                    table=table
                )
                if columns is None:
                    messages.warning(request, f"No columns in table {table}")
                else:
                    table_def = f"{table}({', '.join(columns)})"
                    prompt += f"\n* {table_def}"
            prompt += "\n"
            prompt += f"A well-written SQL query that finds: {description}:"
            prompt += f"```"
            openai.api_key = config.get('config', 'OPENAI_API_KEY')
            response = openai.Completion.create(
                model="code-davinci-002",
                prompt=prompt,
                temperature=0,
                max_tokens=256,
                stop="```"
            )
            # TODO inspect response for errors and handle
            query_text = response.choices[0].text
            # pretty formatting of the returned query
            pretty_query_text = sqlparse.format(query_text, reindent=True).strip()
            query = Query(
                title=description,
                database=database,
                query=pretty_query_text,
                author=user
            )
            query.save()
            return redirect('query-update', pk=query.id)
        else:
            messages.error(request, "Form invalid")
            return redirect(reverse('query-ai-create'))
    else:
        context = {
            'form': QueryAiCreateForm(),
            'title': 'Create Query with AI',
            'submit_text': '🤖 Create'
        }
        return render(request, "queries/generic_form.html", context)


def split_string(string):
    # Split the string by either a comma or a space
    split_list = [word for word in re.split(',| ', string) if word]

    return split_list