# -*- coding: utf-8 -*-

"""Top-level package for Cinnecta - AWS Elastic Beanstalk Cleaner."""
from .eb_cleaner import run

__author__ = """Cinnecta"""
__email__ = 'cinnecta.dev@gmail.com'
__version__ = '1.0.1'


__all__ = [
    'run'
]


def main():
    run()
