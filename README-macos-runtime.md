# DGHub macOS runtime

Generated from DGHub 1.3.19 extracted bytecode plus macOS compatibility shims.

- Entry wrapper: `python main.py` runs from the repository root.
- Source files are kept in the root-level `src/` tree.
- Local bytecode/runtime artifacts can remain in the ignored `local_artifacts/macos_runtime/` directory; the root launcher detects it automatically. The legacy ignored `macos_runtime/` path is still supported.

This is a compatibility runtime, not clean recovered source.
