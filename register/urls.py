from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'register',views.register, name='register'),
    url(r'update',views.update, name='update'),
    url(r'revoke',views.revoke, name='revoke'),
]
