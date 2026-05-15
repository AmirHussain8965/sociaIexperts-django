from django.contrib import admin
from .models import Package, PackageFeature


class PackageFeatureInline(admin.TabularInline):
    model = PackageFeature
    extra = 1


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_popular', 'order')
    list_editable = ('is_popular', 'order')
    inlines = [PackageFeatureInline]


@admin.register(PackageFeature)
class PackageFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_text', 'package', 'is_included', 'order')
    list_filter = ('package', 'is_included')
    list_editable = ('is_included', 'order')

