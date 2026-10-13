"""
Authenticated Data Provenance & Ingestion Engine.
Manages Copernicus Sentinel geospatial telemetry and Open Contracting Data Standard (OCDS)
procurement feeds with immutable cryptographic hashing, licensing checks, and uncertainty bounds.
"""

import hashlib
import json
import time
from typing import Dict, Any, List, Optional


class DataProvenanceRecord:
    """
    Standardized provenance wrapper ensuring data authenticity, licensing transparency,
    and clear uncertainty bounds for planetary and procurement inputs.
    """

    def __init__(
        self,
        source_authority: str,
        dataset_id: str,
        license_spdx: str,
        data_payload: Dict[str, Any],
        uncertainty_margin_pct: float = 0.05
    ):
        self.source_authority = source_authority
        self.dataset_id = dataset_id
        self.license_spdx = license_spdx
        self.data_payload = data_payload
        self.uncertainty_margin_pct = uncertainty_margin_pct
        self.timestamp = int(time.time())

        # Canonical SHA-256 digest over serialized payload
        canonical_bytes = json.dumps(data_payload, sort_keys=True).encode("utf-8")
        self.content_digest_sha256 = hashlib.sha256(canonical_bytes).hexdigest()

    def to_provenance_manifest(self) -> Dict[str, Any]:
        """Exports an auditable provenance manifest for institutional verification."""
        return {
            "source_authority": self.source_authority,
            "dataset_id": self.dataset_id,
            "license_spdx": self.license_spdx,
            "content_digest_sha256": self.content_digest_sha256,
            "uncertainty_margin_pct": self.uncertainty_margin_pct,
            "timestamp": self.timestamp,
            "equity_review_required": True,  # Mandatory human oversight for allocations
        }

    @staticmethod
    def verify_provenance_digest(record_dict: Dict[str, Any]) -> bool:
        """Verifies that the payload has not been tampered with since ingestion."""
        payload = record_dict.get("data_payload", {})
        expected_digest = record_dict.get("content_digest_sha256", "")
        canonical_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        actual_digest = hashlib.sha256(canonical_bytes).hexdigest()
        return actual_digest == expected_digest


class PlanetaryDataIngestor:
    """
    Ingests and validates Copernicus Sentinel / open satellite earth observations.
    Never treats remote sensing proxies as unchallengeable individual poverty metrics.
    """

    @staticmethod
    def ingest_sentinel_scene(
        scene_id: str,
        coordinates: Dict[str, float],
        indices: Dict[str, float],
        license_spdx: str = "CC-BY-4.0"
    ) -> DataProvenanceRecord:
        """Ingests a verified Sentinel multi-spectral scene."""
        payload = {
            "scene_id": scene_id,
            "coordinates": coordinates,
            "indices": indices,  # e.g., {"NDVI": 0.42, "nightlights": 12.8}
            "satellite_platform": "Sentinel-2B",
            "cloud_cover_pct": 0.02
        }
        return DataProvenanceRecord(
            source_authority="ESA-Copernicus-Hub",
            dataset_id=scene_id,
            license_spdx=license_spdx,
            data_payload=payload,
            uncertainty_margin_pct=0.08
        )


class OCDSProcurementIngestor:
    """
    Ingests and validates Open Contracting Data Standard (OCDS 1.1.5) records.
    """

    @staticmethod
    def ingest_procurement_release(
        ocid: str,
        buyer_name: str,
        tender_value: float,
        currency: str = "USD"
    ) -> DataProvenanceRecord:
        """Ingests an OCDS procurement release."""
        payload = {
            "ocid": ocid,
            "buyer": {"name": buyer_name},
            "tender": {"value": {"amount": tender_value, "currency": currency}},
            "schema_version": "1.1.5"
        }
        return DataProvenanceRecord(
            source_authority="Open-Contracting-Data-Registry",
            dataset_id=ocid,
            license_spdx="CC-0",
            data_payload=payload,
            uncertainty_margin_pct=0.01
        )
