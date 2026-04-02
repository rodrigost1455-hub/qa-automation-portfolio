"""
tests/unit/test_report_schemas.py

Unit tests for FA-Report-System Pydantic schemas.
Tests: field validation, model validators, edge cases, boundary conditions.

Based on: https://github.com/rodrigost1455-hub/FA-Report-System
Schema: backend/app/schemas/report.py
"""

import uuid
from datetime import date
from typing import Optional

import pytest
from pydantic import BaseModel, Field, ValidationError, model_validator


# ── Local schema replica (avoids needing the full app stack) ─────────────────

class ReportCreate(BaseModel):
    report_number: str = Field(..., min_length=1, max_length=20)
    title: str = Field(default="Warranty Plant Return", max_length=120)
    request_date: date
    part_name: str = Field(..., min_length=1, max_length=120)
    part_number: str = Field(..., min_length=1, max_length=60)
    yazaki_part_number: str = Field(..., min_length=1, max_length=60)
    notes: Optional[str] = None
    prepared_by_id: Optional[uuid.UUID] = None
    prepared_by_name: Optional[str] = Field(None, max_length=120)
    verified_by_name: Optional[str] = Field(None, max_length=120)
    is_ntf: bool = False
    reuse_images: bool = False
    source_report_id: Optional[uuid.UUID] = None

    @model_validator(mode='after')
    def validate_ntf_source(self):
        if self.reuse_images and not self.source_report_id:
            raise ValueError('source_report_id es requerido cuando reuse_images=True')
        return self

    @model_validator(mode='after')
    def validate_at_least_one_signature(self):
        has_prepared = self.prepared_by_id or self.prepared_by_name
        if not has_prepared:
            raise ValueError('Se requiere al menos prepared_by_id o prepared_by_name')
        return self


class TestReportCreateHappyPath:
    def test_minimal_valid_payload(self, valid_report_payload):
        report = ReportCreate(**valid_report_payload)
        assert report.report_number == '2506-001'
        assert report.part_name == 'PHEV BEC GEN 4'
        assert report.is_ntf is False

    def test_default_title_applied(self, valid_report_payload):
        payload = {k: v for k, v in valid_report_payload.items() if k != 'title'}
        report = ReportCreate(**payload)
        assert report.title == 'Warranty Plant Return'

    def test_custom_title_accepted(self, valid_report_payload):
        valid_report_payload['title'] = 'Custom FA Report'
        report = ReportCreate(**valid_report_payload)
        assert report.title == 'Custom FA Report'

    def test_ntf_report_with_source_id(self, ntf_report_payload):
        report = ReportCreate(**ntf_report_payload)
        assert report.is_ntf is True
        assert report.reuse_images is True
        assert report.source_report_id is not None

    def test_signature_via_uuid(self, valid_report_payload):
        valid_report_payload.pop('prepared_by_name', None)
        valid_report_payload['prepared_by_id'] = uuid.uuid4()
        report = ReportCreate(**valid_report_payload)
        assert report.prepared_by_id is not None

    def test_optional_notes_accepted(self, valid_report_payload):
        valid_report_payload['notes'] = 'Component shows physical damage on connector J1.'
        report = ReportCreate(**valid_report_payload)
        assert 'connector J1' in report.notes

    def test_optional_notes_none_by_default(self, valid_report_payload):
        report = ReportCreate(**valid_report_payload)
        assert report.notes is None


class TestReportCreateValidationErrors:
    def test_missing_report_number_raises(self, valid_report_payload):
        del valid_report_payload['report_number']
        with pytest.raises(ValidationError) as exc_info:
            ReportCreate(**valid_report_payload)
        assert 'report_number' in str(exc_info.value)

    def test_empty_report_number_raises(self, valid_report_payload):
        valid_report_payload['report_number'] = ''
        with pytest.raises(ValidationError):
            ReportCreate(**valid_report_payload)

    def test_report_number_exceeds_max_length(self, valid_report_payload):
        valid_report_payload['report_number'] = 'X' * 21
        with pytest.raises(ValidationError):
            ReportCreate(**valid_report_payload)

    def test_report_number_at_max_length(self, valid_report_payload):
        valid_report_payload['report_number'] = 'X' * 20
        report = ReportCreate(**valid_report_payload)
        assert len(report.report_number) == 20

    def test_missing_part_name_raises(self, valid_report_payload):
        del valid_report_payload['part_name']
        with pytest.raises(ValidationError) as exc_info:
            ReportCreate(**valid_report_payload)
        assert 'part_name' in str(exc_info.value)

    def test_no_signature_raises(self, valid_report_payload):
        del valid_report_payload['prepared_by_name']
        with pytest.raises(ValidationError) as exc_info:
            ReportCreate(**valid_report_payload)
        assert 'prepared_by' in str(exc_info.value).lower()

    def test_reuse_images_without_source_raises(self, valid_report_payload):
        valid_report_payload['reuse_images'] = True
        valid_report_payload['source_report_id'] = None
        with pytest.raises(ValidationError) as exc_info:
            ReportCreate(**valid_report_payload)
        assert 'source_report_id' in str(exc_info.value)

    def test_invalid_date_format_raises(self, valid_report_payload):
        valid_report_payload['request_date'] = 'not-a-date'
        with pytest.raises(ValidationError):
            ReportCreate(**valid_report_payload)

    def test_title_exceeds_max_length(self, valid_report_payload):
        valid_report_payload['title'] = 'T' * 121
        with pytest.raises(ValidationError):
            ReportCreate(**valid_report_payload)

    def test_title_at_max_length_is_valid(self, valid_report_payload):
        valid_report_payload['title'] = 'T' * 120
        report = ReportCreate(**valid_report_payload)
        assert len(report.title) == 120


class TestReportCreateEdgeCases:
    def test_report_number_single_char(self, valid_report_payload):
        valid_report_payload['report_number'] = '1'
        report = ReportCreate(**valid_report_payload)
        assert report.report_number == '1'

    def test_future_request_date_accepted(self, valid_report_payload):
        valid_report_payload['request_date'] = date(2030, 12, 31)
        report = ReportCreate(**valid_report_payload)
        assert report.request_date.year == 2030

    def test_is_ntf_defaults_false(self, valid_report_payload):
        report = ReportCreate(**valid_report_payload)
        assert report.is_ntf is False

    def test_reuse_images_defaults_false(self, valid_report_payload):
        report = ReportCreate(**valid_report_payload)
        assert report.reuse_images is False

    def test_source_report_id_accepted_as_string_uuid(self, valid_report_payload):
        source_id = uuid.uuid4()
        valid_report_payload['source_report_id'] = str(source_id)
        valid_report_payload['reuse_images'] = True
        report = ReportCreate(**valid_report_payload)
        assert report.source_report_id == source_id

    def test_invalid_uuid_for_source_report_id_raises(self, valid_report_payload):
        valid_report_payload['source_report_id'] = 'not-a-uuid'
        valid_report_payload['reuse_images'] = True
        with pytest.raises(ValidationError):
            ReportCreate(**valid_report_payload)
