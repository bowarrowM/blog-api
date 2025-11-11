
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include all blog routes under /api/blog/
    path('api/blog/', include('blog.urls')),
]
