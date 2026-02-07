from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse
from .models import Products,ProductMedia
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from django.db.models import Q

from django.contrib.auth.decorators import login_required
from DjangoEcommerceApp.models import Categories,SubCategories,CustomUser,MerchantUser,Products,ProductAbout,ProductDetails,ProductMedia,ProductTransaction,ProductTags,StaffUser,CustomerUser
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from DjangoEcommerce.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")

def demoPageTemplate(request):
    return render(request,"demo.html")

def adminLogin(request):
    return render(request,"admin_templates/signin.html")

def adminLoginProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")

    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        login(request=request,user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request,"Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))

def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Successfully!")
    return HttpResponseRedirect(reverse("admin_login"))


def basetemp(request):
    return render(request,"base_template.html")

class Product_lists(ListView):

     model=Products
     template_name="admin_templates/product_list_.html"
     paginate_by=3

     def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
                products=Products.objects.filter(Q(product_name__contains=filter_val) | Q(product_description__contains=filter_val)).order_by(order_by)
        else:
                products=Products.objects.all().order_by(order_by)
            
        product_list=[]
        for product in products:
                product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1,is_active=1).first()
                product_list.append({"product":product,"media":product_media})

        return product_list

     def get_context_data(self,**kwargs): 
        context=super(Product_lists,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Products._meta.get_fields()
        return context
   

def product_detail(request, url_slug):
    products = get_object_or_404(Products, slug=url_slug, is_active=True)
    media = ProductMedia.objects.filter(product=products, is_active=True)
    return render(request, "admin_templates/product_detail.html",{"product": products, "media": media})