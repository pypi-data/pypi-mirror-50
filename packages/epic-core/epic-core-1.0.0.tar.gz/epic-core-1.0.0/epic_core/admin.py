from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.conf.urls import url
from django.http import Http404, HttpResponse
from django.utils.translation import gettext_lazy as _

from .site import epic_site
from .models import Organization, UserProfile

class ReadOnlyAdmin:
    """
        Make Admin class read only
        """

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class EpicAdminMixin:
    """
        Epic Admin mixin class
        """
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        app_name = self.model._meta.app_label
        model_name = self.model._meta.model_name

        # export url used in reverse() and templates
        self.export_url = '{}_{}_export'.format(app_name, model_name)
        self.detail_url = '{}_{}_detail'.format(app_name, model_name)

    def get_urls(self):
        """ Add export view """
        urls = super().get_urls()
        my_urls = [
            url(r'^(?P<id>.+)/detail/$',
                self.admin_site.admin_view(self.get_detail_view), name=self.detail_url),
            url(r'^export/$', self.admin_site.admin_view(self.get_export_view), name=self.export_url),
        ]
        return my_urls + urls

    def get_export_view(self, request):
        """ Export view, return csv file from model db table """
        from .helpers import export_model_to_csv
        return export_model_to_csv(self.model)

    def get_detail_view(self, request, id):
        """ Object detail view, abstract method """
        if self.has_show_detail_permission(request):
            raise NotImplementedError(_("Show detail activated, you should implement this method"))
        else:
            raise Http404("Detail view not found, please implement get_detail_view() method !")

    def has_export_permission(self, request):
        codename = get_permission_codename('export', self.opts)
        return request.user.has_perm("%s.%s" % (self.opts.app_label, codename))

    def has_show_detail_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('detail', opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))

    def changelist_view(self, request, extra_context=None):
        """ Add export permission context data """
        response = super().changelist_view(request, extra_context)
        response.context_data['has_export_permission'] = self.has_export_permission(request)
        response.context_data['has_detail_permission'] = self.has_show_detail_permission(request)

        print(response.context_data)
        return response

class EpicModelAdmin(EpicAdminMixin, admin.ModelAdmin):
    """
        Epic custom model admin instance,
        """

class EpicTabularInline(admin.TabularInline):
    """ Epic Admin custom TabularInline """
    pass


class EpicStackedInline(admin.TabularInline):
    """ Epic Admin custom StackedInline """
    pass


class ReadOnlyModelAdmin(EpicModelAdmin, ReadOnlyAdmin):
    """ Epic Admin readonly ModelAdmin """
    pass


class ReadOnlyTabularInline(EpicTabularInline, ReadOnlyAdmin):
    """ Epic Admin readonly TabularInline """
    pass


class ReadOnlyStackedInline(EpicTabularInline, ReadOnlyAdmin):
    """ Epic Admin readonly StackedInline """
    pass


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('email', 'first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    inlines = [UserProfileInline, ]
    list_select_related = ['userprofile']


class OrganizationAdmin(EpicModelAdmin):
    list_display = [ 'name', 'phone_1', 'phone_2', 'province', 'city', 'zip' ]
    pass

epic_site.register(User, CustomUserAdmin)
epic_site.register(Group, GroupAdmin)
epic_site.register(Organization, OrganizationAdmin)