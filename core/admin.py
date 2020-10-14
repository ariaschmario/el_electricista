from django.contrib import admin

# Register your models here.
from core.models import Client, Ticket, CentroCargaSecundario, EquipoAcometida, CircuitosRamales, GeneralInfo, CentroCarga, GeneralRecomendatios


class ClientAdmin(admin.ModelAdmin):
    list_display = ['legalId',
                    'name',
                    'phoneNumber',
                    'email'
                    ]
    list_display_links = [
                    ]
    list_filter = ['name'
    ]
    search_fields = [
        'legalId',
        'phoneNumber',
        'email'
    ]

class TicketAdmin(admin.ModelAdmin):
    list_display = ['client',
                    'equipo_acometida',
                    'circuitos_ramales',
                    'general_info',
                    'centro_carga',
                    'general_recomendations',
                    'file_url',
                    'superId',
                    ]
    list_display_links = ['client',
                    'equipo_acometida',
                    'circuitos_ramales',
                    'general_info',
                    'centro_carga',
                    'general_recomendations'
    ]
    list_filter = [
    ]
    search_fields = [
        'superId'
    ]


admin.site.register(Client, ClientAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(CentroCargaSecundario)
admin.site.register(EquipoAcometida)
admin.site.register(CircuitosRamales)
admin.site.register(GeneralInfo)
admin.site.register(CentroCarga)
admin.site.register(GeneralRecomendatios)



