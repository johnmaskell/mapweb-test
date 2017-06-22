from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^runtide/',views.display_map,name='display_map'),    
    url(r'^runtide/',views.display_map,name='display_map'),
    url(r'^model_parameters/',views.model_parameters,name='model_parameters'),

]
