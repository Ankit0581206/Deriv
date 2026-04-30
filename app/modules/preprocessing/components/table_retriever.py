from typing import List
import json
from app.services.llm import llm_service

class TableRetriever:
    """
    LLM-based table retriever that intelligently selects relevant tables 
    based on the user's natural language query.
    """
    
    # Available tables in the database
    AVAILABLE_TABLES = {
        "users": "Stores user profiles including ID, email, full_name, country, KYC status, risk level, PEP status, and account status",
        "transactions": "Records financial activities with transaction type, instrument, amount, currency, status, payment method, and flags",
        "login_events": "Logs user login attempts including IP address, location, device information, status, and failure reasons"
    }
    
    async def retrieve(self, query: str, top_k: int = 3) -> List[str]:
        """
        Identifies relevant tables using keyword analysis.
        For a small schema (3 tables), rule-based selection is faster
        and avoids consuming LLM rate-limit quota.
        """
        return self._keyword_fallback(query)
    
    
    def _keyword_fallback(self, query: str) -> List[str]:
        """
        Simple keyword-based fallback for table selection if LLM fails.
        """
        relevant = []
        q = query.lower()
        
        # Check for user-related keywords
        if any(keyword in q for keyword in ["user", "customer", "kyc", "risk", "pep", "account", "profile"]):
            relevant.append("users")
        
        # Check for transaction-related keywords
        if any(keyword in q for keyword in ["transaction", "deposit", "withdrawal", "trade", "payment", "amount", "transfer", "instrument", "amzn", "aapl", "tsla", "gold", "amazon", "google", "bitcoin", "flag", "reason"]):
            relevant.append("transactions")
        
        # Check for login-related keywords
        if any(keyword in q for keyword in ["login", "activity", "auth", "ip", "device", "session", "access"]):
            relevant.append("login_events")
        
        # If no keywords matched, return all tables
        return relevant if relevant else list(self.AVAILABLE_TABLES.keys())
