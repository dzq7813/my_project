import sys
import tkinter as tk
from tkinter import ttk
import webbrowser
##修改测试

class TabbedApp(tk.Tk):
    LINK_URL = "https://docs.python.org/zh-cn/3/library/tkinter.ttk.html"

    def __init__(self) -> None:
        super().__init__()
        self.title("示例：Tkinter 标签页")
        self.minsize(480, 360)

        self.style = ttk.Style(self)
        self.style.configure("TNotebook.Tab", padding=(12, 6))
        self.style.configure("Content.TFrame", padding=16)
        self.available_themes = sorted(self.style.theme_names())

        self.counter_value = tk.IntVar(value=0)
        self.counter_text = tk.StringVar(value="点击次数：0")
        self.selected_theme = tk.StringVar(value=self.style.theme_use())
        self.option_enabled = tk.BooleanVar(value=False)
        self.option_status = tk.StringVar(value="提示已禁用")

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
            f"Python 版本：{sys.version.split()[0]}"
        )
        info_label = ttk.Label(wrapper, text=app_info, justify="left")
        info_label.grid(row=0, column=0, sticky="w")

        link_style = "Link.TLabel"
        self.style.configure(link_style, foreground="#1a0dab")
        self.style.map(link_style, foreground=[("active", "#551A8B")])

        link_label = ttk.Label(wrapper, text="访问 Tkinter ttk 文档", cursor="hand2", style=link_style)
        link_label.configure(font=("", 10, "underline"))
        link_label.grid(row=1, column=0, pady=(12, 0), sticky="w")
        link_label.bind("<Button-1>", self._open_link)

    def _increment_counter(self) -> None:
        new_value = self.counter_value.get() + 1
        self.counter_value.set(new_value)
        self.counter_text.set(f"点击次数：{new_value}")

    def _apply_theme(self, event: tk.Event) -> None:
        selected = self.selected_theme.get()
        if selected:
            self.style.theme_use(selected)

    def _toggle_option(self) -> None:
        enabled = self.option_enabled.get()
        self.option_status.set("提示已启用" if enabled else "提示已禁用")

    def _open_link(self, event: tk.Event) -> None:
        webbrowser.open(self.LINK_URL)


def main() -> None:
    app = TabbedApp()
    app.mainloop()


if __name__ == "__main__":
    main()
