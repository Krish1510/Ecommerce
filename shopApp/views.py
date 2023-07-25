import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from shopApp.form import CustomUserForm
from . models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def home(request):
    product= products.objects.filter(treading=1)
    return render(request,'shop/home.html',{'product':product})
def logout_page(request):
  if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Logged out Successfully")
  return redirect("/")
 
 
def login_page(request):
  if request.user.is_authenticated:
    return redirect("/")
  else:
    if request.method=='POST':
      name=request.POST.get('username')
      pwd=request.POST.get('password')
      user=authenticate(request,username=name,password=pwd)
      if user is not None:
        login(request,user)
        messages.success(request,"Logged in Successfully")
        return redirect("/")
      else:
        messages.error(request,"Invalid User Name or Password")
        return redirect("/login")
    return render(request,"shop/login.html")
  
def register(request):
    form=CustomUserForm()
    if request.method=='POST':
       form=CustomUserForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,"Registration Success you cab login now...")
    return render(request,'shop/register.html',{'form':form})
def collection(request):
   cat= catagory.objects.filter(status=0)
   # collect=list()
   # for i in cat:
   #    collect.append({
   #       "name": i.name,
   #       "image":i.image,
   #       "description":i.description
   #    })
   return render(request,'shop/collections.html',{"catagory":cat})
def collectionview(request,name):
  if(catagory.objects.filter(name=name,status=0)):
    product=products.objects.filter(catagory__name=name)
   #  pro_list = list()
   #  for i in product:
   #      pro_list.append({
   #         "product_image": i.product_image,
   #         "name": i.name,
   #         "original_price": i.original_price,
   #         "selling_price": i.selling_price
   #      })
    return render(request,'shop/product/index.html',{"product":product,'catagory_name':name})
  else:
     messages.warning(request,"No such Catagory Found")
     return redirect('collections')
  
def product_details(request,cname,pname):
    if(catagory.objects.filter(name=cname,status=0)):
      if(products.objects.filter(name=pname,status=0)):
        product=products.objects.filter(name=pname,status=0).first()
        return render(request,"shop/product/product_details.html",{"product":product})
      else:
        messages.error(request,"No Such Produtct Found")
        return redirect('collections')
    else:
      messages.error(request,"No Such Catagory Found")
      return redirect('collections')
    
  
def add_to_cart(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_qty=data['product_qty']
      product_id=data['pid']
      #print(request.user.id)
      product_status=products.objects.get(id=product_id)
      if product_status:
        if Cart.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Cart'}, status=200)
        else:
          if product_status.quantity>=product_qty:
            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
            return JsonResponse({'status':'Product Added to Cart'}, status=200)
          else:
            return JsonResponse({'status':'Product Stock Not Available'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Cart'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   
 
def cart_page(request):
  if request.user.is_authenticated:
    cart=Cart.objects.filter(user=request.user)
    return render(request,"shop/cart.html",{"cart":cart})
  else:
    return redirect("/")
  
def remove_cart(request,cid):
  cartitem=Cart.objects.get(id=cid)
  cartitem.delete()
  return redirect("/cart")

def fav_page(request):
   if request.headers.get('x-requested-with')=='XMLHttpRequest':
    if request.user.is_authenticated:
      data=json.load(request)
      product_id=data['pid']
      product_status=products.objects.get(id=product_id)
      if product_status:
         if Favourite.objects.filter(user=request.user.id,product_id=product_id):
          return JsonResponse({'status':'Product Already in Favourite'}, status=200)
         else:
          Favourite.objects.create(user=request.user,product_id=product_id)
          return JsonResponse({'status':'Product Added to Favourite'}, status=200)
    else:
      return JsonResponse({'status':'Login to Add Favourite'}, status=200)
   else:
    return JsonResponse({'status':'Invalid Access'}, status=200)
   
 
def favviewpage(request):
  if request.user.is_authenticated:
    fav=Favourite.objects.filter(user=request.user)
    return render(request,"shop/fav.html",{"fav":fav})
  else:
    return redirect("/")
  
def remove_fav(request,fid):
  item=Favourite.objects.get(id=fid)
  item.delete()
  return redirect("/favviewpage")