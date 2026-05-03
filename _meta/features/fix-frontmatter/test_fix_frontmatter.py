#!/usr/bin/env python3
"""
test_fix_frontmatter.py — Tests for the frontmatter backfill feature.

Each test builds an isolated .md file (or synthetic vault) in a tmpdir and
asserts that `fix_frontmatter.process_file` produces the expected action and
output. No git required for most tests (git add date is just one fallback
path — we test it separately).

Stdlib only. Run with:  python3 _meta/features/fix-frontmatter/test_fix_frontmatter.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(SCRIPT_DIR.parents[1] / "lib"))
import fix_frontmatter as ff  # noqa: E402


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class ParseFrontmatterTests(unittest.TestCase):
    def test_no_frontmatter(self):
        keys, body_start = ff.parse_frontmatter("# Hello\n\nBody.")
        self.assertEqual(keys, {})
        self.assertEqual(body_start, 0)

    def test_complete_frontmatter(self):
        text = "---\ntitle: Foo\ncreated: 2025-01-02\n---\n\n# Foo\n"
        keys, body_start = ff.parse_frontmatter(text)
        self.assertEqual(keys["title"], "Foo")
        self.assertEqual(keys["created"], "2025-01-02")
        # Body starts at line index 4 (after closing fence).
        self.assertEqual(body_start, 4)

    def test_partial_frontmatter(self):
        text = "---\ntitle: Foo\n---\nBody\n"
        keys, _ = ff.parse_frontmatter(text)
        self.assertIn("title", keys)
        self.assertNotIn("created", keys)

    def test_malformed_frontmatter_treated_as_none(self):
        text = "---\ntitle: Foo\nBody without closing fence\n"
        keys, body_start = ff.parse_frontmatter(text)
        self.assertEqual(keys, {})
        self.assertEqual(body_start, 0)

    def test_ignores_list_and_nested(self):
        text = "---\ntitle: Foo\ntags:\n  - a\n  - b\n---\n"
        keys, _ = ff.parse_frontmatter(text)
        self.assertEqual(keys["title"], "Foo")
        self.assertIn("tags", keys)  # key present, empty value


class InferTitleTests(unittest.TestCase):
    def test_uses_first_h1(self):
        text = "# The Title\n\nBody.\n"
        self.assertEqual(ff.infer_title(text, 0, "fallback"), "The Title")

    def test_falls_back_to_stem(self):
        text = "No heading here.\n"
        self.assertEqual(ff.infer_title(text, 0, "fallback"), "fallback")

    def test_skips_past_frontmatter(self):
        text = "---\ntitle: X\n---\n\n# Real Title\n"
        self.assertEqual(ff.infer_title(text, 4, "fallback"), "Real Title")

    def test_ignores_hash_in_code_word(self):
        text = "text #hashtag more\n# Real One\n"
        self.assertEqual(ff.infer_title(text, 0, "fallback"), "Real One")


class BuildNewContentTests(unittest.TestCase):
    def test_prepend_block_when_no_frontmatter(self):
        text = "# Title\n\nBody.\n"
        out = ff.build_new_content(text, {}, 0, {"title": "Title", "created": "2025-01-02"})
        self.assertTrue(out.startswith("---\ntitle: Title\ncreated: 2025-01-02\n---\n"))
        self.assertIn("# Title", out)
        self.assertIn("Body.", out)

    def test_insert_before_closing_fence(self):
        text = "---\ntype: note\n---\n\n# Hello\n"
        out = ff.build_new_content(
            text, {"type": "note"}, 3, {"title": "Hello", "created": "2025-01-02"}
        )
        # Both original type and new keys must be in the frontmatter.
        self.assertIn("type: note", out)
        self.assertIn("title: Hello", out)
        self.assertIn("created: 2025-01-02", out)
        # Original body preserved.
        self.assertIn("# Hello", out)
        # New keys appear before the closing fence (verify order).
        head = out.split("---\n\n", 1)[0]
        self.assertIn("title: Hello", head)

    def test_only_adds_missing_key(self):
        text = "---\ntitle: Foo\n---\nBody\n"
        out = ff.build_new_content(text, {"title": "Foo"}, 3, {"created": "2025-01-02"})
        # title should appear once and unchanged.
        self.assertEqual(out.count("title: Foo"), 1)
        self.assertIn("created: 2025-01-02", out)


class YamlQuoteTests(unittest.TestCase):
    def test_simple_plain(self):
        self.assertEqual(ff.yaml_quote_if_needed("Hello World"), "Hello World")

    def test_quotes_special_start(self):
        self.assertTrue(ff.yaml_quote_if_needed("!bang").startswith('"'))

    def test_quotes_colon_space(self):
        self.assertTrue(ff.yaml_quote_if_needed("a: b").startswith('"'))

    def test_quotes_true_false(self):
        self.assertTrue(ff.yaml_quote_if_needed("true").startswith('"'))


class ProcessFileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _run(self, rel: str, content: str, apply: bool = True) -> ff.FileResult:
        path = self.root / rel
        write(path, content)
        return ff.process_file(path, Path(rel), self.root, apply=apply)

    def test_skips_empty_file(self):
        r = self._run("empty.md", "")
        self.assertEqual(r.action, "skipped")
        self.assertEqual(r.reason, "empty_file")

    def test_skips_whitespace_only(self):
        r = self._run("ws.md", "   \n\t\n")
        self.assertEqual(r.action, "skipped")
        self.assertEqual(r.reason, "empty_file")

    def test_unchanged_when_complete(self):
        content = "---\ntitle: Foo\ncreated: 2025-01-02\n---\n\n# Foo\n"
        r = self._run("ok.md", content)
        self.assertEqual(r.action, "unchanged")
        # File should be byte-identical.
        self.assertEqual((self.root / "ok.md").read_text(encoding="utf-8"), content)

    def test_adds_both_keys_when_missing(self):
        r = self._run("note.md", "# Hello\n\nBody.\n")
        self.assertEqual(r.action, "updated")
        self.assertEqual(set(r.added_keys), {"title", "created"})
        out = (self.root / "note.md").read_text(encoding="utf-8")
        self.assertIn("title: Hello", out)
        self.assertRegex(out, r"created: \d{4}-\d{2}-\d{2}")

    def test_adds_only_missing_key(self):
        content = "---\ntitle: ExistingTitle\n---\n\n# Hello\n"
        r = self._run("note.md", content)
        self.assertEqual(r.action, "updated")
        self.assertEqual(r.added_keys, ("created",))
        out = (self.root / "note.md").read_text(encoding="utf-8")
        self.assertIn("title: ExistingTitle", out)
        self.assertRegex(out, r"created: \d{4}-\d{2}-\d{2}")

    def test_dry_run_does_not_write(self):
        content = "# Hello\n"
        path = self.root / "note.md"
        write(path, content)
        r = ff.process_file(path, Path("note.md"), self.root, apply=False)
        self.assertEqual(r.action, "updated")
        self.assertEqual(path.read_text(encoding="utf-8"), content)

    def test_title_from_filename_when_no_h1(self):
        r = self._run("my-note-slug.md", "No heading here.\n")
        self.assertEqual(r.action, "updated")
        out = (self.root / "my-note-slug.md").read_text(encoding="utf-8")
        self.assertIn("title: my-note-slug", out)


class GitAddDateTests(unittest.TestCase):
    """Only runs if git is available — creates a repo and tests the fallback chain."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _git(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", "-C", str(self.root), *args],
            capture_output=True,
            text=True,
            check=True,
        )

    def test_returns_add_date_for_tracked_file(self):
        try:
            self._git("init", "-q")
            self._git("config", "user.email", "t@t.t")
            self._git("config", "user.name", "t")
            write(self.root / "a.md", "# a\n")
            self._git("add", "a.md")
            self._git(
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-q",
                "-m",
                "init",
            )
        except (OSError, subprocess.CalledProcessError) as e:
            self.skipTest(f"git unavailable or failed: {e}")

        d = ff.git_add_date(self.root, Path("a.md"))
        self.assertIsNotNone(d)
        self.assertRegex(d, r"^\d{4}-\d{2}-\d{2}$")

    def test_returns_none_for_untracked(self):
        if not (self.root / ".git").exists():
            # No repo init'd — git_add_date should still return None gracefully.
            d = ff.git_add_date(self.root, Path("ghost.md"))
            self.assertIsNone(d)


class WalkVaultTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # Canonical-ish layout.
        write(self.root / "1-projects/a.md", "# a\n")
        write(self.root / "_archive/old.md", "# old\n")
        write(self.root / "_secretary/tasks.md", "# tasks\n")
        write(self.root / "_meta/core/conventions.md", "# c\n")
        write(self.root / ".git/config", "[core]\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_skips_exempt_top_levels(self):
        exempt = {".git", "_meta", "_archive", "_secretary"}
        files = ff.walk_vault(self.root, exempt, set(), None)
        rel_strs = {str(p) for p in files}
        self.assertIn("1-projects/a.md", rel_strs)
        self.assertNotIn("_archive/old.md", rel_strs)
        self.assertNotIn("_secretary/tasks.md", rel_strs)
        self.assertNotIn("_meta/core/conventions.md", rel_strs)

    def test_subpath_overrides_exemption(self):
        exempt = {".git", "_meta", "_archive", "_secretary"}
        files = ff.walk_vault(self.root, exempt, set(), Path("_archive"))
        rel_strs = {str(p) for p in files}
        self.assertIn("_archive/old.md", rel_strs)

    def test_skips_append_only_files(self):
        write(self.root / "inbox.md", "# Inbox\n")
        write(self.root / "todo.md", "# Todo\n")
        exempt = {".git", "_meta", "_archive", "_secretary"}
        append_only = {"inbox.md", "todo.md"}
        files = ff.walk_vault(self.root, exempt, append_only, None)
        rel_strs = {p.as_posix() for p in files}
        self.assertNotIn("inbox.md", rel_strs)
        self.assertNotIn("todo.md", rel_strs)
        self.assertIn("1-projects/a.md", rel_strs)


if __name__ == "__main__":
    unittest.main(verbosity=2)
