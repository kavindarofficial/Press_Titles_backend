# api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NewspaperTitle
from .utils import verify_title  

@api_view(['POST'])
def verify_title_view(request):
    # Get the title from the POST request body
    new_title = request.data.get('title', '')

    if not new_title:
        return Response({"error": "No title provided"}, status=400)

    # Existing titles in the database
    existing_titles = NewspaperTitle.objects.values_list('name', flat=True)

    # Call the verify_title function to validate the new title
    # is_valid, message, probability = verify_title(new_title, existing_titles)
    x = verify_title(new_title, existing_titles)
    # print(x)
    # Return the result
    return Response(x)
