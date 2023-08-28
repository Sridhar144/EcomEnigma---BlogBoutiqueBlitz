from django.shortcuts import render,HttpResponse
from .models import Product, Shop_Contact, Orders, OrderUpdate
from math import ceil
import json
# Create your views here.
def index(request):
    
    products=Product.objects.all()
    # print(products)
    n=len(products)
    ns=n//4+ceil((n/4)-(n//4))
    allprods=[]
    # allprods=[[products, range(1,ns), ns],
    #           [products, range(1,ns), ns]]
    # dictio={'product':products, 'slides':ns, 'range':range(1,ns)}
    catprod=Product.objects.values('product_category')
    cats={item['product_category'] for item in catprod}
    for cat in cats:
        current=Product.objects.filter(product_category=cat)
        no=len(current)
        sample=no//4+ceil((no/4)-(no//4))
        print(sample)
        no=range(sample)
        allprods.append([current, range(1,ns), ns, no])
    dictio={'allprods':allprods}
    return render(request, 'shop/index.html', dictio)

def searchMatch(query, item):
    if query.lower() in item.product_desc.lower() or query.lower() in item.product_name.lower() or query.lower() in item.product_category.lower() or query.lower() in item.product_subcategory.lower():
        return True
    else:
        return False

def search(request):
    query=request.GET.get('search')
    products=Product.objects.all()
    # print(products)
    n=len(products)
    ns=n//4+ceil((n/4)-(n//4))
    allprods=[]
    # allprods=[[products, range(1,ns), ns],
    #           [products, range(1,ns), ns]]
    # dictio={'product':products, 'slides':ns, 'range':range(1,ns)}
    catprod=Product.objects.values('product_category')
    cats={item['product_category'] for item in catprod}
    for cat in cats:
        currenttemp=Product.objects.filter(product_category=cat)
        current=[item for item in currenttemp if searchMatch(query, item)]
        no=len(current)
        sample=no//4+ceil((no/4)-(no//4))
        print(sample)
        no=range(sample)
        if len(current)!=0 and len(query)>3:
            allprods.append([current, range(1,ns), ns, no])
    
        
    dictio={'allprods':allprods, 'dotell':""}
    if not len(allprods) or len(query)<4:
        dictio['dotell']="Query not set properly, Please search appropriate phrase to search for an item"
    return render(request, 'shop/search.html',dictio)

def prodview(request, myid):
    curr=Product.objects.filter(id=myid)
    print(curr)
    return render(request, 'shop/products.html',{'product':curr})



def about(request):
    return render(request, 'shop/about.html')

def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('itemsJson','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        preferred_address=request.POST.get('preferred_address','')
        second_preferred_address=request.POST.get('second_preferred_address','')

        city=request.POST.get('city','')
        state=request.POST.get('state','')  
        zip_code=request.POST.get('zip_code','')
        order=Orders(items_json=items_json, name=name, email=email, phone=phone, preferred_address=preferred_address, second_preferred_address=second_preferred_address, city=city, state=state, zip_code=zip_code)
        order.save()
        update=OrderUpdate(order_id=order.order_id, update_description="Order has been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request, 'shop/checkout.html',{'thank':thank, 'id':id})

    return render(request, 'shop/checkout.html')

def items(request):
    cur=Product.objects.all()

    return render(request, 'shop/items.html',{'product':cur})

def tracker(request):
    if request.method=="POST":
        order_id=request.POST.get('order_id','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        try:
            order=Orders.objects.filter(order_id=order_id, name=name, email=email, phone=phone)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=order_id)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_description, 'time':item.timestamp.date()})
                    response=json.dumps({"status": "success" ,"updates": updates, "itemsJson":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                
                return HttpResponse('{"status": "noitem"}')

        except Exception as e:
            pass
            return HttpResponse('{"status": "error"}')
    return render(request, 'shop/tracker.html')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        subject=request.POST.get('subject','')
        message=request.POST.get('message','')
        contact=Shop_Contact(name=name, email=email, phone=phone, subject=subject, message=message)
        contact.save()
    return render(request,'shop/contacts.html')

