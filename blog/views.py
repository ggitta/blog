import datetime
import json
import locale
import time

from django.core.mail import send_mail
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from blog.models import *

def getallcat():
    cates=Category.objects.all()
    catelist=[]
    catedict={}
    for cate in cates:
        catedict=cate.__dict__
        blogcount= Blog.objects.filter(category_id=cate.id).count()
        catedict["blogcount"]=blogcount
        author=cate.account.nickname if cate.account.nickname!=None else cate.account.username
        catedict["author"]=author
        if "_state" in catedict:
            del catedict["_state"]
        catelist.append(catedict)
    return catelist

def getalltag(req):
    if not "uid" in req.session:
        return render(req, "blog/home.html",{"error":"管理员功能请登录后使用"})
    uid=req.session["uid"]
    tagstext=""
    tagslist=[]
    tagstextlist=Blog.objects.filter(account_id=uid).values("tag")
    for blogtag in tagstextlist:
        tagstext+=blogtag["tag"]+","
    tags=tagstext.split(",")
    tagslist=list(set(tags))
    if "" in tagslist:
        tagslist.remove("")
    return tagslist

def getalltagwouser():
    tagstext=""
    tagslist=[]
    tagstextlist=Blog.objects.all().values("tag")
    for blogtag in tagstextlist:
        tagstext+=blogtag["tag"]
    tags=tagstext.split(",")
    tagslist=list(set(tags))
    if "" in tagslist:
        tagslist.remove("")
    return tagslist

def getallcatwouser():
    cates=Category.objects.all()
    catelist=[]
    catedict={}
    for cate in cates:
        catedict=cate.__dict__
        blogcount= Blog.objects.filter(category_id=cate.id).count()
        catedict["blogcount"]=blogcount
        catedict["name"]=cate.name.replace(" ","") if cate.name!=None else ""
        if "_state" in catedict:
            del catedict["_state"]
        catelist.append(catedict)
    return catelist

# Create your views here.
def index(req):
    return render(req,"blog/index.html")

def home(req):
    cate=Category.objects.all().count()
    blog=Blog.objects.all()
    blogtag=blog.values("tag")
    blogcount=blog.count()
    tagstext=""
    for blogtag in blogtag:
        tagstext+=blogtag["tag"]
    tags=tagstext.split(",")
    tagscount=len(list(set(tags)))
    ip=Ip.objects.all().count()
    ##最热文章
    blogs=Blog.objects.all().order_by("-viewcount")[:5]
    ##最新评论
    cmts_qs=Comment.objects.all().order_by("-addtime")[:5]
    ##标签
    tags=getalltagwouser()
    cmts=[]
    cmr_obj={}
    for cm in cmts_qs:
        cmr_obj=cm.__dict__
        cmr_obj["name"]="EM"+cm.email.split("@")[0][0:5]
        cmr_obj["content"]=cm.content.replace("<br/>","\n").replace("&nbsp;"," ")
        cmts.append(cmr_obj)
    return render(req,"blog/home.html",{"cate":cate,"blog":blogcount,"tag":tagscount,"ips":ip,"blogs":blogs,"cmts":cmts,"tags":tags[0:45]})

def shell(req):
    cate=Category.objects.all().count()
    blog=Blog.objects.all()
    blogtag=blog.values("tag")
    blogcount=blog.count()
    tagstext=""
    for blogtag in blogtag:
        tagstext+=blogtag["tag"]
    tags=tagstext.split(",")
    tagscount=len(list(set(tags)))
    ip=Ip.objects.all().count()
    return render(req,"blog/shell.html",{"cate":cate,"blog":blogcount,"tag":tagscount,"ips":ip})


def toblogadd(req):
    if not "uid" in req.session:
        return render(req, "blog/home.html",{"error":"管理员功能请登录后使用"})
    catelist=getallcat()
    taglist=getalltag(req)
    return  render(req,"blog/addblog.html",{"tags":taglist,"cates":catelist})
