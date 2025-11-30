"""
Core services for the chatbot including data retrieval and context building.
"""
import hashlib
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

# Import all the models we'll need to query
from home.models import (
    SiteConfiguration, AboutUs, AboutUsSection, 
    FacultyMember, PrincipalMessage, NewsArticle
)
from notice_board2.models import NoticeBoard
from academic_calendar.models import Event, Holiday, AcademicYear
from admission.models import (
    AdmissionStep, AdmissionRequirement, 
    AdmissionFee, AdmissionFAQ, AdmissionDeadline
)
from gallery.models import Album
from rules.models import Rule, RuleCategory

from .models import ChatFAQ, ChatAnalytics


class SchoolDataRetriever:
    """
    Retrieves relevant school information from the database based on query keywords.
    """
    
    def __init__(self):
        self.results = {}
    
    def search_all(self, query):
        """
        Main search method that queries all relevant models.
        Returns a dictionary of results organized by category.
        """
        keywords = self._extract_keywords(query.lower())
        self.results = {}
        query_lower = query.lower()  # Keep full query for better matching
        
        # Search different categories based on keywords (using substring matching)
        if self._contains_any(query_lower, ['notice', 'announcement', 'circular']):
            self.results['notices'] = self._search_notices(keywords)
        
        if self._contains_any(query_lower, ['event', 'calendar', 'upcoming', 'holiday']):
            self.results['events'] = self._search_events(keywords)
            self.results['holidays'] = self._search_holidays(keywords)
        
        if self._contains_any(query_lower, ['admission', 'admit', 'enroll', 'fee', 'requirement']):
            self.results['admission'] = self._search_admission(keywords)
        
        if self._contains_any(query_lower, ['teacher', 'faculty', 'staff', 'principal', 'vice']):
            self.results['faculty'] = self._search_faculty(keywords)
        
        if self._contains_any(query_lower, ['about', 'history', 'mission', 'vision', 'goal']):
            self.results['about'] = self._search_about(keywords)
        
        # Contact/basic info - expanded to include name, school, etc.
        if self._contains_any(query_lower, ['contact', 'address', 'email', 'phone', 'location', 
                                            'where', 'find', 'name', 'school', 'called']):
            self.results['contact'] = self._get_contact_info()
        
        if self._contains_any(query_lower, ['rule', 'regulation', 'policy', 'discipline']):
            self.results['rules'] = self._search_rules(keywords)
        
        if self._contains_any(query_lower, ['gallery', 'photo', 'album', 'picture']):
            self.results['gallery'] = self._search_gallery(keywords)
        
        if self._contains_any(query_lower, ['news', 'latest', 'recent']):
            self.results['news'] = self._search_news(keywords)
        
        # If no specific category matched, do a general search
        if not self.results:
            self._general_search(keywords)
        
        return self.results
    
    def _contains_any(self, text, keywords):
        """Check if text contains any of the keywords (substring matching)."""
        return any(keyword in text for keyword in keywords)
    
    def _extract_keywords(self, query):
        """Extract meaningful keywords from query."""
        # Remove common stop words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for'}
        words = query.split()
        return [word for word in words if word not in stop_words and len(word) > 2]
    
    def _search_notices(self, keywords):
        """Search notices."""
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword) | Q(content__icontains=keyword)
        
        notices = NoticeBoard.objects.filter(query).order_by('-created_at')[:5]
        
        # If no notices match keywords, return all recent notices
        if not notices and NoticeBoard.objects.exists():
            notices = NoticeBoard.objects.all().order_by('-created_at')[:5]
        
        return [{
            'title': notice.title,
            'content': notice.content[:200] + '...' if len(notice.content) > 200 else notice.content,
            'date': notice.created_at.strftime('%Y-%m-%d'),
            'grades': notice.formatted_target_grades
        } for notice in notices]
    
    def _search_events(self, keywords):
        """Search upcoming events."""
        # Get events from today onwards
        today = timezone.now().date()
        query = Q(event_date__gte=today)
        
        # Try keyword search first
        keyword_query = query
        for keyword in keywords:
            keyword_query &= (Q(name__icontains=keyword) | Q(description__icontains=keyword))
        
        events = Event.objects.filter(keyword_query).order_by('event_date')[:5]
        
        # If no events match keywords, return all upcoming events
        if not events and Event.objects.filter(event_date__gte=today).exists():
            events = Event.objects.filter(event_date__gte=today).order_by('event_date')[:5]
        
        return [{
            'name': event.name,
            'description': event.description,
            'date': event.event_date.strftime('%Y-%m-%d'),
            'is_holiday': event.is_holiday
        } for event in events]
    
    def _search_holidays(self, keywords):
        """Search holidays."""
        today = timezone.now().date()
        holidays = Holiday.objects.filter(holiday_date__gte=today).order_by('holiday_date')[:5]
        return [{
            'name': holiday.name,
            'date': holiday.holiday_date.strftime('%Y-%m-%d')
        } for holiday in holidays]
    
    def _search_admission(self, keywords):
        """Search admission-related information."""
        data = {}
        
        # Admission steps
        data['steps'] = [{
            'title': step.title,
            'description': step.description
        } for step in AdmissionStep.objects.all().order_by('order')]
        
        # Requirements
        data['requirements'] = [{
            'title': req.title,
            'details': req.details,
            'category': req.get_category_display()
        } for req in AdmissionRequirement.objects.all().order_by('order')]
        
        # Fees
        data['fees'] = [{
            'grade': fee.grade_level,
            'admission_fee': str(fee.admission_fee),
            'monthly_fee': str(fee.monthly_fee),
            'annual_fee': str(fee.annual_fee)
        } for fee in AdmissionFee.objects.all().order_by('order')]
        
        # FAQs
        query = Q()
        for keyword in keywords:
            query |= Q(question__icontains=keyword) | Q(answer__icontains=keyword)
        
        data['faqs'] = [{
            'question': faq.question,
            'answer': faq.answer
        } for faq in AdmissionFAQ.objects.filter(query)[:3]]
        
        return data
    
    def _search_faculty(self, keywords):
        """Search faculty members."""
        query = Q()
        for keyword in keywords:
            query |= Q(name__icontains=keyword) | Q(designation__icontains=keyword) | Q(category__icontains=keyword)
        
        faculty = FacultyMember.objects.filter(query)[:10]
        
        # If no faculty match keywords, return all faculty
        if not faculty and FacultyMember.objects.exists():
            faculty = FacultyMember.objects.all()[:10]
        
        return [{
            'name': member.name,
            'designation': member.designation,
            'category': member.category
        } for member in faculty]
    
    def _search_about(self, keywords):
        """Get about us information."""
        try:
            about = AboutUs.objects.first()
            if not about:
                return {}
            
            data = {
                'title': about.title,
                'description': about.short_description
            }
            
            # Get sections (mission, vision, goals)
            sections = AboutUsSection.objects.filter(about_us=about)
            data['sections'] = [{
                'title': section.title,
                'content': section.content
            } for section in sections]
            
            return data
        except Exception:
            return {}
    
    def _get_contact_info(self):
        """Get school contact information."""
        try:
            config = SiteConfiguration.objects.first()
            if not config:
                return {}
            
            return {
                'school_name': config.site_name,
                'address': config.address,
                'email': config.email,
                'phone': config.phone,
                'facebook': config.facebook_url,
                'instagram': config.instagram_url,
                'youtube': config.youtube_url,
                'twitter': config.twitter_url
            }
        except Exception:
            return {}
    
    def _search_rules(self, keywords):
        """Search school rules."""
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword) | Q(description__icontains=keyword)
        
        rules = Rule.objects.filter(query, status='active')[:5]
        return [{
            'title': rule.title,
            'description': rule.description,
            'category': rule.category.name,
            'severity': rule.get_severity_display(),
            'applicable_to': rule.applicable_to
        } for rule in rules]
    
    def _search_gallery(self, keywords):
        """Search photo albums."""
        query = Q(is_public=True)
        for keyword in keywords:
            query &= (Q(title__icontains=keyword) | Q(description__icontains=keyword))
        
        albums = Album.objects.filter(query).order_by('-created_at')[:5]
        return [{
            'title': album.title,
            'description': album.description,
            'photo_count': album.photos.count()
        } for album in albums]
    
    def _search_news(self, keywords):
        """Search news articles."""
        query = Q()
        for keyword in keywords:
            query |= Q(title__icontains=keyword) | Q(short_description__icontains=keyword)
        
        news = NewsArticle.objects.filter(query).order_by('-published_date')[:3]
        return [{
            'title': article.title,
            'description': article.short_description,
            'date': article.published_date.strftime('%Y-%m-%d')
        } for article in news]
    
    def _general_search(self, keywords):
        """Fallback general search when no specific category matches."""
        # Get basic school info
        self.results['contact'] = self._get_contact_info()
        
        # Get recent notices
        recent_notices = NoticeBoard.objects.all().order_by('-created_at')[:3]
        if recent_notices:
            self.results['recent_notices'] = [{
                'title': notice.title,
                'date': notice.created_at.strftime('%Y-%m-%d')
            } for notice in recent_notices]
        
        # Get upcoming events
        today = timezone.now().date()
        upcoming_events = Event.objects.filter(event_date__gte=today).order_by('event_date')[:3]
        if upcoming_events:
            self.results['upcoming_events'] = [{
                'name': event.name,
                'date': event.event_date.strftime('%Y-%m-%d')
            } for event in upcoming_events]


