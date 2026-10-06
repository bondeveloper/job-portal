from rest_framework import serializers
from .payment_models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    invoice_number = serializers.CharField(source='invoice.invoice_number', read_only=True)
    employer_name = serializers.CharField(source='invoice.employer.name', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'invoice_number', 'employer_name', 'amount', 'status', 'payment_method',
                  'payment_reference', 'payment_url', 'created_at', 'completed_at']
        read_only_fields = ['id', 'invoice_number', 'employer_name', 'amount', 'status', 'payment_method',
                           'payment_reference', 'payment_url', 'created_at', 'completed_at']


class PaymentInitiateSerializer(serializers.Serializer):
    payment_method = serializers.ChoiceField(choices=['bank_transfer', 'credit_card', 'paycloud_balance'])
