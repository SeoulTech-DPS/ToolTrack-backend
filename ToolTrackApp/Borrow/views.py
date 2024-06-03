from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Item
from ToolTrackApp.Student.models import Student
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_GET
import json


@csrf_exempt
@require_http_methods(["POST"])
def borrow_item(request):
    try:
        data = json.loads(request.body)
        student_id = data.get('studentId')
        room_id = data.get('roomId')
        item_name = data.get('itemName')
        # Get the student object
        student = get_object_or_404(Student, studentId=student_id)
        # Get the list of items with the same name that are available
        items = Item.objects.filter(name=item_name, roomId=room_id, holderId=0, available=True)
        if items.exists():
            # Borrow the first available item
            item = items.first()
            item.holderId = student_id
            item.available = False
            item.save()
            return JsonResponse({
                'message': 'Item borrowed successfully',
                'item': {
                    'id': item.id,
                    'name': item.name,
                    'available': item.available,
                    'holderId': item.holderId,
                    'roomId': item.roomId,
                }
            }, status=200)
        else:
            return JsonResponse({'message': 'Item not available'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

    


@require_GET
@csrf_exempt
def get_items_by_room(request):
    room_id = request.GET.get('roomId')
    if room_id is None:
        return JsonResponse({'error': 'roomId parameter is required'}, status=400)

    items = Item.objects.filter(roomId=room_id, holderId=0)
    items_count = {}

    for item in items:
        if item.name in items_count:
            items_count[item.name] += 1
        else:
            items_count[item.name] = 1

    items_list = [{'name': name, 'amount': amount} for name, amount in items_count.items()]

    return JsonResponse(items_list, safe=False)