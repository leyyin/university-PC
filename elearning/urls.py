"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
import django.contrib.auth.views as auth_views
from django.conf.urls import include, url
from django.contrib import admin

from . import views
from .course import views as course_views
urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),

    # See https://docs.djangoproject.com/en/1.8/topics/auth/default/#module-django.contrib.auth.views
    # url(r'^', include('django.contrib.auth.urls')),
    url(r'^login/', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/', auth_views.logout, {'template_name': 'registration/logout.html'}, name='logout'),

    # /admin
    url(r'^admin/', include(admin.site.urls)),
    # /course
    url(r'^course/add-course/', course_views.add_course, name='add_course'),
    url(r'^course/see-courses/', course_views.see_courses, name='see_courses'),
    url(r'^course/see-assignments/(?P<id>[-\w]+)/$', course_views.see_assignments, name='see_assignments'),
    url(r'^course/add-assignment/(?P<id>[-\w]+)/$', course_views.add_assignment, name='add_assignment'),
    url(r'^course/give_assignment_to_students/([-\w]+)/$', course_views.give_assignment_to_students, name="give_assignment_to_students"),
    url(r'^course/give_assignment_to_groups/([-\w]+)/$', course_views.give_assignment_to_groups, name="give_assignment_to_groups")
]
