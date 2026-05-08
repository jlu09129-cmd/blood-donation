from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, HealthStatus, Request
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.utils import timezone

from .serializers import (
    UserSerializer,
    HealthStatusSerializer,
    RequestSerializer
)
# --------------------------------------------------
# User ViewSet (CRUD for Users / Donors)
# --------------------------------------------------
class UserViewSet(viewsets.ModelViewSet):
    """
    Provides Create, Read, Update, Delete operations
    for User (Donor) model automatically.
    """

    # Fetch all user records from database
    queryset = User.objects.all()

    # Serializer used to convert model data to JSON and vice versa
    serializer_class = UserSerializer


# --------------------------------------------------
# Donor Search API
# --------------------------------------------------
class DonorSearchAPIView(APIView):
    """
    Search donors based on blood group, city and state.
    This API is read-only (GET).
    """

    def get(self, request):
        # Get query parameters from URL
        blood_group = request.GET.get("blood_group")
        city = request.GET.get("city")
        state = request.GET.get("state")

        # Fetch only available donors
        users = User.objects.filter(availability="Yes")

        # Apply filters only if values are provided
        if blood_group:
            users = users.filter(blood_group=blood_group)

        if city:
            users = users.filter(city__iexact=city)

        if state:
            users = users.filter(state__iexact=state)

        # Convert queryset to JSON format
        serializer = UserSerializer(users, many=True)

        # Return successful response
        return Response(serializer.data, status=status.HTTP_200_OK)


