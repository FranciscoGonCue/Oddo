from rest_framework import serializers

# La app 'api' se mantiene vacía
# Todos los serializers han sido movidos a apps específicas:
# - core.serializers: PartnerSerializer, ProductSerializer
# - purchases.serializers: PurchaseOrderSerializer, PurchaseOrderLineSerializer
# - inventory.serializers: WarehouseSerializer, StockQuantSerializer
# - pos.serializers: PosOrderSerializer, PosOrderLineSerializer
# - invoicing.serializers: InvoiceSerializer, PaymentSerializer
# - hr.serializers: EmployeeSerializer
