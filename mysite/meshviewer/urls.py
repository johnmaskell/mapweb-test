from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^meshviewer/',views.model_form_upload,name='model_form_upload'),

]
