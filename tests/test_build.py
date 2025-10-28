from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace


def test_spec_configuration_and_assets(tmp_path):
    project_root = Path(__file__).resolve().parents[1]
    spec_path = project_root / "packaging" / "app.spec"
    assert spec_path.exists(), "Expected PyInstaller spec file to exist"

    recorded: dict[str, dict[str, object]] = {}

    class DummyAnalysis:
        def __init__(self, scripts, *args, **kwargs):  # type: ignore[no-untyped-def]
            recorded["Analysis"] = {"args": (scripts,) + args, "kwargs": kwargs}
            self.scripts = scripts
            self.binaries = []
            self.zipfiles = []
            self.datas = list(kwargs.get("datas", []))
            self.pure = []
            self.zipped_data = []

    def _recorder(name: str):
        def _inner(*args, **kwargs):  # type: ignore[no-untyped-def]
            recorded[name] = {"args": args, "kwargs": kwargs}
            return SimpleNamespace()

        return _inner

    context = {
        "__file__": str(spec_path),
        "__name__": "__main__",
        "Analysis": DummyAnalysis,
        "PYZ": _recorder("PYZ"),
        "EXE": _recorder("EXE"),
        "COLLECT": _recorder("COLLECT"),
        "BUNDLE": SimpleNamespace,
        "MERGE": _recorder("MERGE"),
    }

    exec(spec_path.read_text(encoding="utf-8"), context)

    analysis_kwargs = recorded["Analysis"]["kwargs"]  # type: ignore[index]
    datas = analysis_kwargs["datas"]  # type: ignore[index]

    asset_sources = {Path(src).name for src, _ in datas}
    asset_destinations = {dest for _, dest in datas}

    icon_call = recorded["EXE"]  # type: ignore[index]
    icon_path = Path(icon_call["kwargs"].get("icon"))  # type: ignore[arg-type]

    assert (project_root / "assets" / "icons" / "app.ico").exists()
    assert (project_root / "assets" / "icons" / "app.png").exists()
    assert (project_root / "config" / "config.json").exists()
    assert spec_path.parent.joinpath("hooks").exists(), "Custom hook directory missing"

    assert "app.ico" in asset_sources
    assert "app.png" in asset_sources
    assert "config.json" in asset_sources
    assert any(dest.startswith("assets") for dest in asset_destinations)
    assert any(dest.startswith("templates") for dest in asset_destinations)

    assert icon_path.exists(), "Icon path referenced in spec should exist"
    assert str(project_root / "packaging" / "hooks") in analysis_kwargs["hookspath"]

    hooksconfig = analysis_kwargs["hooksconfig"]
    assert "PySide6" in hooksconfig
    assert "plugins" in hooksconfig["PySide6"]

    spec_scripts = recorded["Analysis"]["args"][0]  # type: ignore[index]
    assert Path(spec_scripts[0]).name == "main.py"
