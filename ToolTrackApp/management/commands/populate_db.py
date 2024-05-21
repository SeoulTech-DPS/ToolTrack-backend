from django.core.management.base import BaseCommand
from ToolTrackApp.Student.models import Student
from ToolTrackApp.Borrow.models import Item
from ToolTrackApp.Room.models import Room

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        # Add items
        items = [
            Item(name='Item1'),
            Item(name='Item2'),
            Item(name='Item3')
        ]
        Item.objects.bulk_create(items)

        # Add rooms
        rooms = [
            Room(name='Room1'),
            Room(name='Room2')
        ]
        Room.objects.bulk_create(rooms)

        # Link items and rooms
        room1 = Room.objects.get(name='Room1')
        room2 = Room.objects.get(name='Room2')
        item1 = Item.objects.get(name='Item1')
        item2 = Item.objects.get(name='Item2')
        item3 = Item.objects.get(name='Item3')

        room1.items.add(item1, item2, item3)

        # Add students
        students = [
            Student(studentId='S001', name='Student1', username='student1', password='pass1', isAdmin=True),
            Student(studentId='S002', name='Student2', username='student2', password='pass2', isAdmin=False)
        ]
        Student.objects.bulk_create(students)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
