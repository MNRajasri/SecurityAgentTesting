from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()

class RuleChangeRequest(BaseModel):
    source_ip: str
    dest_port: int
    protocol: str
    action: str
    justification: str

@app.post("/apply-rule")
async def apply_rule(rule: RuleChangeRequest):
    return {
        "status": "success",
        "rule_id": str(uuid.uuid4()),
        "applied_at": datetime.utcnow().isoformat(),
        "details": rule.dict()
    }
