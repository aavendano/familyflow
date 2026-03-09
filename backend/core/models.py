from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class FamilyGroup(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_memberships')
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'family')

class CalendarConnection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='calendar_connection')
    provider = models.CharField(max_length=50, default='google')
    access_token = models.TextField()
    refresh_token = models.TextField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Event(models.Model):
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='events')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True, null=True)
    is_all_day = models.BooleanField(default=False)
    google_event_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class EventReminder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders')
    minutes_before = models.IntegerField()
    method = models.CharField(max_length=20, choices=(('email', 'Email'), ('popup', 'Popup')))

class EventAttachment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments')
    file_url = models.URLField()
    filename = models.CharField(max_length=255)

class EventResponse(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='responses')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=(('accepted', 'Accepted'), ('declined', 'Declined'), ('tentative', 'Tentative')))

class Activity(models.Model):
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='activities')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='activities')
    action = models.CharField(max_length=255)
    entity_type = models.CharField(max_length=50) # 'Event', 'Task', 'Grocery', etc.
    entity_id = models.IntegerField(null=True, blank=True)
    details = models.JSONField(default=dict, blank=True)
    trace_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_entity_type = models.CharField(max_length=50, blank=True, null=True)
    related_entity_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class GroceryList(models.Model):
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='grocery_lists')
    name = models.CharField(max_length=255, default="Main List")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class GroceryItem(models.Model):
    list = models.ForeignKey(GroceryList, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=50, blank=True, null=True)
    is_purchased = models.BooleanField(default=False)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TodoList(models.Model):
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='todo_lists')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class TodoTask(models.Model):
    list = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(blank=True, null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomList(models.Model):
    family = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='custom_lists')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CustomListItem(models.Model):
    list = models.ForeignKey(CustomList, on_delete=models.CASCADE, related_name='items')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
