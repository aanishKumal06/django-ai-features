from pydantic import BaseModel, Field
from typing import List

class HealthAdviceSchema(BaseModel):
    recommended_activities: List[str] | None = Field(description="Activities that help cure or manage the condition.")
    foods_to_eat: List[str] | None = Field(description="Foods the patient should eat.")
    foods_to_avoid: List[str] | None = Field(description="Foods the patient should avoid.")

