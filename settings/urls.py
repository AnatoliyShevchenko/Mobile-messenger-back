# Django
from django.contrib import admin
from django.urls import (
    path, 
    include,
)
from django.conf import settings
from django.conf.urls.static import static

# SimpleJWT
from rest_framework_simplejwt.views import TokenRefreshView

# Local
from auths.views import (
    AuthorizationView,
    RegistrationView,
)
from messenger.views import (
    ChatRoomsView,
    MessagesView,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/chats/', ChatRoomsView.as_view()),
    path('api/v1/messages/<str:pk>/', MessagesView.as_view()),
    path('api/v1/messages/', MessagesView.as_view()),
    path('api/v1/registration/', RegistrationView.as_view()),
    path('api/token/', AuthorizationView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

    