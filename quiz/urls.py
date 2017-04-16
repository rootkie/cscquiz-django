from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>\d+)/answer$', views.answer, name='answer'),
    url(r'^(?P<question_id>\d+)/score$', views.scoring, name='score'),
    url(r'^reset/questions$', views.reset_questions, name='reset questions'),
    url(r'^reset/scores$', views.reset_scores, name='reset scores'),
    url(r'^activeset/generate$', views.createSet, name='gen active'),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)