from rest_framework import serializers
from .invoice_models import Invoice, InvoiceLineItem


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    commission_id = serializers.IntegerField(source='commission.id', read_only=True)
    candidate_name = serializers.SerializerMethodField(read_only=True)
    job_title = serializers.CharField(source='commission.hire_confirmation.application.job.title', read_only=True)

    class Meta:
        model = InvoiceLineItem
        fields = ['id', 'commission_id', 'candidate_name', 'job_title', 'description', 'amount', 'created_at']
        read_only_fields = ['id', 'commission_id', 'created_at']

    def get_candidate_name(self, obj):
        candidate = obj.commission.hire_confirmation.application.candidate
        return f"{candidate.first_name} {candidate.last_name}"


class InvoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'total_amount', 'status', 'date_issued', 'due_date', 'paid_at']
        read_only_fields = ['id', 'invoice_number', 'date_issued', 'due_date', 'paid_at']


class InvoiceDetailSerializer(serializers.ModelSerializer):
    line_items = InvoiceLineItemSerializer(many=True, read_only=True)
    employer_name = serializers.CharField(source='employer.name', read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'employer_name', 'total_amount', 'status', 'date_issued', 'due_date',
                  'paid_at', 'line_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'invoice_number', 'employer_name', 'total_amount', 'status', 'date_issued',
                           'due_date', 'paid_at', 'line_items', 'created_at', 'updated_at']
