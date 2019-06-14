from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from blog.models import *
import blog.sv as sv
class Stamv(MiddlewareMixin):
    def process_request(self, request):
        if sv.issy == 0:
            ips = Ip.objects.all().values("ipaddress").distinct()
            for ip in ips:
                sv.ips.append(ip["ipaddress"])
            print(sv.ips)
            sv.issy=1
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        print(ip)
        if not ip in sv.ips:
            try:
                Ip.objects.get(ipaddress=ip).save()
            except:
                Ip(ipaddress=ip).save()
            ips = Ip.objects.all().values("ipaddress").distinct()
            sv.ips.clear()
            for ip in ips:
                sv.ips.append(ip["ipaddress"])
            print(sv.ips)
        return None
    def process_response(self, request, response):
        return response
    '''
    分类编辑
    文章编辑
    标签
    评论管理
    留言板
    文章页面优化
    '''