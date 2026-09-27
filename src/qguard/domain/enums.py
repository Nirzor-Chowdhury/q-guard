from enum import StrEnum


class SecurityState(StrEnum):
    """Security state used by the adaptive policy engine."""

    NORMAL = "NORMAL"
    DEGRADED = "DEGRADED"
    SUSPICIOUS = "SUSPICIOUS"
    MITM_SUSPECTED = "MITM_SUSPECTED"
    BLOCKED = "BLOCKED"


class SecurityMode(StrEnum):
    """Permitted cryptographic operating modes."""

    QKD_ASSISTED = "QKD_ASSISTED"
    PQC_ONLY = "PQC_ONLY"
    HYBRID = "HYBRID"


class PolicyAction(StrEnum):
    """Actions that the policy engine may return."""

    CONTINUE = "CONTINUE"
    SWITCH_SECURITY_MODE = "SWITCH_SECURITY_MODE"
    REAUTHENTICATE = "REAUTHENTICATE"
    REQUEST_NEW_KEYS = "REQUEST_NEW_KEYS"
    TERMINATE = "TERMINATE"
    BLOCK = "BLOCK"


class FindingCategory(StrEnum):
    """Categories for security findings produced by the handshake analyzer."""

    CERTIFICATE = "CERTIFICATE"
    TLS = "TLS"
    KEY_EXCHANGE = "KEY_EXCHANGE"
    AUTHENTICATION = "AUTHENTICATION"
    PQC = "PQC"
    DOWNGRADE = "DOWNGRADE"
    CONFIGURATION = "CONFIGURATION"


class FindingSeverity(StrEnum):
    """Severity levels for security findings."""

    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class PQCMode(StrEnum):
    """Observed PQC capability of a connection (telemetry only in Phase 2)."""

    CLASSICAL = "CLASSICAL"
    HYBRID = "HYBRID"
    PQC_ONLY = "PQC_ONLY"
    UNKNOWN = "UNKNOWN"
