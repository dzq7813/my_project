from __future__ import annotations

import json
import os
import sys
import tkinter as tk
import webbrowser
from pathlib import Path
from tkinter import ttk

APP_ROOT = Path(__file__).resolve().parent


def resource_path(*segments: str) -> Path:
    """Return absolute path to a bundled resource."""
    base_path = Path(getattr(sys, "_MEIPASS", APP_ROOT))  # type: ignore[attr-defined]
    return base_path.joinpath(*segments)


class TabbedApp(tk.Tk):
    LINK_URL = "https://docs.python.org/zh-cn/3/library/tkinter.ttk.html"
    APPDATA_DIRNAME = "TabbedApp"
    CONFIG_FILENAME = "config.json"

    def __init__(self) -> None:
        super().__init__()

        self.appdata_dir = self._resolve_user_data_dir()
        self.config_path = self._ensure_user_config()
        self.config: dict[str, object] = self._load_config()
        self._prepare_user_directories()

        window_title = str(self.config.get("windowTitle") or "示例：Tkinter 标签页")
        self.title(window_title)
        self.minsize(480, 360)

        icon_path = resource_path("assets", "icons", "app.ico")
        if icon_path.exists():
            try:
                self.iconbitmap(icon_path)
            except tk.TclError:
                # `.ico` 仅在 Windows 上可用，忽略其他平台的错误
                pass

        self.style = ttk.Style(self)
        self.style.configure("TNotebook.Tab", padding=(12, 6))
        self.style.configure("Content.TFrame", padding=16)

        self.available_themes = sorted(self.style.theme_names())
        default_theme = self.config.get("defaultTheme")
        if isinstance(default_theme, str) and default_theme in self.available_themes:
            self.style.theme_use(default_theme)
        else:
            default_theme = self.style.theme_use()

        self.counter_value = tk.IntVar(value=0)
        self.counter_text = tk.StringVar(value="点击次数：0")
        self.selected_theme = tk.StringVar(value=default_theme)

        telemetry_enabled = bool(self.config.get("telemetryEnabled", False))
        self.option_enabled = tk.BooleanVar(value=telemetry_enabled)
        self.option_status = tk.StringVar(
            value="提示已启用" if telemetry_enabled else "提示已禁用"
        )

        self._create_widgets()

    def _create_widgets(self) -> None:
        container = ttk.Frame(self, style="Content.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.home_tab = ttk.Frame(notebook, style="Content.TFrame")
        self.settings_tab = ttk.Frame(notebook, style="Content.TFrame")
        self.about_tab = ttk.Frame(notebook, style="Content.TFrame")

        notebook.add(self.home_tab, text="首页")
        notebook.add(self.settings_tab, text="设置")
        notebook.add(self.about_tab, text="关于")

        for tab in (self.home_tab, self.settings_tab, self.about_tab):
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)

        self._build_home_tab()
        self._build_settings_tab()
        self._build_about_tab()

    def _build_home_tab(self) -> None:
        wrapper = ttk.Frame(self.home_tab)
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.columnconfigure(0, weight=1)

        greeting_label = ttk.Label(wrapper, text="你好，欢迎使用！", anchor="center")
        greeting_label.grid(row=0, column=0, pady=(0, 12), sticky="ew")

        click_button = ttk.Button(wrapper, text="点击我", command=self._increment_counter)
        click_button.grid(row=1, column=0, pady=(0, 12))

        counter_label = ttk.Label(wrapper, textvariable=self.counter_text, anchor="center")
        counter_label.grid(row=2, column=0, sticky="ew")

    def _build_settings_tab(self) -> None:
        wrapper = ttk.Frame(self.settings_tab)
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.columnconfigure(0, weight=1)

        theme_label = ttk.Label(wrapper, text="选择主题：")
        theme_label.grid(row=0, column=0, sticky="w")

        theme_combo = ttk.Combobox(
            wrapper,
            values=self.available_themes,
            textvariable=self.selected_theme,
            state="readonly",
        )
        theme_combo.grid(row=1, column=0, pady=(4, 12), sticky="ew")
        theme_combo.bind("<<ComboboxSelected>>", self._apply_theme)

        option_check = ttk.Checkbutton(
            wrapper,
            text="启用提示",
            variable=self.option_enabled,
            command=self._toggle_option,
        )
        option_check.grid(row=2, column=0, sticky="w")

        status_label = ttk.Label(wrapper, textvariable=self.option_status)
        status_label.grid(row=3, column=0, pady=(8, 0), sticky="w")

    def _build_about_tab(self) -> None:
        wrapper = ttk.Frame(self.about_tab)
        wrapper.grid(row=0, column=0, sticky="nsew")
        wrapper.columnconfigure(0, weight=1)

        app_info = (
            "应用名称：Tkinter 标签页示例\n"
            f"配置位置：{self.appdata_dir}\n"
            f"Python 版本：{sys.version.split()[0]}"
        )
        info_label = ttk.Label(wrapper, text=app_info, justify="left")
        info_label.grid(row=0, column=0, sticky="w")

        link_style = "Link.TLabel"
        self.style.configure(link_style, foreground="#1a0dab")
        self.style.map(link_style, foreground=[("active", "#551A8B")])

        link_label = ttk.Label(
            wrapper,
            text="访问 Tkinter ttk 文档",
            cursor="hand2",
            style=link_style,
        )
        link_label.configure(font=("", 10, "underline"))
        link_label.grid(row=1, column=0, pady=(12, 0), sticky="w")
        link_label.bind("<Button-1>", self._open_link)

    def _increment_counter(self) -> None:
        new_value = self.counter_value.get() + 1
        self.counter_value.set(new_value)
        self.counter_text.set(f"点击次数：{new_value}")

    def _apply_theme(self, event: tk.Event | None = None) -> None:
        selected = self.selected_theme.get()
        if selected:
            self.style.theme_use(selected)
            self.config["defaultTheme"] = selected
            self._persist_user_config()

    def _toggle_option(self) -> None:
        enabled = self.option_enabled.get()
        self.option_status.set("提示已启用" if enabled else "提示已禁用")
        self.config["telemetryEnabled"] = enabled
        self._persist_user_config()

    def _open_link(self, event: tk.Event) -> None:
        webbrowser.open(self.LINK_URL)

    def _persist_user_config(self) -> None:
        if not self.config_path:
            return
        try:
            self.config_path.write_text(
                json.dumps(self.config, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def _resolve_user_data_dir(self) -> Path:
        if sys.platform.startswith("win"):
            appdata = os.getenv("APPDATA")
            base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
            return base / self.APPDATA_DIRNAME
        return Path.home() / f".{self.APPDATA_DIRNAME.lower()}"

    def _ensure_user_config(self) -> Path:
        self.appdata_dir.mkdir(parents=True, exist_ok=True)
        user_config = self.appdata_dir / self.CONFIG_FILENAME
        default_config = resource_path("config", self.CONFIG_FILENAME)
        if default_config.exists() and not user_config.exists():
            try:
                user_config.write_text(default_config.read_text(encoding="utf-8"), encoding="utf-8")
            except OSError:
                pass
        return user_config

    def _load_config(self) -> dict[str, object]:
        for candidate in (self.config_path, resource_path("config", self.CONFIG_FILENAME)):
            try:
                return json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
        return {}

    def _prepare_user_directories(self) -> None:
        logs_dir = self.appdata_dir / "logs"
        try:
            logs_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass


def main() -> None:
    app = TabbedApp()
    app.mainloop()


if __name__ == "__main__":
    main()
