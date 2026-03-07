"""
FastDC — A Fast Discord Bot Framework
https://github.com/AryaWiratama26/fastdc
"""

from .bot import FastBot
from .exceptions import FastDCError, ProviderNotConfigured, InvalidProvider
from .models import AIProvider, AutoReplyRule, ReactionRoleMapping, AntiSpamConfig
from .utils.embed_builder import QuickEmbed
from .utils.paginator import EmbedPaginator

__version__ = '2.2.0'

__all__ = [
    'FastBot',
    'FastDCError',
    'ProviderNotConfigured',
    'InvalidProvider',
    'AIProvider',
    'AutoReplyRule',
    'ReactionRoleMapping',
    'AntiSpamConfig',
    'QuickEmbed',
    'EmbedPaginator',
    '__version__',
]