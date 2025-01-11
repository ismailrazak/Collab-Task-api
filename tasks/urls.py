from rest_framework.routers import DefaultRouter

from .views import AttachmentViewSet, TaskListViewSet, TaskViewSet

router = DefaultRouter()

router.register("task", TaskViewSet)
router.register("tasklist", TaskListViewSet)
router.register("attachments", AttachmentViewSet)
urlpatterns = router.urls
