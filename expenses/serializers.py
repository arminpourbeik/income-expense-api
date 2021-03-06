from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for expense instance
    """

    # owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Expense
        fields = (
            "id",
            "date",
            "description",
            "amount",
            "category",
        )
