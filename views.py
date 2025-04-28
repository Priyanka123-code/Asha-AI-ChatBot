from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .nlp_engine import process_query
from .models import SessionContext
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(['POST'])

def chatbot_query(request):
    if request.method == "POST":
        try:
            data = request.json()
            message = data.get("message")
            session_id = data.get("session_id")

            logger.info(f"Received request: Method={request.method}, Path={request.path}")
            logger.info(f"Parsed data: {data}")

            # Create or get session context
            session_context, created = SessionContext.objects.get_or_create(session_id=session_id)
            if created:
                logger.info(f"Created new session: {session_id}")
                logger.info(f"No existing session data for session: {session_id}")
                session_context.last_intent = ""
                session_context.last_message = ""
            else:
                logger.info(f"Loaded existing session data for session: {session_id}")

            session_data = {
                "intent": session_context.last_intent,
                "history": []  # Initialize history if not present
            }

            response_data = process_query(message, session_id, session_data)
            session_context.last_intent = response_data["session_data"].get("intent", "")
            session_context.last_message = message
            session_context.save()

            logger.info(f"Updated session data for session: {session_id}")
            return JsonResponse(response_data)
        except Exception as e:
            logger.error(f"Server error: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Method not allowed"}, status=405)