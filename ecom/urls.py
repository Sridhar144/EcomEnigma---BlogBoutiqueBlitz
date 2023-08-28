from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from . import views
admin.site.site_header="SriChadBlops Admin"
admin.site.site_title="Sridhar Admin"
admin.site.index_title="Welcome to your web Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),

    path('shop/', include('shop.urls')),
    path('blog/', include('blog.urls'))
]  +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
