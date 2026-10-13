"""
Tests for Authenticated Data Provenance and Ingestion (Copernicus & OCDS).
"""

from core.data.provenance import (
    DataProvenanceRecord,
    PlanetaryDataIngestor,
    OCDSProcurementIngestor,
)
from core.data.copernicus_adapter import CopernicusSentinelAdapter
from core.data.ocds_adapter import OCDSProcurementAdapter


def test_copernicus_sentinel_ingestion_and_digest():
    record = PlanetaryDataIngestor.ingest_sentinel_scene(
        scene_id="S2B_MSIL2A_20261013T100000",
        coordinates={"lat": 28.6139, "lon": 77.2090},
        indices={"NDVI": 0.55, "surface_temp_kelvin": 298.2}
    )

    manifest = record.to_provenance_manifest()
    assert manifest["source_authority"] == "ESA-Copernicus-Hub"
    assert manifest["license_spdx"] == "CC-BY-4.0"
    assert manifest["equity_review_required"] is True
    assert len(manifest["content_digest_sha256"]) == 64

    # Verification of payload integrity
    verified = DataProvenanceRecord.verify_provenance_digest({
        "data_payload": record.data_payload,
        "content_digest_sha256": record.content_digest_sha256
    })
    assert verified is True


def test_ocds_procurement_ingestion():
    record = OCDSProcurementIngestor.ingest_procurement_release(
        ocid="ocds-213kz6-EXP-2026-001",
        buyer_name="Ministry of Public Health & Social Parity",
        tender_value=12_500_000.0,
        currency="USD"
    )

    manifest = record.to_provenance_manifest()
    assert manifest["source_authority"] == "Open-Contracting-Data-Registry"
    assert manifest["license_spdx"] == "CC-0"
    assert len(record.content_digest_sha256) == 64


def test_copernicus_adapter_validation_and_bounds():
    adapter = CopernicusSentinelAdapter()

    # Valid scene
    valid, record, msg = adapter.fetch_or_verify_scene(
        scene_id="S2A_OPER_MSI_L2A_2026",
        coordinates={"lat": 45.0, "lon": 9.0},
        indices={"NDVI": 0.42}
    )
    assert valid is True
    assert record is not None
    assert "VERIFIED_LOCAL" in msg

    # Invalid coordinates
    valid_bad_coord, _, msg_coord = adapter.fetch_or_verify_scene(
        scene_id="BAD_COORDS",
        coordinates={"lat": 95.0, "lon": 9.0},
        indices={"NDVI": 0.42}
    )
    assert valid_bad_coord is False
    assert "Invalid geographic coordinates" in msg_coord

    # Invalid NDVI (out of [-1, 1])
    valid_bad_ndvi, _, msg_ndvi = adapter.fetch_or_verify_scene(
        scene_id="BAD_NDVI",
        coordinates={"lat": 45.0, "lon": 9.0},
        indices={"NDVI": 1.5}
    )
    assert valid_bad_ndvi is False
    assert "NDVI vegetation index out of mathematical bounds" in msg_ndvi


def test_copernicus_adapter_live_collections_or_network_fallback():
    adapter = CopernicusSentinelAdapter()
    ok, record, msg = adapter.fetch_live_collections(timeout=5.0)
    if ok:
        assert record is not None
        assert record.license_spdx == "CC-BY-4.0"
        assert len(record.content_digest_sha256) == 64
        assert "LIVE_VERIFIED" in msg
    else:
        # If offline or network timeout, ensure graceful, honest status
        assert "NETWORK_UNAVAILABLE" in msg or "BLOCKED" in msg or "ERROR" in msg


def test_ocds_adapter_validation():
    # Valid release
    ok, record, msg = OCDSProcurementAdapter.validate_and_ingest_release(
        ocid="ocds-998877-PROJECT-01",
        buyer_id="AGENCY-42",
        tender_amount=500_000.0,
        currency="EUR"
    )
    assert ok is True
    assert record is not None
    assert record.license_spdx == "CC-0"

    # Malformed OCID (missing prefix)
    ok_bad, _, msg_bad = OCDSProcurementAdapter.validate_and_ingest_release(
        ocid="INVALID-PREFIX-01",
        buyer_id="AGENCY-42",
        tender_amount=500_000.0,
        currency="EUR"
    )
    assert ok_bad is False
    assert "Invalid OCID identifier prefix" in msg_bad

    # Negative tender
    ok_neg, _, msg_neg = OCDSProcurementAdapter.validate_and_ingest_release(
        ocid="ocds-998877-PROJECT-NEG",
        buyer_id="AGENCY-42",
        tender_amount=-100.0,
        currency="EUR"
    )
    assert ok_neg is False
    assert "Negative tender valuation" in msg_neg
