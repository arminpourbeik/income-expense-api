from rest_framework import serializers

from incomes.models import Income


class IncomeSerializer(serializers.ModelSerializer):
    """
    Serializer for income instance
    """

    # owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Income
        fields = (
            "id",
            "date",
            "description",
            "amount",
            "source",
        )
