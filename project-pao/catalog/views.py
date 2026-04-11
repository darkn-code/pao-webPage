from rest_framework.decorators import api_view
from rest_framework.response import Response
from .services import get_catalog_all, group_by_category

@api_view(['GET'])
def get_products_grouped(request):
    products = get_catalog_all()
    grouped = group_by_category(products)
    return Response(grouped)