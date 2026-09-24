from django.db import models
import random
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
class Users(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

def create_order_number():
    while True:
        number = f"ORD-{random.randint(0,9999):04d}"
        #Check if the number created is in the Orders model or not
        #ORM Filter method
        if not Orders.objects.filter(order_number = number):
            return number

#Orders model
class Orders(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="orders")
    order_number = models.CharField(max_length=50, unique=True, editable = False, default=create_order_number)
    order_date = models.DateTimeField(auto_now_add=True)
    shipment_location = models.CharField(max_length=100)
    grand_total = models.DecimalField(max_digits=20, decimal_places=2, default=0, editable=False)
    def recalculate_total(self):
        total = sum(item.total for item in self.items.all())
        self.grand_total = total
        self.save(update_fields=["grand_total"])

class OrderItems(models.Model):
    order = models.ForeignKey(Orders,on_delete=models.CASCADE, related_name="items")
    product_name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits = 20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2, editable=False)

    def save(self, *args,**kwargs):
        self.total = self.quantity * self.rate
        super().save(*args,**kwargs)
#This is triggered whenever a new row in the OrderItems model is added 
# post_save is the signal that is listening to new row being added to the sender = OrderItems
# instance is the new row with all the fields being added
# instance.order = as we can see each row has the order_id so instance.order is getting the order_id and for that
# order_id -> call recalcuate_total()        
@receiver(post_save, sender=OrderItems)
def update_order_total_on_save(sender, instance, **kwargs):
    instance.order.recalculate_total()


@receiver(post_delete, sender=OrderItems)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.order.recalculate_total()