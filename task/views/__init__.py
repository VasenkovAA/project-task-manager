from task.views.view_category import CategoryListCreateView, CategoryRetrieveUpdateDestroyView
from task.views.view_file import FileListCreateView, FileRetrieveUpdateDestroyView
from task.views.view_link import LinkListCreateView, LinkRetrieveUpdateDestroyView
from task.views.view_location import LocationListCreateView, LocationRetrieveUpdateDestroyView
from task.views.view_space import SpaceListCreateView, SpaceRetrieveUpdateDestroyView
from task.views.view_status import StatusListCreateView, StatusRetrieveUpdateDestroyView
from task.views.view_task import TaskListCreateView, TaskRetrieveUpdateDestroyView
from task.views.view_task_link import TaskLinkListCreateView, TaskLinkRetrieveUpdateDestroyView

__all__ = [
    'CategoryListCreateView',
    'CategoryRetrieveUpdateDestroyView',
    'FileListCreateView',
    'FileRetrieveUpdateDestroyView',
    'LinkListCreateView',
    'LinkRetrieveUpdateDestroyView',
    'LocationListCreateView',
    'LocationRetrieveUpdateDestroyView',
    'SpaceListCreateView',
    'SpaceRetrieveUpdateDestroyView',
    'StatusListCreateView',
    'StatusRetrieveUpdateDestroyView',
    'TaskLinkListCreateView',
    'TaskLinkRetrieveUpdateDestroyView',
    'TaskListCreateView',
    'TaskRetrieveUpdateDestroyView',
]
