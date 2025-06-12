
#? Import necessary modules
from django.views.generic import TemplateView

#? IssueListView
class IssueListView(TemplateView):
    template_name = 'issues/issues_list.html'      #* Template for the issues list page