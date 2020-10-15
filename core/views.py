import os

from django.http import HttpResponseRedirect, FileResponse, JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.base import View
from google.cloud import storage
import pdfcrowd
import sys

from elElectricistaProject import settings
from .models import Ticket, TicketCreateForm, Client, GeneralInfo, GeneralInfoUpdateForm, EquipoAcometidaUpdateForm, EquipoAcometida, CentroCarga, \
    CentroCargaUpdateForm, CircuitosRamales, CircuitosRamalesUpdateForm, GeneralRecomendatios, GeneralRecomendationsUpdateForm, CentroCargaSecundario
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect



class PdfView(View):
    def get(self, *args, **kwargs):
        link = self.kwargs['link']
        return FileResponse(open('tmp/' + link, 'rb'), content_type='application/pdf')



class PdfHtmlView(View):
    def get(self, *args, **kwargs):
        tikect = Ticket.objects.get(superId=self.kwargs['slug'])
        secundarios = CentroCargaSecundario.objects.filter(principal=Ticket.objects.get(superId=self.kwargs['slug']).centro_carga)
        context = {'ticket': tikect,
                   'secundarios': secundarios}
        return render(self.request, "pdf.html", context)


class SendedView(View):
    def get(self, *args, **kwargs):
        slug = self.kwargs['slug']
        context = {'slug': slug}
        return render(self.request, "boletaenviada.html", context)