def addblog(req):
    if not "uid" in req.session:
        return render(req, "blog/home.html",{"error":"管理员功能请登录后使用"})
    uid=req.session["uid"]
    title= req.POST.get("title")
    content= req.POST.get("content")
    category= req.POST.get("category")
    htmlcontent= req.POST.get("htmlcontent")
    categorys=Category.objects.filter(name=category)
    result={}
    try:
        if categorys.count() > 0:
            category = categorys[0].id
        else:
            cate = Category(name=category, account_id=uid)
            cate.save()
            category = cate.id
        tags = req.POST.get("tags")
        blog = Blog(name=title, star=0, viewcount=0, content=content, like=0, account_id=uid,htmlcontent=htmlcontent, category_id=category,
                    tag=tags, type=1, public=1,addtime=datetime.datetime.now())
        blog.save()
        result["state"]=1
        result["msg"]="添加成功"
    except Exception as a:
        print(a)
        result["state"]=0
        result["msg"]="添加失败"
    return HttpResponse(json.dumps(result))

def articles(req):
    blogs=Blog.objects.all()
    try:
        cate = req.GET.get("cate")
        tag = req.GET.get("tag")
        cate="all" if cate==None else cate
        cate = int(cate) if cate!="all" else "all"
        tag="all" if tag==None else tag
        if cate != "all":
            blogs = blogs.filter(category_id=cate)
        if tag != "all":
            blogs = blogs.filter(tag__contains =tag)
    except Exception as a:
        print(a)
    paginator = Paginator(blogs, 6)
    page = req.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # 如果请求的页数不是整数，返回第一页。
        blogs = paginator.page(1)
    except EmptyPage:
        # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
        blogs = paginator.page(paginator.num_pages)

    bloglist=[]
    blogdict={}
    tags = getalltagwouser()
    cats = getallcatwouser()
    for blog in blogs:
        blogdict=blog.__dict__
        commontcount=Comment.objects.filter(blog_id=blog.id).count()
        blogdict["commentcount"]=commontcount
        author=blog.account.nickname if blog.account.nickname!=None else blog.account.username
        blogdict["author"]=author
        if "_state" in blogdict:
            del blogdict["_state"]
        bloglist.append(blogdict)
    return  render(req,"blog/articles.html",{"blogs":bloglist,"pgs":blogs,"tags":tags,"cates":cats,"nowcate":cate,"nowtag":tag[0:60]})
def categories(req):
    catelist=getallcat()
    return  render(req,"blog/categories.html",{"cates":catelist})

##########################################
def adminindex(req):
    if not "uid" in req.session:
        return render(req, "blog/home.html",{"error":"未登录，管理员功能请登录后使用"})
    return  render(req,"blog/adminindex.html")

def adminarticles(req):
    if not "uid" in req.session:
        return render(req, "blog/home.html",{"error":"未登录，管理员功能请登录后使用"})
    uid=req.session["uid"]
    blogs = Blog.objects.filter(account_id=uid)
    bloglist = []
    blogdict = {}
    for blog in blogs:
        blogdict = blog.__dict__
        commontcount = Comment.objects.filter(blog_id=blog.id).count()
        blogdict["commentcount"] = commontcount
        author = blog.account.nickname if blog.account.nickname != None else blog.account.username
        blogdict["author"] = author
        if "_state" in blogdict:
            del blogdict["_state"]
        bloglist.append(blogdict)
    return  render(req,"blog/adminarticles.html",{"blogs":bloglist})

def tomail(req):
    return render(req, "blog/mail.html")



def toblog(req,id):
    blogs=Blog.objects.filter(id=id)
    if blogs.count() > 0:
        blog=blogs[0]
        cmtslist=[]
        cmtdict={}
        cmts=Comment.objects.filter(blog_id=blog.id)
        for cmt in cmts:
            cmtdict=cmt.__dict__
            if "_state" in cmtdict:
                del cmtdict["_state"]
            repid=int(str(cmt.repaly)) if cmt.repaly!=None else -1
            repcmt = Comment.objects.filter(id=repid)
            if repcmt.count()>0:
                cmtdict["repemail"]="EM"+repcmt[0].email.split("@")[0][0:5] if repcmt.count()>0 else None
                cmtdict["repcnt"]=repcmt[0].content.replace("<br/>","\n").replace("&nbsp;"," ") if repcmt.count()>0 else None
                cmtdict["repid"]=repcmt[0].id if repcmt.count()>0 else None
                reps=Comment.objects.filter(repaly=cmt.id)
                repsingledict={}
                replist=[]
                for repsingle in reps:
                    repsingledict=repsingle.__dict__
                    repsingledict["name"]="EM"+repsingle.email.split("@")[0][0:5]
                    replist.append(repsingledict)
                cmtdict["replist"]=replist
                cmtdict["repcount"]=reps.count()
            cmtdict["name"]="EM"+cmt.email.split("@")[0][0:5]
            cmtslist.append(cmtdict)

        author=Account.objects.get(id=blog.account_id)
        category=Category.objects.get(id=blog.category_id)
        commontcount=len(Comment.objects.filter(blog_id=blog.id))
        blog.viewcount+=1
        blog.save()
        tags=blog.tag.split(",")
        tags.remove("")
        return render(req, "blog/blog.html",{"blog":blog,"tags":tags,"author":author,"category":category,"commontcount":commontcount,"cmtsbefore":cmtslist[:3],"cmtsafter":cmtslist[4:],"cmtsaftercount":len(cmtslist)-3})
    else:
        return HttpResponseRedirect("/")

