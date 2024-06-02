# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
import json
from ToolTrackApp.Borrow.models import Item
from ToolTrackApp.Room.models import Room

@csrf_exempt
@require_http_methods(["POST"])
def update_item(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        room_id = data.get('roomId')

        if not name:
            return JsonResponse({'message': 'Name is required'}, status=400)
        if not room_id:
            return JsonResponse({'message': 'Room ID is required'}, status=400)

        # Get the room object
        new_room = get_object_or_404(Room, number=room_id)

        # Get all items with the specified name
        items = Item.objects.filter(name=name)

        if not items.exists(): 
            return JsonResponse({'message': 'No items found with the specified name'}, status=404)

        # Update the room(desired)
        for item in items:
            # Remove item from its current rooms. because We change roomId
            # in room models.py -> manyTomanyField name is rooms 

            item.rooms.clear()
            
            # Update the roomId for our desired room_id
            item.roomId = room_id
            item.save()

            # Add items in Room model(new room)

            new_room.items.add(item)

        new_room.save()

        return JsonResponse({'message': f'{items.count()} items updated successfully'}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)