from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=96)
    name_en = models.CharField(max_length=96, null=True)
    name_ru = models.CharField(max_length=96, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subcategory', null=True, blank=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    name = models.CharField(max_length=96, unique=True)
    name_en = models.CharField(max_length=96, null=True, unique=True)
    name_ru = models.CharField(max_length=96, null=True, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.category, self.name)


class Order(models.Model):
    STATUSES = (
        ('New', 'New'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey('bot.TelegramUser', on_delete=models.CASCADE, related_name='orders')
    cart = models.ManyToManyField('CartItem')
    status = models.CharField(max_length=10, choices=STATUSES, default='New')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return '{}'.format(self.user.phone_number)

    # def order_date(self):
    #     return self.created.strftime('%B %d %Y')

    # def deliver_date(self):
    #     return self.updated.strftime('%B %d %Y')


class CartItem(models.Model):
    user = models.ForeignKey('bot.TelegramUser', on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} - {}".format(self.product.name, self.quantity)
