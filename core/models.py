from autoslug import AutoSlugField
from django.db import models
from django.shortcuts import reverse
from django import forms
from django.utils.text import slugify

LABEL_CHOICES = (
    ('c', 'Cédula'),
    ('d', 'Dimex'),
    ('p', 'Pasaporte'),
    ('a', 'Otro')
)

PROPOERTY_TYPE_CHOICES = (
    ('c', 'Casa de habitación'),
    ('a', 'Apartamento'),
    ('l', 'Local Comercial'),
    ('o', 'Oficina')
)

KIND_VISIT = (
    ('a', 'Avería'),
    ('i', 'Inspección'),
)

ELECTRIC_COMPANY = (
    ('c', 'CNFL'),
    ('i', 'ICE'),
    ('e', 'ESPH'),
    ('j', 'JASEC'),
    ('a', 'Otro'),
)

YES_NO = (
    ('a', 'Sí'),
    ('n', 'No')
)

RATE_TYPE = (
    ('c', 'Comercial'),
    ('r', 'Residencial'),
    ('a', 'Otro')
)

BAJANTE_ACOMETIDA = (
    ('a', 'Aereo'),
    ('s', 'Subterraneo'),
    ('c', 'Cruce de calle'),
    ('f', 'Frente a casa')
)

EQUIPO_MEDICION = (
    ('c', 'Base clase 100'),
    ('d', 'Base clase 200'),
    ('i', 'Indirecto'),
    ('b', 'Base con breaker principal'),
    ('d', 'Ducto de medidor'),
    ('a', 'Otro tipo de interruptor')
)

ESTADO = (
    ('b', 'Bueno'),
    ('r', 'Regular'),
    ('d', 'Dificiente')
)

UBICACION = (
    ('a', 'Accesible'),
    ('f', 'Fácilmente Accesible'),
    ('p', 'Poco Accesible')
)

class Client(models.Model):
    legalId = models.CharField(max_length=15)
    slug = models.CharField(max_length=15, default=None, blank=True, null=True)
    idType = models.CharField(choices=LABEL_CHOICES, max_length=1, default='o')
    name = models.CharField(max_length=25)
    phoneNumber = models.CharField(max_length=15)
    email = models.CharField(max_length=25)
    adress = models.CharField(max_length=200)

    def __str__(self):
        return self.legalId

    def get_id(self):
        return self.legalId

    def get_absolute_url(self):
        return reverse('core:login')

class CalibreConductores(models.Model):
    f1 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f2 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f3 = models.CharField(max_length=15, default=None, blank=True, null=True)
    n = models.CharField(max_length=15, default=None, blank=True, null=True)
    t = models.CharField(max_length=15, default=None, blank=True, null=True)


    def __str__(self):
        return "Calibre de Condutores"




class VoltajesEntrada(models.Model):
    f1 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f2 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f3 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f1_f2 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f2_f3 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f1_f3 = models.CharField(max_length=15, default=None, blank=True, null=True)

    def __str__(self):
        return "Voltajes de entrada"


class CorrienteEntrada(models.Model):
    f1 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f2 = models.CharField(max_length=15, default=None, blank=True, null=True)
    f3 = models.CharField(max_length=15, default=None, blank=True, null=True)

    def __str__(self):
        return "Corriente de entrada"


class CircuitosRamales(models.Model):
    superId = models.CharField(max_length=15)
    slug = models.CharField(max_length=15, default=None, blank=True, null=True)
    resultado = models.CharField(max_length=900, default=None, blank=True, null=True)

    def __str__(self):
        return self.superId

    def get_id(self):
        return self.superId

    def get_absolute_url(self):
        return reverse('core:login')


class GeneralRecomendatios(models.Model):
    superId = models.CharField(max_length=15)
    slug = models.CharField(max_length=15, default=None, blank=True, null=True)
    result = models.CharField(max_length=900, default=None, blank=True, null=True)

    def __str__(self):
        return self.superId

    def get_id(self):
        return self.superId

    def get_absolute_url(self):
        return reverse('core:login')


