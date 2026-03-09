from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, FamilyGroup, FamilyMember, CalendarConnection,
    Event, EventReminder, EventAttachment, EventResponse,
    Activity, Notification, GroceryList, GroceryItem,
    TodoList, TodoTask, CustomList, CustomListItem
)

admin.site.register(User, UserAdmin)
admin.site.register(FamilyGroup)
admin.site.register(FamilyMember)
admin.site.register(Event)
admin.site.register(Activity)
admin.site.register(TodoList)
admin.site.register(TodoTask)
admin.site.register(GroceryList)
admin.site.register(GroceryItem)
