import os
from openai import OpenAI
from pydantic import BaseModel
import instructor

from src.schema import LMRemedy, LMRuling
import dotenv
import json

dotenv.load_dotenv()

# client = instructor.from_openai(
#     OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
# )

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

def deepseek_ruling(ruling):
    res = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {
                "role": "user", 
                "content": """
{ruling}

Given the legal ruling above, parse it into JSON format following the schema:

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
    terms: Optional[List[str]] = None  # Specific requirements or conditions
    restrictions: Optional[List[str]] = None  # What is prohibited/restricted
    
    # Status tracking
    status: str = "ordered"  # ordered, in_effect, completed, modified, terminated
    effective_date: datetime
    end_date: Optional[datetime] = None


Now return your response in JSON, and ONLY IN JSON:
    """.format(ruling=ruling)
            },
        ],
    )
    print(res.choices[0].message.content)
    return json.loads(res.choices[0].message.content)


if __name__ == "__main__":
    with open("cases/onsc/2024onsc6990", encoding="utf-8") as f:
        ruling = f.read()
        res = deepseek_ruling(ruling)
        print(res)