class GeneralRecomendationsUpdateView(UpdateView):
    template_name = 'recomendacionesgenerales.html'
    form_class = GeneralRecomendationsUpdateForm
    model = GeneralRecomendatios


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if 'sigt' in self.request.POST:
            me = pdfcrowd.HtmlToPdfClient('ariaschmario', 'c9aeae493b830137cf765dcd473ad9f1')
            context = {'ticket': Ticket.objects.get(superId=self.kwargs['slug'])}
            x = render_to_string('pdf.html', context)

            me.setPageSize(u'Letter')
            me.setOrientation(u'landscape')
            response = HttpResponse(content_type='application/pdf')
            me.convertStringToStream(x, response)

            storage_client = storage.Client()

            bucket = storage_client.bucket('elelectricista')
            blob = bucket.blob('boletas/' + self.kwargs['slug'] + '.pdf')
            blob.upload_from_string(response.getvalue(), content_type='application/pdf')
            Ticket.objects.get(superId=self.kwargs['slug']).update_file_url('https://storage.cloud.google.com/elelectricista/boletas/' + self.kwargs['slug'] + '.pdf')
            #return redirect("core:pdfhtml", slug=self.kwargs['slug'])

            # link = self.kwargs["slug"] + '.pdf'
            return redirect("core:sended", slug=self.kwargs['slug'])
        else:
            return redirect("core:circuitosramales", slug=self.kwargs['slug'])

    def form_invalid(self, form):
        return redirect("core:createTicket")

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(GeneralRecomendationsUpdateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class CircuitosRamalesUpdateView(UpdateView):
    template_name = 'circuitosremanentes.html'
    form_class = CircuitosRamalesUpdateForm
    model = CircuitosRamales

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if 'sigt' in self.request.POST:
            return redirect("core:generalrecomendations", slug=self.kwargs['slug'])
        else:
            return redirect("core:centrocarga", slug=self.kwargs['slug'])

    def form_invalid(self, form):
        return redirect("core:createTicket")

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CircuitosRamalesUpdateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class CentroCargaUpdateView(UpdateView):
    template_name = 'centrodecarga.html'
    form_class = CentroCargaUpdateForm
    model = CentroCarga

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if 'sigt' in self.request.POST:
            return redirect("core:circuitosramales", slug=self.kwargs['slug'])
        else:
            return redirect("core:equipoacometida", slug=self.kwargs['slug'])

    def form_invalid(self, form):
        return redirect("core:createTicket")

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CentroCargaUpdateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class EquipoAcometidaUpdateView(UpdateView):
    template_name = 'equipoacometida.html'
    form_class = EquipoAcometidaUpdateForm
    model = EquipoAcometida

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if 'sigt' in self.request.POST:
            return redirect("core:centrocarga", slug=self.kwargs['slug'])
        else:
            return redirect("core:generalInfo", slug=self.kwargs['slug'])

    def form_invalid(self, form):
        return redirect("core:createTicket")

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EquipoAcometidaUpdateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class GeneralInfoUpdateView(UpdateView):
    template_name = 'informaciongeneral.html'
    form_class = GeneralInfoUpdateForm
    model = GeneralInfo

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if 'sigt' in self.request.POST:
            return redirect("core:equipoacometida", slug=self.kwargs['slug'])
        else:
            return redirect('core:UpdateTicket', superId=self.kwargs['slug'], slug=self.kwargs['slug'][0:-2])


    def form_invalid(self, form):
        return redirect("core:createTicket")

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(GeneralInfoUpdateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class TicketUpdateView(UpdateView):
    template_name = 'index.html'
    form_class = TicketCreateForm
    model = Client

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        client_id = form.cleaned_data['legalId']
        superId = self.kwargs['superId']
        new_super_id = client_id + "-" + superId[-1]
        Ticket.objects.get(superId=superId).set_superId(new_super_id)
        return redirect("core:generalInfo", slug=new_super_id)

    def form_invalid(self, form):
        return redirect("/")

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(TicketUpdateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class TicketCreateView(CreateView):
    template_name = 'index.html'
    form_class = TicketCreateForm

    def form_invalid(self, form):
        return redirect("/")

    def form_valid(self, form):
        idType = form.cleaned_data['idType']
        client_id = form.cleaned_data['legalId']
        name = form.cleaned_data['name']
        phoneNumber = form.cleaned_data['phoneNumber']
        email = form.cleaned_data['email']
        adress = form.cleaned_data['adress']
        if Client.objects.filter(legalId=client_id).exists():
            Client.objects.filter(legalId=client_id).update(idType=idType, legalId=client_id, name=name, phoneNumber=phoneNumber, email=email,
                                  adress=adress, slug =client_id)
        else:
            self.object = form.save(commit=False)
            self.object.save()
            Client.objects.filter(legalId=client_id).update(slug=client_id)
        client_id = form.cleaned_data['legalId']
        x = 1
        superIdAux = client_id + "-"
        while True:
            ticketAux = Ticket.objects.filter(superId=superIdAux + str(x))
            if ticketAux.exists():
                x += 1
            else:
                break
        general_info = GeneralInfo.objects.create(superId=superIdAux + str(x), slug=superIdAux + str(x))
        centro_carga = CentroCarga.objects.create(superId=superIdAux + str(x), slug=superIdAux + str(x))
        equipo_acometida = EquipoAcometida.objects.create(superId=superIdAux + str(x), slug=superIdAux + str(x))
        circuitos_ramales = CircuitosRamales.objects.create(superId=superIdAux + str(x), slug=superIdAux + str(x))
        general_recomendations = GeneralRecomendatios.objects.create(superId=superIdAux + str(x), slug=superIdAux + str(x))
        ticket = Ticket.objects.create(superId=superIdAux + str(x), client=Client.objects.get(legalId=client_id),
                                       general_info=GeneralInfo.objects.get(superId=superIdAux + str(x)),
                                       equipo_acometida=EquipoAcometida.objects.get(superId=superIdAux + str(x)),
                                       centro_carga=CentroCarga.objects.get(superId=superIdAux + str(x)),
                                       circuitos_ramales=CircuitosRamales.objects.get(superId=superIdAux + str(x)),
                                       general_recomendations=GeneralRecomendatios.objects.get(superId=superIdAux + str(x)))
        return redirect("core:generalInfo", slug=superIdAux + str(x))

    def get_context_data(self, **kwargs):
        ctx = super(TicketCreateView, self).get_context_data(**kwargs)
        ctx['create'] = True
        return ctx

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(TicketCreateView, self).get_form_kwargs(*args, **kwargs)
        return kwargs


class CentroCargaSecundarioView(View):
    quantity = 0

    def add_centro(request, slug):
        if request.is_ajax() and request.method == "POST":
            marca_catalogo = request.POST.get("marca_catalogo")
            espacios_ocupados = request.POST.get("espacios_ocupados")
            estado_tablero = request.POST.get("estado_tablero")
            estado_tablero_especifique = request.POST.get("estado_tablero_especifique")
            ubicacion = request.POST.get("ubicacion")
            canalizacion = request.POST.get("canalizacion")
            canalizacion_especifique = request.POST.get("canalizacion_especifique")
            canalizacion_distancia = request.POST.get("canalizacion_distancia")
            estado_alimentadores = request.POST.get("estado_alimentadores")
            estado_alimentadores_especifique = request.POST.get("estado_alimentadores_especifique")
            estado_puesta = request.POST.get("estado_puesta")
            estado_puesta_especifique = request.POST.get("estado_puesta_especifique")
            quantity = request.POST.get("quantity")


            CentroCargaSecundario.objects.create(principal=CentroCarga.objects.get(superId=slug), local_id=slug + "-" + str(quantity), marca_catalogo=marca_catalogo,
                                                 espacios_ocupados=espacios_ocupados, estado_tablero=estado_tablero, estado_tablero_especifique=estado_tablero_especifique,
                                                 ubicacion=ubicacion, canalizacion=canalizacion, canalizacion_especifique= canalizacion_especifique,
                                                 canalizacion_distancia=canalizacion_distancia, estado_alimentadores=estado_alimentadores,
                                                 estado_alimentadores_especifique=estado_alimentadores_especifique, estado_puesta=estado_puesta,
                                                 estado_puesta_especifique=estado_puesta_especifique)
            return JsonResponse({"scc": "true"}, status=200)
        else:
            return JsonResponse({"scc": "false"}, status=400)




# class HomeView(View):
#     def get(self, *args, **kwargs):
#         context = {}
#         return render(self.request, 'index.html', context);
#
#     def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
#         """Uploads a file to the bucket."""
#         # bucket_name = "your-bucket-name"
#         # source_file_name = "local/path/to/file"
#         # destination_blob_name = "storage-object-name"
#
#         storage_client = storage.Client()
#         bucket = storage_client.bucket(bucket_name)
#         blob = bucket.blob(destination_blob_name)
#
#         blob.upload_from_filename(source_file_name)
#

#
#     def download_blob(self):
#         client = storage.Client()
#         bucket = client.get_bucket('personerias')
#         blob = bucket.blob('GooglePdf1.pdf')
#         with open('tmp/example1.pdf', 'wb') as file_obj:
#             blob.download_to_file(file_obj)
#
#     def toPdf(self):
#         try:
#             # create the API client instance
#             client = pdfcrowd.HtmlToPdfClient('ariaschmario', 'c9aeae493b830137cf765dcd473ad9f1')
#
#             # run the conversion and write the result to a file
#             client.convertUrlToFile('http://www.google.com', 'tmp/example1.pdf')
#             self.upload_blob('personerias', 'tmp/example1.pdf', 'GooglePdf1.pdf')
#
#         except pdfcrowd.Error as why:
#             # report the error
#             sys.stderr.write('Pdfcrowd Error: {}\n'.format(why))
#
#             # rethrow or handle the exception
#             raise
