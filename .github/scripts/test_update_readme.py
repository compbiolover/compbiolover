from datetime import datetime, timezone
from update_readme import START, END, render, replace_section

user = {
    "contributionsCollection": {"totalCommitContributions": 12, "totalPullRequestContributions": 3,
                                "totalPullRequestReviewContributions": 1, "totalIssueContributions": 0,
                                "restrictedContributionsCount": 5},
    "repositories": {"nodes": [
        {"name": "a", "url": "https://x/a", "description": "Tool", "pushedAt": "", "primaryLanguage": {"name": "Rust"}},
        {"name": "b", "url": "https://x/b", "description": None, "pushedAt": "", "primaryLanguage": None},
    ]},
}
out = render(user, datetime(2026, 11, 1, tzinfo=timezone.utc))
assert "**17** contributions" in out and "November 1, 2026" in out
assert "- [a](https://x/a) — Tool · Rust" in out and "- [b](https://x/b)\n" not in out and out.endswith("- [b](https://x/b)")
doc = f"top\n{START}\nold\n{END}\nbottom"
assert replace_section(doc, "new") == f"top\n{START}\nnew\n{END}\nbottom"
assert replace_section(replace_section(doc, "new"), "new") == f"top\n{START}\nnew\n{END}\nbottom"
print("ok")
