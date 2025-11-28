from django.contrib import admin

# La app 'api' se mantiene vacía
# Todos los modelos admin han sido movidos a apps específicas:
# - core.admin: PartnerAdmin, ProductAdmin
# - purchases.admin: PurchaseOrderAdmin, PurchaseOrderLineAdmin
# - inventory.admin: WarehouseAdmin, StockQuantAdmin
# - pos.admin: PosOrderAdmin, PosOrderLineAdmin
# - invoicing.admin: InvoiceAdmin, PaymentAdmin
# - hr.admin: EmployeeAdmin