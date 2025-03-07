from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import date
from decimal import Decimal

class Ruling(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic Case Identification
    case_name: str = Field(index=True)  # e.g., "Smith v. Jones"
    case_number: str = Field(unique=True, index=True)
    court: str  # e.g., "Ontario Superior Court"
    jurisdiction: str  # e.g., "Ontario", "Federal"
    ruling_date: date
    
    # Monetary Outcomes
    compensation_amount: Optional[Decimal] = Field(default=None, ge=0)  # in dollars
    damages_type: Optional[str] = Field(default=None)  # e.g., "pain and suffering", "punitive"
    settlement_amount: Optional[Decimal] = Field(default=None, ge=0)
    child_support_amount: Optional[Decimal] = Field(default=None, ge=0)
    spousal_support_amount: Optional[Decimal] = Field(default=None, ge=0)
    severance_months: Optional[float] = Field(default=None, ge=0)  # months of severance
    
    # Success Rates / Statistical Outcomes
    plaintiff_won: Optional[bool] = Field(default=None)
    claim_amount: Optional[Decimal] = Field(default=None, ge=0)  # original claim amount
    success_percentage: Optional[float] = Field(default=None, ge=0, le=100)  # for appeals, reductions
    
    # Penalty/Consequence Patterns
    penalty_type: Optional[str] = Field(default=None)  # e.g., "license suspension", "fine"
    penalty_amount: Optional[Decimal] = Field(default=None, ge=0)  # fine amount
    penalty_duration: Optional[int] = Field(default=None, ge=0)  # in days/months
    
    # Decision Factors
    key_factors: Optional[str] = Field(default=None)  # text description of influencing factors
    
    # Remedy Types
    remedy_type: Optional[str] = Field(default=None)  # e.g., "specific performance", "damages"
    contract_voided: Optional[bool] = Field(default=None)
    contract_reformed: Optional[bool] = Field(default=None)
    
    # Legal Treatment Patterns
    legal_issue: str  # e.g., "noise complaint", "breach of contract"
    ruling_outcome: str  # e.g., "upheld", "dismissed", "modified"
    
    # Comparative Outcomes
    offender_type: Optional[str] = Field(default=None)  # e.g., "first-time", "repeat"
    
    # Timeline and Procedural Information
    filing_date: Optional[date] = Field(default=None)
    resolution_date: Optional[date] = Field(default=None)
    settled_before_trial: Optional[bool] = Field(default=None)
    appeal_successful: Optional[bool] = Field(default=None)
    
    # Precedent Relationships
    cited_cases: Optional[str] = Field(default=None)  # comma-separated case numbers
    judge_name: str
    precedent_impact: Optional[str] = Field(default=None)  # e.g., "landmark", "minor"
    
    # Additional Categorization
    case_type: str  # e.g., "family law", "personal injury", "contract dispute"
    dispute_amount: Optional[Decimal] = Field(default=None, ge=0)  # amount in dispute
    
    class Config:
        arbitrary_types_allowed = True

# Example usage:
if __name__ == "__main__":
    from sqlmodel import create_engine, Session
    
    # Create SQLite database for testing
    sqlite_url = "sqlite:///legal_rulings.db"
    engine = create_engine(sqlite_url)
    
    # Create tables
    SQLModel.metadata.create_all(engine)
    
    # Example ruling
    ruling = Ruling(
        case_name="Smith v. Jones",
        case_number="CV-2023-001",
        court="Ontario Superior Court",
        jurisdiction="Ontario",
        ruling_date=date(2023, 5, 15),
        compensation_amount=Decimal("25000.00"),
        damages_type="wrongful dismissal",
        plaintiff_won=True,
        legal_issue="employment",
        ruling_outcome="upheld",
        case_type="employment law",
        judge_name="Justice A. Brown"
    )
    
    with Session(engine) as session:
        session.add(ruling)
        session.commit()