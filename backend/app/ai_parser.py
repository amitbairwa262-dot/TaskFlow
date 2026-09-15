import re
from typing import Dict, Any


class MockAIParser:
    """
    Deterministic mock parser mimicking an NLP entity-extraction system.
    No network calls. Simulates prompting an LLM by building a
    role-structured prompt (system/user pair) and then applying
    rule-based extraction as the "model response".
    """

    @staticmethod
    def build_prompt(text: str) -> Dict[str, str]:
        """
        Builds a role-structured prompt object (system/user message pair).
        In a real integration this dict would be sent to an LLM API.
        Kept here purely for documentation/demonstration of prompting
        technique, since MockAIParser itself uses regex, not an API call.
        """
        system_message = (
            "You are a task-parsing assistant. Extract three fields from "
            "the user's natural language statement: title (the task itself, "
            "with priority/date phrases removed), priority (one of "
            "'low', 'medium', 'high'), and due_date (a normalized date "
            "string, or null if no date is mentioned). "
            "Priority keywords -> high: 'urgent', 'critical', 'asap'. "
            "low: 'low priority', 'whenever', 'backlog', 'minor'. "
            "Date keywords -> 'today', 'tomorrow', 'next week', "
            "'next <weekday>', or a bare weekday name."
        )
        user_message = f"Parse this task statement: \"{text}\""

        return {
            "system": system_message,
            "user": user_message
        }

    @staticmethod
    def parse_natural_language(text: str) -> Dict[str, Any]:
        """
        Deterministic token parser mimicking an NLP entity extraction system.
        Extracts structural attributes using keyword and regex markers.
        """
        clean_text = text.strip()

        # Build the prompt object (documents the prompting technique;
        # not actually sent anywhere since this is a mock/offline parser).
        _prompt = MockAIParser.build_prompt(clean_text)

        # ---------------- PRIORITY ----------------
        priority = "medium"
        if re.search(r'\b(high|urgent|critical|asap)\b', clean_text, re.IGNORECASE):
            priority = "high"
        elif re.search(r'\b(low|backlog|minor|whenever|low\s+priority)\b', clean_text, re.IGNORECASE):
            priority = "low"

        # ---------------- DUE DATE ----------------
        due_date = None

        weekday_pattern = r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)'

        if re.search(r'\btoday\b', clean_text, re.IGNORECASE):
            due_date = "today"
        elif re.search(r'\btomorrow\b', clean_text, re.IGNORECASE):
            due_date = "tomorrow"
        elif re.search(r'\bnext\s+week\b', clean_text, re.IGNORECASE):
            due_date = "next week"
        else:
            next_weekday_match = re.search(
                rf'\bnext\s+{weekday_pattern}\b', clean_text, re.IGNORECASE
            )
            if next_weekday_match:
                due_date = f"next {next_weekday_match.group(1).lower()}"
            else:
                bare_weekday_match = re.search(
                    rf'\b{weekday_pattern}\b', clean_text, re.IGNORECASE
                )
                if bare_weekday_match:
                    due_date = bare_weekday_match.group(1).lower()

        # ---------------- TITLE ----------------
        title = clean_text

        # Remove date phrases
        title = re.sub(r'\bnext\s+week\b', '', title, flags=re.IGNORECASE)
        title = re.sub(rf'\bnext\s+{weekday_pattern}\b', '', title, flags=re.IGNORECASE)
        title = re.sub(rf'\b{weekday_pattern}\b', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\btoday\b', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\btomorrow\b', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\bby\s+', '', title, flags=re.IGNORECASE)

        # Remove priority phrases
        title = re.sub(r'\bwith\s+(high|medium|low)\s+priority\b', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\b(high|medium|low)\s+priority\b', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\b(urgent|critical|asap|backlog|minor|whenever)\b', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\b(high|low|medium)\b', '', title, flags=re.IGNORECASE)

        title = re.sub(r'\s{2,}', ' ', title).strip()
        title = title.strip(" ,.-")

        if not title:
            title = "Untitled task"

        return {
            "title": title,
            "priority": priority,
            "due_date": due_date
        }