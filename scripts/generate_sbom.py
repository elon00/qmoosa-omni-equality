"""
Software Bill of Materials (SBOM) Generator.
Generates an auditable, CycloneDX/SPDX-aligned dependency inventory for supply-chain integrity.
"""

import hashlib
import importlib.metadata
import json
import os
import sys
import time


def generate_sbom(output_path: str = "sbom.json") -> dict:
    packages = []
    for dist in importlib.metadata.distributions():
        name = dist.metadata["Name"]
        version = dist.version
        license_str = dist.metadata.get("License", "Unknown")
        packages.append({
            "name": name,
            "version": version,
            "license": license_str,
            "purl": f"pkg:pypi/{name}@{version}",
        })

    # Sort packages alphabetically for determinism
    packages.sort(key=lambda p: p["name"].lower())

    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "serialNumber": f"urn:uuid:{hashlib.sha256(str(time.time()).encode()).hexdigest()[:32]}",
        "version": 1,
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "component": {
                "name": "qmoosa-omni-equality",
                "version": "1.0.0",
                "type": "application",
            }
        },
        "components": packages
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sbom, f, indent=2)

    print(f"[OK] SBOM generated with {len(packages)} components at {output_path}")
    return sbom


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "sbom.json"
    generate_sbom(out)
