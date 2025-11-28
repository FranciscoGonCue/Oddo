from django.db import models

# La app 'api' se mantiene vacía
# Todos los modelos han sido movidos a apps específicas:
# - core: Partner, Product
# - purchases: PurchaseOrder, PurchaseOrderLine
# - inventory: Warehouse, StockQuant
# - pos: PosOrder, PosOrderLine
# - invoicing: Invoice, Payment
# - hr: Employee