def addcmt(req):
    email=req.POST.get("email")
    rep=req.POST.get("rep")
    blog=req.POST.get("blog")
    site=req.POST.get("site")
    content=req.POST.get("content")
    if len(email)>100 or len(site)>100 or len(content)>5000:
        return HttpResponse(json.dumps({"state":0,"msg":"评论内容过长"}))
    try:
        cmt = Comment(email=email,site=site,content=content,blog_id=blog,repaly=rep)
        cmt.save()
        send_mail("Javafeng有人评论:","评论者："+email+"\n内容："+content, 'blog@javafeng.com', ["1392670234@qq.com"], fail_silently=False)
        if  rep != -1 and rep != "-1":
            cmrrep=Comment.objects.get(id=rep)
            send_mail("您在[javafeng.com]的评论有人回复。", "原评论："+cmrrep.content+"\n内容："+content+'\n请移至[http://javafeng.com/toblog/'+str(blog)+']查看','blog@javafeng.com', [cmrrep.email], fail_silently=False)
        return HttpResponse(json.dumps({"state": 1, "msg": "成功"}))
    except Exception as a:
        print(a)
        return HttpResponse(json.dumps({"state": 0, "msg": "失败"}))

def archive(req):
    dates = Blog.objects.datetimes('addtime', 'month', order='DESC')
    print(dates)
    return render(req, 'blog/archive.html', {'dates': dates})

def mail(req):
    content = req.POST.get("content")
    mail = req.POST.get("mail")
    # send_mail的参数分别是  邮件标题，邮件内容，发件箱(settings.py中设置过的那个)，收件箱列表(可以发送给多个人),失败静默(若发送失败，报错提示我们)
    mailmsg = send_mail("邮件测试", content, '1148095417@qq.com',
                        [mail], fail_silently=False)
    return render(req, "blog/mail.html")

def addrss(req):
    email=req.POST.get("email")
    rsses=Rss.objects.filter(email=email)
    if  rsses.count() > 0:
        return HttpResponse(json.dumps({"state": 0, "msg": "您已订阅，不可重复订阅"}))
    else:
        try:
            rss=Rss(email=email)
            rss.save()
            return HttpResponse(json.dumps({"state": 1, "msg": "订阅成功"}))
        except:
            return HttpResponse(json.dumps({"state": 0, "msg": "订阅失败"}))

def getips(req):
    ips=Ip.objects.all().order_by("-lastview")
    iplist=[]
    ipdict={}
    for ip in ips:
        ipdict=ip.__dict__
        ipcut=ip.ipaddress.split(".")
        ipdict["ipaddress"]=ipcut[0]+"."+ipcut[1]+".***."+ipcut[3]
        ipdict["lastview"] = ip.lastview.split(".")[0]
        if "_state" in ipdict:
            del ipdict["_state"]
        iplist.append(ipdict)
    return HttpResponse(json.dumps({"ips":iplist}))

def bad_request(request, exception=None, template_name='error/400.html'):
    return render(request, template_name)



def permission_denied(request, exception=None, template_name='error/403.html'):
    return render(request, template_name)


def page_not_found(request, exception=None, template_name='error/404.html'):
    return render(request, template_name)


def server_error(request, exception=None, template_name='error/500.html'):
    return render(request, template_name)

def ggauth(req):
    return render(req, "google5fa9c06babaa0799.html")