# --------------------------------------------------
# Health Status ViewSet (CRUD)
# --------------------------------------------------
class HealthStatusViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD operations for HealthStatus model.
    """

    # Fetch all health status records
    queryset = HealthStatus.objects.all()

    # Serializer for HealthStatus model
    serializer_class = HealthStatusSerializer


# --------------------------------------------------
# Get Health Status by User ID
# --------------------------------------------------
class HealthStatusByUserAPIView(APIView):
    """
    Fetch health status of a specific user using user_id.
    """

    def get(self, request, user_id):
        try:
            # Fetch health status using foreign key relation
            health = HealthStatus.objects.get(user__user_id=user_id)

            # Serialize health status data
            serializer = HealthStatusSerializer(health)

            # Return success response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except HealthStatus.DoesNotExist:
            # Return error if health status not found
            return Response(
                {"error": "Health status not found"},
                status=status.HTTP_404_NOT_FOUND
            )


# --------------------------------------------------
# Blood Request ViewSet (CRUD)
# --------------------------------------------------
class RequestViewSet(viewsets.ModelViewSet):
    """
    Provides Create, Read, Update, Delete operations
    for Blood Request model.
    """

    # Fetch all blood requests
    queryset = Request.objects.all()

    # Serializer for Request model
    serializer_class = RequestSerializer


# --------------------------------------------------
# Update Blood Request Status API
# --------------------------------------------------
class UpdateRequestStatusAPIView(APIView):
    """
    Update only the status field of a blood request.
    Uses PATCH method.
    """

    def patch(self, request, request_id):
        try:
            # Fetch request using request_id
            blood_request = Request.objects.get(request_id=request_id)

            # Get new status from request body
            status_value = request.data.get("status")

            # Validate status input
            if not status_value:
                return Response(
                    {"error": "Status is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Update request status
            blood_request.status = status_value
            blood_request.save()

            # Serialize updated request
            serializer = RequestSerializer(blood_request)

            # Return success response
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Request.DoesNotExist:
            # Return error if request not found
            return Response(
                {"error": "Request not found"},
                status=status.HTTP_404_NOT_FOUND
            )
def home(request):
    return render(request, 'index.html', )

def donors(request):
    donors = User.objects.all().order_by('-created_at')
    return render(request, 'donors.html', {'donors': donors})

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Message sent successfully.')
        return redirect('contact')

    return render(request, 'contact.html', )

def _next_request_id():
    last_request = Request.objects.order_by('-created_at').first()
    if not last_request:
        return 'R001'

    try:
        next_number = int(last_request.request_id.lstrip('R')) + 1
    except ValueError:
        next_number = Request.objects.count() + 1

    request_id = f'R{next_number:03d}'
    while Request.objects.filter(request_id=request_id).exists():
        next_number += 1
        request_id = f'R{next_number:03d}'

    return request_id


def request(request):
    if request.method == 'POST':
        blood_group = request.POST.get('blood_group')
        units_required = request.POST.get('units_required')
        hospital_name = request.POST.get('hospital_name', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not blood_group or not units_required or not phone:
            messages.error(request, 'Blood group, units required, and phone number are required.')
            return render(request, 'request.html')

        try:
            units_required = int(units_required)
        except ValueError:
            messages.error(request, 'Units required must be a valid number.')
            return render(request, 'request.html')

        if units_required < 1:
            messages.error(request, 'Units required must be at least 1.')
            return render(request, 'request.html')

        Request.objects.create(
            request_id=_next_request_id(),
            user=User.objects.filter(phone=phone).first(),
            blood_group=blood_group,
            units_required=units_required,
            hospital_name=hospital_name,
            city=city,
            state=state,
            phone=phone,
            request_date=timezone.localdate(),
            status='Pending',
        )

        messages.success(request, 'Blood request posted successfully.')
        return redirect('request')

    return render(request, 'request.html')

def _next_user_id():
    last_user = User.objects.order_by('-created_at').first()
    if not last_user:
        return 'U001'

    try:
        next_number = int(last_user.user_id.lstrip('U')) + 1
    except ValueError:
        next_number = User.objects.count() + 1

    user_id = f'U{next_number:03d}'
    while User.objects.filter(user_id=user_id).exists():
        next_number += 1
        user_id = f'U{next_number:03d}'

    return user_id


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        age = request.POST.get('age')
        blood_group = request.POST.get('blood_group')
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        last_donation_date = request.POST.get('last_donation_date') or None

        if not age or not blood_group or not phone:
            messages.error(request, 'Age, blood group, and phone number are required.')
            return render(request, 'register.html')

        try:
            age = int(age)
        except ValueError:
            messages.error(request, 'Age must be a valid number.')
            return render(request, 'register.html')

        if age < 18:
            messages.error(request, 'Donors must be at least 18 years old.')
            return render(request, 'register.html')

        try:
            User.objects.create(
                user_id=_next_user_id(),
                name=name,
                age=age,
                blood_group=blood_group,
                city=city,
                state=state,
                phone=phone,
                last_donation_date=last_donation_date,
                availability='Yes',
            )
        except IntegrityError:
            messages.error(request, 'A donor with this phone number already exists.')
            return render(request, 'register.html')

        messages.success(request, 'Donor registered successfully.')
        return redirect('donor')

    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html', )
       
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User


@csrf_exempt
def add_donor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # ✅ Validation
            required_fields = ['user_id', 'age', 'blood_group', 'phone']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'error': f'{field} is required'
                    }, status=400)

            # ✅ Check if user already exists
            if User.objects.filter(user_id=data['user_id']).exists():
                return JsonResponse({
                    'error': 'User already exists'
                }, status=400)

            # ✅ Create donor
            user = User.objects.create(
                user_id=data.get('user_id') or _next_user_id(),
                name=data.get('name') or data.get('full_name'),
                age=data['age'],
                blood_group=data['blood_group'],
                city=data.get('city'),
                state=data.get('state'),
                phone=data['phone'],
                last_donation_date=data.get('last_donation_date'),
                availability=data.get('availability', 'Yes')
            )

            return JsonResponse({
                'success': True,
                'message': 'Donor added successfully',
                'data': {
                    'user_id': user.user_id,
                    'blood_group': user.blood_group
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
