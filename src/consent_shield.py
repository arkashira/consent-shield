import json
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

class ConsentType(str, Enum):
    RESEARCH = "research"
    MARKETING = "marketing"

@dataclass
class ConsentModal:
    id: int
    type: ConsentType
    message: str
    audit_log: List[str]

class ConsentShield:
    def __init__(self):
        self.consents = {}

    def add_consent(self, consent_modal: ConsentModal):
        self.consents[consent_modal.id] = consent_modal

    def get_consent(self, id: int) -> ConsentModal:
        return self.consents.get(id)

    def revoke_consent(self, id: int):
        if id in self.consents:
            del self.consents[id]

    def trigger_retraining_alert(self, id: int):
        if id not in self.consents:
            raise ValueError("Consent not found")

    def audit_log(self, id: int, message: str):
        if id in self.consents:
            self.consents[id].audit_log.append(message)

def create_consent_modal(id: int, type: ConsentType, message: str) -> ConsentModal:
    return ConsentModal(id, type, message, [])

def main():
    consent_shield = ConsentShield()
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    consent_shield.add_consent(consent_modal)
    print(json.dumps(consent_shield.get_consent(1).__dict__))

if __name__ == "__main__":
    main()