class CentroCarga(models.Model):
    superId = models.CharField(max_length=15)
    slug = models.CharField(max_length=15, default=None, blank=True, null=True)
    marca_catalogo = models.CharField(max_length=25, default=None, blank=True, null=True)
    espacios_ocupados = models.CharField(max_length=25, default=None, blank=True, null=True)
    estado_tablero = models.CharField(choices=ESTADO, max_length=1)
    estado_tablero_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    ubicacion = models.CharField(choices=UBICACION, max_length=1, default=None, blank=True, null=True)
    canalizacion = models.CharField(choices=ESTADO, max_length=1, default=None, blank=True, null=True)
    canalizacion_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    canalizacion_distancia = models.CharField(max_length=25, default=None, blank=True, null=True)
    estado_alimentadores = models.CharField(choices=ESTADO, max_length=1)
    estado_alimentadores_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    estado_puesta = models.CharField(choices=ESTADO, max_length=1)
    estado_puesta_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)

    prueba_carga_f1_v = models.CharField(max_length=25, default=None, blank=True, null=True)
    prueba_carga_f1_a = models.CharField(max_length=25, default=None, blank=True, null=True)
    prueba_carga_f2_v = models.CharField(max_length=25, default=None, blank=True, null=True)
    prueba_carga_f2_a = models.CharField(max_length=25, default=None, blank=True, null=True)
    prueba_carga_f3_v = models.CharField(max_length=25, default=None, blank=True, null=True)
    prueba_carga_f3_a = models.CharField(max_length=25, default=None, blank=True, null=True)
    prueba_carga_n_a = models.CharField(max_length=25, default=None, blank=True, null=True)
    nota = models.CharField(max_length=25, default=None, blank=True, null=True)
    resultado = models.CharField(max_length=900, default=None, blank=True, null=True)

    def __str__(self):
        return self.superId

    def get_id(self):
        return self.superId

    def get_absolute_url(self):
        return reverse('core:login')


class CentroCargaSecundario(models.Model):
    principal = models.ForeignKey(CentroCarga, on_delete=models.CASCADE, default=None, blank=True, null=True, related_name='secundarios')
    local_id = models.CharField(max_length=25, default=None, blank=True, null=True)
    marca_catalogo = models.CharField(max_length=25, default=None, blank=True, null=True)
    espacios_ocupados = models.CharField(max_length=25, default=None, blank=True, null=True)
    estado_tablero = models.CharField(choices=ESTADO, max_length=1)
    estado_tablero_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    ubicacion = models.CharField(choices=UBICACION, max_length=1, default=None, blank=True, null=True)
    canalizacion = models.CharField(choices=ESTADO, max_length=1, default=None, blank=True, null=True)
    canalizacion_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    canalizacion_distancia = models.CharField(max_length=25, default=None, blank=True, null=True)
    estado_alimentadores = models.CharField(choices=ESTADO, max_length=1)
    estado_alimentadores_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    estado_puesta = models.CharField(choices=ESTADO, max_length=1)
    estado_puesta_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)

    def __str__(self):
        return self.local_id

    def get_id(self):
        return self.local_id

    def get_add_centro(self):
        return reverse("core:centroCargaSecundario", kwargs={
            'slug': self.slug
        })

    def get_absolute_url(self):
        return reverse("core:centroCargaSecundario", kwargs={
            'slug': self.slug
        })


class EquipoAcometida(models.Model):
    superId = models.CharField(max_length=15)
    slug = models.CharField(max_length=15, default=None, blank=True, null=True)
    bajante_acometida = models.CharField(choices=BAJANTE_ACOMETIDA, max_length=1, default=None, blank=True, null=True)
    equipo_medicion = models.CharField(choices=EQUIPO_MEDICION, max_length=1, default=None, blank=True, null=True)
    equipo_medicion_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    estado_interruptor = models.CharField(choices=ESTADO, max_length=1)
    estado_interruptor_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    estado_alimentadores = models.CharField(choices=ESTADO, max_length=1)
    estado_alimentadores_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    calibre_conductores_f1 = models.CharField(max_length=25, default=None, blank=True, null=True)
    calibre_conductores_f2 = models.CharField(max_length=25, default=None, blank=True, null=True)
    calibre_conductores_f3 = models.CharField(max_length=25, default=None, blank=True, null=True)
    calibre_conductores_n = models.CharField(max_length=25, default=None, blank=True, null=True)
    calibre_conductores_t = models.CharField(max_length=25, default=None, blank=True, null=True)
    voltajes_entrada_f1 = models.CharField(max_length=25, default=None, blank=True, null=True)
    voltajes_entrada_f2 = models.CharField(max_length=25, default=None, blank=True, null=True)
    voltajes_entrada_f3 = models.CharField(max_length=25, default=None, blank=True, null=True)
    voltajes_entrada_f1_f2 = models.CharField(max_length=25, default=None, blank=True, null=True)
    voltajes_entrada_f2_f3 = models.CharField(max_length=25, default=None, blank=True, null=True)
    voltajes_entrada_f1_f3 = models.CharField(max_length=25, default=None, blank=True, null=True)
    corriente_entrada_f1 = models.CharField(max_length=25, default=None, blank=True, null=True)
    corriente_entrada_f2 = models.CharField(max_length=25, default=None, blank=True, null=True)
    corriente_entrada_f3 = models.CharField(max_length=25, default=None, blank=True, null=True)
    estado_puesta = models.CharField(choices=ESTADO, max_length=1)
    estado_puesta_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    estado_neutro = models.CharField(choices=ESTADO, max_length=1, default=None, blank=True, null=True)
    estado_neutro_especifique = models.CharField(max_length=250, default=None, blank=True, null=True)
    resultado = models.CharField(max_length=900, default=None, blank=True, null=True)

    def __str__(self):
        return self.superId

    def get_id(self):
        return self.superId

    def get_absolute_url(self):
        return reverse('core:login')


