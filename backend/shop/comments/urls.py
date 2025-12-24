from django.urls import path
from django.urls import register_converter

from shop.comments import views

shop_comments_endpoint_prefix = "shop_comments_"

from shop.comments.converters import NegativeIntegerConverter
register_converter(NegativeIntegerConverter, 'negint')

urlpatterns = [
    path('vote-comment/<int:comment_id>/<str:action>/', views.vote_comment, name='vote_comment'),
    path('get-comment/<int:comment_id>/', views.get_comment, name='get_comment'),
    path('reject-comment/<int:comment_id>/', views.reject_comment, name='reject_comment'),
    path('approve-comment/<int:comment_id>/', views.approve_comment, name='approve_comment'),
    path('list/<negint:status>/', views.load_comments, name='load_comments'),
    path('list/non-js/<negint:status>/', views.load_comments, name='comments_list'),
    path('', views.IndexView.as_view(), name='comments_index'),
]

for endpoint in urlpatterns:
    endpoint.name = shop_comments_endpoint_prefix + endpoint.name