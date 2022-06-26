from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import (
    UpdateView
)

from queries.models import Parameter
from queries.common.access import user_can_access_query


class ParameterEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Parameter
    fields = ['name', 'default', 'template']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParameterEditView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Update"
        context['query'] = self.object.query
        return context

    def get_success_url(self):
        return reverse('query-detail', args=[self.object.query.id])

    def test_func(self):
        return True

    def test_func(self):
        user = self.request.user
        query = self.get_object().query
        user_can_access_query(user, query)
        return True
