from rest_framework import viewsets

# La app 'api' se mantiene vacía
# Todos los viewsets han sido movidos a apps específicas:
# - core.views: PartnerViewSet, ProductViewSet
# - purchases.views: PurchaseOrderViewSet, PurchaseOrderLineViewSet
# - inventory.views: WarehouseViewSet, StockQuantViewSet
# - pos.views: PosOrderViewSet, PosOrderLineViewSet
# - invoicing.views: InvoiceViewSet, PaymentViewSet
# - hr.views: EmployeeViewSet
