from django.contrib import admin
from models import (
    Category,
    File,
    Link,
    Location,
    Space,
    Status,
    task,
)

admin.site.register(Category)
admin.site.register(File)
admin.site.register(Link)
admin.site.register(Location)
admin.site.register(Space)
admin.site.register(Status)
admin.site.register(task)
