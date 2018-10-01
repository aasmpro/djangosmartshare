from django.contrib import admin
from .models import Location


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        ('', {
            'fields': (
                'path',
            ),
        }),

        ('Public', {
            'fields': (
                'active_p',
                ('show_f_p', 'show_d_p', 'show_h_f_p', 'show_h_d_p'),
                ('can_down_p', 'can_up_p', 'can_crt_p', 'can_del_p', 'can_run_p'),
            ),
            'classes': ('collapse',)
        }),

        ('User', {
            'fields': (
                'active_u',
                ('show_f_u', 'show_d_u', 'show_h_f_u', 'show_h_d_u'),
                ('can_down_u', 'can_up_u', 'can_crt_u', 'can_del_u', 'can_run_u'),
            ),
            'classes': ('collapse',)
        }),

        ('Admin', {
            'fields': (
                'active_a',
                ('show_f_a', 'show_d_a', 'show_h_f_a', 'show_h_d_a'),
                ('can_down_a', 'can_up_a', 'can_crt_a', 'can_del_a', 'can_run_a'),
            ),
            'classes': ('collapse',)
        })
    ]


admin.site.register(Location, LocationAdmin)
