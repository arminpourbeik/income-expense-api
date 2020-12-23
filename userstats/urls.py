from django.urls import path

from . import views

urlpatterns = [
    path(
        "expense-category-data/",
        view=views.ExpenseSummaryStats.as_view(),
        name="expense-category-data",
    ),
    path(
        "income-source-data/",
        view=views.IncomeSourceSummaryStats.as_view(),
        name="income-source-data",
    ),
]