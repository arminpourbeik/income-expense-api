from rest_framework import generics
from rest_framework import permissions

from incomes import serializers
from incomes.permissions import IsOwner
from incomes.models import Income


class IncomeListView(generics.ListCreateAPIView):
    """
    View for listing and creating income
    """

    serializer_class = serializers.IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for an income instance, updating, deleting
    """

    serializer_class = serializers.IncomeSerializer
    queryset = Income.objects.all()
    lookup_field = "id"
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
