from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Item
from ToolTrackApp.Student.models import Student

def borrow_item(request):
    if request.method == 'GET':
        # //Item's id(pk)
        Item_id = request.GET.get('id')   
        student_id = request.GET.get('studentId')
        # //In swagger, I guess holderId means roomId. Anyway It should represent room_id
        room_id = request.GET.get('holderId')

        # Get the item and student objects
        item = get_object_or_404(Item, id=Item_id)
        student = get_object_or_404(Student, studentId=student_id)

     # Check if the item is available for borrowing
        if item.available and item.quantity > 0:
            # Update item status
            item.quantity -= 1 
            item.holderId = student.id
            item.update_availability()  # Update availability based on the new quantity
            item.save()

            return JsonResponse({'message': 'Item borrowed successfully'}, status=200)
        else:
            return JsonResponse({'message': 'Item not available'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)