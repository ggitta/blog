from django.contrib.sitemaps import Sitemap
from blog.models import Blog,Category

class BlogSiteMap(Sitemap):
    changefreq = "monthly"
    priority = "0.8"
    def items(self):
        return Blog.objects.all()

    def lastmod(self, obj):
        return obj.addtime

# class CategorySiteMap(Sitemap):
#     changefreq = "monthly"
#     priority = "0.6"
#     def items(self):
#         return Category.objects.all()
#
#     def lastmod(self, obj):
#         return obj.addtime
