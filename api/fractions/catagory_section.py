from django.shortcuts import get_object_or_404
from ..serializer import CatagorySerializer
from django.db.utils import IntegrityError
from django.http import JsonResponse
from ..models import Category
import json


# ======================
# ===== Add Catagory
# ======================
def AddCatagory(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)

        name = data.get('name')
        unit = data.get('unit')
        catagory = Category.objects.create(name=name, unit=unit)
        catagory.save()
        
        return JsonResponse({'message': 'Catagory registered successfully.'}, status=201)

    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

# ======================
# ===== View Catagory
# ======================
def ViewCatagory(request):
    catagory = Category.objects.all().order_by('-id')
    serializer = CatagorySerializer(catagory, many=True)
    return JsonResponse(serializer.data, safe=False)

# =======================
# ===== Delete Catagory
# =======================
def DeleteCatagory(request, pk):
    catagory = get_object_or_404(Category, pk=pk)
    try:
        catagory.delete()
    except IntegrityError:
        return JsonResponse({'message': "Can't delete this Catagory"}, status=201)

    return JsonResponse({'message': 'Removed Catagory from database.'}, status=201)
