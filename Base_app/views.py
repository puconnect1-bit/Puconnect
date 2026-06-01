"""
Base App Views - Homepage, About, Help, Terms, Privacy, Safety
"""

from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def home(request):
    """
    Homepage / Landing Page
    GET /
    
    Displays:
    - Hero section with call-to-action
    - Features overview
    - How it works
    - Categories
    - Statistics
    """
    context = {
        'page_title': 'PU-Marketplace - Campus Commerce, Reimagined',
        'page_description': 'Buy, sell, and trade on campus. Exclusively for university students.',
    }
    return render(request, 'base/index.html', context)


def about(request):
    """
    About Page
    GET /about/
    
    Displays:
    - Company mission and vision
    - Team information
    - History and milestones
    - Values
    """
    context = {
        'page_title': 'About PU-Marketplace',
        'page_description': 'Learn about our mission to revolutionize campus commerce.',
    }
    return render(request, 'base/about.html', context)


def help_page(request):
    """
    Help & Support Center
    GET /help/
    
    Displays:
    - FAQs
    - Getting started guide
    - Troubleshooting
    - Contact support
    """
    context = {
        'page_title': 'Help & Support - PU-Marketplace',
        'page_description': 'Find answers to common questions and get support.',
        'faqs': [
            {
                'question': 'How do I verify my student status?',
                'answer': 'Sign up with your university email address. Our system automatically verifies your status when you use your @student.pu.edu.gh email.'
            },
            {
                'question': 'Is it safe to buy and sell here?',
                'answer': 'Yes! All users are verified students. We also provide in-app messaging, secure payment options, and a rating system to ensure safe transactions.'
            },
            {
                'question': 'How do I create a listing?',
                'answer': 'Go to your Dashboard, click "New Listing", upload photos, add a description and price. Your listing goes live immediately!'
            },
            {
                'question': 'Can I meet buyers outside campus?',
                'answer': 'We recommend meeting at designated campus locations for safety. You can arrange meetups through our in-app messaging.'
            },
            {
                'question': 'What payment methods do you support?',
                'answer': 'We support Mobile Money (Vodafone Cash, MTN Mobile Money), bank transfers, and our secure escrow system.'
            },
            {
                'question': 'How do ratings work?',
                'answer': 'After each transaction, both parties can rate each other from 1-5 stars and leave comments. This builds trust in our community.'
            },
        ]
    }
    return render(request, 'base/help.html', context)


def terms(request):
    """
    Terms & Conditions Page
    GET /terms/
    
    Displays:
    - User agreement
    - Rights and responsibilities
    - Prohibited items
    - Dispute resolution
    """
    context = {
        'page_title': 'Terms & Conditions - PU-Marketplace',
        'page_description': 'Read our terms of service and user agreement.',
    }
    return render(request, 'base/terms.html', context)


def privacy(request):
    """
    Privacy Policy Page
    GET /privacy/
    
    Displays:
    - Data collection practices
    - How data is used
    - User rights
    - Cookies and tracking
    """
    context = {
        'page_title': 'Privacy Policy - PU-Marketplace',
        'page_description': 'Learn how we protect your privacy.',
    }
    return render(request, 'base/privacy.html', context)


def safety(request):
    """
    Safety Guidelines Page
    GET /safety/
    
    Displays:
    - Safe trading tips
    - Scam warnings
    - What to avoid
    - Emergency contacts
    """
    context = {
        'page_title': 'Safety Guidelines - PU-Marketplace',
        'page_description': 'Stay safe while buying and selling on campus.',
        'safety_tips': [
            {
                'title': 'Meet in Public Places',
                'description': 'Always meet at well-known campus locations like the library, student center, or cafeteria. Never meet strangers outside campus.'
            },
            {
                'title': 'Verify Before You Trade',
                'description': 'Check the seller\'s profile, reviews, and ratings. Ask questions and request additional photos if needed.'
            },
            {
                'title': 'Use In-App Messaging',
                'description': 'Communicate through our platform, not personal phone numbers. This keeps your privacy protected.'
            },
            {
                'title': 'Inspect Items Carefully',
                'description': 'Before handing over money, thoroughly inspect the item. Check for damage, missing parts, or wear.'
            },
            {
                'title': 'Trust Your Gut',
                'description': 'If something feels wrong, walk away. There are plenty of other sellers and buyers on PU-Marketplace.'
            },
            {
                'title': 'Report Suspicious Activity',
                'description': 'See scams or harassment? Report them immediately. Our team reviews all reports and takes action.'
            },
        ]
    }
    return render(request, 'base/safety.html', context)


def browse_categories(request, category=None):
    """
    Browse by Category
    GET /categories/
    GET /categories/<category>/
    
    Displays:
    - All available categories
    - Filtered listings by category
    """
    categories = [
        {'slug': 'textbooks', 'name': 'Textbooks', 'emoji': '📚', 'count': 245},
        {'slug': 'electronics', 'name': 'Electronics', 'emoji': '💻', 'count': 189},
        {'slug': 'services', 'name': 'Services', 'emoji': '🎨', 'count': 156},
        {'slug': 'fashion', 'name': 'Fashion', 'emoji': '👗', 'count': 423},
        {'slug': 'furniture', 'name': 'Furniture', 'emoji': '🛋️', 'count': 234},
        {'slug': 'food', 'name': 'Food & Snacks', 'emoji': '🍱', 'count': 178},
    ]
    
    context = {
        'page_title': 'Browse by Category - PU-Marketplace',
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'base/categories.html', context)


def contact(request):
    """
    Contact Us Page
    GET /contact/
    POST /contact/
    
    Displays:
    - Contact form
    - Support email
    - Response time info
    """
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # TODO: Send email and save to database
        
        context = {
            'success': True,
            'message': 'Thank you for your message. We\'ll get back to you soon!'
        }
    else:
        context = {
            'page_title': 'Contact Us - PU-Marketplace',
            'page_description': 'Get in touch with our support team.',
        }
    
    return render(request, 'base/contact.html', context)
