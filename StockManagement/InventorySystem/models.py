from django.db import models
from django.contrib.auth.models import User, Group, Permission

class UserDetail(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.BigIntegerField()
    gender = models.CharField(max_length=255)
    adress = models.CharField(max_length=255, blank=True, null=True)
    photo = models.FileField(upload_to='User Photos', blank=True, null=True)
    is_bussines_owner = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "User Detail"
        db_table = "User Detail"

# class Customer(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=255)
#     user = models.ForeignKey(User, on_delete = models.CASCADE)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Customer"
#         db_table = "Customer"

class ShopCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Shop Category"
        db_table = "Shop Category"

class Shop(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ShopCategory, on_delete = models.CASCADE)
    location = models.CharField(max_length=255)
    is_main_branch = models.BooleanField(default=True)
    sellers = models.ForeignKey(User, on_delete = models.CASCADE)
    owner = models.OneToOneField(UserDetail, on_delete = models.CASCADE)
    # created_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user_created', related_name='user_created')
    # updated_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user updated', related_name='user updated')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Shop"
        db_table = "Shop"

class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user_created', related_name='user_created')
    # updated_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user updated', related_name='user updated')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product Category"
        db_table = "Product Category"

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete = models.CASCADE)
    # created_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user_created', related_name='created_by')
    # updated_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user updated', related_name='user updated')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Product"
        db_table = "Product"

class ProductImported(models.Model):
    price = models.BigIntegerField()
    manufacture = models.CharField(max_length=255)
    quantity = models.BigIntegerField()
    measurement = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    # created_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user_created', editable=False)
    # updated_by = models.ForeignKey(User, on_delete = models.CASCADE, name='user updated', related_name='user updated')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def total_price(self):
        total = self.price * self.quantity
        return total

    class Meta:
        verbose_name = "Product Imported"
        db_table = "Product Imported"

class ProductSoldOut(models.Model):
    price = models.BigIntegerField()
    quantity = models.BigIntegerField()
    measurement = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete = models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer = models.ForeignKey(UserDetail, on_delete = models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def total_price(self):
        total = self.price * self.quantity
        return total

    class Meta:
        verbose_name = "Product Sold Out"
        db_table = "Product Sold Out"
