from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext, gettext_lazy as _

import website

# Register your models here.
from website.models import *


class EduTextA(admin.ModelAdmin):
    list_display = ("id", "text", "text_type")
    list_filter = ("text_type",)
    search_fields = ("text",)
    ordering = ["id", "text", "text_type"]


class RefBookTitleDescriptionA(admin.ModelAdmin):
    list_display = ("title", "description")
    search_fields = ("title", "description")
    ordering = ["title"]


class RefBookTitleA(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
    ordering = ["title"]


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = website.models.User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = website.models.User
        fields = ("email", "username")


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = website.models.User

    list_display = (
        "username",
        "email",
        "last_name",
        "first_name",
        "phone",
        "user_type",
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "middle_name",
                    "email",
                    "phone",
                    "address",
                    "user_type",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    list_filter = UserAdmin.list_filter + ("user_type",)
    search_fields = UserAdmin.search_fields


class CourtDistrictA(admin.ModelAdmin):
    list_display = ("title", "address", "phone")
    search_fields = ("title", "address", "phone")
    ordering = ["title"]


class CourtDistrictA(admin.ModelAdmin):
    list_display = ("title", "address", "phone")
    search_fields = ("title", "address", "phone")
    ordering = ["title"]


class CourtOrderHistoryItemInline(admin.TabularInline):
    model = CourtOrderHistory
    raw_id_fields = [
        "court_order",
    ]
    extra = 0
    # exclude = ('cost',)
    readonly_fields = ("registration_date", "user", "status")


class CancellationRequestItemInline(admin.TabularInline):
    model = CancellationRequest
    raw_id_fields = [
        "court_order",
    ]
    extra = 0
    # exclude = ('cost',)
    # readonly_fields = ('get_total_cost',)


class CourtOrderA(admin.ModelAdmin):
    list_display = (
        "registration_date",
        "date",
        "number",
        "claimant",
        "defendant",
        "court_district",
        "status",
    )
    list_filter = (
        "registration_date",
        "date",
        "number",
        "claimant",
        "defendant",
        "author",
        "court_district",
        "category",
        "status",
    )
    search_fields = ("content",)
    ordering = ["registration_date"]
    inlines = [CourtOrderHistoryItemInline, CancellationRequestItemInline]


class CancellationRequestHistoryItemInline(admin.TabularInline):
    model = CancellationRequestHistory
    raw_id_fields = [
        "cancellation_request",
    ]
    extra = 0
    # exclude = ('cost',)
    readonly_fields = ("registration_date", "user", "status")


class CancellationRequestA(admin.ModelAdmin):
    list_display = ("registration_date", "court_order", "user", "status")
    list_filter = ("registration_date", "user", "status")
    search_fields = ("content",)
    ordering = ["registration_date"]
    inlines = [CancellationRequestHistoryItemInline]


class CourtOrderCategoryA(admin.ModelAdmin):
    list_display = ("title",)
    list_filter = ("templates",)
    search_fields = ("title",)
    # ordering = ['registration_date']


class TemplateA(admin.ModelAdmin):
    list_display = ("title", "file")
    # list_filter = ('templates', )
    search_fields = ("title",)
    # ordering = ['registration_date']


admin.site.register(website.models.User, CustomUserAdmin)
admin.site.register(UserType, RefBookTitleA)
admin.site.register(CourtOrderStatus, RefBookTitleA)

admin.site.register(CourtOrderCategory, CourtOrderCategoryA)
admin.site.register(Template, TemplateA)

admin.site.register(CancellationRequestStatus, RefBookTitleA)
admin.site.register(CourtDistrict, CourtDistrictA)
admin.site.register(CourtOrder, CourtOrderA)
admin.site.register(CancellationRequest, CancellationRequestA)


admin.site.site_header = "Судебные приказы"
