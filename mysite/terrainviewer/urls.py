from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^terrainviewer/',views.user_map,name='user_map'),

]
