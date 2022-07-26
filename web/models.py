from django.db import models


class Customer(models.Model):
    customer_name = models.CharField(max_length=50)


class Shop(models.Model):
    shop_name = models.CharField(max_length=50)

    def __str__(self):
        return self.shop_name


class Bill(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill_id = models.BigIntegerField()
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    bill_sum = models.IntegerField()

    def __str__(self):
        return f'{self.user.customer_name} - {self.bill_id} - {self.bill_sum}'


class Entity(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.FloatField()
    entity_sum = models.FloatField()
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.quantity} - {self.entity_sum}'
