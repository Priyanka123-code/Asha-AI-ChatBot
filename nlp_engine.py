from knowledgebase.models import JobListing, StartupEvent, MentorshipOpportunity, WomenEmpowerment
from faq.models import FAQ
import re
import requests
from django.conf import settings
import bleach

def sanitize_input(text):
    """Sanitize user input to prevent XSS or injection attacks."""
    return bleach.clean(text, tags=[], attributes={}, strip=True)

def fetch_job_listings(session_filter=None):
    jobs = JobListing.objects.all().order_by('posted_at')[:5]
    if session_filter == "remote":
        jobs = jobs.filter(location="Remote")
    return [f"{job.title} at {job.company} ({job.location}) - {job.description}" for job in jobs]

def fetch_event_details_from_api():
    try:
        url = "https://www.eventbriteapi.com/v3/events/search/"
        headers = {"Authorization": f"Bearer {settings.EVENTBRITE_API_KEY}"}
        params = {"q": "startup", "sort_by": "date", "location.address": "global"}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        events = response.json().get("events", [])
        return [
            f"{event['name']['text']} on {event['start']['local']} - {event['description']['text'][:100]}..."
            for event in events[:5]
            if event.get("start") and event.get("name") and event.get("description")
        ]
    except requests.RequestException as e:
        print(f"API Error: {e}")
        return ["Error fetching events from API. Showing local data instead."]

def fetch_event_details():
    api_events = fetch_event_details_from_api()
    if api_events[0] != "Error fetching events from API. Showing local data instead.":
        return api_events
    events = StartupEvent.objects.all().order_by('event_date')[:5]
    return [f"{event.event_name} on {event.event_date} ({event.location}) - {event.description}" for event in events]

def fetch_mentorship_opportunities():
    mentorships = MentorshipOpportunity.objects.all().order_by('available_slots')[:5]
    return [f"{mentorship.mentor_name} ({mentorship.expertise_area}, {mentorship.available_slots} slots) - {mentorship.description}" for mentorship in mentorships]

def fetch_faqs(query):
    faqs = FAQ.objects.all()
    for faq in faqs:
        if re.search(re.escape(faq.question.lower()), sanitize_input(query.lower())):
            return f"Q: {faq.question}\nA: {faq.answer}"
    return None

def fetch_empowerment_insights():
    insights = WomenEmpowerment.objects.all()[:3]
    return [f"{insight.title}: {insight.description}" for insight in insights]

def detect_intent(query, session_data):
    query_lower = sanitize_input(query.lower())
    previous_intent = session_data.get("intent")

    if previous_intent == "event" and "online" in query_lower:
        return "event_online"
    if any(word in query_lower for word in ["job", "career", "work"]):
        return "job"
    if any(word in query_lower for word in ["event", "summit", "conference"]):
        return "event"
    if any(word in query_lower for word in ["mentor", "guidance", "advice"]):
        return "mentorship"
    return "faq"

def detect_bias(query):
    """Detect biased language in the query."""
    query_lower = sanitize_input(query.lower())
    biased_phrases = [
        "only men", "men only", "for men", "male only", "only male",
        "not for women", "women not allowed", "no women", "exclude women",
        "only for whites", "whites only", "no minorities", "exclude minorities",
        "for young people only", "no seniors", "exclude seniors"
    ]
    return any(phrase in query_lower for phrase in biased_phrases)

def generate_response(intent):
    """Generate a response based on the detected intent."""
    if intent == "job":
        jobs = fetch_job_listings()
        return "Here are some job opportunities:\n" + "\n".join(jobs) if jobs else "No job opportunities found."
    elif intent == "event":
        events = fetch_event_details()
        return "Here are some upcoming events:\n" + "\n".join(events) if events else "No upcoming events found."
    elif intent == "event_online":
        events = [event for event in fetch_event_details() if "Online" in event]
        return "Here are some online events:\n" + "\n".join(events) if events else "No online events found."
    elif intent == "mentorship":
        mentorships = fetch_mentorship_opportunities()
        return "Here are some mentorship opportunities:\n" + "\n".join(mentorships) if mentorships else "No mentorship opportunities found."
    else:  # FAQ or default
        response = "I can help with jobs, events, mentorships, or FAQs. What are you looking for?"
        # Add women empowerment insights for relevant queries
        query_lower = sanitize_input(intent.lower())  # Using intent as a proxy for query context
        if any(keyword in query_lower for keyword in ["women", "empowerment", "female", "gender"]):
            empowerment_insights = fetch_empowerment_insights()
            if empowerment_insights:
                response += "\n\nWomen Empowerment Insights:\n" + "\n".join(empowerment_insights)
            else:
                response += "\n\nNo women empowerment insights available at the moment."
        return response

def process_query(query, session_id, session_data):
    query = sanitize_input(query)
    if "history" not in session_data:
        session_data["history"] = []
    session_data["history"].append(query)
    session_data["history"] = session_data["history"][-5:]

    intent = detect_intent(query, session_data)
    response = generate_response(intent)

    # Include women empowerment insights for relevant queries
    query_lower = query.lower()
    if any(keyword in query_lower for keyword in ["women", "empowerment", "female", "gender"]):
        empowerment_insights = fetch_empowerment_insights()
        if empowerment_insights:
            response += "\n\nWomen Empowerment Insights:\n" + "\n".join(empowerment_insights)
        else:
            response += "\n\nNo women empowerment insights available at the moment."

    session_data["history"].append(response)
    session_data["history"] = session_data["history"][-5:]

    return {"session_id": session_id, "response": response, "session_data": session_data}