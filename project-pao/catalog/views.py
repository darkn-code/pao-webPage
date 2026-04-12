from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import get_catalog_all, group_by_category
from .services import get_catalog_all, save_products_to_db
from rest_framework.decorators import api_view
from .models import Product

@api_view(['GET'])
def get_products_grouped(request):
    products = get_catalog_all()
    grouped = group_by_category(products)
    return Response(grouped)

@api_view(['GET'])
def get_products_db(request):
    products = Product.objects.all()

    data = {}

    for p in products:
        data.setdefault(p.category, []).append({
            "sku": p.sku,
            "name": p.name,
            "price": p.price,
            "image": p.image,
            "color": p.color,
        })

    return Response(data)

@api_view(['GET'])
def sync_products(request):
    products = get_catalog_all()
    save_products_to_db(products)

    return Response({"message": "Productos sincronizados"})