# keywords.py - Fixed version with corrected spelling and comprehensive keywords

KEYWORDS = {
    "FR": [
        "shall", "must", "will", "allow", "enable", "support", "provide",
        "create", "delete", "update", "read", "write", "display", "send",
        "receive", "authenticate", "authorize", "login", "logout", "register",
        "search", "filter", "sort", "upload", "download", "export", "import",
        "generate", "validate", "calculate", "schedule", "notify", "store",
        "retrieve", "sync", "merge", "submit", "process", "view", "add",
        "remove", "edit", "modify", "insert", "select", "query", "fetch"
    ],
    
    # NFR subcategories
    "performance": [
        "fast", "response time", "latency", "throughput", "speed", "milliseconds",
        "performance", "benchmark", "optimize", "optimization", "optimized",
        "scalable", "scalability",
        "concurrent", "concurrency", "load", "stress", "timeout", "time out",
        "low latency", "high performance", "millisecond", "second", "minute",
        "requests per second", "transactions per second", "rps", "tps",
        "processing time", "execution time", "query time", "render time",
        "page load", "fps", "frames per second"
    ],
    
    "security": [
        "encrypt", "encryption", "decrypt", "decryption", "secure", "security",
        "authentication", "authorize", "authorization", "access control",
        "role", "token", "oauth", "ssl", "tls", "https", "hash", "hashing",
        "password", "credential", "xss", "csrf", "sql injection",
        "input sanitize", "input sanitization", "sanitize",
        "audit", "audit log", "audit trail", "vulnerability", "securely store",
        "confidentiality", "integrity", "non-repudiation", "session timeout",
        "two-factor", "multi-factor", "mfa", "2fa", "firewall", "penetration",
        "aes", "rsa", "sha", "md5", "salt", "rbac", "saml", "attack",
        "malware", "virus", "breach", "threat"
    ],
    
    "usability": [
        "user friendly", "user-friendly", "usability", "intuitive", "easy to use",
        "help", "guide", "guideline", "document", "documentation",
        "error message", "error messages", "ux", "user experience", "ui",
        "user interface", "accessibility", "accessible", "responsive",
        "onboarding", "tutorial", "tooltip", "help text", "wizard",
        "navigation", "navigate", "learn", "learning curve", "training",
        "clarity", "clear", "simple", "readable", "consistency", "consistent",
        "design", "layout", "color scheme", "typography", "visual",
        "mobile-friendly", "screen reader"
    ],
    
    "reliability": [
        "reliability", "reliable", "fault", "fault-tolerant", "fault tolerant",
        "recover", "recovery", "recoverable", "consistent", "consistency",
        "data integrity", "durable", "durability", "backup", "restore",
        "redundant", "redundancy", "failover", "fail-over", "transactional",
        "acid", "availability", "available", "uptime", "downtime",
        "mtbf", "mttr", "disaster recovery", "high availability", "ha",
        "replication", "replicate", "rpo", "rto", "recovery point",
        "recovery time", "resilient", "resilience", "robust", "stable"
    ],
    
    "scalability": [
        "scale", "scalable", "scalability", "scaling", "horizontal",
        "vertical", "elastic", "elasticity", "auto-scale", "auto scale",
        "auto scaling", "auto-scaling", "distributed", "shard", "sharding",
        "partition", "partitioning", "cluster", "clustering", "load balance",
        "load balancing", "node", "nodes", "instance", "instances",
        "capacity", "growth", "expand", "concurrent users", "simultaneous",
        "peak load", "traffic spike", "workload"
    ],
    
    "maintainability": [
        "maintain", "maintenance", "maintainable", "modular", "module",
        "component", "extensible", "flexible", "reusable", "reuse",
        "refactor", "refactoring", "code quality", "technical debt",
        "documentation", "comment", "readable", "test", "testing",
        "testable", "debug", "debugging", "logging", "log", "monitor",
        "monitoring", "clean code", "coupling", "cohesion", "dependency",
        "versioning", "api", "backward compatible", "deprecation",
        "automated testing", "unit test", "integration test", "coverage",
        "complexity", "cyclomatic", "naming convention", "inline documentation",
        "rollback", "deployment", "continuous integration", "ci", "cd",
        "build automation", "lint", "linting", "code review", "artifact",
        "repository", "version control", "git", "dependency injection",
        "separation of concerns", "solid", "design pattern", "architecture",
        "tracing", "diagnostics", "profiling", "performance monitoring",
        "health check", "metrics", "dashboard", "alerting", "observability"
    ],
    
    "portability": [
        "portable", "portability", "platform", "cross-platform",
        "operating system", "os", "windows", "linux", "macos", "unix",
        "android", "ios", "browser", "chrome", "firefox", "safari",
        "mobile", "desktop", "web", "cloud", "on-premise", "on-premises",
        "hybrid", "migrate", "migration", "port", "porting",
        "compatible", "compatibility", "interoperable", "interoperability",
        "platform independent", "platform-independent", "database agnostic",
        "vendor neutral", "vendor-neutral", "containerized", "docker",
        "kubernetes", "virtualization", "virtual machine", "vm",
        "cross-browser", "responsive design", "adaptive", "multi-platform",
        "processor architecture", "arm", "x86", "x64", "instruction set",
        "endianness", "byte order", "file system", "path separator",
        "environment variable", "configuration", "runtime", "jvm",
        "interpreter", "compilation", "cross-compilation", "abstraction layer",
        "wrapper", "adapter", "bridge", "facade", "plugin", "extension",
        "cloud provider", "aws", "azure", "google cloud", "gcp",
        "infrastructure", "deployment target", "package format"
    ],
    
    "legal": [
        "gdpr", "hipaa", "compliance", "compliant", "comply",
        "regulation", "regulatory", "law", "legal", "audit",
        "audit trail", "audit log", "sox", "pci-dss", "pci",
        "privacy", "data protection", "terms of service", "tos",
        "license", "licensing", "copyright", "trademark",
        "intellectual property", "contract", "agreement", "policy",
        "policies", "standard", "iso", "certification", "certified",
        "personal data", "personally identifiable", "pii", "phi",
        "protected health information", "consent", "opt-in", "opt-out",
        "data subject", "data controller", "data processor", "right to erasure",
        "right to be forgotten", "data portability", "retention period",
        "retention policy", "data residency", "data sovereignty", "jurisdiction",
        "cookie", "eprivacy", "coppa", "children", "parental consent",
        "age verification", "lawful intercept", "legal hold", "disclosure",
        "breach notification", "drm", "digital rights", "algorithmic decision",
        "explainability", "transparency", "export control", "sanction",
        "embargo", "wcag", "accessibility standard", "ada", "terms and conditions",
        "eula", "end user license", "electronic signature", "esign", "dmca",
        "takedown", "safe harbor", "anti-money laundering", "aml", "kyc",
        "know your customer", "fcra", "tcpa", "do not call", "ferpa",
        "student privacy", "fda", "sec", "fcc", "regulatory body",
        "data breach", "incident response", "forensics", "chain of custody"
    ]
}

