from rest_framework.decorators import api_view
from rest_framework.response import Response


from django.contrib.auth import authenticate
from rest_framework.decorators import authentication_classes, permission_classes


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password


from .models import Turf, Booking, UserCode
from .serializers import TurfSerializer,BookingSerializer


@api_view(['POST'])
def add_turf(request):
    data = TurfSerializer(data=request.data)

    if data.is_valid():
        data.save()
        return Response({"message": "Turf added successfully"})

    return Response(data.errors)
@api_view(['GET'])
def view_turf(request):
    data = Turf.objects.all()
    serializer = TurfSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def update_turf(request, id):
    try:
        turf = Turf.objects.get(id=id)
    except Turf.DoesNotExist:
        return Response({"message": "Turf not found"})

    serializer = TurfSerializer(turf, data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"message": "Turf updated successfully"})

    return Response(serializer.errors)

@api_view(['DELETE'])
def delete_turf(request, id):
    try:
        turf = Turf.objects.get(id=id)
        turf.delete()
        return Response({"message": "Turf deleted successfully"})

    except Turf.DoesNotExist:
        return Response({"message": "Turf not found"})

@api_view(['POST'])
def add_booking(request):

    turf_id = request.data.get('turf')
    booking_date = request.data.get('booking_date')
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')

    # Check existing booking
    existing_booking = Booking.objects.filter(
        turf_id=turf_id,
        booking_date=booking_date,
        status__in=[0, 1],
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exists()

    if existing_booking:
        return Response({
            "message": "This turf is already booked for this time"
        })

    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Booking added successfully"
        })

    return Response(serializer.errors)

@api_view(['GET'])
def view_booking(request):
    data = Booking.objects.all()
    serializer = BookingSerializer(data, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def cancel_booking(request, id):

    try:
        booking = Booking.objects.get(id=id)
    except Booking.DoesNotExist:
        return Response({"message": "Booking not found"})

    if booking.status == 2:
        return Response({"message": "Booking already cancelled"})

    booking.status = 2
    booking.save()

    return Response({"message": "Booking cancelled successfully"})

@api_view(['GET'])
def single_booking(request, id):

    try:
        booking = Booking.objects.get(id=id)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    except Booking.DoesNotExist:
        return Response({"message": "Booking not found"})

@api_view(['POST'])
def register_user(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"})

    if User.objects.filter(email=email).exists():
        return Response({"message": "Email already registered"})

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    return Response({
        "message": "Registration successful",
        "user_id": user.id
    })


@api_view(['POST'])
def login_user(request):

    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:

        token, created = Token.objects.get_or_create(user=user)

        user_code, created = UserCode.objects.get_or_create(
        user=user,
        defaults={
        'code': f"TOKEN{user.id:03d}"
    }
)

        return Response({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username,
            "user_code": user_code.code,
            "token": token.key
        })

    else:
        return Response({
            "message": "Invalid username or password"
        })

@api_view(['POST'])
def register_user(request):

    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({"message": "Username already exists"})

    if User.objects.filter(email=email).exists():
        return Response({"message": "Email already registered"})

    user = User.objects.create(
        username=username,
        email=email,
        password=make_password(password)
    )

    # Generate unique ascending code
    user_code = f"TOKEN{user.id:03d}"

    UserCode.objects.create(
        user=user,
        code=user_code
    )

    return Response({
        "message": "Registration successful",
        "user_id": user.id,
        "user_code": user_code
    })


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_booking(request):

    turf_id = request.data.get('turf')
    booking_date = request.data.get('booking_date')
    start_time = request.data.get('start_time')
    end_time = request.data.get('end_time')

    existing_booking = Booking.objects.filter(
        turf_id=turf_id,
        booking_date=booking_date,
        status__in=[0, 1],
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exists()

    if existing_booking:
        return Response({
            "message": "This turf is already booked for this time"
        })

    serializer = BookingSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({
            "message": "Booking added successfully"
        })

    return Response(serializer.errors)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_booking(request):
    bookings = Booking.objects.all()
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def view_booking(request):

    bookings = Booking.objects.filter(user=request.user)

    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def cancel_booking(request, id):

    try:
        booking = Booking.objects.get(
            id=id,
            user=request.user
        )

        booking.status = 2
        booking.save()

        return Response({
            "message": "Booking cancelled successfully"
        })

    except Booking.DoesNotExist:
        return Response({
            "message": "Booking not found"
        }, status=404)