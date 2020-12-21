from django.urls import path

from . import views

urlpatterns = [
    path("", views.IncomeListView.as_view(), name="incomes"),
    path("<int:id>", views.IncomeDetailView.as_view(), name="incomes-detail"),
]