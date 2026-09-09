from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest
from contextlib import redirect_stdout
from io import StringIO
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_manifest


class ManifestTest(unittest.TestCase):
    def test_left_regular_manifest_uses_the_paper_parameters(self) -> None:
        data = verify_manifest.load_manifest(verify_manifest.DEFAULT_MANIFEST)
        entry = next(item for item in data["entries"] if item["id"] == "binary-left-regular")
        for command, expected in zip(entry["commands"], (
            {"--k": "1048576", "--regions": "64", "--region-length": "32768", "--cutoff": "230718"},
            {"--k": "1048572", "--regions": "28", "--region-length": "74898", "--cutoff": "230730", "--memory": "9"},
        )):
            argv = command["argv"]
            for name, value in expected.items():
                self.assertEqual(argv[argv.index(name) + 1], value)
            self.assertIn("success: True", command["expect"])

    def test_left_regular_commands_exit_nonzero_on_failed_certificate(self) -> None:
        import regular_ea_certificate as ea
        import regular_ec_certificate as ec

        result = SimpleNamespace(success=False, total_bound=2, security_bits=-1,
            exact_bound=2, intermediate_bound=0, dense_bound=0,
            largest_exact_r=1, largest_exact_term=2, intermediate_blocks=1, dense_blocks=1)
        for module, name in ((ea, "verify_regular_ea_parameters"),
                             (ec, "verify_regular_ec_parameters")):
            with patch.object(module, name, return_value=result), patch.object(
                sys, "argv", [module.__file__]
            ), redirect_stdout(StringIO()), self.assertRaises(SystemExit) as raised:
                module.main()
            self.assertEqual(raised.exception.code, 1)

    def test_entire_manifest_survives_crlf_checkout(self) -> None:
        data = verify_manifest.load_manifest(verify_manifest.DEFAULT_MANIFEST)
        paths = set(verify_manifest.trusted_source_paths())
        paths.update(verify_manifest.ROOT / name for name in data["artifacts"])
        with TemporaryDirectory() as directory:
            root = Path(directory)
            for source in paths:
                destination = root / source.relative_to(verify_manifest.ROOT)
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(verify_manifest.canonical_bytes(source).replace(b"\n", b"\r\n"))
            with patch.object(verify_manifest, "ROOT", root):
                self.assertEqual(verify_manifest.check_manifest(data, strict_versions=False), [])

    def test_line_endings_do_not_change_artifact_or_source_digest(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "example.py"
            source.write_bytes(b"value = 7\nprint(value)\n")
            with patch.object(verify_manifest, "ROOT", root), patch.object(
                verify_manifest, "trusted_source_paths", return_value=[source]
            ):
                original = (verify_manifest.sha256_file(source),
                            verify_manifest.source_tree_sha256())
                source.write_bytes(b"value = 7\r\nprint(value)\r\n")
                self.assertEqual(original, (verify_manifest.sha256_file(source),
                                            verify_manifest.source_tree_sha256()))
                source.write_bytes(b"value = 8\r\nprint(value)\r\n")
                self.assertNotEqual(original[0], verify_manifest.sha256_file(source))
                self.assertNotEqual(original[1], verify_manifest.source_tree_sha256())

    def test_checked_in_manifest(self) -> None:
        data = verify_manifest.load_manifest(verify_manifest.DEFAULT_MANIFEST)
        self.assertEqual(verify_manifest.check_manifest(data, strict_versions=True), [])

    def test_rejects_changed_artifact(self) -> None:
        data = verify_manifest.load_manifest(verify_manifest.DEFAULT_MANIFEST)
        changed = json.loads(json.dumps(data))
        relative = next(iter(changed["artifacts"]))
        changed["artifacts"][relative] = "0" * 64
        errors = verify_manifest.check_manifest(changed, strict_versions=False)
        self.assertTrue(any("artifact digest mismatch" in error for error in errors))

    def test_rejects_path_escape(self) -> None:
        with self.assertRaises(ValueError):
            verify_manifest.resolve_artifact("../outside.json")

    def test_rejects_unpinned_command_input(self) -> None:
        data = verify_manifest.load_manifest(verify_manifest.DEFAULT_MANIFEST)
        changed = json.loads(json.dumps(data))
        relative = next(iter(changed["artifacts"]))
        del changed["artifacts"][relative]
        errors = verify_manifest.check_manifest(changed, strict_versions=False)
        self.assertTrue(any("unpinned artifact" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
