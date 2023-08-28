from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    product_desc=models.CharField(max_length=2000)
    product_date_pub=models.DateField()
    product_category=models.CharField(max_length=50, default="")
    product_subcategory=models.CharField(max_length=50, default="")
    product_prize=models.IntegerField(default=0)
    product_image=models.ImageField(upload_to="shop/images", default="")
    def __str__(self):
        return self.product_name+'-'+str(self.product_prize)

class Shop_Contact(models.Model):
    msgid=models.AutoField(primary_key=True)
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    subject=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    message=models.TextField()
    def __str__(self):
        return self.name+'-'+self.subject

class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    preferred_address=models.CharField(max_length=400)
    second_preferred_address=models.CharField(max_length=400)
    city=models.CharField(max_length=15)
    state=models.CharField(max_length=20)
    zip_code=models.CharField(max_length=11)
    
    # +'ITEMS'+self.items_json+'NAME'+self.name+'city-zip'+self.city+'-'+self.zip_code
    
class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default="")
    update_description=models.CharField(max_length=5000)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_description[0:7]+'..'