from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from automation import state


class RunStateTests(unittest.TestCase):
    def test_transition_writes_state_and_progress(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            paths = state.RunPaths.create(Path(temp_dir), "trie")
            store = state.RunStore(paths)
            snapshot = state.RunSnapshot(
                run_id="trie",
                algorithm_name="Trie",
                checklist_label="Trie",
                branch_name="trie",
                topic_path="string/Trie",
                display_name="Trie",
                pr_title="Add Trie",
            )
            store.initialize(snapshot)
            snapshot = store.transition(
                snapshot,
                step_name="create_branch",
                next_state=state.STATE_BRANCH_CREATED,
                evidence={"branch": "trie"},
                note="created branch",
            )

            state_payload = json.loads(paths.state_path.read_text(encoding="utf-8"))
            progress_payload = json.loads(paths.progress_path.read_text(encoding="utf-8"))

            self.assertEqual(state_payload["current_state"], state.STATE_BRANCH_CREATED)
            self.assertEqual(snapshot.current_state, state.STATE_BRANCH_CREATED)
            self.assertEqual(len(progress_payload), 1)
            self.assertEqual(progress_payload[0]["step_name"], "create_branch")
            self.assertEqual(progress_payload[0]["state_before"], state.STATE_QUEUED)
            self.assertEqual(progress_payload[0]["state_after"], state.STATE_BRANCH_CREATED)
            self.assertEqual(progress_payload[0]["evidence"]["branch"], "trie")

    def test_invalid_transition_raises(self) -> None:
        with self.assertRaises(ValueError):
            state.validate_transition(state.STATE_QUEUED, state.STATE_VERIFIED)


if __name__ == "__main__":
    unittest.main()
