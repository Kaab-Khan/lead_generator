from typing import List, Tuple

from src.domain.models import BusinessLead
from src.domain.lead_rules import has_website


class LeadClassifier:
    def split_by_website(
        self, leads: List[BusinessLead]
    ) -> Tuple[List[BusinessLead], List[BusinessLead]]:
        """
        Returns (with_website, without_website)
        """
        with_website = [lead for lead in leads if has_website(lead)]
        without_website = [lead for lead in leads if not has_website(lead)]
        return with_website, without_website

