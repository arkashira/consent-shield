import pytest
from consent_shield import ConsentShield, ConsentModal, ConsentType, create_consent_modal

def test_create_consent_modal():
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    assert consent_modal.id == 1
    assert consent_modal.type == ConsentType.RESEARCH
    assert consent_modal.message == "Allow data use for research"
    assert consent_modal.audit_log == []

def test_add_consent():
    consent_shield = ConsentShield()
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    consent_shield.add_consent(consent_modal)
    assert consent_shield.get_consent(1) == consent_modal

def test_get_consent():
    consent_shield = ConsentShield()
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    consent_shield.add_consent(consent_modal)
    assert consent_shield.get_consent(1) == consent_modal

def test_revoke_consent():
    consent_shield = ConsentShield()
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    consent_shield.add_consent(consent_modal)
    consent_shield.revoke_consent(1)
    assert consent_shield.get_consent(1) is None

def test_trigger_retraining_alert():
    consent_shield = ConsentShield()
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    consent_shield.add_consent(consent_modal)
    with pytest.raises(ValueError):
        consent_shield.trigger_retraining_alert(2)

def test_audit_log():
    consent_shield = ConsentShield()
    consent_modal = create_consent_modal(1, ConsentType.RESEARCH, "Allow data use for research")
    consent_shield.add_consent(consent_modal)
    consent_shield.audit_log(1, "Test message")
    assert consent_shield.get_consent(1).audit_log == ["Test message"]
