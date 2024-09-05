from apps.core import generics
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView
from apps.transaction.models import Transaction
from apps.transaction.serializers import TransactionSerializers,TransactionInputSerializers
from rest_framework.response import Response
from apps.transaction.usecases import ListTransactionUseCase,AddTransactionUseCase
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.transaction.utils import generate_pdf_from_html
from django.http import HttpResponse
from apps.users.permission import IsManagerUser,IsManagerOrStaffUser


class TransactionApi(APIView):
    def get_permissions(self):
        """
        Dynamically apply permissions based on the request method.
        """
        if self.request.method in ['GET', 'PUT','PATCH']:
            # Apply permission for GET and POST methods
            return [IsManagerOrStaffUser()]
        # No permissions for DELETE (allow anyone)
        return [IsManagerUser()]

    def get(self, request, txnid, *args, **kwargs):
        try:
            obj = Transaction.objects.get(pk=txnid)
            serializer = TransactionSerializers(obj)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, txnid, *args, **kwargs):
        try:
            obj = Transaction.objects.get(pk=txnid)
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Transaction.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_description="This is update section where you can update transaction data",
                         request_body=TransactionInputSerializers)
    def put(self, request, txnid, *args, **kwargs):
        try:
            obj = Transaction.objects.get(pk=txnid)
            serializer = TransactionInputSerializers(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(operation_description="This is update section where you can update transaction data",
                         request_body=TransactionInputSerializers)
    def patch(self, request, txnid, *args, **kwargs):
        try:
            obj = Transaction.objects.get(pk=txnid)
            serializer = TransactionInputSerializers(obj, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class TransactionCreate(generics.CreateWithMessageAPIView):
    """
    Use this end-point to add transaction
    """
    serializer_class = TransactionInputSerializers
    message = 'Created successfully'
    permission_classes = [IsManagerOrStaffUser]

    def perform_create(self, serializer):
        return AddTransactionUseCase(serializer=serializer).execute()

class TransactionList(generics.ListAPIView):
    serializer_class = TransactionSerializers
    no_content_error_message = _('No transaction at the moment')
    permission_classes = [IsManagerOrStaffUser]
    def get_queryset(self):
        return ListTransactionUseCase().execute()


class TransactionPDFView(APIView):
    permission_classes = [IsManagerUser]
    def get(self, request,txnid, *args, **kwargs):
        try:
            data = Transaction.objects.get(pk=txnid)
            context = {
                    'items': data
                }
            pdf = generate_pdf_from_html(context,'single_transaction_pdf.html')
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sample.pdf"'
            return response
        except Transaction.DoesNotExist:
            return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)


class TransactionListPDFView(APIView):
    permission_classes = [IsManagerUser]
    def get(self, request, *args, **kwargs):
        data = Transaction.objects.all()
        context = {
            'items': data
        }
        pdf = generate_pdf_from_html(context,'pdf_template.html')
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sample.pdf"'
        return response