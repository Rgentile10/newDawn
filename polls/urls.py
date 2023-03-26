from django.urls import path

from .import views

# The tutorial project has just one app, polls. In real Django projects, there might be five, ten, twenty apps or more. How does Django differentiate the URL names between them?
# For example, the polls app has a detail view, and so might an app on the same project that is for a blog. How does one make it so that Django knows which app view to create for a url when using the {% url %} template tag?

# The answer is to add namespaces to your URLconf. In the polls/urls.py file, go ahead and add an app_name to set the application namespace:

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# no we have a wired indec view into the URLconf

# verify working: >> py manage.py runserver

# Next step is tp point the root URLconf at the polls.urls module.
# so we add the following
