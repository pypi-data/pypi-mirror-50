from django.urls import path
from contact.views import ContactView

app_name = 'contact'

urlpatterns = [
    # contact app url
    path('contact/', ContactView.as_view(), name="contact"),
]
