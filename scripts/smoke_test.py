"""Small script to verify DB and model operations without running server.

Usage: python scripts/smoke_test.py
"""
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Make sure project root is on sys.path so `oddo_project` is importable
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oddo_project.settings')
django.setup()

from api.models import Item

def main():
    print('Item count before:', Item.objects.count())
    item = Item.objects.create(name='Smoke item', description='Created by smoke_test')
    print('Created item id:', item.id)
    print('Item count after:', Item.objects.count())

if __name__ == '__main__':
    main()
