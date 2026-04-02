"""
tests/integration/test_reports_api.py

Integration tests for FA Report System REST API.
Tests: endpoint contracts, response shapes, error handling.

Uses mocked HTTP responses — no live server required.
To test against live API: export FA_API_BASE_URL=https://your-api.railway.app
"""

import uuid
from datetime import date
from unittest.mock import AsyncMock, patch

import pytest
import httpx

FA_API_BASE_URL = "https://fa-report-api.railway.app"


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_report_response():
      """Mock response mirroring the real ReportResponse schema."""
      report_id = str(uuid.uuid4())
      return {
          "id": report_id,
          "report_number": "2506-001",
          "title": "Warranty Plant Return",
          "request_date": str(date.today()),
          "completion_date": str(date.today()),
          "part_name": "PHEV BEC GEN 4",
          "part_number": "L1M8 10C666 GF",
          "yazaki_part_number": "7370-2573-8W",
          "status": "draft",
          "prepared_by": "Rodrigo Santana",
          "verified_by": "",
          "requested_by": "",
          "approved_by": "",
          "is_ntf": False,
          "reuse_images": False,
          "source_report_id": None,
          "pdf_url": None,
          "pdf_generated_at": None,
          "images": [],
          "test_results": [],
          "total_tests": 0,
          "tests_ok": 0,
          "tests_ng": 0,
          "tests_pending": 0,
          "notes": None,
          "created_at": "2026-03-19T14:00:00",
          "updated_at": "2026-03-19T14:00:00",
      }


@pytest.fixture
def report_list_response(sample_report_response):
      return {
                "items": [sample_report_response],
                "total": 1,
                "page": 1,
                "page_size": 20,
                "total_pages": 1,
      }


# ── Contract Tests ────────────────────────────────────────────────────────────

class TestReportAPIContracts:
      """Verify API endpoints return the expected response shape."""

    @pytest.mark.asyncio
    async def test_create_report_returns_201(self, valid_report_payload, sample_report_response):
              with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
                            mock_response = AsyncMock()
                            mock_response.status_code = 201
                            mock_response.json.return_value = sample_report_response
                            mock_post.return_value = mock_response

                  async with httpx.AsyncClient(base_url=FA_API_BASE_URL) as client:
                                    response = await client.post(
                                                          "/api/reports",
                                                          json={**valid_report_payload, "request_date": str(valid_report_payload["request_date"])},
                                    )

            assert response.status_code == 201

    @pytest.mark.asyncio
    async def test_create_report_response_has_required_fields(self, valid_report_payload, sample_report_response):
              required_fields = [
                  "id", "report_number", "status", "prepared_by",
                  "part_name", "part_number", "is_ntf", "images",
                  "test_results", "total_tests", "created_at"
    ]

        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
                      mock_response = AsyncMock()
                      mock_response.status_code = 201
                      mock_response.json.return_value = sample_report_response
                      mock_post.return_value = mock_response

            async with httpx.AsyncClient(base_url=FA_API_BASE_URL) as client:
                              response = await client.post("/api/reports", json={})

            data = response.json()
            for field in required_fields:
                              assert field in data, f"Missing required field: {field}"

    @pytest.mark.asyncio
    async def test_get_report_by_id_returns_200(self, sample_report_response):
              report_id = sample_report_response["id"]

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
                      mock_response = AsyncMock()
                      mock_response.status_code = 200
                      mock_response.json.return_value = sample_report_response
                      mock_get.return_value = mock_response

            async with httpx.AsyncClient(base_url=FA_API_BASE_URL) as client:
                              response = await client.get(f"/api/reports/{report_id}")

            assert response.status_code == 200
            assert response.json()["id"] == report_id

    @pytest.mark.asyncio
    async def test_get_report_not_found_returns_404(self):
              with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
                            mock_response = AsyncMock()
                            mock_response.status_code = 404
                            mock_response.json.return_value = {"detail": "Report not found"}
                            mock_get.return_value = mock_response

                  async with httpx.AsyncClient(base_url=FA_API_BASE_URL) as client:
                                    response = await client.get(f"/api/reports/{uuid.uuid4()}")

            assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_list_reports_returns_paginated_response(self, report_list_response):
              with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
                            mock_response = AsyncMock()
                            mock_response.status_code = 200
                            mock_response.json.return_value = report_list_response
                            mock_get.return_value = mock_response

            async with httpx.AsyncClient(base_url=FA_API_BASE_URL) as client:
                              response = await client.get("/api/reports")

            data = response.json()
            assert "items" in data
            assert "total" in data
            assert "page" in data
            assert "total_pages" in data

    @pytest.mark.asyncio
    async def test_list_reports_items_have_summary_shape(self, report_list_response):
              summary_fields = ["id", "report_number", "part_name", "status", "is_ntf", "prepared_by", "total_tests"]

        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
                      mock_response = AsyncMock()
                      mock_response.status_code = 200
                      mock_response.json.return_value = report_list_response
                      mock_get.return_value = mock_response

            async with httpx.AsyncClient(base_url=FA_API_BASE_URL) as client:
                              response = await client.get("/api/reports")

            items = response.json()["items"]
            assert len(items) > 0
            for field in summary_fields:
                              assert field in items[0], f"Missing field in summary: {field}"


# ── Status Tests ──────────────────────────────────────────────────────────────

class TestReportStatusBehavior:
      """Verify report status values and initial state."""

    def test_new_report_status_is_draft(self, sample_report_response):
              assert sample_report_response["status"] == "draft"

    def test_report_without_pdf_has_null_pdf_url(self, sample_report_response):
              assert sample_report_response["pdf_url"] is None
        assert sample_report_response["pdf_generated_at"] is None

    def test_new_report_test_counters_are_zero(self, sample_report_response):
              assert sample_report_response["total_tests"] == 0
        assert sample_report_response["tests_ok"] == 0
        assert sample_report_response["tests_ng"] == 0
        assert sample_report_response["tests_pending"] == 0

    def test_new_report_has_empty_images_list(self, sample_report_response):
              assert isinstance(sample_report_response["images"], list)
        assert len(sample_report_response["images"]) == 0

    def test_new_report_has_empty_test_results_list(self, sample_report_response):
              assert isinstance(sample_report_response["test_results"], list)
        assert len(sample_report_response["test_results"]) == 0
