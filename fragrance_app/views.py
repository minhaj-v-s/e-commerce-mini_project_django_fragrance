from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . models import Products,Cart
# Create your views here.

def home(request):
    
        query = request.GET.get("search")
        if query:
            products = Products.objects.filter(name = query)
        else:  
            products = Products.objects.all()

        return render(request,"home.html",{'products':products,'q':query} )


# def cart(request,pk):
#     cart_item = Products.objects.get(id = pk)
#     price = cart_item.price
#     Cart(product = cart_item,price = price).save()     
#     cart_products = Cart.objects.all()
#     return render(request,"cart.html",{'cart_products': cart_products})

     
# def cart_update(request,pk,action):
#      cart_item = Cart.objects.get(id=pk)
#      if action == 'decrement':
#           cart_item.quantity -= 1

#      return redirect('cart_update')
    

def view_cart(request):
     cart_products = Cart.objects.all()
     total_price = sum(item.price * item.quantity for item in cart_products)
     return render(request,"cart.html",{"cart_products":cart_products,"total_price":total_price})
     
def cart(request,pk):
     cart_item = get_object_or_404(Products,id=pk)
     cart_product, created = Cart.objects.get_or_create(product = cart_item, defaults = {'price':cart_item.price})

     if not created:
          cart_product.quantity +=1
          cart_product.save()
     return redirect('view_cart')

def cart_update(request,pk,action):
     cart_item = get_object_or_404(Cart,id=pk)
     
     if action == 'increment':
          cart_item.quantity += 1
     elif action == 'decrement':
          if cart_item.quantity > 1:
               cart_item.quantity -= 1
          else:
               cart_item.delete()
               return redirect('view_cart')
          
     cart_item.save()
     return redirect('view_cart')



def product(request,pk):
     thisProduct = Products.objects.get(id = pk)
     return render(request,"product.html",{'thisProduct':thisProduct})
