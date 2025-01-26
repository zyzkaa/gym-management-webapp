from datetime import date

from django.http import HttpResponse
from django.shortcuts import render, redirect

from memberships.models import Membership, Payment


def show_memberships(request):
    memberships = Membership.objects.all().values()
    desc = {
        'basic': ['Unlimited gym access',
                  'Participation in one group workout',
                  'One complimentary personal training session']
    }
    desc['student'] = desc['basic'].copy() + ['Discounted pricing for students with valid ID']
    desc['premium'] = ['Unlimited gym access',
                       'Participation in group classes (full schedule)',
                       'Three complimentary personal training sessions',
                       'Access to sauna and spa facilities',]
    for membership in memberships:
        membership['desc'] = desc[membership['name']]
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
        return redirect('users:current_profile')

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
    for workout in user.client_workouts.all():
        workout.client.remove(user)
    for payment in Payment.objects.filter(client=user).filter(status='scheduled'):
        payment.status = 'cancelled'
        payment.save()

    return redirect('users:current_profile')