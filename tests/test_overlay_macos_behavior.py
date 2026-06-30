from __future__ import annotations

import unittest

from src.overlay.desktop_overlay import (
    MACOS_COLLECTION_BEHAVIOR_NAMES,
    _macos_collection_behavior_mask,
)


class FakeAppKit:
    NSWindowCollectionBehaviorCanJoinAllSpaces = 1
    NSWindowCollectionBehaviorFullScreenAuxiliary = 256
    NSWindowCollectionBehaviorStationary = 16
    NSWindowCollectionBehaviorIgnoresCycle = 64


class OverlayMacOSBehaviorTest(unittest.TestCase):
    def test_overlay_joins_all_spaces_and_full_screen_spaces(self) -> None:
        self.assertEqual(
            set(MACOS_COLLECTION_BEHAVIOR_NAMES),
            {
                "NSWindowCollectionBehaviorCanJoinAllSpaces",
                "NSWindowCollectionBehaviorFullScreenAuxiliary",
                "NSWindowCollectionBehaviorStationary",
                "NSWindowCollectionBehaviorIgnoresCycle",
            },
        )
        self.assertEqual(_macos_collection_behavior_mask(FakeAppKit), 337)


if __name__ == "__main__":
    unittest.main()
