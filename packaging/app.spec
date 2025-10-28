# -*- mode: python ; coding: utf-8 -*-

from __future__ import annotations

from pathlib import Path

block_cipher = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SOURCE_ENTRY = PROJECT_ROOT / "main.py"
ICON_FILE = PROJECT_ROOT / "assets" / "icons" / "app.ico"


def _collect_directory(source: Path, destination_root: str) -> list[tuple[str, str]]:
    files = []
    if not source.exists():
        return files
    for item in source.rglob("*"):
        if item.is_file():
            relative_parent = item.relative_to(source).parent
            if str(relative_parent) in (".", ""):
                target = destination_root
            else:
                target = str(Path(destination_root) / relative_parent)
            files.append((str(item), target))
    return files


def _gather_datas() -> list[tuple[str, str]]:
    datas: list[tuple[str, str]] = []
    datas.extend(_collect_directory(PROJECT_ROOT / "assets", "assets"))
    datas.extend(_collect_directory(PROJECT_ROOT / "templates", "templates"))

    config_file = PROJECT_ROOT / "config" / "config.json"
    if config_file.exists():
        datas.append((str(config_file), "config"))
    return datas


a = Analysis(
    [str(SOURCE_ENTRY)],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=_gather_datas(),
    hiddenimports=[],
    hookspath=[str(PROJECT_ROOT / "packaging" / "hooks")],
    hooksconfig={"PySide6": {"plugins": ["platforms", "styles"]}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="TabbedApp",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON_FILE) if ICON_FILE.exists() else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="TabbedApp",
)
