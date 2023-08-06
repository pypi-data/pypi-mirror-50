from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django_scopes import scopes_disabled
from pretix.base.signals import periodic_task
from pretix.control.signals import nav_event
from pretix_cartshare.models import SharedCart


@receiver(nav_event, dispatch_uid='cartshare_nav')
def navbar_info(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(request.organizer, request.event, 'can_change_orders', request=request):
        return []
    return [{
        'label': _('Share a cart'),
        'icon': 'shopping-cart',
        'url': reverse('plugins:pretix_cartshare:list', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_cartshare',
    }]


@receiver(signal=periodic_task)
@scopes_disabled()
def clean_cart_positions(sender, **kwargs):
    for sc in SharedCart.objects.filter(expires__lt=now()):
        sc.positions.delete()
        sc.delete()
