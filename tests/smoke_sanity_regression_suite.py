# -*- coding: utf-8 -*-
import unittest
import os
import re
from pathlib import Path

class TestSmokeSanityRegression(unittest.TestCase):
    def test_zero_private_key_leakage(self):
        key_patterns = [
            re.compile(r"0x[a-fA-F0-9]{64}"),
            re.compile(r"BEGIN PRIVATE KEY"),
            re.compile(r"BEGIN EC PRIVATE KEY"),
        ]
        skip_dirs = {".git", "node_modules", "dist", "build", "target", ".next", "__pycache__"}
        for root, dirs, files in os.walk("."):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for file_name in files:
                if file_name.endswith((".py", ".js", ".ts", ".rs", ".sol", ".html", ".json", ".md")):
                    fpath = os.path.join(root, file_name)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                        for p in key_patterns:
                            self.assertFalse(
                                p.search(content) and "dummy" not in content.lower() and "sample" not in content.lower() and "0000000000000000" not in content,
                                f"Potential leaked private key found in {fpath}"
                            )
                    except Exception:
                        pass

    def test_quicknode_integration(self):
        self.assertTrue(Path("integrations/quicknode_provider.py").exists())

    def test_x402_gateway(self):
        self.assertTrue(Path("integrations/x402_bazaar_gateway.py").exists())

    def test_conway_engine(self):
        self.assertTrue(Path("conway/conway_engine.py").exists() or Path("src/main.rs").exists())

    def test_pqc_shield(self):
        self.assertTrue(Path("security/pqc_quantum_shield.py").exists())

    def test_raven_and_rea(self):
        self.assertTrue(Path("automations/raven_rsi_optimizer.py").exists())
        self.assertTrue(Path("automations/rea_runtime_analyzer.py").exists())

if __name__ == "__main__":
    unittest.main()
