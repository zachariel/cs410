from django.conf.urls import url

from . import views

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'jobs', views.JobViewSet)

#urlpatterns = [
#        url(r'^$', views.index, name='index'),
#]
urlpatterns = router.urls
