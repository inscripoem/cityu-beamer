# SPDX-License-Identifier: MIT
"""Exercise the release packager with real files, without TeX dependencies."""

import hashlib
import importlib
import os
from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import unquote, urlsplit
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
EXPECTED_ARCHIVE_FILES = (
    "beamerthemeCityU.sty", "main.tex", "example-zh.tex", "minimal.tex",
    "latexmkrc", "LICENSE", "NOTICE.md", "README.md", "README.zh.md",
    "assets/title.png", "assets/section.png", "assets/content.png",
    "assets/closing.png", "assets/README.md", "docs/USAGE.md", "docs/USAGE.zh.md",
)
# Include repository-only files so accidental packaging is observable.
FIXTURE_FILES = (
    "beamerthemeCityU.sty", "main.tex", "example-zh.tex", "minimal.tex",
    "latexmkrc", "LICENSE", "NOTICE.md", "README.md", "README.zh.md",
    "CONTRIBUTING.md", "CHANGELOG.md", "requirements-dev.txt",
    "assets/title.png", "assets/section.png", "assets/content.png",
    "assets/closing.png", "assets/README.md",
    "docs/USAGE.md", "docs/VALIDATION.md", "docs/OVERLEAF.md", "docs/GITHUB.md",
    "tests/options.tex", "tests/sections.tex", "tests/manual-pages.tex",
    "tests/test_package.py", "tools/inspect_pdf.py", "tools/check_layout.py",
    "tools/check_examples.py", "tools/package.py",
    "docs/USAGE.zh.md", "overleaf/README.md", "overleaf/README.zh.md",
)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.assertTrue(
            (PROJECT / "tools/package.py").is_file(),
            "The release packager tools/package.py has not been implemented",
        )
        self.packager = importlib.import_module("tools.package")
        build = PROJECT / "build"
        build.mkdir(exist_ok=True)
        temporary = tempfile.TemporaryDirectory(prefix="package-tests-", dir=build)
        self.addCleanup(temporary.cleanup)
        self.temporary = Path(temporary.name)
        self.source = self.temporary / "source with spaces"
        self.output = self.source / "dist"
        for relative in FIXTURE_FILES:
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(f"fixture for {relative}\n".encode())

    def build(self, *, overwrite=False):
        return self.packager.build_package(self.source, self.output, overwrite=overwrite)

    def test_archive_has_root_main_portable_names_and_both_license_notices(self):
        archive = self.build()
        self.assertEqual(archive, self.output / "cityu-beamer-overleaf.zip")
        with zipfile.ZipFile(archive) as package:
            self.assertIsNone(package.testzip())
            self.assertEqual(package.namelist(), sorted(EXPECTED_ARCHIVE_FILES))
            self.assertEqual(package.read("main.tex"), b"fixture for main.tex\n")
            self.assertEqual(package.read("LICENSE"), b"fixture for LICENSE\n")
            self.assertEqual(package.read("assets/README.md"), b"fixture for assets/README.md\n")
            for relative in EXPECTED_ARCHIVE_FILES:
                if relative not in ("README.md", "README.zh.md"):
                    self.assertEqual(package.read(relative), (self.source / relative).read_bytes())

    def test_readmes_use_package_instructions_instead_of_repository_previews(self):
        with zipfile.ZipFile(self.build()) as package:
            self.assertEqual(package.read("README.md"), b"fixture for overleaf/README.md\n")
            self.assertEqual(package.read("README.zh.md"), b"fixture for overleaf/README.zh.md\n")

    def test_repository_only_files_are_not_required_to_build_the_package(self):
        for relative in (
            "README.md", "README.zh.md", "CONTRIBUTING.md", "CHANGELOG.md",
            "requirements-dev.txt", "docs/VALIDATION.md", "docs/OVERLEAF.md",
            "docs/GITHUB.md", "tests/options.tex", "tests/sections.tex",
            "tests/manual-pages.tex", "tests/test_package.py",
            "tools/inspect_pdf.py", "tools/check_layout.py",
            "tools/check_examples.py", "tools/package.py",
        ):
            (self.source / relative).unlink()
        try:
            archive = self.build()
        except FileNotFoundError as error:
            self.fail(f"Compilation package depends on repository-only material: {error}")
        with zipfile.ZipFile(archive) as package:
            self.assertEqual(package.namelist(), sorted(EXPECTED_ARCHIVE_FILES))

    def test_packaged_document_links_resolve_without_repository_files(self):
        archive = self.packager.build_package(PROJECT, self.temporary / "real package")
        checked = 0
        with zipfile.ZipFile(archive) as package:
            names = set(package.namelist())
            for name in sorted(names):
                if not name.endswith(".md"):
                    continue
                content = package.read(name).decode("utf-8")
                # Project documentation uses inline Markdown links and images.
                for target in re.findall(r"\]\(([^\s)]+)\)", content):
                    with self.subTest(document=name, target=target):
                        url = urlsplit(target)
                        if url.scheme or url.netloc:
                            self.assertIn(url.scheme, ("https", "http"))
                            self.assertTrue(url.netloc)
                        else:
                            resolved = posixpath.normpath(posixpath.join(
                                posixpath.dirname(name), unquote(url.path),
                            )) if url.path else name
                            self.assertIn(resolved, names, f"Broken packaged link: {name} -> {target}")
                        checked += 1
        self.assertGreater(checked, 0, "The archive contains no documentation links to check")

    def test_checksum_describes_the_actual_archive(self):
        archive = self.build()
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        checksum = archive.with_suffix(".zip.sha256")
        self.assertEqual(checksum.read_text(), f"{digest}  cityu-beamer-overleaf.zip\n")

    def test_unlisted_private_files_and_build_outputs_are_not_packaged(self):
        for relative in (
            ".env", ".git/config", "original.pptx", "build/main.pdf",
            "previews/overview.png", "assets/unapproved.svg", "docs/private-notes.md",
            "tools/private-helper.py", ".github/workflows/latex.yml",
        ):
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b"DO NOT PUBLISH")
        with zipfile.ZipFile(self.build()) as package:
            self.assertEqual(set(package.namelist()), set(EXPECTED_ARCHIVE_FILES))
            self.assertFalse(any(b"DO NOT PUBLISH" in package.read(name) for name in package.namelist()))

    def test_same_inputs_produce_identical_bytes_despite_different_file_times(self):
        first = self.build().read_bytes()
        for relative in FIXTURE_FILES:
            os.utime(self.source / relative, (1700000000, 1700000000))
        second = self.packager.build_package(self.source, self.temporary / "another output")
        self.assertEqual(first, second.read_bytes())

    def test_existing_archive_is_not_overwritten_without_permission(self):
        archive = self.build()
        before = archive.read_bytes()
        (self.source / "main.tex").write_bytes(b"changed source")
        with self.assertRaises(FileExistsError):
            self.build()
        self.assertEqual(archive.read_bytes(), before)

    def test_explicit_overwrite_refreshes_archive_and_checksum(self):
        archive = self.build()
        before = archive.read_bytes()
        (self.source / "main.tex").write_bytes(b"changed source")
        self.build(overwrite=True)
        with zipfile.ZipFile(archive) as package:
            self.assertEqual(package.read("main.tex"), b"changed source")
        self.assertNotEqual(archive.read_bytes(), before)
        digest = hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertTrue(archive.with_suffix(".zip.sha256").read_text().startswith(digest + "  "))

    def test_missing_artwork_does_not_replace_a_good_archive(self):
        archive = self.build()
        before = archive.read_bytes()
        checksum_before = archive.with_suffix(".zip.sha256").read_bytes()
        (self.source / "assets/content.png").unlink()
        with self.assertRaises(FileNotFoundError):
            self.build(overwrite=True)
        self.assertEqual(archive.read_bytes(), before)
        self.assertEqual(archive.with_suffix(".zip.sha256").read_bytes(), checksum_before)

    def test_missing_package_instructions_do_not_replace_a_good_archive(self):
        archive = self.build()
        before = archive.read_bytes()
        checksum_before = archive.with_suffix(".zip.sha256").read_bytes()
        for relative in ("overleaf/README.md", "overleaf/README.zh.md"):
            with self.subTest(source=relative):
                source = self.source / relative
                content = source.read_bytes()
                source.unlink()
                try:
                    with self.assertRaises(FileNotFoundError):
                        self.build(overwrite=True)
                    self.assertEqual(archive.read_bytes(), before)
                    self.assertEqual(archive.with_suffix(".zip.sha256").read_bytes(), checksum_before)
                finally:
                    source.write_bytes(content)

    def test_cli_uses_the_script_location_not_the_working_directory(self):
        script = self.source / "tools/package.py"
        shutil.copyfile(PROJECT / "tools/package.py", script)
        result = subprocess.run(
            [sys.executable, str(script)], cwd=self.temporary,
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.output / "cityu-beamer-overleaf.zip").is_file())


if __name__ == "__main__":
    unittest.main()
