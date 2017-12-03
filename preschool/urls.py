"""preschool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from management.views import (MainView, ChildrenListView, GroupView, GroupListView, 
                        ChildView, AddChildView, PresenceDateView, PresenceListView, 
                        HoursAndMealsView, TeachersView, AddTeacherView)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name="main"),
    url(r'^children/$', ChildrenListView.as_view(), name="children"),
    url(r'^group/$', GroupView.as_view(), name="group"),
    url(r'^group/(?P<group_id>(\d)+)$', GroupListView.as_view(), name="group_list"),
    url(r'^group/(?P<group_id>(\d)+)/(?P<child_id>(\d)+)', ChildView.as_view(), name="child"),
    url(r'^group/(?P<group_id>(\d)+)/add_child', AddChildView.as_view(), name="add_child"),
    url(r'^group/(?P<group_id>(\d)+)/presence_date', PresenceDateView.as_view(), name="presence_date"),
    url(r'^group/(?P<group_id>(\d)+)/presence_list/(?P<date>(\d{4}-\d{2}-\d{2}))', 
        PresenceListView.as_view(), name="presence_list"),
    url(r'^group/(?P<group_id>(\d)+)/presence_list/(?P<date>(\d{4}-\d{2}-\d{2}))/hours_and_meals', 
        HoursAndMealsView.as_view(), name="hours_and_meals"),
    url(r'^teachers/$', TeachersView.as_view(), name="teachers"),
    url(r'^teachers/add$', AddTeacherView.as_view(), name="add_teachers"),
]

