from django.urls import path
from . import views

queue_api_urlpatterns = [
   path('queues/create/', views.QueueCreateAPIView.as_view(), name='queue_creation'),
   path('queues/<int:queue_id>/', views.QueueInfoAPIView.as_view(), name='queue_info'),
   path('queues/<int:queue_id>/add_waiter/', views.QueueAddWaiterAPIView.as_view(), name='queue_add_waiter'),
   path('queues/<int:queue_id>/process_waiter/<int:waiter_id>/', views.QueueProcessWaiterAPIView.as_view(), name='queue_process_waiter'),
   path('queues/<int:queue_id>/process_next_waiter/', views.QueueProcessNextWaiterAPIView.as_view(), name='queue_process_next_waiter'),
   path('queues/<int:queue_id>/finish_processing_waiter/<int:waiter_id>/', views.QueueFinishProcessingWaiterAPIView.as_view(), name='queue_finish_processing_waiter'),
   path('queues/<int:queue_id>/expected_waiting_time/', views.QueueExpectedWaitingTimeAPIView.as_view(), name='queue_expected_waiting_time'),
   path('queues/<int:queue_id>/expected_waiting_time/<int:waiter_id>/', views.QueueWaiterExpectedWaitingTimeAPIView.as_view(), name='queue_waiter_expected_waiting_time'),
   path('queues/<int:queue_id>/expected_processing_time/', views.QueueExpectedProcessingTimeAPIView.as_view(), name='queue_expected_processing_time'),
]