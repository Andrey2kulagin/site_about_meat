from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class ProductCategories(models.Model):
    category_name = models.CharField(max_length=300)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=200)
    cost = models.PositiveIntegerField()
    category_name = models.ManyToManyField(ProductCategories, default="Вне категорий")
    preview = RichTextField(default="Без описания", max_length=500)
    description = RichTextField(default="Без описания")
    image = models.ImageField(upload_to='img', default="img/1.png")

    def __str__(self):
        return self.name


class Application(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    phone_number = models.CharField(verbose_name="phone_name", max_length=12)
    comment = models.CharField(verbose_name="comment", max_length=350)

    def __str__(self):
        return self.phone_number


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    phone_number = models.CharField(max_length=12, default="")
    address = models.CharField(max_length=250, default="")


class GoodsInShoppingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, null=True)

    def cost(self):
        return self.product.cost

    def total_cost(self):
        if self.count:
            return self.product.cost * self.count
        return None


class Order(models.Model):
    my_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250, null=True)
    created = models.DateTimeField()
    is_processed = models.BooleanField(default=False)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    delivery_date = models.DateTimeField()
    comment = models.TextField()
    total_cost = models.PositiveIntegerField(default=0, null=True)
    total_items = models.PositiveIntegerField(default=0)
    total_kgs = models.PositiveIntegerField(default=0)
    ORDER_STATUS = (
        ('r', 'Зарегистрирован'),
        ('p', 'Собирается'),
        ('s', 'Отправлен на доставку'),
        ('d', 'Доставлен'),
    )
    status = models.CharField(max_length=1, choices=ORDER_STATUS, null=True, default="Зарегистрирован")

    def __str__(self):
        return self.my_id

    def position_number(self):
        return len(OrderItems.objects.filter(order_id=self))

    def sum_kgs(self):
        items = OrderItems.objects.filter(order_id=self)
        sum_gks_eq = 0
        for item in items:
            sum_gks_eq += item.product_count
        return sum_gks_eq

    def sum_rubs(self):
        items = OrderItems.objects.filter(order_id=self)
        sum_rubs_eq = 0
        for item in items:
            sum_rubs_eq += item.product_id.cost * item.product_count
        return sum_rubs_eq


class OrderItems(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_count = models.PositiveIntegerField()
