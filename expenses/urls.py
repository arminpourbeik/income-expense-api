from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.ExpenseListView.as_view(), name="expenses-list"),
    path("<int:id>", view=views.ExpenseDetailView.as_view(), name="expenses-detail"),
]
