from pydantic import BaseModel


class ConsultationResponseSchema(BaseModel):
    mobile_number: str
    response: str