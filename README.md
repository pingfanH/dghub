# DGHub macOS Source Runtime

This repository keeps the recovered DGHub macOS runtime source and compatibility patches at the repository root.

Binary files, extracted PyInstaller contents, decompiler output, local runtime artifacts, virtual environments, and user plugins are intentionally ignored.

## Layout

- `main.py` - macOS launcher wrapper.
- `src/` - recovered DGHub application modules and patched runtime code.
- `plugins/demo_external/` - tracked sample plugin.
- `docs/` - plugin/runtime documentation.
- `local_artifacts/` - archive of installer/extraction/decompile materials from before source recovery; ignored by Git.
- `macos_runtime/` - local frontend assets/config/logs/plugins used while running the reconstructed app; ignored by Git.
- `venv/` - local Python virtual environment; ignored by Git.

## Run Locally

The source tree no longer depends on `main.pyc` or runtime `.pyc` files. Keep locally extracted frontend assets/config/plugins under the ignored `macos_runtime/` directory when running the reconstructed app.

```bash
venv/bin/python main.py
```

If you want to reuse another local Python 3.11 virtual environment, install the runtime dependencies first:

```bash
python -m pip install -r requirements-macos.txt
```

## Notes

- macOS Bluetooth permission fixes are applied by `macos_tcc_patch.py`.
- macOS DGLab compatibility patches are applied by `pydglab_macos_patch.py`.
- The repository is kept source-only for GitHub; build outputs and extraction workspaces stay local.
