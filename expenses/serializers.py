from rest_framework import serializers

from expenses.models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Seializer for expense instance
    #"""

    # owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Expense
        fields = (
            "date",
            "description",
            "amount",
            "category",
        )
