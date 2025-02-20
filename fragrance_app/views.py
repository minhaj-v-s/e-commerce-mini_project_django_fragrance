from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from . models import Products,Cart,Register,OrderHistory
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import get_messages
from reportlab.pdfgen import canvas

# Create your views here.


def home(request):
    
        query = request.GET.get("search")
        if query:
            products = Products.objects.filter(name = query)
        else:  
            products = Products.objects.all()
        
        id = request.session.get('id')
        name = request.session.get('name')
        if name:
          return render(request,"home.html",{'products':products,'q':query,'id':id,'name':name} )
        else:
          return render(request,"home.html",{'products':products,'q':query})

        


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

     if not request.session.get('id'):
          storage = get_messages(request)
          storage.used = True

          messages.warning(request,"Login to add to cart.")
          return redirect('login')
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


def cart_remove(request,pk,action):
     if action == 'remove':

          cart_item = get_object_or_404(Cart,id=pk)
          cart_item.delete()
          return redirect('view_cart')

def product(request,pk):
     thisProduct = Products.objects.get(id = pk)
     return render(request,"product.html",{'thisProduct':thisProduct})

def register(request):
     if request.method == "POST":
          name = request.POST.get('name')
          email = request.POST.get('email')
          phone = request.POST.get('phone')
          new_password = request.POST.get('new_password')
          password = request.POST.get('password')

          if new_password == password:
               Register(name=name,email=email,phone=phone,password=password).save()

     return render(request,"register.html")

def login(request):
     return render(request,"login.html")

def userlog(request):
     if request.method == "POST":
          username = request.POST.get("username")
          password = request.POST.get("password")

          check = Register.objects.filter(email=username,password = password)

          if check:
               user_details = Register.objects.get(email = username,password = password)
               id = user_details.id
               name = user_details.name
               email = user_details.email

               request.session['id'] = id
               request.session['name'] = name

               return redirect('home')
          else:
               return render(request,"login.html")


def logoutuser(request):
     request.session.flush()
     return redirect('login')


def checkout(request):
     if not request.session.get('id'):
          messages.warning(request,"Login to proceed with checkout.")
          return redirect("login")

     user_id = request.session.get('id')
     user = Register.objects.get(id = user_id)
     cart_items = Cart.objects.all()

     if not cart_items:
          messages.error(request,"Your Cart is empty!")
          return redirect("view_cart")
     
     for item in cart_items:
          OrderHistory.objects.create(
               user = user,
               product = item.product,
               quantity = item.quantity,
               total_price = item.price * item.quantity,
          )

     cart_items.delete()

     messages.success(request,"Purchase successfull! Your order has been recorded.")
     return redirect("purchase_history")


def purchase_history(request):
     if not request.session.get('id'):
          messages.warning(request,"Login to view purchase history.")
          return redirect("login")
     
     user_id = request.session.get('id')
     user = Register.objects.get(id = user_id)
     orders = OrderHistory.objects.filter(user = user).order_by("-purchased_at")

     return render(request,"purchase_history.html",{"orders":orders})

def download_invoice(request, order_id):
     order = OrderHistory.objects.get(id = order_id)

     response = HttpResponse(content_type = "application/pdf")
     response['Content-Disposition'] = f'attachment; filename ="invoice_{order.id}.pdf'

     p = canvas.Canvas(response)
     p.drawString(100,800,"Invoice")
     p.drawString(100,780, f"Order ID: {order.id}")
     p.drawString(100,760, f"Customer: {order.user.name}")
     p.drawString(100,740, f"Product: {order.product.name}")
     p.drawString(100,720, f"Quantity: {order.quantity}")
     p.drawString(100,700, f"Total Price: ₹{order.total_price}")
     p.drawString(100,680, f"Date: {order.purchased_at}")

     p.showPage()
     p.save()

     return response


def cancel_order(request,order_id):
     user_id = request.session.get('id')
     user = Register.objects.get(id = user_id)
     order = get_object_or_404(OrderHistory,id=order_id,user=user)

     if order.status != 'Cancelled':
          order.status = 'Cancelled'
          order.save()
          messages.success(request,"Order has been cancelled.")

     else:
          messages.warning(request,"Order is already cancelled.")

     return redirect("purchase_history")
     
