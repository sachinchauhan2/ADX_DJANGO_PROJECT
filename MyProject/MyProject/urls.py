from django.contrib import admin
from django.urls import path
from UploadFiles import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('adx-chart/<int:id>', views.adx_chart ,name="chart"),
    path('uploadfile',views.uploadfile,name="uploadfile"),
    path('deleteFile/<int:id>',views.deleteFile),
    path('viewFile/<int:id>',views.viewFile)
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
