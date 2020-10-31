import os

import firebase_admin
from firebase_admin import auth
from django.http import HttpResponseRedirect, FileResponse, JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic.base import View
from google.cloud import storage
import pdfcrowd
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from urllib.request import urlopen


from elElectricistaProject import settings
from .models import Ticket, TicketCreateForm, Client, GeneralInfo, GeneralInfoUpdateForm, EquipoAcometidaUpdateForm, EquipoAcometida, CentroCarga, \
    CentroCargaUpdateForm, CircuitosRamales, CircuitosRamalesUpdateForm, GeneralRecomendatios, GeneralRecomendationsUpdateForm, CentroCargaSecundario
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect

default_app = firebase_admin.initialize_app()
user = None


class LoginView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "login.html")




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

    def access_secret_version(self, project_manager_id, secret_id, version_id):
        """
        Access the payload for the given secret version if one exists. The version
        can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
        """

        # Import the Secret Manager client library.
        from google.cloud import secretmanager

        # Create the Secret Manager client.
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{project_manager_id}/secrets/{secret_id}/versions/{version_id}"

        # Access the secret version.
        response = client.access_secret_version(request={"name": name})

        # Print the secret payload.
        #
        # WARNING: Do not print the secret in a production environment - this
        # snippet is showing how to access the secret material.
        payload = response.payload.data.decode("UTF-8")
        return payload


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        if 'sigt' in self.request.POST:
            me = pdfcrowd.HtmlToPdfClient('ariaschmario', os.getenv('PDFCROWD_PASSWORD'))
            context = {'ticket': Ticket.objects.get(superId=self.kwargs['slug'])}
            x = render_to_string('pdf.html', context)

            me.setPageSize(u'Letter')
            me.setOrientation(u'landscape')
            response = HttpResponse(content_type='application/pdf')
            me.convertStringToStream(x, response)

            storage_client = storage.Client()

            bucket = storage_client.bucket('elelectricista')
            blob = bucket.blob('boletas/' + self.kwargs['slug'] + '.pdf')
            filePfd = response.getvalue()
            blob.upload_from_string(filePfd, content_type='application/pdf')
            Ticket.objects.get(superId=self.kwargs['slug']).update_file_url('https://storage.cloud.google.com/elelectricista/boletas/' + self.kwargs['slug'] + '.pdf')

            mail_content = "Te adjuntamos la boleta técnica de la visita de El Electricista"
            sender_address = 'mario@zacatearca.com'
            #sender_pass = self.access_secret_version(os.getenv('PROJECT_SECRET_MANAGER_ID'), os.getenv('GMAIL_APP_PASSWORD_ID'), 1),
            sender_pass = os.getenv('GMAIL_PASSWORD_ID')
            receiver_address = 'ariaschmario@gmail.com'
            # Setup the MIME
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'El Electricista Boleta'
            # The subject line
            # The body and the attachments for the mail
            message.attach(MIMEText(mail_content, 'plain'))
            # attach_file = open(filePfd, 'rb')  # Open the file as binary mode
            payload = MIMEBase('application', 'octate-stream')
            payload.set_payload(filePfd)
            encoders.encode_base64(payload)  # encode the attachment
            # add payload header with filename
            filename = "boleta.pdf"
            payload.add_header('Content-Disposition', 'attachment; filename="%s"' % filename)
            message.attach(payload)
            # Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
            session.starttls()  # enable security
            session.login(sender_address, sender_pass[0])  # login with mail_id and password
            text = message.as_string()
            session.sendmail(sender_address, receiver_address, text)
            session.quit()

            return redirect("core:sended", slug=self.kwargs['slug'])
        else:
            return redirect("core:circuitosramales", slug=self.kwargs['slug'])

    def form_invalid(self, form):
        return redirect("core:login")

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
        return redirect("core:login")

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
        return redirect("core:login")

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
        return redirect("core:login")

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
        return redirect("core:login")

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

    def get(self, *args, **kwargs):
        userId = kwargs["user"]
        try:
            auth.verify_id_token(userId, check_revoked=True)
        except auth.RevokedIdTokenError as ex:
            return redirect("core:login")
        except auth.ExpiredIdTokenError as ex:
            return redirect("core:login")
        except auth.InvalidIdTokenError as ex:
            return redirect("core:login")
        global user
        user = True
        return render(self.request, self.template_name, {'form': self.form_class})

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


