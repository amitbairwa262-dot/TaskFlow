import re
from typing import Dict, Any

class MockAIParser:
    @staticmethod
    def parse_natural_language(text: str) -> Dict[str, Any]:
        """
        Deterministic token parser mimicking an NLP entity extraction system.
        Extracts structural attributes using regex markers: [priority], by [due_date].
        """
        clean_text = text.strip()

        
        priority = "medium" 
        if re.search(r'\b(high|urgent|critical)\b', clean_text, re.IGNORECASE):
            priority = "high"
        elif re.search(r'\b(low|backlog|minor)\b', clean_text, re.IGNORECASE):
            priority = "low"

      
        due_date = "today"  
        date_match = re.search(r'\bby\s+(.+)$', clean_text, re.IGNORECASE)
        if date_match:
            due_date = date_match.group(1).strip()
            due_date = re.sub(
                r'\b(with\s+high|with\s+medium|with\s+low|priority)\b.*$',
                '', due_date, flags=re.IGNORECASE
            ).strip()

        title = clean_text
        title = re.sub(r'\bby\s+.+$', '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'\bwith\s+(high|medium|low)\s+priority\b', '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'\b(high|medium|low)\s+priority\b', '', title, flags=re.IGNORECASE).strip()

        title = re.sub(r'\b(urgent|critical|backlog|minor|high|low|medium)\b', '', title, flags=re.IGNORECASE).strip()

        title = re.sub(r'\s{2,}', ' ', title).strip()

        if not title:
            title = clean_text

        return {
            "title": title,
            "priority": priority,
            "due_date": due_date
        }
