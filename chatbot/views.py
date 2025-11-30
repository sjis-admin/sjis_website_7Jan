"""
Views for the chatbot API endpoints.
"""
import uuid
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from .models import ChatConversation, ChatMessage
from .services import ChatbotService


# Simple rate limiting with in-memory storage (for production, use Redis)
RATE_LIMIT_STORAGE = {}
RATE_LIMIT_COUNT = 10  # messages per minute
RATE_LIMIT_WINDOW = 60  # seconds


def check_rate_limit(ip_address):
    """Simple rate limiting check."""
    now = timezone.now().timestamp()
    
    if ip_address not in RATE_LIMIT_STORAGE:
        RATE_LIMIT_STORAGE[ip_address] = []
    
    # Remove old entries
    RATE_LIMIT_STORAGE[ip_address] = [
        timestamp for timestamp in RATE_LIMIT_STORAGE[ip_address]
        if now - timestamp < RATE_LIMIT_WINDOW
    ]
    
    # Check limit
    if len(RATE_LIMIT_STORAGE[ip_address]) >= RATE_LIMIT_COUNT:
        return False
    
    # Add current request
    RATE_LIMIT_STORAGE[ip_address].append(now)
    return True


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
@require_http_methods(["POST"])
def chat_message(request):
    """
    Main chat endpoint.
    POST /chatbot/api/chat/
    Body: {"message": "user question", "conversation_id": "optional"}
    Returns: {"response": "bot response", "conversation_id": "id", "success": true}
    """
    try:
        # Parse request body
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        conversation_id = data.get('conversation_id', '')
        
        # Validate message
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Message cannot be empty'
            }, status=400)
        
        # Rate limiting
        ip_address = get_client_ip(request)
        if not check_rate_limit(ip_address):
            return JsonResponse({
                'success': False,
                'error': 'Too many requests. Please wait a moment.'
            }, status=429)
        
        # Get or create conversation
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
            conversation = ChatConversation.objects.create(
                session_id=conversation_id,
                user_ip=ip_address,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
        else:
            try:
                conversation = ChatConversation.objects.get(session_id=conversation_id)
            except ChatConversation.DoesNotExist:
                # Create if doesn't exist
                conversation = ChatConversation.objects.create(
                    session_id=conversation_id,
                    user_ip=ip_address,
                    user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
                )
        
        # Save user message
        ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # Get response from chatbot service
        chatbot = ChatbotService()
        response_text, context_used, _ = chatbot.get_response(user_message, conversation_id)
        
        # Save assistant message
        ChatMessage.objects.create(
            conversation=conversation,
            role='assistant',
            content=response_text,
            context_used=context_used[:1000] if context_used else ''  # Truncate context
        )
        
        # Update conversation stats
        conversation.message_count = conversation.messages.count()
        conversation.save()
        
        return JsonResponse({
            'success': True,
            'response': response_text,
            'conversation_id': conversation_id
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON in request body'
        }, status=400)
    
    except Exception as e:
        # Log error (in production, use proper logging)
        print(f"Chat error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred. Please try again.'
        }, status=500)


@require_http_methods(["GET"])
def get_context(request):
    """
    Debug endpoint to test context retrieval.
    GET /chatbot/api/context/?q=search query
    Returns: Retrieved context data
    """
    query = request.GET.get('q', '')
    
    if not query:
        return JsonResponse({
            'success': False,
            'error': 'Query parameter "q" is required'
        }, status=400)
    
    try:
        from .services import SchoolDataRetriever, ContextBuilder
        
        retriever = SchoolDataRetriever()
        data = retriever.search_all(query)
        
        builder = ContextBuilder()
        context = builder.build_context(data)
        
        return JsonResponse({
            'success': True,
            'query': query,
            'data': data,
            'context': context
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
