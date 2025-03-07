from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field
from decimal import Decimal
from datetime import datetime
from enum import Enum
from pydantic import BaseModel

class RemedyCategory(str, Enum):
    MONETARY = "monetary"
    INJUNCTIVE = "injunctive"
    DECLARATORY = "declaratory"
    SPECIFIC_PERFORMANCE = "specific_performance"
    CRIMINAL_PENALTY = "criminal_penalty"
    ADMINISTRATIVE_PENALTY = "administrative_penalty"

class RemedySubtype(str, Enum):
    # Monetary subtypes
    COMPENSATORY_DAMAGES = "compensatory_damages"
    PUNITIVE_DAMAGES = "punitive_damages"
    STATUTORY_DAMAGES = "statutory_damages"
    RESTITUTION = "restitution"
    CHILD_SUPPORT = "child_support"
    SPOUSAL_SUPPORT = "spousal_support"
    COSTS = "costs"
    
    # Injunctive subtypes
    PERMANENT_INJUNCTION = "permanent_injunction"
    TEMPORARY_INJUNCTION = "temporary_injunction"
    RESTRAINING_ORDER = "restraining_order"
    
    # Criminal/Administrative subtypes
    INCARCERATION = "incarceration"
    PROBATION = "probation"
    LICENSE_SUSPENSION = "license_suspension"
    FINE = "fine"
    COMMUNITY_SERVICE = "community_service"

class Remedy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ruling_id: int = Field(foreign_key="ruling.id")
    
    # Core classification
    category: RemedyCategory
    subtype: RemedySubtype
    
    # Monetary components (used when category is MONETARY)
    amount: Optional[Decimal] = Field(default=None)
    
    # Duration components (used for injunctions, criminal penalties, etc.)
    duration_value: Optional[int] = None
    duration_unit: Optional[str] = None  # "days", "months", "years"
    
    # Specific terms and conditions
    terms: Optional[str] = None  # Specific requirements or conditions
    restrictions: Optional[str] = None  # What is prohibited/restricted
    
    # Status tracking
    status: str = "ordered"  # ordered, in_effect, completed, modified, terminated
    effective_date: datetime
    end_date: Optional[datetime] = None

    @classmethod
    def from_json(cls, json_data: dict):
        if "effective_date" in json_data:
            json_data["effective_date"] = datetime.fromisoformat(json_data["effective_date"])
        if "end_date" in json_data and json_data["end_date"]:
            json_data["end_date"] = datetime.fromisoformat(json_data["end_date"])
        if "amount" in json_data and json_data["amount"]:
            json_data["amount"] = Decimal(str(json_data["amount"]))
        if "category" in json_data:
            json_data["category"] = RemedyCategory(json_data["category"])
        if "subtype" in json_data:
            json_data["subtype"] = RemedySubtype(json_data["subtype"])
        return cls(**json_data)

    def to_json(self):
        data = {
            "id": self.id,
            "ruling_id": self.ruling_id,
            "category": self.category.value,
            "subtype": self.subtype.value,
            "amount": str(self.amount) if self.amount else None,
            "duration_value": self.duration_value,
            "duration_unit": self.duration_unit,
            "terms": self.terms,
            "restrictions": self.restrictions,
            "status": self.status,
            "effective_date": self.effective_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None
        }
        return data

