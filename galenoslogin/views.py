from django.shortcuts import render, redirect, get_object_or_404


from .forms import ReservarCitaForm
from .models import Reserva
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def indexwithlogin(request):
    return render(request, 'galenoslogin/indexwithlogin.html', {})

def reservarCita(request):
    if request.method == 'POST':
        form = ReservarCitaForm(request.POST)
        if form.is_valid():
            reserva = Reserva(
                rut=form.cleaned_data['rut'],
                sucursal=form.cleaned_data['sucursal'],
                prevision=form.cleaned_data['prevision'],
                especialidad=form.cleaned_data['especialidad'],
                fecha=form.cleaned_data['fecha'],
                email=form.cleaned_data['email']
            )
            

            # Enviar correo electrónico con los detalles de la reserva
            subject = 'Confirmación de Reserva'
            message = f"""
            Estimado/a,

            Su reserva ha sido confirmada con los siguientes detalles:
            
            RUT: {reserva.rut}
            Sucursal: {reserva.sucursal}
            Previsión: {reserva.prevision}
            Especialidad: {reserva.especialidad}
            Fecha: {reserva.fecha}
            Email: {reserva.email}
            
            Gracias por utilizar nuestro servicio.

            Atentamente,
            Tu Equipo de Reservas
            """
            recipient_list = [reserva.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            reserva.save()

            return redirect('reservaRealizada')
    else:
        form = ReservarCitaForm()
    return render(request, 'galenoslogin/reservarCita.html', {'form': form})

from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from .models import Reserva

def reserva_del(request, pk):
    context = {}
    try:
        reserva = Reserva.objects.get(id=pk)  # Assuming 'id' is the primary key field of the Reserva model

        # Guardar el email antes de eliminar la reserva
        email = reserva.email

        reserva.delete()
        mensaje = "Bien, datos eliminados..."
        reservas = Reserva.objects.all()  # Retrieve the remaining reservations
        context = {'reservas': reservas, 'mensaje': mensaje}  # Update the context with the remaining reservations

        # Enviar correo electrónico notificando al usuario que su reserva ha sido cancelada
        subject = 'Cancelación de Reserva'
        message = f"""
        Estimado/a,

        Lamentamos informarle que su reserva ha sido cancelada.

        Si tiene alguna pregunta o necesita más información, no dude en ponerse en contacto con nosotros.

        Atentamente,
        Tu Equipo de Reservas
        """
        recipient_list = [email]
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

    except Reserva.DoesNotExist:
        mensaje = "Error, reserva no existe..."
        reservas = Reserva.objects.all()  # Retrieve all reservations
        context = {'reservas': reservas, 'mensaje': mensaje}  # Update the context with all reservations

    return render(request, 'galenoslogin/admin.html', context)


def reservaRealizada(request):
    return render(request, 'galenoslogin/reservaRealizada.html', {})

def admin(request):
    reservas = Reserva.objects.all()
    return render(request, 'galenoslogin/admin.html', {'reservas': reservas})

def editar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == "POST":
        form = ReservarCitaForm(request.POST)
        if form.is_valid():
            reserva.rut = form.cleaned_data['rut']
            reserva.sucursal = form.cleaned_data['sucursal']
            reserva.prevision = form.cleaned_data['prevision']
            reserva.especialidad = form.cleaned_data['especialidad']
            reserva.fecha = form.cleaned_data['fecha']
            reserva.email = form.cleaned_data['email']
            reserva.save()

            # Enviar correo electrónico notificando al usuario que su reserva ha sido modificada
            subject = 'Modificación de Reserva'
            message = f"""
            Estimado/a,

            Su reserva ha sido modificada con los siguientes detalles:
            
            RUT: {reserva.rut}
            Sucursal: {reserva.sucursal}
            Previsión: {reserva.prevision}
            Especialidad: {reserva.especialidad}
            Fecha: {reserva.fecha}
            Email: {reserva.email}
            
            Si tiene alguna pregunta, no dude en ponerse en contacto con nosotros.

            Atentamente,
            Tu Equipo de Reservas
            """
            recipient_list = [reserva.email]
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)

            return redirect('admin')
    else:
        form = ReservarCitaForm(initial={
            'rut': reserva.rut,
            'sucursal': reserva.sucursal,
            'prevision': reserva.prevision,
            'especialidad': reserva.especialidad,
            'fecha': reserva.fecha,
            'email': reserva.email
        })
    return render(request, 'galenoslogin/editar_reserva.html', {'form': form})