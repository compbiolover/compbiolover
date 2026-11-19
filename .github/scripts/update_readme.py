"""Rewrite the README section between the ACTIVITY markers with recent GitHub activity."""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timedelta, timezone

LOGIN = "compbiolover"
START, END = "<!-- ACTIVITY:START -->", "<!-- ACTIVITY:END -->"
DAYS = 30

QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    contributionsCollection(from: $from, to: $to) {
      totalCommitContributions
      totalPullRequestContributions
      totalPullRequestReviewContributions
      totalIssueContributions
      restrictedContributionsCount
    }
    repositories(first: 5, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false,
                 orderBy: {field: PUSHED_AT, direction: DESC}) {
      nodes { name url description pushedAt primaryLanguage { name } }
    }
  }
}
"""


def fetch(token, now):
    body = json.dumps({"query": QUERY, "variables": {
        "login": LOGIN,
        "from": (now - timedelta(days=DAYS)).isoformat(),
        "to": now.isoformat(),
    }}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", body, {
        "Authorization": f"bearer {token}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    return data["data"]["user"]


def render(user, now):
    c = user["contributionsCollection"]
    lines = [
        f"_Last {DAYS} days, updated {now:%B %-d, %Y}:_ "
        f"**{c['totalCommitContributions'] + c['restrictedContributionsCount']}** contributions "
        f"(**{c['totalCommitContributions']}** public commits, "
        f"**{c['totalPullRequestContributions']}** pull requests, "
        f"**{c['totalPullRequestReviewContributions']}** reviews, "
        f"**{c['totalIssueContributions']}** issues)",
        "",
        "Recently updated projects:",
        "",
    ]
    for repo in user["repositories"]["nodes"]:
        lang = f" · {repo['primaryLanguage']['name']}" if repo["primaryLanguage"] else ""
        desc = f" — {repo['description']}" if repo["description"] else ""
        lines.append(f"- [{repo['name']}]({repo['url']}){desc}{lang}")
    return "\n".join(lines)


def replace_section(readme, section):
    pattern = re.compile(re.escape(START) + ".*?" + re.escape(END), re.S)
    if not pattern.search(readme):
        sys.exit("README is missing the ACTIVITY markers")
    return pattern.sub(lambda _: f"{START}\n{section}\n{END}", readme)


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    with open("README.md") as f:
        readme = f.read()
    new = replace_section(readme, render(fetch(os.environ["GITHUB_TOKEN"], now), now))
    with open("README.md", "w") as f:
        f.write(new)
