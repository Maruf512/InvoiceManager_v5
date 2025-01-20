from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..models import Category, Product
from ..serializer import ProductsSerializer
import json


# =======================
# ===== Add Products
# =======================
def AddProducts(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        name = data.get('name')
        rate = data.get('rate')
        catagory_id = data.get('category')
        production_cost = data.get('production_cost')
        other_cost = data.get('other_cost')

        category = get_object_or_404(Category, pk=catagory_id)

        products = Product.objects.create(name=name, rate=rate, category=category, production_cost=production_cost, other_cost=other_cost)
        products.save()
        
        return JsonResponse({'message': 'Products added successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)


# =======================
# ===== View Products
# =======================
def ViewProducts(request, pk):
    data = []
    if pk > 0:
        query = Product.objects.all().order_by('-id')
        limit = 10
        offset = (pk - 1) * limit
        number_of_pages = len(query)/limit
        if offset + limit > len(query):
            to_value = offset + (len(query) - offset)
        else:
            to_value = offset + limit

        filter_records = query[offset:to_value]
        if isinstance(number_of_pages, float):
            number_of_pages = int(number_of_pages) + 1
        
        for i in filter_records:
            catagory_name = get_object_or_404(Category, pk=i.category.id)
            data.append({'id': i.id, 'name': i.name, 'category':catagory_name.name, 'rate': i.rate, 'production_cost':i.production_cost, 'other_cost':i.other_cost})

        return JsonResponse([{"total_page": number_of_pages}] + data, safe=False)


# =======================
# ===== Update Products
# =======================

def UpdateProducts(request, pk):
    products = get_object_or_404(Product, pk=pk)
    serializer = ProductsSerializer(products, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# def UpdateProducts(request):
#
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
#     # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
#
#         print(data)
#         pk = data.get('pk')
#         print(f"pk {pk}")
#         updateAll = data.get('updateAll')
#
#         products = get_object_or_404(Product, pk=pk)
#
#         if updateAll == True:
#     #         update all
#             print(f"updateAll {updateAll}")
#             pass
#         else:
#             # single update
#             print(f"updateAll {updateAll}")
#             pass
#
#         print(f"id: {products.id}, name: {products.name}, rate: {products.rate}, production_cost: {products.production_cost}, other_cost: {products.other_cost}, category: {products.category}")
#
#
#         rate = data.get('rate')
#         production_cost = data.get('production_cost')
#         products.production_cost = production_cost
#         products.rate = rate
#         products.save()
#         print("++++++++++++++ Updated +++++++++++++++++")
#         print(f"id: {products.id}, name: {products.name}, rate: {products.rate}, production_cost: {products.production_cost}, other_cost: {products.other_cost}, category: {products.category}")
#
#
#         return JsonResponse( {'messagge': "done"} ,status=200)
#
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)


# =======================
# ===== Delete Products
# =======================
def DeleteProducts(request, pk):
    products = get_object_or_404(Product, pk=pk)
    try:
        products.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Product"}, status=201)
    
    return JsonResponse({'message': 'Removed Products from database.'}, status=201)