class ContextBuilder:
    """
    Builds formatted context from retrieved data for the LLM.
    """
    
    def __init__(self, max_length=3000):
        self.max_length = max_length
    
    def build_context(self, data_results):
        """
        Convert retrieval results into a formatted context string.
        """
        if not data_results:
            return "No specific information found in the database."
        
        context_parts = []
        
        # Build context for each category
        if 'contact' in data_results and data_results['contact']:
            context_parts.append(self._format_contact(data_results['contact']))
        
        if 'about' in data_results and data_results['about']:
            context_parts.append(self._format_about(data_results['about']))
        
        if 'notices' in data_results and data_results['notices']:
            context_parts.append(self._format_notices(data_results['notices']))
        
        if 'events' in data_results and data_results['events']:
            context_parts.append(self._format_events(data_results['events']))
        
        if 'holidays' in data_results and data_results['holidays']:
            context_parts.append(self._format_holidays(data_results['holidays']))
        
        if 'admission' in data_results and data_results['admission']:
            context_parts.append(self._format_admission(data_results['admission']))
        
        if 'faculty' in data_results and data_results['faculty']:
            context_parts.append(self._format_faculty(data_results['faculty']))
        
        if 'rules' in data_results and data_results['rules']:
            context_parts.append(self._format_rules(data_results['rules']))
        
        if 'gallery' in data_results and data_results['gallery']:
            context_parts.append(self._format_gallery(data_results['gallery']))
        
        if 'news' in data_results and data_results['news']:
            context_parts.append(self._format_news(data_results['news']))
        
        if 'recent_notices' in data_results:
            context_parts.append(self._format_recent_notices(data_results['recent_notices']))
        
        if 'upcoming_events' in data_results:
            context_parts.append(self._format_upcoming_events(data_results['upcoming_events']))
        
        # Join all parts
        full_context = "\n\n".join(context_parts)
        
        # Truncate if too long
        if len(full_context) > self.max_length:
            full_context = full_context[:self.max_length] + "..."
        
        return full_context
    
    def _format_contact(self, contact):
        text = f"**School Contact Information:**\n"
        text += f"- Name: {contact.get('school_name', 'N/A')}\n"
        text += f"- Address: {contact.get('address', 'N/A')}\n"
        text += f"- Email: {contact.get('email', 'N/A')}\n"
        text += f"- Phone: {contact.get('phone', 'N/A')}\n"
        if contact.get('facebook'):
            text += f"- Facebook: {contact.get('facebook')}\n"
        return text
    
    def _format_about(self, about):
        text = f"**About the School:**\n{about.get('description', '')}\n"
        if 'sections' in about:
            for section in about['sections']:
                text += f"\n**{section['title']}:**\n{section['content']}\n"
        return text
    
    def _format_notices(self, notices):
        text = "**Recent Notices:**\n"
        for notice in notices:
            text += f"- **{notice['title']}** ({notice['date']}) - {notice['grades']}\n"
            text += f"  {notice['content']}\n"
        return text
    
    def _format_events(self, events):
        text = "**Upcoming Events:**\n"
        for event in events:
            text += f"- **{event['name']}** on {event['date']}\n"
            text += f"  {event['description']}\n"
        return text
    
    def _format_holidays(self, holidays):
        text = "**Upcoming Holidays:**\n"
        for holiday in holidays:
            text += f"- {holiday['name']} on {holiday['date']}\n"
        return text
    
    def _format_admission(self, admission):
        text = "**Admission Information:**\n"
        
        if admission.get('steps'):
            text += "\n**Admission Steps:**\n"
            for step in admission['steps']:
                text += f"- **{step['title']}**: {step['description']}\n"
        
        if admission.get('requirements'):
            text += "\n**Requirements:**\n"
            for req in admission['requirements']:
                text += f"- **{req['title']}** ({req['category']}): {req['details']}\n"
        
        if admission.get('fees'):
            text += "\n**Fee Structure:**\n"
            for fee in admission['fees']:
                text += f"- **{fee['grade']}**: Admission: {fee['admission_fee']}, Monthly: {fee['monthly_fee']}, Annual: {fee['annual_fee']}\n"
        
        if admission.get('faqs'):
            text += "\n**FAQs:**\n"
            for faq in admission['faqs']:
                text += f"- **Q: {faq['question']}**\n  A: {faq['answer']}\n"
        
        return text
    
    def _format_faculty(self, faculty):
        text = "**Faculty Members:**\n"
        for member in faculty:
            text += f"- **{member['name']}** - {member['designation']} ({member['category']})\n"
        return text
    
    def _format_rules(self, rules):
        text = "**School Rules:**\n"
        for rule in rules:
            text += f"- **{rule['title']}** ({rule['category']}) - {rule['severity']}\n"
            text += f"  {rule['description']} (Applies to: {rule['applicable_to']})\n"
        return text
    
    def _format_gallery(self, gallery):
        text = "**Photo Albums:**\n"
        for album in gallery:
            text += f"- **{album['title']}**: {album['description']} ({album['photo_count']} photos)\n"
        return text
    
    def _format_news(self, news):
        text = "**Recent News:**\n"
        for article in news:
            text += f"- **{article['title']}** ({article['date']})\n"
            text += f"  {article['description']}\n"
        return text
    
    def _format_recent_notices(self, notices):
        text = "**Recent Notices:**\n"
        for notice in notices:
            text += f"- {notice['title']} ({notice['date']})\n"
        return text
    
    def _format_upcoming_events(self, events):
        text = "**Upcoming Events:**\n"
        for event in events:
            text += f"- {event['name']} on {event['date']}\n"
        return text


