from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from InventorySystem.models import Product, ProductCategory, ProductImported, ProductSoldOut, Shop, ShopCategory, UserDetail
from django.contrib.auth.models import User, Group, Permission

def ShopCategoryList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        ShopCategory.objects.create(name = name, description = description)
        messages.success(request,'Product Category created Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    categories = ShopCategory.objects.all()
    context = {'categories':categories}
    return render(request,'InventorySystem/list-categories.html', context)


def EditShopCategory(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        categories = ShopCategory.objects.filter(id = id).first()
        categories.name = name
        categories.description = description
        categories.save()
        messages.success(request,'Product Category updated Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteShopCategory(request, id):
    categories = ShopCategory.objects.filter(id = id)
    if categories.exists():
        categories.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ShopList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        location = request.POST.get('location')
        is_main_branch = request.POST.get('is_main_branch')
        sellers_id = request.POST.get('sellers')
        owner_id = request.POST.get('owner')
        category = ShopCategory.objects.filter(id = category_id).first()

        owner= UserDetail.objects.filter(id = owner_id).first()
        sellers = User.objects.filter(id = sellers_id).first()
        Shop.objects.create(name = name, category = category, location  = location, is_main_branch= is_main_branch, sellers = sellers, owner = owner)
        messages.success(request,'Shop is created Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    sellers = User.objects.all()
    Shops = Shop.objects.all()
    owner =UserDetail.objects.all()
    categories = ShopCategory.objects.all()
    context = {'Shops':Shops, 'categories':categories, 'sellers':sellers, 'owner':owner}
    return render(request,'InventorySystem/list-Shops.html', context)


def EditShop(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        location = request.POST.get('location')
        is_main_branch = request.POST.get('is_main_branch')
        sellers_id = request.POST.get('sellers')
        owner_id = request.POST.get('owner')
        owner= UserDetail.objects.filter(id = owner_id).first()
        sellers = User.objects.filter(id = sellers_id).first()
        
        category = ShopCategory.objects.filter(id = category_id).first()
        Shops = Shop.objects.filter(id = id).first()
        name = name
        Shops.category = category
        Shops.location  = location
        Shops.is_main_branch= is_main_branch
        Shops.sellers = sellers
        Shops.owner = owner
        Shops.save()
        messages.success(request,'Shop is updated Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteShop(request, id):
    Shops = Shop.objects.filter(id = id)
    if Shops.exists():
        Shops.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ProductCategoryList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = request.user
        ProductCategory.objects.create(name = name, user_created = user)
        messages.success(request,'Product Category created Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    categories = ProductCategory.objects.all()
    context = {'categories':categories}
    return render(request,'InventorySystem/list-product-categories.html', context)


def EditProductCategory(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        # description = request.POST.get('description')
        categories = ProductCategory.objects.filter(id = id).first()
        categories.name = name
        categories.user_created = request.user
        categories.save()
        messages.success(request,'Product Category updated Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteProductCategory(request, id):
    categories = ProductCategory.objects.filter(id = id)
    if categories.exists():
        categories.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ProductList(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = ProductCategory.objects.filter(id = category_id).first()
        Product.objects.create(name = name, description = description, category = category)
        messages.success(request,'Product Category created Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    categories = ProductCategory.objects.all()
    products = Product.objects.all()
    context = {'products':products, 'categories':categories}
    return render(request,'InventorySystem/list-products.html', context)


def EditProduct(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        category = ProductCategory.objects.filter(id = category_id).first()
        products = Product.objects.filter(id = id).first()
        products.name = name
        products.description = description
        products.category = category
        products.save()
        messages.success(request,'Product Category updated Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteProduct(request, id):
    products = Product.objects.filter(id = id)
    if products.exists():
        products.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def ProductImportedList(request):
    if request.method == 'POST':
        product_id = request.POST.get('name')
        measurement = request.POST.get('measurement')
        price = request.POST.get('price')
        manufacture = request.POST.get('manufacture')
        quantity = request.POST.get('quantity')
        product = Product.objects.filter(id = product_id).first()
        
        ProductImported.objects.create(price = price, manufacture = manufacture, quantity = quantity, measurement = measurement, product = product)
        messages.success(request,'ProductImported Category created Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    categories = Product.objects.all()
    ProductImporteds = ProductImported.objects.all()
    context = {'ProductImporteds':ProductImporteds, 'categories':categories}
    return render(request,'InventorySystem/list-product-imported.html', context)


def EditProductImported(request, id):
    if request.method == 'POST':
        product_id = request.POST.get('name')
        measurement = request.POST.get('measurement')
        price = request.POST.get('price')
        manufacture = request.POST.get('manufacture')
        quantity = request.POST.get('quantity')
        product_obj = Product.objects.filter(id = product_id).first()
        
        product = ProductImported.objects.filter(id = id).first()
        product.price = price
        product.manufacture = manufacture
        product.quantity = quantity
        product.measurement = measurement
        product.product = product_obj
        product.save()
        messages.success(request,'ProductImported Category updated Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteProductImported(request, id):
    ProductImporteds = ProductImported.objects.filter(id = id)
    if ProductImporteds.exists():
        ProductImporteds.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def ProductSoldOutList(request):
    if request.method == 'POST':
        product_id = request.POST.get('name')
        measurement = request.POST.get('measurement')
        price = request.POST.get('price')
        customer_name = request.POST.get('customer_name')
        quantity = request.POST.get('quantity')
        product = Product.objects.filter(id = product_id).first()
        shop_exist = Shop.objects.filter(sellers = request.user)
        
        if shop_exist.exists():
            shop = shop_exist.first()
            ProductSoldOut.objects.create(price = price, quantity = quantity, measurement = measurement, product = product, shop = shop, customer_name = customer_name)
            messages.success(request,'ProductSoldOut Category created Succesfuly')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        else:
            messages.success(request,'you have not access privillage to this add sales')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    products = Product.objects.all()
    user_detalis = UserDetail.objects.all()
    ProductSoldOuts = ProductSoldOut.objects.all()
    context = {'ProductSoldOuts':ProductSoldOuts, 'products':products, 'user_detalis':user_detalis}
    return render(request,'InventorySystem/list-product-sold-out.html', context)


def EditProductSoldOut(request, id):
    if request.method == 'POST':
        product_id = request.POST.get('name')
        measurement = request.POST.get('measurement')
        price = request.POST.get('price')
        customer_name = request.POST.get('customer_name')
        quantity = request.POST.get('quantity')
        product = Product.objects.filter(id = product_id).first()
        
        sales = ProductSoldOut.objects.filter(id = id).first()
        sales.price = price
        sales.quantity = quantity
        sales.measurement = measurement
        sales.product = product
        sales.shop = sales.shop
        sales.customer_name = customer_name
        sales.save()
        messages.success(request,'ProductSoldOut updated Succesfuly')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def DeleteProductSoldOut(request, id):
    ProductSoldOuts = ProductSoldOut.objects.filter(id = id)
    if ProductSoldOuts.exists():
        ProductSoldOuts.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
