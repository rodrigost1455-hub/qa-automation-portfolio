"""
conftest.py
Shared fixtures and pytest configuration for the entire test suite.
"""

import uuid
import pytest
from datetime import date


@pytest.fixture
def today():
    return date.today()


@pytest.fixture
def valid_report_payload():
    return {
        'report_number': '2506-001',
        'title': 'Warranty Plant Return',
        'request_date': date.today(),
        'part_name': 'PHEV BEC GEN 4',
        'part_number': 'L1M8 10C666 GF',
        'yazaki_part_number': '7370-2573-8W',
        'prepared_by_name': 'Rodrigo Santana',
        'is_ntf': False,
        'reuse_images': False,
    }


@pytest.fixture
def ntf_report_payload(valid_report_payload):
    return {
        **valid_report_payload,
        'report_number': '2506-002',
        'is_ntf': True,
        'reuse_images': True,
        'source_report_id': str(uuid.uuid4()),
    }
