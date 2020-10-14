from django.urls import path
from .views import (
    TicketCreateView,
    GeneralInfoUpdateView,
    TicketUpdateView,
    EquipoAcometidaUpdateView,
    CentroCargaUpdateView,
    CircuitosRamalesUpdateView,
    GeneralRecomendationsUpdateView,
    SendedView,
    PdfView,
    PdfHtmlView,
    CentroCargaSecundarioView
)

app_name = 'core'

urlpatterns = [
    path('', TicketCreateView.as_view(), name='createTicket'),
    path('equipoacometida/<slug>', EquipoAcometidaUpdateView.as_view(), name='equipoacometida'),
    path('centrocarga/<slug>', CentroCargaUpdateView.as_view(), name='centrocarga'),
    path('circuitosramales/<slug>', CircuitosRamalesUpdateView.as_view(), name='circuitosramales'),
    path('generalInfo/<slug>', GeneralInfoUpdateView.as_view(), name='generalInfo'),
    path('generalrecomendations/<slug>', GeneralRecomendationsUpdateView.as_view(), name='generalrecomendations'),
    path('UpdateTicket/<superId>/<slug>', TicketUpdateView.as_view(), name='UpdateTicket'),
    path('sended/<link>', SendedView.as_view(), name='sended'),
    path('pdf/<link>', PdfView.as_view(), name='pdf'),
    path('pdfhtml/<slug>', PdfHtmlView.as_view(), name='pdfhtml'),
    path('centroCargaSecundario/<slug>', CentroCargaSecundarioView.add_centro, name='centroCargaSecundario')
]
