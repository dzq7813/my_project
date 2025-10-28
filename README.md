# Tkinter 标签页示例

一个使用 Tkinter 构建的简易标签页界面示例程序。本仓库已准备好在 Windows 下使用 PyInstaller 进行发布打包。

## 运行方式

1. 确保已安装 Python 3。
2. 在项目根目录执行：

   ```bash
   python3 main.py
   ```

## 项目结构速览

- `assets/icons/`：Windows 可执行程序使用的 `.ico` 与 `.png` 图标。
- `config/config.json`：默认配置文件，首次运行时会复制到用户目录。
- `templates/`：打包示例中随应用发布的静态模板资源。
- `packaging/app.spec`：PyInstaller 配置，负责收集资源与设置图标。
- `packaging/hooks/hook-PySide6.py`：可选的自定义钩子，若未来引入 PySide6 时确保所需插件被打包。
- `build.bat`：Windows 一键打包脚本（创建虚拟环境、安装依赖并运行 PyInstaller）。
- `tests/test_build.py`：轻量烟囱测试，验证 spec 文件结构与关键资源存在。

## Windows 打包指南

1. 在 Windows 上安装 Python 3.10+ 并确保 `python` 命令可用。
2. 打开命令提示符（或 PowerShell），切换到项目根目录。
3. 执行：

   ```bat
   build.bat
   ```

   脚本会：
   - 删除旧的临时虚拟环境（`.venv-build`）。
   - 创建新的虚拟环境并升级 `pip`。
   - 安装 `requirements.txt` 中的依赖（默认包含 `pyinstaller`）。
   - 调用 `pyinstaller packaging\app.spec --clean --noconfirm`，产出位于 `dist/TabbedApp/` 的可执行文件。

### 手动验收建议

1. 打开 `dist\TabbedApp\TabbedApp.exe`。
2. 验证界面图标以及首页、设置、关于三个标签页均能正常显示。
3. 切换主题或勾选“启用提示”后，重新启动程序，可确认设置已持久化到 `%APPDATA%\TabbedApp\config.json`。
4. 检查 `%APPDATA%\TabbedApp\logs` 目录已创建（用于未来日志输出），并确认 `dist` 内未额外携带日志/配置目录。
5. 如需进一步确认资源是否被正确打包，可在可执行目录中查看 `assets` 与 `templates` 子目录内容。

### 常见问题排查

- **缺少 DLL / Qt 插件**：若未来引入 PySide6 组件，请确保 `requirements.txt` 中包含相应版本，并保留 `packaging/hooks/hook-PySide6.py`。该钩子会自动收集常见的 Qt 插件目录。
- **图标未显示**：保证在 Windows 环境使用 `.ico` 文件；若自定义图标，请同时更新 `assets/icons/app.ico` 与 spec 文件引用。
- **首次运行无法写入配置**：确认当前用户对 `%APPDATA%` 目录拥有写权限，或手动在该目录下创建 `TabbedApp` 文件夹后重试。

## 配置与日志

应用首次运行时会将 `config/config.json` 复制到：

- Windows：`%APPDATA%\TabbedApp\config.json`
- 其他平台：`~/.tabbedapp/config.json`

同级还会创建 `logs/` 目录以供未来的运行日志使用。这些目录不包含在打包产物中，符合 Windows 平台将可变数据放置在 `%APPDATA%` 的约定。

## 测试与验证

在开发环境中可运行：

```bash
pytest tests/test_build.py
```

该测试会模拟加载 PyInstaller spec，确保关键资源与配置项完备，从而在 CI 中对打包结构进行基本验证。
