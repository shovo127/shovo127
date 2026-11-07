import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from update_blog_feed import parse_feed, update_readme, START, END


class FeedParserTests(unittest.TestCase):
    def test_rss_entries_are_sorted_and_limited_to_safe_http_links(self):
        xml = b"""<?xml version="1.0"?>
        <rss version="2.0"><channel>
          <item><title>Older &amp; useful</title><link>https://example.com/older</link><pubDate>Mon, 02 Nov 2026 10:00:00 GMT</pubDate></item>
          <item><title>Newest</title><link>https://example.com/newest</link><pubDate>Tue, 03 Nov 2026 10:00:00 GMT</pubDate></item>
          <item><title>Unsafe</title><link>javascript:alert(1)</link></item>
        </channel></rss>"""
        items = parse_feed(xml)
        self.assertEqual([item["title"] for item in items], ["Newest", "Older & useful"])
        self.assertEqual(items[0]["date_label"], "2026-11-03")

    def test_atom_alternate_link(self):
        xml = b"""<feed xmlns="http://www.w3.org/2005/Atom">
          <entry><title>Atom post</title><link rel="alternate" href="https://example.com/atom"/>
          <updated>2026-11-04T09:30:00Z</updated></entry>
        </feed>"""
        items = parse_feed(xml)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["url"], "https://example.com/atom")

    def test_empty_feed_does_not_modify_readme(self):
        readme = "# Profile\n\n## Connect\n"
        self.assertEqual(update_readme(readme, []), readme)

    def test_first_run_inserts_one_section_before_connect(self):
        readme = "# Profile\n\n## Connect\n- GitHub\n"
        items = [{"title": "A [post]", "url": "https://example.com/post", "date_label": "2026-11-05"}]
        updated = update_readme(readme, items)
        self.assertLess(updated.index("## Latest writing"), updated.index("## Connect"))
        self.assertIn(START, updated)
        self.assertIn(END, updated)
        self.assertIn(r"A \[post\]", updated)

    def test_subsequent_run_replaces_without_duplicate_heading(self):
        readme = "# Profile\n\n## Latest writing\n\n" + START + "\n- Old\n" + END + "\n\n## Connect\n"
        items = [{"title": "New post", "url": "https://example.com/new", "date_label": ""}]
        updated = update_readme(readme, items)
        self.assertEqual(updated.count("## Latest writing"), 1)
        self.assertNotIn("Old", updated)
        self.assertIn("New post", updated)


if __name__ == "__main__":
    unittest.main()
