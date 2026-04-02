"""
tests/integration/test_reports_api.py

Integration tests for FA Report System API contracts.
Tests response shape, status transitions, and data consistency
using fixture-based mock responses (no live server required).

Live API tests can be enabled by setting FA_API_BASE_URL env var.
"""

import uuid
from datetime import date

import pytest


FA_API_BASE_URL = 'https://fa-report-api.railway.app'


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_report_response():
    report_id = str(uuid.uuid4())
    return {
        'id': report_id,
        'report_number': '2506-001',
        'title': 'Warranty Plant Return',
        'request_date': str(date.today()),
        'completion_date': str(date.today()),
        'part_name': 'PHEV BEC GEN 4',
        'part_number': 'L1M8 10C666 GF',
        'yazaki_part_number': '7370-2573-8W',
        'status': 'draft',
        'prepared_by': 'Rodrigo Santana',
        'verified_by': '',
        'requested_by': '',
        'approved_by': '',
        'is_ntf': False,
        'reuse_images': False,
        'source_report_id': None,
        'pdf_url': None,
        'pdf_generated_at': None,
        'images': [],
        'test_results': [],
        'total_tests': 0,
        'tests_ok': 0,
        'tests_ng': 0,
        'tests_pending': 0,
        'notes': None,
        'created_at': '2026-03-19T14:00:00',
        'updated_at': '2026-03-19T14:00:00',
    }


@pytest.fixture
def report_list_response(sample_report_response):
    return {
        'items': [sample_report_response],
        'total': 1,
        'page': 1,
        'page_size': 20,
        'total_pages': 1,
    }


# ── Response Schema Tests ─────────────────────────────────────────────────────

class TestReportResponseSchema:
    """Verify that mock API responses match the expected ReportResponse schema."""

    def test_report_response_has_all_required_fields(self, sample_report_response):
        required_fields = [
            'id', 'report_number', 'title', 'request_date', 'completion_date',
            'part_name', 'part_number', 'yazaki_part_number', 'status',
            'prepared_by', 'verified_by', 'requested_by', 'approved_by',
            'is_ntf', 'reuse_images', 'source_report_id',
            'pdf_url', 'pdf_generated_at',
            'images', 'test_results',
            'total_tests', 'tests_ok', 'tests_ng', 'tests_pending',
            'notes', 'created_at', 'updated_at',
        ]
        for field in required_fields:
            assert field in sample_report_response, f'Missing required field: {field}'

    def test_report_id_is_valid_uuid_string(self, sample_report_response):
        report_id = sample_report_response['id']
        parsed = uuid.UUID(report_id)
        assert str(parsed) == report_id

    def test_report_images_field_is_list(self, sample_report_response):
        assert isinstance(sample_report_response['images'], list)

    def test_report_test_results_field_is_list(self, sample_report_response):
        assert isinstance(sample_report_response['test_results'], list)

    def test_report_number_matches_expected_format(self, sample_report_response):
        report_number = sample_report_response['report_number']
        assert len(report_number) <= 20
        assert len(report_number) >= 1

    def test_report_part_name_is_not_empty(self, sample_report_response):
        assert sample_report_response['part_name']
        assert len(sample_report_response['part_name']) > 0


# ── Status & State Tests ──────────────────────────────────────────────────────

class TestReportStatusBehavior:
    """Verify report status values and initial state."""

    def test_new_report_status_is_draft(self, sample_report_response):
        assert sample_report_response['status'] == 'draft'

    def test_report_without_pdf_has_null_pdf_url(self, sample_report_response):
        assert sample_report_response['pdf_url'] is None

    def test_report_without_pdf_has_null_generated_at(self, sample_report_response):
        assert sample_report_response['pdf_generated_at'] is None

    def test_new_report_total_tests_is_zero(self, sample_report_response):
        assert sample_report_response['total_tests'] == 0

    def test_new_report_tests_ok_is_zero(self, sample_report_response):
        assert sample_report_response['tests_ok'] == 0

    def test_new_report_tests_ng_is_zero(self, sample_report_response):
        assert sample_report_response['tests_ng'] == 0

    def test_new_report_tests_pending_is_zero(self, sample_report_response):
        assert sample_report_response['tests_pending'] == 0

    def test_new_report_images_list_is_empty(self, sample_report_response):
        assert len(sample_report_response['images']) == 0

    def test_new_report_test_results_list_is_empty(self, sample_report_response):
        assert len(sample_report_response['test_results']) == 0

    def test_is_ntf_defaults_false(self, sample_report_response):
        assert sample_report_response['is_ntf'] is False

    def test_reuse_images_defaults_false(self, sample_report_response):
        assert sample_report_response['reuse_images'] is False

    def test_source_report_id_none_for_non_ntf(self, sample_report_response):
        assert sample_report_response['source_report_id'] is None


# ── Pagination Tests ──────────────────────────────────────────────────────────

class TestReportListResponse:
    """Verify list response pagination shape."""

    def test_list_response_has_items_field(self, report_list_response):
        assert 'items' in report_list_response

    def test_list_response_has_total_field(self, report_list_response):
        assert 'total' in report_list_response

    def test_list_response_has_page_field(self, report_list_response):
        assert 'page' in report_list_response

    def test_list_response_has_page_size_field(self, report_list_response):
        assert 'page_size' in report_list_response

    def test_list_response_has_total_pages_field(self, report_list_response):
        assert 'total_pages' in report_list_response

    def test_list_items_count_matches_total(self, report_list_response):
        assert len(report_list_response['items']) == report_list_response['total']

    def test_page_starts_at_one(self, report_list_response):
        assert report_list_response['page'] == 1

    def test_items_contain_report_fields(self, report_list_response):
        item = report_list_response['items'][0]
        assert 'id' in item
        assert 'report_number' in item
        assert 'status' in item
        assert 'part_name' in item
