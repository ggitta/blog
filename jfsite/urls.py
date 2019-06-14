"""jfsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,re_path
import blog
from blog import views as blog_view
from blog import image as blog_images
from blog import account as blog_account
from django.conf.urls import handler400, handler403, handler404, handler500
from blog.sitemap import  BlogSiteMap
from django.contrib.sitemaps.views import sitemap
from blog.models import Blog

sitemaps = {
    'Article': BlogSiteMap,
    # 'Category': CategorySiteMap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path('google5fa9c06babaa0799.html/',blog_view.ggauth),
    path('shellindex', blog_view.index,name="blog_view_index"),
    path('', blog_view.home,name="blog_view_home"),
    path('shell', blog_view.shell,name="blog_view_shell"),
    path('archive', blog_view.archive,name="blog_view_archive"),
    path('addcmt', blog_view.addcmt,name="blog_view_addcmt"),
    path('addrss', blog_view.addrss,name="blog_view_addrss"),
    path('tomail', blog_view.tomail,name="blog_view_tomail"),
    path('mail', blog_view.mail,name="blog_view_mail"),
    path('loginv', blog_account.login,name="blog_account_login"),
    path('articles', blog_view.articles,name="blog_view_articles"),
    path('categories', blog_view.categories ,name="blog_view_articles"),
    path('toblogadd', blog_view.toblogadd ,name="blog_view_toblogadd"),
    path('upload', blog_images.upload ,name="blog_images_upload"),
    path('addblog', blog_view.addblog ,name="blog_view_addblog"),
    path('toblog/<id>', blog_view.toblog ,name="blog_view_toblog"),
    path('getips', blog_view.getips ,name="blog_view_getips"),
    path('adminindex', blog_view.adminindex ,name="blog_view_adminindex"),
    path('adminarticles', blog_view.adminarticles ,name="blog_view_adminarticles"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

handler400 = blog_view.bad_request
handler403 = blog_view.permission_denied
handler404 = blog_view.page_not_found
handler500 = blog_view.server_error