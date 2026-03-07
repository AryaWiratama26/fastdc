"""
FastDC Custom Exceptions
"""


class FastDCError(Exception):
    """Base exception for FastDC"""
    pass


class ProviderNotConfigured(FastDCError):
    """Raised when trying to use an AI provider that hasn't been configured"""
    def __init__(self, provider: str):
        super().__init__(f"Provider '{provider}' not configured. Use add_ai_provider() first.")


class InvalidProvider(FastDCError):
    """Raised when an unsupported AI provider is specified"""
    def __init__(self, provider: str):
        super().__init__(f"Unsupported provider: '{provider}'. Use 'groq' or 'openai'.")
