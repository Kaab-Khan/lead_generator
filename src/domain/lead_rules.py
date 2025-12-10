from .models import BusinessLead

def has_website(lead: BusinessLead) -> bool:
    return bool(lead.website)