class Ruling(SQLModel, table=True):
    """
    A minimal SQLModel schema for a single legal ruling,
    capturing core information needed for analytics on outcomes,
    success rates, typical damages, decision factors, etc.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic Identifiers / Metadata
    case_name: str
    docket_number: Optional[str] = None
    date_filed: Optional[date] = None
    date_decided: Optional[date] = None
    jurisdiction: Optional[str] = None
    court_level: Optional[str] = None  # e.g., "Superior Court", "Court of Appeal"
    judge_name: Optional[str] = None

    # Categorization / Legal Context
    case_category: Optional[str] = None  # e.g. "Employment", "Family", "Personal Injury", etc.
    legal_issues: Optional[str] = None   # Text or JSON to capture key legal questions

    # Outcome / Success Information
    outcome_for_plaintiff: Optional[bool] = None  # True if plaintiff prevailed, etc.
    outcome_details: Optional[str] = None         # e.g., "Partial settlement", "Dismissed", etc.

    # Penalty or Sentence (for criminal/administrative cases)
    penalty_type: Optional[str] = None  # e.g., "6-month license suspension", "3 months jail", etc.
    penalty_amount: Optional[Decimal] = Field(default=None, ge=0)  # fine amount
    penalty_duration: Optional[int] = Field(default=None, ge=0)  # in days/months

    remedy_id: Optional[int] = Field(default=None, foreign_key="remedy.id")

    # Decision Factors
    decision_factors: Optional[str] = None  # Text or JSON describing what influenced the judge's ruling

    # Precedent / References
    cited_cases: Optional[str] = None       # Could store references in JSON or comma-separated form

    # Procedural or Timeline Information
    # (date_filed and date_decided can help derive duration)
    summary: Optional[str] = None           # A short textual summary if desired

    @classmethod
    def from_json(cls, json_data: dict):
        if "date_filed" in json_data and json_data["date_filed"]:
            json_data["date_filed"] = date.fromisoformat(json_data["date_filed"])
        if "date_decided" in json_data and json_data["date_decided"]:
            json_data["date_decided"] = date.fromisoformat(json_data["date_decided"])
        if "penalty_amount" in json_data and json_data["penalty_amount"]:
            json_data["penalty_amount"] = Decimal(str(json_data["penalty_amount"]))
        if "remedy" in json_data and json_data["remedy"]:
            json_data["remedy"] = Remedy.from_json(json_data["remedy"])
        return cls(**json_data)

    def to_json(self):
        data = {
            "id": self.id,
            "case_name": self.case_name,
            "docket_number": self.docket_number,
            "date_filed": self.date_filed.isoformat() if self.date_filed else None,
            "date_decided": self.date_decided.isoformat() if self.date_decided else None,
            "jurisdiction": self.jurisdiction,
            "court_level": self.court_level,
            "judge_name": self.judge_name,
            "case_category": self.case_category,
            "legal_issues": self.legal_issues,
            "outcome_for_plaintiff": self.outcome_for_plaintiff,
            "outcome_details": self.outcome_details,
            "penalty_type": self.penalty_type,
            "penalty_amount": str(self.penalty_amount) if self.penalty_amount else None,
            "penalty_duration": self.penalty_duration,
            "remedy": self.remedy.to_json() if self.remedy else None,
            "decision_factors": self.decision_factors,
            "cited_cases": self.cited_cases,
            "summary": self.summary
        }
        return data


class LMRemedy(BaseModel):
    """Represents the remedy ordered by the court"""
    remedy_type: Optional[str] = None  # e.g., "damages", "injunction", "specific performance"
    monetary_amount: Optional[Decimal] = None
    terms: Optional[List[str]] = None  # List of remedy terms/conditions
    duration: Optional[int] = None  # Duration in days if applicable
    description: Optional[str] = None  # Detailed description of remedy

    @classmethod
    def from_json(cls, json_data: dict):
        if "monetary_amount" in json_data and json_data["monetary_amount"]:
            json_data["monetary_amount"] = Decimal(str(json_data["monetary_amount"]))
        if "terms" in json_data and json_data["terms"] and isinstance(json_data["terms"], str):
            json_data["terms"] = json_data["terms"].split(",")
        return cls(**json_data)

    def to_json(self):
        return {
            "remedy_type": self.remedy_type,
            "monetary_amount": str(self.monetary_amount) if self.monetary_amount else None,
            "terms": ",".join(self.terms) if self.terms else None,
            "duration": self.duration,
            "description": self.description
        }

class LMRuling(BaseModel):
    """Represents a legal ruling/decision"""
    id: Optional[int] = None
    case_name: str
    docket_number: str
    date_filed: Optional[date] = None
    date_decided: Optional[date] = None
    jurisdiction: str
    court_level: str
    judge_name: str
    case_category: str
    legal_issues: Optional[List[str]] = None
    outcome_for_plaintiff: Optional[bool] = None
    outcome_details: Optional[str] = None
    penalty_type: Optional[str] = None
    penalty_amount: Optional[Decimal] = None
    penalty_duration: Optional[int] = None
    remedy: Optional[Remedy] = None
    decision_factors: Optional[List[str]] = None
    cited_cases: Optional[List[str]] = None
    summary: Optional[str] = None

