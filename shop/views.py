from django.http import HttpResponse
from django.shortcuts import render 
from .models import Product,Contact,Orders,Orderupdate
from math import ceil
import json
def index(request):
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nslides=n//4 + ceil((n/4) - (n//4))
        allprods.append([prod,range(1,nslides),nslides])
    context={"allprods":allprods}
    return render(request, 'shop/index.html',context)

def searchMatch(query,item):
    '''return true only if query matches the items'''
    if query in item.discription.lower() or query in item.product_name.lower() or  query in item.category.lower() :
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    allprods=[]
    catprods=Product.objects.values('category','id')
    cats={item['category'] for item in catprods}
    for cat in cats:
        prodtemp= Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nslides=n//4 + ceil((n/4) - (n//4))
        if len(prod)!=0:
            allprods.append([prod,range(1,nslides),nslides])
    context={"allprods":allprods,'msg':''}
    if len(allprods)==0 or len(query)<4:
        context={'msg':'please enter relevent search query'}

    return render(request, 'shop/search.html',context)


def about(request):
    return render(request,"shop/about.html")

def contact(request):
    thankyou=False
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        contact = Contact(name=name,email=email,phone=phone,desc=desc)
        contact.save()
        thankyou=True
    return render(request,"shop/contact.html",{'thankyou':thankyou})

def tracker(request):
    if request.method=="POST":
        orderId=request.POST.get('orderId','')
        email=request.POST.get('email','')
       
        try :
            order = Orders.objects.filter(order_id=orderId , email = email)
            if len(order)>0:
                update = Orderupdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response = json.dumps({'status':'success','updates':updates, 'itemsJson':order[0].items_json }, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"No items"}')
        except Exception as e:
            return HttpResponse("{'status':'Error'}")
    return render(request,"shop/tracker.html")


def productView(request,myid):
    # fatch the priduct using id
    product= Product.objects.filter(id=myid)
    print(product)
    return render(request,"shop/prodview.html",{'product':product[0]})

def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name',''),
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')  + " " + request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        zip_code=request.POST.get('zip_code','')
        phone=request.POST.get('phone','')
        

        order = Orders(items_json,name=name,email=email,city=city,state=state,address=address,zip_code=zip_code,phone=phone,amount=amount)
        order.save()
        update = Orderupdate(order_id = order.order_id, update_desc = " the order has been placed")
        update.save()
        thank=True
        id= order.order_id
        return render(request,"shop/checkout.html",{'thank': thank ,'id':id})
    return render(request,"shop/checkout.html")
