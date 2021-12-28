from django.utils.translation import gettext_lazy as _, ngettext_lazy
ngettext_lazy(
    "This password is too short. It must contain at least %(min_length)d character.",
    "This password is too short. It must contain at least %(min_length)d characters.",
    1
)

_("This password is entirely numeric.")

_("The password is too similar to the %(verbose_name)s.") % {'verbose_name': 'verbose_name'}

_("This password is too common.")