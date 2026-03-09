import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from core.models import User, FamilyGroup, FamilyMember, Event, TodoList, TodoTask, GroceryList, GroceryItem, Activity

class Command(BaseCommand):
    help = 'Seeds the database with initial FamilyFlow data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        family, created = FamilyGroup.objects.get_or_create(name="The Smiths")
        if not created:
            self.stdout.write(self.style.WARNING('Family already exists. Skipping seed.'))
            return

        users_data = [
            {'username': 'john', 'email': 'john@smith.com', 'role': 'admin', 'first': 'John'},
            {'username': 'jane', 'email': 'jane@smith.com', 'role': 'admin', 'first': 'Jane'},
            {'username': 'timmy', 'email': 'timmy@smith.com', 'role': 'member', 'first': 'Timmy'},
        ]

        users = []
        for u_data in users_data:
            user, _ = User.objects.get_or_create(username=u_data['username'], email=u_data['email'])
            user.set_password('password123')
            user.first_name = u_data['first']
            user.save()
            users.append(user)
            FamilyMember.objects.create(user=user, family=family, role=u_data['role'])

        now = datetime.now()
        events_data = [
            ("Family Dinner", now + timedelta(hours=2), now + timedelta(hours=4), "Home"),
            ("Timmy's Soccer Match", now + timedelta(days=1, hours=10), now + timedelta(days=1, hours=12), "Local Park"),
        ]

        for title, start, end, loc in events_data:
            event = Event.objects.create(
                family=family,
                creator=random.choice(users[:2]),
                title=title,
                start_time=make_aware(start),
                end_time=make_aware(end),
                location=loc
            )
            Activity.objects.create(
                family=family,
                actor=event.creator,
                action=f"created event '{title}'",
                entity_type='Event',
                entity_id=event.id
            )

        todo_list = TodoList.objects.create(family=family, name="Weekend Chores")
        tasks_data = [("Mow the lawn", True), ("Clean the garage", False), ("Wash the car", False)]

        for task_title, is_completed in tasks_data:
            task = TodoTask.objects.create(
                list=todo_list,
                title=task_title,
                assignee=random.choice(users),
                is_completed=is_completed,
                due_date=make_aware(now + timedelta(days=random.randint(1, 3)))
            )
            if is_completed:
                 Activity.objects.create(
                    family=family,
                    actor=task.assignee,
                    action=f"completed task '{task_title}'",
                    entity_type='Task',
                    entity_id=task.id
                )

        grocery_list = GroceryList.objects.create(family=family, name="Weekly Groceries")
        GroceryItem.objects.create(list=grocery_list, name="Milk", quantity="1 gallon", added_by=users[2])
        Activity.objects.create(
            family=family,
            actor=users[2],
            action=f"added Milk to groceries",
            entity_type='Grocery',
        )

        self.stdout.write(self.style.SUCCESS('Database successfully seeded!'))
