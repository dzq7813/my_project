"""Custom PyInstaller hook for PySide6 plugins and libraries.

The project currently uses Tkinter, but this hook ensures that if PySide6
widgets are introduced later the required Qt plugins and shared libraries are
collected automatically. The logic is defensive so that the hook does not raise
errors when PySide6 is not installed in the build environment.
"""
from __future__ import annotations

from typing import Any, Iterable

hiddenimports: list[str] = []
binaries: list[tuple[str, str]] = []
datas: list[tuple[str, str]] = []

try:  # pragma: no cover - executed only when PyInstaller provides utilities
    from PyInstaller.utils.hooks import collect_dynamic_libs, collect_qt_plugins
except ModuleNotFoundError:  # pragma: no cover - makes the hook import-safe locally
    collect_dynamic_libs = None  # type: ignore[assignment]
    collect_qt_plugins = None  # type: ignore[assignment]


def _safe_call(func: Any, *args: Iterable[Any]) -> list[tuple[str, str]]:
    if func is None:
        return []
    try:
        return list(func(*args))  # type: ignore[misc]
    except Exception:
        return []


qt_plugins = ["platforms", "styles", "iconengines"]

binaries.extend(_safe_call(collect_dynamic_libs, "PySide6"))
datas.extend(_safe_call(collect_qt_plugins, qt_plugins))

if binaries or datas:
    hiddenimports.extend(
        ["PySide6.QtCore", "PySide6.QtGui", "PySide6.QtWidgets", "PySide6.QtSvg"]
    )
