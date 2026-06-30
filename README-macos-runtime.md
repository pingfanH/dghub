# DGHub macOS runtime

Generated from DGHub 1.3.19 extracted bytecode plus macOS compatibility shims.

- Entry wrapper: `python main.py` runs from the repository root.
- Source files are kept in the root-level `src/` tree.
- Local bytecode/runtime artifacts can remain in the ignored `macos_runtime/` directory; the root launcher detects `macos_runtime/main.pyc` automatically.

This is a compatibility runtime, not clean recovered source.
