from rest_framework import generics
from rest_framework import permissions

from expenses import serializers
from expenses.permissions import IsOwner
from expenses.models import Expense
from expenses.renderers import ExpenseRenderers


class ExpenseListView(generics.ListCreateAPIView):
    """
    View for listing and creating expense
    """

    serializer_class = serializers.ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (ExpenseRenderers,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for an expense instance, updating, deleting
    """

    serializer_class = serializers.ExpenseSerializer
    queryset = Expense.objects.all()
    lookup_field = "id"
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
