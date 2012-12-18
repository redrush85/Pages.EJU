# Create your views here.
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.shortcuts import render_to_response, get_object_or_404, RequestContext
from Catalog.models import url, category
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf


def detailedlist(request):
    categories = category.objects.all()
    urls = url.objects.all().order_by("category")
    return render_to_response("detailedlist.html", {'urls': urls, 'categories': categories})

@csrf_protect
def search(request):
    if (request.method == 'POST'):
        search_str = request.POST['what']

        if search_str == '': return HttpResponseRedirect('/')

        categories = category.objects.all()
        urls_list = url.objects.filter(description__contains=search_str)
        urls_count = urls_list.count()

        return render_to_response("search.html", {'urls': urls_list, 'urls_count':urls_count, 'categories': categories, 'search_str': search_str}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')

@cache_page(60 * 15)
def index(request):
    categories = category.objects.all()
    #urls = url.objects.all().order_by("category")
    urls = []
    for catname in categories:
        urlsfromcategory = url.objects.filter(category__id=catname.id).order_by('?')[:3]
        for urlline in urlsfromcategory:
            urlobject = {}
            urlobject['name'] = urlline
            urlobject['url'] = urlline.url
            urlobject['image'] = urlline.image
            urlobject['thumbnail'] = urlline.thumbnail
            urlobject['category'] = catname
            urlobject['category_id'] = catname.id
            urlobject['description'] = urlline.description
            urlobject['geturl'] = urlline.getUrl()
            urls.append(urlobject)

    return render_to_response("index.html", {'urls': urls, 'categories': categories}, context_instance=RequestContext(request))

@cache_page(60 * 15)
def showcategory(request, categoryid):
    obj = get_object_or_404(category, id=categoryid)
    categoryname = obj
    categories = category.objects.all()

    urls_list = url.objects.filter(category__id=categoryid).order_by('-id')
    urls_count = urls_list.count()

    paginator = Paginator(urls_list, 10)

    page = request.GET.get('page')
    try:
        urls = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        urls = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        urls = paginator.page(paginator.num_pages)
    catid = int(categoryid)
    return render_to_response("category.html", {'urls': urls, 'urls_count':urls_count, 'categoryname': categoryname, 'categories': categories, 'category_id': catid}, context_instance=RequestContext(request))


#@cache_page(60 * 15)
def showurl(request, urlid):
    obj = get_object_or_404(url, id=urlid)
    #c = {}
    #c.update(csrf(request))
    categories = category.objects.all()
    title = obj
    if obj.image:
        imageurl = obj.image._get_url()
    else:
        imageurl = None
    return render_to_response("showurl.html",  {'obj': obj, 'title': title, 'imageurl': imageurl,'categories': categories}, context_instance=RequestContext(request))
