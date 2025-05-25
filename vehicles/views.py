from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  
from .models import Vehicle
from .forms import VehicleForm
from django.utils.timezone import now
from reminders.models import Reminder 
from django.db import IntegrityError
from django.core.paginator import Paginator


@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # Normalize input data
            vehicle_name = form.cleaned_data['vehicle_name'].strip().upper()
            model = form.cleaned_data['model'].strip().upper()
            plate_number = form.cleaned_data['plate_number'].strip().upper()

            # Check for existing vehicle with same details
            existing_vehicle = Vehicle.objects.filter(
                user=request.user,
                vehicle_name__iexact=vehicle_name,
                model__iexact=model,
                plate_number__iexact=plate_number
            ).first()

            if existing_vehicle:
                # Check if reminder is still active
                reminder = Reminder.objects.filter(
                    vehicle=existing_vehicle,
                    user=request.user,
                    status='pending'
                ).order_by('-reminder_date').first()

                if reminder and existing_vehicle.expiry_date >= now().date():
                    messages.error(
                        request,
                        "A vehicle with these details already exists and has an active reminder."
                    )
                    return render(request, 'vehicles/add_vehicle.html', {'form': form})

            # Save the vehicle
            vehicle = form.save(commit=False)
            vehicle.user = request.user
            vehicle.vehicle_name = vehicle_name
            vehicle.model = model
            vehicle.plate_number = plate_number

            try:
                vehicle.save()
                messages.success(request, "Vehicle added successfully!")
                return redirect('dashboard')
            except IntegrityError:
                messages.error(
                    request,
                    "A vehicle with these details already exists. Please check your input."
                )
                return render(request, 'vehicles/add_vehicle.html', {'form': form})
        else:
            messages.error(request, "There was an error in the form. Please check the details.")
    else:
        form = VehicleForm(user=request.user)

    return render(request, 'vehicles/add_vehicle.html', {'form': form})


@login_required
def edit_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle, user=request.user)
        if form.is_valid():
            vehicle_name = form.cleaned_data['vehicle_name']
            model = form.cleaned_data['model']
            plate_number = form.cleaned_data['plate_number']

            # Check for conflicts with other vehicles
            conflicting_vehicle = Vehicle.objects.filter(
                user=request.user,
                vehicle_name__iexact=vehicle_name,
                model__iexact=model,
                plate_number__iexact=plate_number
            ).exclude(pk=vehicle.pk).first()

            if conflicting_vehicle:
                reminder = Reminder.objects.filter(
                    vehicle=conflicting_vehicle,
                    user=request.user,
                    status='pending'
                ).order_by('-reminder_date').first()

                if reminder and conflicting_vehicle.expiry_date >= now().date():
                    messages.error(request, "Another vehicle with these details exists and has an active reminder.")
                    return render(request, 'vehicles/edit_vehicle.html', {'form': form})

            try:
                form.save()
                messages.success(request, "Vehicle details updated successfully!")
                return redirect('dashboard')
            except IntegrityError:
                messages.error(request, "A vehicle with this plate number already exists for your account.")
                return render(request, 'vehicles/edit_vehicle.html', {'form': form})
        else:
            messages.error(request, "There was an error in the form. Please check the details.")
    else:
        form = VehicleForm(instance=vehicle, user=request.user)

    return render(request, 'vehicles/edit_vehicle.html', {'form': form})


@login_required
def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, user=request.user)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully.")  # Success message
        return redirect('dashboard')
    return render(request, 'vehicles/delete_vehicle_confirm.html', {'vehicle': vehicle})


@login_required
def user_vehicles(request):
    vehicle_list = Vehicle.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(vehicle_list, 5)  # Show 5 vehicles per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vehicles/user_vehicles.html', {'page_obj': page_obj})
