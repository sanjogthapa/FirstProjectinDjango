"""FirstProjectSept URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from lib_mgmt_sys import views
from django.conf.urls.static import static
from FirstProjectSept import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sample_view, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('lms/', include('lib_mgmt_sys.urls'))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
    MEDIA_URL = '/MEDIA/'
    document_root:
        dir(MEDIA_ROOT)->
            fed 1.jpg
            dir(books_photos) ->
                ......
                .....
                
     o/p is:
     /media/fed 1.jpg
     /media/books_photos/fed 2.jpg       
"""