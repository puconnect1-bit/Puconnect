from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from .models import Conversation, Message


@login_required(login_url='auth:auth_view')
def chat(request):
    """
    Chat/Messaging Page
    GET /chat/chat/
    """
    context = {
        'page_title': 'Messages - PU-Marketplace',
        'page_description': 'Chat with buyers and sellers.',
    }
    return render(request, 'chat/chat.html', context)

@login_required
def get_conversations(request):
    """Returns a list of all conversations for the current user."""
    convs = request.user.conversations.all()
    data = []
    for c in convs:
        other_user = c.participants.exclude(id=request.user.id).first()
        last_msg = c.messages.last()
        data.append({
            'id': c.id,
            'name': other_user.get_full_name() or other_user.username if other_user else "System",
            'username': other_user.username if other_user else "system",
            'initials': (other_user.username[:2] if other_user else "SY").upper(),
            'listing': c.listing.title if c.listing else "General",
            'listingEmoji': "📦" if not c.listing else "🛠️" if c.listing.listing_type == 'service' else "📦",
            'price': f"GH₵ {c.listing.price}" if c.listing else "",
            'time': last_msg.timestamp.strftime("%I:%M %p") if last_msg else "New",
            'badge': c.messages.filter(is_read=False).exclude(sender=request.user).count(),
            'status': 'online', # Mock for now
        })
    return JsonResponse(data, safe=False)

@login_required
def get_messages(request, conv_id):
    """Returns all messages for a specific conversation."""
    try:
        conv = request.user.conversations.get(id=conv_id)
        messages = conv.messages.all()
        data = []
        for m in messages:
            data.append({
                'from': 'out' if m.sender == request.user else 'in',
                'text': m.text,
                'image_url': m.image_url,
                'voice_url': m.voice_url,
                'meetup_spot': m.meetup_spot,
                'meetup_time': m.meetup_time if m.meetup_time else None,
                'time': m.timestamp.strftime("%I:%M %p"),
            })
        return JsonResponse(data, safe=False)
    except Conversation.DoesNotExist:
        return JsonResponse({'error': 'Conversation not found'}, status=404)

@login_required
@require_POST
def start_conversation(request):
    """Starts a new conversation regarding a listing."""
    try:
        data = json.loads(request.body)
        listing_id = data.get('listing_id')
        
        from Listings_app.models import Listing
        listing = Listing.objects.get(id=listing_id)
        seller = listing.user
        
        # Don't let users chat with themselves
        if seller == request.user:
            return JsonResponse({'status': 'error', 'message': 'You cannot start a chat with yourself'}, status=400)
        
        # Check if conversation already exists for this buyer, seller, and listing
        conv = Conversation.objects.filter(participants=request.user).filter(participants=seller).filter(listing=listing).first()
        
        if not conv:
            conv = Conversation.objects.create(listing=listing)
            conv.participants.add(request.user, seller)
        
        return JsonResponse({'status': 'success', 'conv_id': conv.id})
    except Listing.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Listing not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