class ChatbotService:
    """
    Main chatbot service that orchestrates data retrieval and response generation.
    """
    
    def __init__(self, use_ollama=True):
        self.retriever = SchoolDataRetriever()
        self.context_builder = ContextBuilder()
        
        # Initialize Ollama service
        self.ollama = None
        if use_ollama:
            try:
                from .ollama_service import OllamaService
                self.ollama = OllamaService()
            except Exception as e:
                import logging
                logging.warning(f"Could not initialize Ollama: {e}")
    
    def get_response(self, user_message, conversation_id=None):
        """
        Main method to get chatbot response.
        Returns: (response_text, context_used, conversation_id)
        """
        # Check for custom FAQs first
        faq_response = self._check_faqs(user_message)
        if faq_response:
            return faq_response, "", conversation_id
        
        # Retrieve relevant data
        data = self.retriever.search_all(user_message)
        
        # Build context
        context = self.context_builder.build_context(data)
        
        # Try Ollama first if available
        response = None
        if self.ollama and self.ollama.is_available():
            response = self.ollama.generate_response(user_message, context)
        
        # Fallback to rule-based if Ollama failed or unavailable
        if not response:
            response = self._generate_rule_based_response(user_message, context, data)
        
        # Track analytics
        self._track_analytics(user_message)
        
        return response, context, conversation_id
    
    def _check_faqs(self, message):
        """Check if message matches any custom FAQs."""
        faqs = ChatFAQ.objects.filter(is_active=True).order_by('-priority')
        
        message_lower = message.lower()
        
        for faq in faqs:
            # Check if FAQ keywords match
            if faq.keywords:
                keywords = [k.strip().lower() for k in faq.keywords.split(',')]
                if any(keyword in message_lower for keyword in keywords):
                    return faq.answer
            
            # Check if question is similar
            if faq.question.lower() in message_lower or message_lower in faq.question.lower():
                return faq.answer
        
        return None
    
    def _generate_rule_based_response(self, user_message, context, data):
        """
        Generate response using rule-based system (no LLM required).
        This is a fallback that provides structured responses.
        """
        if not data:
            return (
                "I'm sorry, I couldn't find specific information about that in our database. "
                "However, I can help you with information about:\n\n"
                "- School notices and announcements\n"
                "- Upcoming events and holidays\n"
                "- Admission requirements and fees\n"
                "- Faculty and staff information\n"
                "- School location and contact details\n"
                "- School history, mission, and vision\n"
                "- School rules and regulations\n\n"
                "Please feel free to ask about any of these topics!"
            )
        
        # Build a natural response based on what we found
        response_parts = []
        user_message_lower = user_message.lower()
        
        # Contact info - show if contact data exists and question seems related
        if 'contact' in data and data['contact']:
            contact = data['contact']
            is_contact_query = any(word in user_message_lower for word in 
                                   ['address', 'location', 'where', 'email', 'contact', 
                                    'reach', 'phone', 'call', 'find', 'name', 'school', 'called'])
            
            if is_contact_query:
                # School name
                if any(word in user_message_lower for word in ['name', 'school', 'called']):
                    if contact.get('school_name'):
                        response_parts.append(
                            f"🏫 **School Name:**\n"
                            f"Our school is called **{contact.get('school_name')}** "
                            f"(St. Joseph International School)"
                        )
                
                # Address
                if any(word in user_message_lower for word in ['address', 'location', 'where', 'find']):
                    if contact.get('address'):
                        response_parts.append(
                            f"📍 **School Location:**\n"
                            f"{contact.get('school_name', 'Our school')} is located at:\n"
                            f"{contact.get('address')}"
                        )
                
                # Contact details
                if any(word in user_message_lower for word in ['email', 'contact', 'reach', 'phone', 'call']):
                    contact_info = []
                    if contact.get('email'):
                        contact_info.append(f"📧 Email: {contact['email']}")
                    if contact.get('phone'):
                        contact_info.append(f"📞 Phone: {contact['phone']}")
                    
                    if contact_info:
                        response_parts.append(
                            "**Contact Information:**\n" + "\n".join(contact_info)
                        )
        
        # Notices
        if 'notices' in data and data['notices']:
            response_parts.append("📢 **Latest Notices:**")
            for notice in data['notices'][:3]:
                response_parts.append(
                    f"\n**{notice['title']}** ({notice['date']})\n"
                    f"For: {notice['grades']}\n"
                    f"{notice['content'][:150]}..."
                )
        
        # Events
        if 'events' in data and data['events']:
            response_parts.append("\n🎉 **Upcoming Events:**")
            for event in data['events'][:3]:
                response_parts.append(f"- **{event['name']}** on {event['date']}")
        
        # Holidays
        if 'holidays' in data and data['holidays']:
            response_parts.append("\n🏖️ **Upcoming Holidays:**")
            for holiday in data['holidays'][:3]:
                response_parts.append(f"- {holiday['name']} on {holiday['date']}")
        
        # Admission
        if 'admission' in data and data['admission']:
            adm = data['admission']
            has_admission_info = False
            
            # Steps
            if 'steps' in adm and adm['steps']:
                has_admission_info = True
                response_parts.append("\n📝 **Admission Steps:**")
                for step in adm['steps'][:3]:
                    response_parts.append(f"- {step['title']}")
            
            # Fees
            if 'fees' in adm and adm['fees']:
                has_admission_info = True
                response_parts.append("\n💰 **Fee Structure:**")
                for fee in adm['fees'][:5]:
                    response_parts.append(
                        f"- **{fee['grade']}**: "
                        f"Admission: BDT {fee['admission_fee']}, "
                        f"Monthly: BDT {fee['monthly_fee']}"
                    )
            
            # Requirements
            if 'requirements' in adm and adm['requirements']:
                has_admission_info = True
                response_parts.append("\n📋 **Requirements:**")
                for req in adm['requirements'][:3]:
                    response_parts.append(f"- {req['title']}")
            
            # FAQs
            if 'faqs' in adm and adm['faqs']:
                has_admission_info = True
                response_parts.append("\n❓ **Common Questions:**")
                for faq in adm['faqs'][:2]:
                    response_parts.append(f"**Q:** {faq['question']}\n**A:** {faq['answer'][:100]}...")
            
            # If admission section exists but no data, say so
            if not has_admission_info:
                response_parts.append(
                    "\n📚 **Admission Information:**\n"
                    "Admission details are being updated. "
                    "Please contact the school directly for the latest information.\n"
                    f"📧 Email: {data.get('contact', {}).get('email', 'N/A')}\n"
                    f"📞 Phone: {data.get('contact', {}).get('phone', 'N/A')}"
                )
        
        # Faculty
        if 'faculty' in data and data['faculty']:
            response_parts.append("\n👨‍🏫 **Faculty Information:**")
            for member in data['faculty'][:5]:
                response_parts.append(f"- {member['name']} - {member['designation']}")
        
        # About
        if 'about' in data and data['about']:
            about = data['about']
            if 'sections' in about:
                for section in about['sections']:
                    response_parts.append(f"\n**{section['title']}:**\n{section['content'][:200]}...")
        
        # Recent notices if no specific notices found
        if 'recent_notices' in data and 'notices' not in data:
            response_parts.append("\n📋 **Recent Notices:**")
            for notice in data['recent_notices']:
                response_parts.append(f"- {notice['title']} ({notice['date']})")
        
        # Upcoming events if no specific events found
        if 'upcoming_events' in data and 'events' not in data:
            response_parts.append("\n📅 **Upcoming Events:**")
            for event in data['upcoming_events']:
                response_parts.append(f"- {event['name']} on {event['date']}")
        
        # If we found something, add footer
        if response_parts:
            response_parts.append(
                "\n\n💬 Feel free to ask me more questions!"
            )
            return "\n".join(response_parts)
        else:
            # Fallback if data exists but wasn't formatted
            return (
                "I found some information but I'm not sure how to present it. "
                "Could you please rephrase your question? For example:\n\n"
                "- 'What is the school address?'\n"
                "- 'Tell me about admission fees'\n"
                "- 'Who are the faculty members?'\n"
                "- 'What events are coming up?'"
            )
    
    def _track_analytics(self, message):
        """Track question analytics."""
        try:
            # Create a hash of the question
            question_hash = hashlib.md5(message.lower().encode()).hexdigest()
            
            # Update or create analytics entry
            analytics, created = ChatAnalytics.objects.get_or_create(
                question_hash=question_hash,
                defaults={'question_sample': message[:500]}
            )
            
            if not created:
                analytics.count += 1
                analytics.last_asked = timezone.now()
                analytics.save()
        except Exception:
            # Silently fail if analytics tracking fails
            pass
