# REQUIREMENTS.md – consent‑shield  

**Document version:** 1.0  
**Last updated:** 2026‑06‑18  
**Author:** Senior Product/Engineering Lead, AxentX  

---  

## 1. Overview  

**consent‑shield** is a data‑protection and consent‑management platform built for AI‑driven applications operating in highly regulated domains (e.g., health, education). It provides a unified, auditable API and UI for:

* Capturing, storing, and managing user consent records.  
* Enforcing consent policies at runtime across data‑processing pipelines (including vLLM‑based inference services).  
* Supporting data‑subject rights (access, rectification, erasure, portability).  
* Generating compliance artefacts for GDPR, HIPAA, FERPA, and related regulations.  

The platform must be **privacy‑by‑design**, **secure‑by‑default**, and **scalable** to serve multi‑tenant SaaS environments.

---  

## 2. Scope  

| In‑Scope | Out‑Of‑Scope |
|----------|--------------|
| • REST/GraphQL API for consent CRUD operations. <br>• Web UI for administrators, data‑subjects, and auditors. <br>• Policy engine that integrates with downstream AI services (e.g., vLLM, SGLang). <br>• Immutable audit log with tamper‑evidence. <br>• Encryption at rest & in‑transit, key‑management integration. <br>• Multi‑tenant isolation and RBAC. | • Full‑stack AI model training pipelines (outside of consent enforcement). <br>• On‑premise hardware provisioning. <br>• Legal advisory services. |

---  

## 3. Functional Requirements  

| ID | Requirement | Description |
|----|-------------|-------------|
| **FR‑1** | **Consent Capture API** | Provide a **POST /consents** endpoint that accepts a JSON payload containing: <br>• `subject_id` (UUID) <br>• `data_controller_id` (UUID) <br>• `purpose` (enumerated list) <br>• `legal_basis` (e.g., consent, contract) <br>• `scope` (data categories) <br>• `timestamp` (ISO‑8601) <br>• `signature` (optional client‑side digital signature). The API must validate schema, enforce idempotency, and return a `consent_id`. |
| **FR‑2** | **Consent Retrieval** | **GET /consents/{consent_id}** returns the full consent record, including its current status (active, withdrawn, expired). Must support filtering by `subject_id`, `controller_id`, `purpose`, and `status`. |
| **FR‑3** | **Consent Withdrawal** | **PATCH /consents/{consent_id}** with `{ "status": "withdrawn", "withdrawn_at": "...", "reason": "..." }`. The system must record the withdrawal event in the immutable audit log and instantly propagate the change to downstream policy enforcement points. |
| **FR‑4** | **Data‑Subject Rights API** | Provide endpoints for: <br>• **Access** – `GET /subjects/{subject_id}/data` (export in JSON‑LD). <br>• **Rectification** – `PUT /subjects/{subject_id}` (update personal data). <br>• **Erasure** – `DELETE /subjects/{subject_id}` (hard delete all consent records and associated personal data). <br>All actions must be logged and trigger notifications to the data controller. |
| **FR‑5** | **Policy Evaluation Engine** | Expose a **POST /policy/evaluate** endpoint that receives a data‑access request (subject_id, data_type, purpose) and returns `allow` / `deny` with a justification. The engine must consult the latest consent state and any applicable regulatory constraints. |
| **FR‑6** | **Audit Log Service** | Immutable, append‑only log stored in a tamper‑evident store (e.g., AWS QLDB, Azure Confidential Ledger). Every state‑changing operation (create, update, withdraw, delete) must generate a signed log entry containing: <br>• operation type <br>• actor (service account or user) <br>• timestamp <br>• cryptographic hash of the affected record. |
| **FR‑7** | **Role‑Based Access Control (RBAC)** | Admin UI and API must enforce granular permissions: <br>• `admin` – full access across tenants. <br>• `controller` – manage consents for their own organization only. <br>• `auditor` – read‑only view of audit logs. <br>• `subject` – self‑service rights (FR‑4). |
| **FR‑8** | **Multi‑Tenant Isolation** | All data must be partitioned by `tenant_id`. No cross‑tenant data leakage is allowed, even at the storage layer. |
| **FR‑9** | **Compliance Artefact Generation** | Generate downloadable compliance packages (PDF/JSON) that include: <br>• Consent register summary <br>• Audit log excerpt for a given period <br>• Data‑processing impact assessment (template populated with consent metadata). |
| **FR‑10** | **Integration SDKs** | Provide lightweight client SDKs (Python, JavaScript)
