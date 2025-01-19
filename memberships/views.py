from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect

from memberships.models import Membership, Payment


def show_memberships(request):
    memberships = Membership.objects.all()
    context = {
        'memberships': memberships,
    }
    return render(request, 'memberships/memberships.html', context)

from dateutil.relativedelta import relativedelta
def payment(request, membership_id):
    if request.method == 'POST':
        user = request.user
        client = user.client
        client.membership = Membership.objects.filter(id=membership_id).get()
        client.save()
        payment_method = request.POST.get('method')
        months, price = request.POST.get('option').split(':')
        payments = [Payment.objects.create(
            date = date.today() + relativedelta(months=(month-1)),
            client = request.user,
            amount = price,
            method = payment_method,
            status = 'completed' if month==1 else 'scheduled',
        )  for month in range(1, int(months) + 1)]
        for payment in payments:
            payment.save()
        return HttpResponse("paid")

    try:
        membership = Membership.objects.filter(pk=membership_id).get()
        prices = {
            int(field.name.split('_')[-1]): getattr(membership, field.name)
            for field in membership._meta.get_fields()
            if field.name.startswith('price_')
        }

        context = {
            'membership': membership,
            'payment_options': Payment._meta.get_field('method').choices,
            'prices': prices,
        }
        return render(request, 'memberships/payment.html', context)
    except Membership.DoesNotExist:
        return HttpResponse('no such membership')

def cancel_membership(request):
    user = request.user
    user.client.membership = None
    user.client.save()
    payments = Payment.objects.filter(client=user).filter(status='scheduled')
    for payment in payments:
        payment.status = 'cancelled'
        payment.save()
    return redirect('/users/profile')