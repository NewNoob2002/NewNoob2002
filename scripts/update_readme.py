#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import json
import os
import sys
import urllib.request
from collections import Counter
from typing import Any

USERNAME = os.getenv("GITHUB_USERNAME", "NewNoob2002")
TOKEN = os.getenv("GITHUB_TOKEN", "")
README_PATH = os.getenv("README_PATH", "README.md")

PROJECTS_START = "<!-- AUTO-GENERATED-PROJECTS:START -->"
PROJECTS_END = "<!-- AUTO-GENERATED-PROJECTS:END -->"

STATS_START = "<!-- AUTO-GENERATED-STATS:START -->"
STATS_END = "<!-- AUTO-GENERATED-STATS:END -->"


def github_get(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-readme-updater",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_profile() -> dict[str, Any]:
    return github_get(f"https://api.github.com/users/{USERNAME}")


def fetch_repos() -> list[dict[str, Any]]:
    repos = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/users/{USERNAME}/repos"
            f"?sort=updated&direction=desc&per_page=100&page={page}"
        )
        data = github_get(url)

        if not data:
            break

        repos.extend(data)
        page += 1

    return repos


def clean_repos(repos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    result = []

    for repo in repos:
        name = repo.get("name", "")

        if name == USERNAME:
            continue
        if repo.get("fork"):
            continue
        if repo.get("archived"):
            continue
        if repo.get("private"):
            continue

        result.append(repo)

    result.sort(
        key=lambda r: (
            int(r.get("stargazers_count") or 0),
            int(r.get("forks_count") or 0),
            r.get("pushed_at") or "",
        ),
        reverse=True,
    )

    return result


def format_project(repo: dict[str, Any]) -> str:
    name = repo.get("name", "unknown")
    url = repo.get("html_url", "")
    desc = repo.get("description") or "No description yet."
    lang = repo.get("language") or "Mixed"
    stars = repo.get("stargazers_count") or 0
    forks = repo.get("forks_count") or 0
    pushed_at = (repo.get("pushed_at") or "")[:10]

    topics = repo.get("topics") or []
    topic_text = ""
    if topics:
        topic_text = " · " + " ".join(f"`{topic}`" for topic in topics[:5])

    return (
        f"- [{name}]({url}) — {desc}\n"
        f"  - `{lang}` · ⭐ {stars} · 🍴 {forks} · updated `{pushed_at}`{topic_text}"
    )


def build_projects_block(repos: list[dict[str, Any]]) -> str:
    featured = repos[:6]

    lines = [
        PROJECTS_START,
        "",
        "### Auto-updated repositories",
        "",
    ]

    if featured:
        for repo in featured:
            lines.append(format_project(repo))
            lines.append("")
    else:
        lines.append("No public repositories found.")
        lines.append("")

    lines.append(PROJECTS_END)
    return "\n".join(lines)


def build_stats_block(profile: dict[str, Any], repos: list[dict[str, Any]]) -> str:
    language_counter = Counter()
    total_stars = 0
    total_forks = 0

    for repo in repos:
        language = repo.get("language")
        if language:
            language_counter[language] += 1

        total_stars += int(repo.get("stargazers_count") or 0)
        total_forks += int(repo.get("forks_count") or 0)

    top_languages = ", ".join(lang for lang, _ in language_counter.most_common(5))
    if not top_languages:
        top_languages = "C / C++ / Python / Shell"

    public_repos = profile.get("public_repos", len(repos))
    followers = profile.get("followers", 0)
    following = profile.get("following", 0)
    updated_at = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        STATS_START,
        "",
        "| Item | Value |",
        "| --- | ---: |",
        f"| Public repositories | {public_repos} |",
        f"| Featured repositories | {len(repos)} |",
        f"| Total stars | {total_stars} |",
        f"| Total forks | {total_forks} |",
        f"| Followers | {followers} |",
        f"| Following | {following} |",
        "",
        f"**Main languages:** {top_languages}",
        "",
        "**Focus:** Embedded firmware · GNSS / RTK · MCU · RTOS · Linux tooling",
        "",
        f"_Last updated: {updated_at}_",
        "",
        STATS_END,
    ]

    return "\n".join(lines)


def replace_block(readme: str, start: str, end: str, generated: str) -> str:
    if start not in readme or end not in readme:
        return readme.rstrip() + "\n\n" + generated + "\n"

    before = readme.split(start)[0].rstrip()
    after = readme.split(end, 1)[1].lstrip()

    return before + "\n\n" + generated + "\n\n" + after


def main() -> int:
    if not os.path.exists(README_PATH):
        print(f"README not found: {README_PATH}", file=sys.stderr)
        return 1

    profile = fetch_profile()
    repos = clean_repos(fetch_repos())

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    readme = replace_block(
        readme,
        PROJECTS_START,
        PROJECTS_END,
        build_projects_block(repos),
    )

    readme = replace_block(
        readme,
        STATS_START,
        STATS_END,
        build_stats_block(profile, repos),
    )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

    print("README updated successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())