# Consent Shield
Automated Consent Workflows for AI models.

## Features
* Pre-built React components for consent modals with audit logging
* Support for layered consent (e.g., 'allow data use for research but not marketing')
* Real-time revocation triggers pipeline retraining alerts

## Usage
1. Create a `ConsentModal` instance with the desired type and message.
2. Add the `ConsentModal` instance to the `ConsentShield` instance.
3. Use the `ConsentShield` instance to manage consents and trigger retraining alerts.

## Testing
Run `pytest` to execute the tests.
