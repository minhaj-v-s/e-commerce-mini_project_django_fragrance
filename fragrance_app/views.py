from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . models import Products
# Create your views here.

def home(request):
    
        query = request.GET.get("search")
        if query:
            products = Products.objects.filter(name = query)
        else:  
            products = Products.objects.all()

        return render(request,"home.html",{'products':products,'q':query} )

# def cart(request):
#      return render(request,"cart.html")

# def cart(request,pk):
#     products = Products.objects.get(id=pk)
#     id = products.id
#     name = products.name
#     image = products.image.url
#     price = products.price

#     request.session['id'] = id
#     request.session['name'] = name
#     request.session['image'] = image
#     request.session['price'] = price

#     return redirect('cart_products')

# def cart_products(request):
#      id = request.session['id']
#      name = request.session['name']
#      image = request.session['image']
#      price = request.session['price']

#      return render(request,'cart.html',{'id':id,'name':name,'image':image,'price':price})




def cart(request,pk):
    #  product = Products.objects.get(id=pk)
     product = get_object_or_404(Products, id=pk)

     cart = request.session.get('cart',[])

     new_item = {
          'id':product.id,
          'name':product.name,
          'image':product.image.url,
          'price':product.price,
          'quantity':1
     }

     for item in cart:
          if item['id'] == product.id:
               item['quantity'] += 1
               break
     else:
        cart.append(new_item)

     request.session['cart'] = cart
     request.session.modified = True
     

     return redirect('cart_products')


def product(request,pk):
     thisProduct = Products.objects.get(id = pk)
     return render(request,"product.html",{'thisProduct':thisProduct})