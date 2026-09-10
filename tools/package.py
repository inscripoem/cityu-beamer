# SPDX-License-Identifier: MIT
"""Build a source-only Overleaf ZIP; this does not grant artwork permissions."""

import argparse
import hashlib
from pathlib import Path
import tempfile
import zipfile


# Source path -> archive path. Only compilation inputs and user documents ship.
PACKAGE_FILES = {
    "beamerthemeCityU.sty": "beamerthemeCityU.sty",
    "main.tex": "main.tex",
    "example-zh.tex": "example-zh.tex",
    "minimal.tex": "minimal.tex",
    "latexmkrc": "latexmkrc",
    "LICENSE": "LICENSE",
    "NOTICE.md": "NOTICE.md",
    "overleaf/README.md": "README.md",
    "overleaf/README.zh.md": "README.zh.md",
    "assets/title.png": "assets/title.png",
    "assets/section.png": "assets/section.png",
    "assets/content.png": "assets/content.png",
    "assets/closing.png": "assets/closing.png",
    "assets/README.md": "assets/README.md",
    "docs/USAGE.md": "docs/USAGE.md",
    "docs/USAGE.zh.md": "docs/USAGE.zh.md",
}


def build_package(project_root: Path, output_dir: Path, *, overwrite: bool = False) -> Path:
    project_root = project_root.resolve()
    # Validate every input before touching any existing release files.
    for relative in PACKAGE_FILES:
        source = project_root / relative
        if not source.is_file():
            raise FileNotFoundError(f"Required package file is missing: {relative}")
        if not source.resolve().is_relative_to(project_root):
            raise ValueError(f"Package input points outside the project: {relative}")

    archive = output_dir / "cityu-beamer-overleaf.zip"
    checksum = archive.with_suffix(".zip.sha256")
    if not overwrite and (archive.exists() or checksum.exists()):
        raise FileExistsError("Release output already exists; use --force to replace it")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Stage both outputs locally before replacing the named release files.
    with tempfile.TemporaryDirectory(prefix=".package-", dir=output_dir) as staging:
        staged_archive = Path(staging) / archive.name
        with zipfile.ZipFile(staged_archive, "w") as package:
            for source, destination in sorted(PACKAGE_FILES.items(), key=lambda item: item[1]):
                entry = zipfile.ZipInfo(destination, date_time=(1980, 1, 1, 0, 0, 0))
                entry.create_system = 3
                entry.external_attr = 0o100644 << 16
                package.writestr(
                    entry, (project_root / source).read_bytes(),
                    compress_type=zipfile.ZIP_DEFLATED, compresslevel=9,
                )
        digest = hashlib.sha256(staged_archive.read_bytes()).hexdigest()
        staged_checksum = Path(staging) / checksum.name
        staged_checksum.write_bytes(f"{digest}  {archive.name}\n".encode("ascii"))
        staged_archive.replace(archive)
        staged_checksum.replace(checksum)
    return archive


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="replace existing files in dist/")
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    try:
        archive = build_package(project_root, project_root / "dist", overwrite=args.force)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Packaging failed: {error}\n")
    print(f"Created {archive.name} ({len(PACKAGE_FILES)} files, {archive.stat().st_size} bytes) in dist/")
    print(archive.with_suffix(".zip.sha256").read_text(encoding="ascii").strip())
    print("CityU artwork is not MIT-licensed; check NOTICE.md before public distribution.")


if __name__ == "__main__":
    main()
