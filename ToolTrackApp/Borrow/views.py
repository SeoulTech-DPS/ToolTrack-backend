from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Item
from ToolTrackApp.Student.models import Student

def borrow_item(request):
    if request.method == 'GET':
        # //Item's id(pk)
        item_id = request.GET.get('itemId')   
        student_id = request.GET.get('studentId')
        # //In swagger, I guess holderId means roomId. Anyway It should represent room_id
        room_id = request.GET.get('roomId')

        # Get the item and student objects
        item = get_object_or_404(Item, id=item_id)
        student = get_object_or_404(Student, studentId=student_id)

        # Count items by primary key 'id'
        quantity = Item.objects.filter(id=item_id).count()
     
        # Check if the item is available for borrowing
        if item.available and quantity > 0:
            # Update item status
            item.holderId = student_id
            item.available = False
            item.save()

            return JsonResponse({'message': 'Item borrowed successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Item not available'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
