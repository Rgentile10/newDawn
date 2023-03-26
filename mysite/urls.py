"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# The path() function is passed four arguments, two required: route and view, and two optional: kwargs, and name. At this point, it’s worth reviewing what these arguments are for.
urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]


# ^^ the purpose above is to point the root URLconf at the polls.urls module. In mysite/urls.py, add an import for django.urls.include and insert an include() in the urlpatterns list, so you have:
# Go to http://localhost:8000/polls/ in your browser, and you should see the text “Hello, world. You’re at the polls index.”, which you defined in the index view.

# Patterns don’t search GET and POST parameters, or the domain name. For example, in a request to https://www.example.com/myapp/, the URLconf will look for myapp/. In a request to https://www.example.com/myapp/?page=3, the URLconf will also look for myapp/.
