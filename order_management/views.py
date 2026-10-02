from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Users, Orders, OrderItems


def home(request):
    return render(request,"order_management/home.html")


#This is the view for placing the order

def place_order(request):
    if request.method == "POST":
        # the form values are passed in the request body in a QueryDict
        # Which is a dictionary created with keys which matches the "name" attributes in the form.
        # We use "get" or "getlist" to GET the values from the form
        # These all can be done directly using ModelForm class and using the CreateView
        user_name = request.POST.get("user_name","").strip()
        shipment_location = request.POST.get("shipment_location"," ").strip()
        product_names = request.POST.getlist("product_name[]")
        quantities = request.POST.getlist("quantity[]")
        rates = request.POST.getlist("rate[]")
        if user_name and shipment_location and product_names:
            #Create a user if doesnt exists
            user, _ = Users.objects.get_or_create(name = user_name)
            order = Orders.objects.create(
                user = user,
                shipment_location = shipment_location,

            )
            for product_name, quantity, rate in zip(product_names, quantities, rates):
                if product_name.strip():
                    OrderItems.objects.create(
                        order = order,
                        product_name = product_name,
                        quantity = int(quantity),
                        rate = Decimal(rate)
                    )
            return redirect("order_history")
    return render(request,"order_management/place_order.html")
        # Now we traverse all three lists 
def order_history(request):
    orders = Orders.objects.all().order_by("-order_date")
    return render(request, "order_management/order_history.html", {"orders": orders})


def order_view(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    items = OrderItems.objects.filter(order=order)
    return render(request, "order_management/view_order.html", {"order": order, "items": items})


def order_update(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    items = OrderItems.objects.filter(order=order)

    if request.method == "POST":
        user_name = request.POST.get("user_name", "").strip()
        shipment_location = request.POST.get("shipment_location", "").strip()

        item_ids = request.POST.getlist("item_id[]")
        product_names = request.POST.getlist("product_name[]")
        quantities = request.POST.getlist("quantity[]")
        rates = request.POST.getlist("rate[]")

        if user_name and shipment_location:
            user, _ = Users.objects.get_or_create(name=user_name)
            order.user = user
            order.shipment_location = shipment_location
            order.save()

            # Any item that existed before but whose id is missing from this
            # submission was removed in the browser via its row's Delete button.
            existing_ids = set(str(item.id) for item in items)
            submitted_ids = set(i for i in item_ids if i)
            ids_to_delete = existing_ids - submitted_ids
            if ids_to_delete:
                OrderItems.objects.filter(id__in=ids_to_delete, order=order).delete()

            for item_id, name, qty, rate in zip(item_ids, product_names, quantities, rates):
                if not name.strip():
                    continue
                if item_id:
                    item = get_object_or_404(OrderItems, id=item_id, order=order)
                    item.product_name = name.strip()
                    item.quantity = int(qty)
                    item.rate = Decimal(rate)
                    item.save()
                else:
                    OrderItems.objects.create(
                        order=order,
                        product_name=name.strip(),
                        quantity=int(qty),
                        rate=Decimal(rate),
                    )

            return redirect("view_order", order_id=order.id)

    return render(request, "order_management/order_update.html", {"order": order, "items": items})


def order_delete(request, order_id):
    order = get_object_or_404(Orders, id=order_id)

    if request.method == "POST":
        order.delete()  # CASCADE removes related OrderItem rows automatically
        return redirect("order_history")

    return render(request, "order_management/order_confirm_delete.html", {"order": order})

def view_order(request,order_id):
    order = get_object_or_404(Orders, id = order_id)
    items = OrderItems.objects.filter(order = order)
    return render(request, "order_management/view_order.html",{"order" : order, "items" : items})

def order_delete(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    items = OrderItems.objects.filter(order=order)

    if request.method == "POST":
        order.delete()
        return redirect("order_history")

    return render(request, "order_management/order_confirm_delete.html", {"order": order, "items": items})