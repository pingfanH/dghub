# DGHub macOS runtime

Generated from DGHub 1.3.19 extracted bytecode plus macOS compatibility shims.

- Entry wrapper: `python main.py` runs from the repository root.
- Source files are kept in the root-level `src/` tree.
- Local frontend assets/config/logs/plugins can live in the ignored `macos_runtime/` directory. Python bytecode is archived under `local_artifacts/bytecode_archive/` and is not used by the launcher.

This is a compatibility runtime, not clean recovered source.
