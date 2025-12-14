from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from cart.utils import get_cart
from .forms import CheckoutForm
from .models import OrderItem
from .models import Order
from accounts.models import Profile
import stripe
from django.conf import settings
from django.http import HttpResponseRedirect
# Create your views here.

print("Debug Stripe Key IN SETTINGS:", repr(settings.STRIPE_SECRET_KEY))

@login_required
def checkout(request):
    cart = get_cart(request)
    if not cart.items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("products:product_list")
    # get or create user profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.paid = False         # later connect real payment
            order.payment_method = "stripe"  # later connect real payment
            order.save()
            # sync profile from order from
            profile.full_name = order.full_name
            profile.address = order.address
            profile.city = order.city
            profile.phone = order.phone
            profile.save()

            line_items = []
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                )
                line_items.append({
                    'price_data': {
                        'currency': 'inr',
                        'product_data': {
                            'name': item.product.name,
                        },
                        'unit_amount': int(item.product.price * 100),
                    },
                    'quantity': item.quantity,
                })

            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],mode="payment",
                line_items=line_items,
                success_url=settings.STRIPE_SUCCESS_URL + f"?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=settings.STRIPE_CANCEL_URL,
                )
            order.payment_id = checkout_session.id
            order.save()
            return HttpResponseRedirect(checkout_session.url)
            # clear the cart
        else:
            initial = {
                "full_name": profile.full_name,
                "address": profile.address,
                "city": profile.city,
                "phone": profile.phone,
            }
            form = CheckoutForm(initial=initial)
            return render(request, "orders/checkout.html", {"cart": cart, "form": form})



    else:
        # prefill form with profile data
        initial = {
            "full_name": profile.full_name,
            "address": profile.address,
            "city": profile.city,
            "phone": profile.phone,
        }
        form = CheckoutForm(initial=initial)

    return render(request, "orders/checkout.html", {"cart": cart, "form": form})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at").prefetch_related("items__product")
    return render(request, "orders/my_orders.html", {"orders": orders})

@login_required
def payment_success(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        messages.error(request, "Missing session id.")
        return redirect("orders:my_orders")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.retrieve(session_id)
    # find the order
    order = get_object_or_404(Order, payment_id=session.id, user=request.user)
    if not order.paid and session.payment_status == "paid":
        order.paid = True
        order.save()
        # clear the cart
        cart = get_cart(request)
        cart.items.all().delete()
        messages.success(request, f"Order #{order.pk} placed successfully!")
    return render(request, "orders/payment_success.html", {"order": order})

@login_required
def payment_canceled(request):
    return render(request, "orders/payment_canceled.html")

class PaymentSuccessView(TemplateView):
    template_name = "orders/payment_success.html"

class PaymentCanceledView(TemplateView):
    template_name = "orders/payment_canceled.html"