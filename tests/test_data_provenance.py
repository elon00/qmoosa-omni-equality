"""
Tests for Authenticated Data Provenance and Ingestion (Copernicus & OCDS).
"""

from core.data.provenance import (
    DataProvenanceRecord,
    PlanetaryDataIngestor,
    OCDSProcurementIngestor,
)


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