class GeneralInfo(models.Model):
    superId = models.CharField(max_length=15)
    slug = AutoSlugField(populate_from='superId', always_update=True, default=None, blank=True, null=True)
    kind_visit = models.CharField(choices=KIND_VISIT, max_length=1, default=None, blank=True, null=True)
    property_type = models.CharField(choices=PROPOERTY_TYPE_CHOICES, max_length=1)
    company = models.CharField(choices=ELECTRIC_COMPANY, max_length=1)
    another_company = models.CharField(max_length=25, default=None, blank=True, null=True)
    rate_type = models.CharField(choices=RATE_TYPE, max_length=1)
    another_rate_type = models.CharField(max_length=25, default=None, blank=True, null=True)
    nise_or_location = models.CharField(max_length=25, default=None, blank=True, null=True)
    meter_number = models.CharField(max_length=25, default=None, blank=True, null=True)
    solar_generation = models.CharField(choices=YES_NO, max_length=1)
    solar_generation_capacity = models.CharField(max_length=25, default=None, blank=True, null=True)

    def __str__(self):
        return self.superId

    def get_id(self):
        return self.superId

    def get_absolute_url(self):
        return reverse('core:login')


class Ticket(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tickets')
    equipo_acometida = models.ForeignKey(EquipoAcometida, on_delete=models.CASCADE, default=None, blank=True, null=True)
    circuitos_ramales = models.ForeignKey(CircuitosRamales, on_delete=models.CASCADE, default=None, blank=True, null=True)
    general_info = models.ForeignKey(GeneralInfo, on_delete=models.CASCADE, default=None, blank=True, null=True)
    centro_carga = models.ForeignKey(CentroCarga, on_delete=models.CASCADE, default=None, blank=True, null=True)
    general_recomendations = models.ForeignKey(GeneralRecomendatios, on_delete=models.CASCADE, default=None, blank=True, null=True)
    file_url = models.CharField(max_length=300, default=None, blank=True, null=True)
    superId = models.CharField(max_length=15)

    def __str__(self):
        return self.superId

    def get_id(self):
        return self.superId

    def update_file_url(self, url):
        self.file_url = url
        self.save()

    def set_superId(self, new_super_id):
        self.superId = new_super_id
        self.general_info.superId = new_super_id
        self.general_info.slug = new_super_id
        self.general_info.save()
        self.equipo_acometida.superId = new_super_id
        self.equipo_acometida.slug = new_super_id
        self.equipo_acometida.save()
        self.centro_carga.superId = new_super_id
        self.centro_carga.slug = new_super_id
        self.centro_carga.save()
        self.circuitos_ramales.superId = new_super_id
        self.circuitos_ramales.slug = new_super_id
        self.circuitos_ramales.save()
        self.general_recomendations.superId = new_super_id
        self.general_recomendations.slug = new_super_id
        self.general_recomendations.save()
        self.client.legalId = new_super_id[0:-2]
        self.client.slug = new_super_id[0:-2]
        self.client.save()
        self.save()



NULL_AND_BLANK = {'null': True, 'blank': True}


class Book(models.Model):
    title = models.CharField(max_length=100)
    isbn = models.CharField(max_length=100, unique=True)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:create')


# books/forms.py
class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError("You have already written a book with same title.")
        return title


class TicketCreateForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['slug']

    def __init__(self, *args, **kwargs):
        super(TicketCreateForm, self).__init__(*args, **kwargs)


class GeneralInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = GeneralInfo
        exclude = ['superId']

    def __init__(self, *args, **kwargs):
        super(GeneralInfoUpdateForm, self).__init__(*args, **kwargs)

class EquipoAcometidaUpdateForm(forms.ModelForm):
    class Meta:
        model = EquipoAcometida
        exclude = ['superId']

    def __init__(self, *args, **kwargs):
        super(EquipoAcometidaUpdateForm, self).__init__(*args, **kwargs)


class CentroCargaUpdateForm(forms.ModelForm):
    class Meta:
        model = CentroCarga
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CentroCargaUpdateForm, self).__init__(*args, **kwargs)


class CircuitosRamalesUpdateForm(forms.ModelForm):
    class Meta:
        model = CircuitosRamales
        exclude = ['superId']

    def __init__(self, *args, **kwargs):
        super(CircuitosRamalesUpdateForm, self).__init__(*args, **kwargs)


class GeneralRecomendationsUpdateForm(forms.ModelForm):
    class Meta:
        model = GeneralRecomendatios
        exclude = ['superId']

    def __init__(self, *args, **kwargs):
        super(GeneralRecomendationsUpdateForm, self).__init__(*args, **kwargs)