# Flattened lists for quick access
FR_KEYWORDS = KEYWORDS["FR"]

ALL_NFR_KEYWORDS = (
    KEYWORDS["performance"] + 
    KEYWORDS["security"] + 
    KEYWORDS["usability"] + 
    KEYWORDS["reliability"] + 
    KEYWORDS["scalability"] +
    KEYWORDS["maintainability"] +
    KEYWORDS["portability"] +
    KEYWORDS["legal"]
)

# Individual NFR category keywords (useful for sub-classification)
PERFORMANCE_KEYWORDS = KEYWORDS["performance"]
SECURITY_KEYWORDS = KEYWORDS["security"]
USABILITY_KEYWORDS = KEYWORDS["usability"]
RELIABILITY_KEYWORDS = KEYWORDS["reliability"]
SCALABILITY_KEYWORDS = KEYWORDS["scalability"]
MAINTAINABILITY_KEYWORDS = KEYWORDS["maintainability"]
PORTABILITY_KEYWORDS = KEYWORDS["portability"]
LEGAL_KEYWORDS = KEYWORDS["legal"]

# Category mapping for sub-classification
NFR_CATEGORY_KEYWORDS = {
    "PE": PERFORMANCE_KEYWORDS,      # Performance
    "SE": SECURITY_KEYWORDS,         # Security
    "US": USABILITY_KEYWORDS,        # Usability
    "RA": RELIABILITY_KEYWORDS,      # Reliability/Availability
    "SC": SCALABILITY_KEYWORDS,      # Scalability
    "MA": MAINTAINABILITY_KEYWORDS,  # Maintainability
    "PO": PORTABILITY_KEYWORDS,      # Portability
    "LE": LEGAL_KEYWORDS             # Legal
}