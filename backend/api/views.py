from django.conf import settings
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project, ContactMessage, HireRequest
from .serializers import (
    ProjectSerializer,
    ContactMessageSerializer,
    HireRequestSerializer,
)
from .utils import get_github_projects
from django.http import JsonResponse
from django.db import transaction
import os
@api_view(['POST'])
def sync_github_projects(request):
    """
    Fetch GitHub repos for a user, save them to the database atomically, and return them.
    """
    username = request.data.get('username', 'wess-westley')
    projects_data = get_github_projects(username)

    saved_projects = []
    try:
        with transaction.atomic():
            for proj in projects_data:
                obj, created = Project.objects.update_or_create(
                    title=proj['title'],
                    defaults={
                        'description': proj.get('description', ''),
                        'tech_stack': proj.get('tech_stack', ''),
                        'github_url': proj.get('github_url', f"https://github.com/{username}/{proj['title']}"),
                       'demo_url': proj.get('demo_url') or f"https://{username}.github.io/{proj['title']}",

                    }
                )
                saved_projects.append(obj)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = ProjectSerializer(saved_projects, many=True)
    return Response({'projects': serializer.data}, status=status.HTTP_200_OK)

# --- Root API Test ---
def api_root(request):
    return JsonResponse({"message": "API is working!"})

@api_view(['GET'])
def profile_picture(request):
    picture_url = getattr(
        settings,
        'PROFILE_PICTURE_URL',
        'https://example.com/path/to/westley.jpg'
    )
    return Response({'imageUrl': request.build_absolute_uri(picture_url)})
@api_view(['GET'])
def profile_cv(request):
    cv_url = getattr(settings, 'PROFILE_CV_URL', None)

    if cv_url:
        cv_path = os.path.join(settings.MEDIA_ROOT, 'image', 'gitau.pdf')
        if os.path.exists(cv_path):
            return Response({'cvUrl': request.build_absolute_uri(cv_url)})
        else:
            return Response(
                {'error': 'CV not available at the moment.'},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(
        {'error': 'CV not available at the moment.'},
        status=status.HTTP_404_NOT_FOUND
    )


# --- Projects ---
class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer




# --- Contact ---
@api_view(['POST'])
def contact_view(request):
    serializer = ContactMessageSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        # Send email
        try:
            send_mail(
                subject=f"New Contact Message from {instance.name}",
                message=f"Name: {instance.name}\nEmail: {instance.email}\nMessage: {instance.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        return Response({'message': 'Message sent successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Hire ---
@api_view(['POST'])
def hire_view(request):
    serializer = HireRequestSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save()
        # Send email to you
        try:
            send_mail(
                subject=f"New Hire Request from {instance.applicant_name}",
                message=(
                    f"Name: {instance.applicant_name}\n"
                    f"Email: {instance.applicant_email}\n"
                    f"Phone: {instance.applicant_phone}\n"
                    f"Company: {instance.company_name}\n"
                    f"Role: {instance.role}\n"
                    f"Offered Salary: {instance.offered_salary}\n"
                    f"Message: {instance.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")
        # Send confirmation to applicant
        try:
            send_mail(
                subject="Your hire request was received!",
                message=f"Hi {instance.applicant_name},\n\nYour hire request has been received successfully.\nWestley will reach out shortly.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.applicant_email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Confirmation email failed: {e}")
        return Response({'message': 'Hire request sent successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
