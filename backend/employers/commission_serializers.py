from rest_framework import serializers
from .commission_models import Commission, CommissionInvoice, CommissionRefund


class CommissionSerializer(serializers.ModelSerializer):
    amount_pounds = serializers.SerializerMethodField()
    candidate_email = serializers.CharField(source='hire_confirmation.application.candidate.user.email', read_only=True)
    job_title = serializers.CharField(source='hire_confirmation.application.job.title', read_only=True)

    class Meta:
        model = Commission
        fields = [
            'id', 'hire_confirmation', 'employer', 'amount_gbp', 'amount_pounds', 
            'status', 'candidate_email', 'job_title',
            'confirmed_at', 'invoiced_at', 'paid_at', 'refunded_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'confirmed_at', 'invoiced_at', 'paid_at', 'refunded_at', 'created_at'
        ]

    def get_amount_pounds(self, obj):
        return obj.amount_pounds


class CommissionInvoiceSerializer(serializers.ModelSerializer):
    total_amount_pounds = serializers.SerializerMethodField()
    commission_count = serializers.SerializerMethodField()

    class Meta:
        model = CommissionInvoice
        fields = [
            'id', 'employer', 'status', 'invoice_month', 'total_amount_gbp', 'total_amount_pounds',
            'commission_count', 'invoice_date', 'sent_at', 'due_date', 'paid_at',
            'payment_method', 'payment_reference', 'created_at'
        ]
        read_only_fields = [
            'id', 'total_amount_gbp', 'invoice_date', 'created_at'
        ]

    def get_total_amount_pounds(self, obj):
        return obj.total_amount_pounds

    def get_commission_count(self, obj):
        return obj.commissions.count()


class CommissionRefundSerializer(serializers.ModelSerializer):
    commission_amount_pounds = serializers.SerializerMethodField()

    class Meta:
        model = CommissionRefund
        fields = [
            'id', 'commission', 'status', 'reason', 'reason_detail', 'evidence',
            'commission_amount_pounds', 'requested_at', 'processed_at', 'created_at'
        ]
        read_only_fields = [
            'id', 'status', 'requested_at', 'processed_at', 'created_at'
        ]

    def get_commission_amount_pounds(self, obj):
        return obj.commission.amount_pounds
