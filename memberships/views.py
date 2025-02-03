from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from memberships.models import Membership, Payment


def show_memberships(request):
    memberships = Membership.objects.all()
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
        membership.desc = desc.get(membership.name)
        membership.prices = {
            int(field.name.split('_')[-1]): getattr(membership, field.name)
            for field in membership._meta.get_fields()
            if field.name.startswith('price_')
        }

    context = {
        'memberships': memberships,
        'payment_options': Payment._meta.get_field('method').choices,
    }

    if request.method == 'POST':
        user = request.user
        client = user.client
        membership_id = request.POST.get('membership_id')
        client.membership = memberships.get(pk=membership_id)
        client.save()
        payment_method = request.POST.get('method-' + membership_id)
        months, price = request.POST.get('option-' + membership_id).split(':')
        payments = [Payment.objects.create(
            date=date.today() + relativedelta(months=(month - 1)),
            client=request.user,
            amount=price,
            method=payment_method,
            status='completed' if month == 1 else 'scheduled',
        ) for month in range(1, int(months) + 1)]
        for payment in payments:
            payment.save()
        return redirect('users:current_profile')

    return render(request, 'memberships/memberships.html', context)

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