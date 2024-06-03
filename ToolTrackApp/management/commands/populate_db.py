from django.core.management.base import BaseCommand
from ToolTrackApp.Student.models import Student
from ToolTrackApp.Borrow.models import Item
from ToolTrackApp.Room.models import Room

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):

        Student.objects.all().delete()
        Item.objects.all().delete()
        Room.objects.all().delete() 

        # Add items
        items = [
            Item(name='Calculator', roomId=502),
            Item(name='Blanket', roomId=502),
            Item(name='Medicine', roomId=502),
            Item(name="Earphone"),
            Item(name='Ruler'),
            Item(name='Tissue'),
        ]
        Item.objects.bulk_create(items)

        # Add rooms
        rooms = [
            Room(name='Room 302', number=302),
            Room(name='Room 502', number=502)
        ]
        Room.objects.bulk_create(rooms)

        # Link items and rooms
        room1 = Room.objects.get(name='Room 302')
        room2 = Room.objects.get(name='Room 502')

        item1 = Item.objects.get(name='Calculator')
        item2 = Item.objects.get(name='Blanket')
        item3 = Item.objects.get(name='Medicine')
        item4 = Item.objects.get(name="Earphone")
        item5 = Item.objects.get(name='Ruler')
        item6 = Item.objects.get(name="Tissue")

        room1.items.add(item4, item5, item6)
        room2.items.add(item1, item2, item3)
        # Add students
        students = [
            Student(studentId='23019810', name='John Smith', password='pass1', isAdmin=True),
            Student(studentId='20019801', name='김민수', password='pass2', isAdmin=False)
        ]
        Student.objects.bulk_create(students)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
