from django.contrib import admin
from django.utils.html import format_html
from simple_history.admin import SimpleHistoryAdmin

from task.forms import (
    CategoryForm,
    FileForm,
    LinkForm,
    LocationForm,
    SpaceForm,
    StatusForm,
    TaskForm,
    TaskLinkForm,
)
from task.models import Category, File, Link, Location, Space, Status, Task, TaskLink


@admin.register(Space)
class SpaceAdmin(SimpleHistoryAdmin):
    form = SpaceForm
    list_display = ('space_name', 'created_at', 'users_count')
    search_fields = ('space_name',)
    list_filter = ('created_at',)
    filter_horizontal = ('space_users',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Main Information', {'fields': ('space_name', 'space_settings')}),
        (
            'User Management',
            {'fields': ('space_users',), 'description': 'Select users who should have access to this space'},
        ),
        ('System Information', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    def users_count(self, obj):
        return obj.space_users.count()

    users_count.short_description = 'Users'


@admin.register(Location)
class LocationAdmin(SimpleHistoryAdmin):
    form = LocationForm
    list_display = ('location_name', 'location_space', 'truncated_address')
    search_fields = ('location_name', 'location_address', 'location_space__space_name')
    list_filter = ('location_space',)
    list_select_related = ('location_space',)
    fieldsets = (
        ('Location Details', {'fields': ('location_name', 'location_space')}),
        ('Additional Information', {'fields': ('location_description', 'location_address'), 'classes': ('collapse',)}),
    )

    def truncated_address(self, obj):
        if len(obj.location_address) > 50:  # noqa: PLR2004
            return f'{obj.location_address[:47]}...'
        return obj.location_address

    truncated_address.short_description = 'Address'


@admin.register(Category)
class CategoryAdmin(SimpleHistoryAdmin):
    form = CategoryForm
    list_display = ('category_name', 'category_space')
    search_fields = ('category_name', 'category_space__space_name')
    list_filter = ('category_space',)
    list_select_related = ('category_space',)
    fieldsets = (
        ('Category Identification', {'fields': ('category_name', 'category_space')}),
        ('Configuration', {'fields': ('category_description', 'category_settings'), 'classes': ('collapse',)}),
    )


@admin.register(File)
class FileAdmin(SimpleHistoryAdmin):
    form = FileForm
    list_display = ('file_name', 'file_space', 'file_type', 'download_link')
    search_fields = ('file_name', 'file_space__space_name')
    list_filter = ('file_space',)
    list_select_related = ('file_space',)
    readonly_fields = ('file_preview',)
    fieldsets = (
        ('File Information', {'fields': ('file_name', 'file_space')}),
        (
            'File Content',
            {
                'fields': ('file_description', 'file_upload', 'file_preview'),
            },
        ),
    )

    def file_type(self, obj):
        return obj.file_upload.name.split('.')[-1].upper()

    file_type.short_description = 'Type'

    def file_preview(self, obj):
        if obj.file_upload:
            return format_html('<a href="{}" target="_blank">Download File</a>', obj.file_upload.url)
        return '-'

    file_preview.short_description = 'Preview'
    file_preview.allow_tags = True

    def download_link(self, obj):
        return format_html('<a href="{}" download><i class="fa fa-download"></i></a>', obj.file_upload.url)

    download_link.short_description = 'Download'
    download_link.allow_tags = True


@admin.register(Link)
class LinkAdmin(SimpleHistoryAdmin):
    form = LinkForm
    list_display = ('link_title', 'truncated_url', 'link_space', 'safe_link')
    search_fields = ('link_title', 'link_url', 'link_space__space_name')
    list_filter = ('link_space',)
    list_select_related = ('link_space',)
    fieldsets = (
        ('Link Information', {'fields': ('link_title', 'link_space')}),
        ('URL Details', {'fields': ('link_description', 'link_url'), 'classes': ('collapse',)}),
    )

    def truncated_url(self, obj):
        return obj.link_url[:50] + '...' if len(obj.link_url) > 50 else obj.link_url  # noqa: PLR2004

    truncated_url.short_description = 'URL'

    def safe_link(self, obj):
        return format_html('<a href="{}" target="_blank" rel="noopener noreferrer">Open</a>', obj.link_url)

    safe_link.short_description = 'Open'
    safe_link.allow_tags = True


@admin.register(Status)
class StatusAdmin(SimpleHistoryAdmin):
    form = StatusForm
    list_display = ('status_name', 'status_space')
    search_fields = ('status_name', 'status_space__space_name')
    list_filter = ('status_space',)
    list_select_related = ('status_space',)
    fieldsets = (
        ('Status Information', {'fields': ('status_name', 'status_space')}),
        ('Configuration', {'fields': ('status_description', 'status_settings'), 'classes': ('collapse',)}),
    )


@admin.register(Task)
class TaskAdmin(SimpleHistoryAdmin):
    form = TaskForm
    list_display = ('task_name', 'status', 'assignee', 'priority', 'progress')
    search_fields = ('task_name', 'description', 'status__status_name')
    list_filter = ('status', 'priority', 'risk_level', 'is_ready')
    list_select_related = ('status', 'assignee', 'task_space')
    filter_horizontal = ('dependencies', 'categories')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (
            'Task Details',
            {
                'fields': (
                    'task_name',
                    'description',
                    'task_space',
                    'status',
                    'priority',
                    'complexity',
                    'risk_level',
                    'tags',
                ),
            },
        ),
        (
            'Progress Tracking',
            {
                'fields': (
                    'progress',
                    'progress_dependencies',
                    'is_ready',
                    'quality_rating',
                    'actual_duration',
                    'estimated_duration',
                ),
            },
        ),
        (
            'Dates & Scheduling',
            {
                'fields': ('start_date', 'end_date', 'deadline', 'is_recurring', 'repeat_interval', 'next_activation'),
                'classes': ('collapse',),
            },
        ),
        ('Assignments', {'fields': ('author', 'last_editor', 'assignee', 'location', 'categories', 'dependencies')}),
        ('Financials', {'fields': ('budget',), 'classes': ('collapse',)}),
        ('System Fields', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
        (
            'Advanced Settings',
            {
                'fields': (
                    'time_intervals',
                    'reminders',
                    'notifications',
                    'cancel_reason',
                    'needs_approval',
                    'is_template',
                ),
                'classes': ('collapse',),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        """Автоматически устанавливаем автора и последнего редактора"""
        if not change:  # Новый объект
            obj.author = request.user
        obj.last_editor = request.user
        super().save_model(request, obj, form, change)


@admin.register(TaskLink)
class TaskLinkAdmin(SimpleHistoryAdmin):
    form = TaskLinkForm
    list_display = ('task', 'link', 'truncated_description')
    search_fields = ('task__task_name', 'link__link_title')
    list_select_related = ('task', 'link')

    def truncated_description(self, obj):
        if obj.description:
            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description  # noqa: PLR2004
        return ''

    truncated_description.short_description = 'Description'
