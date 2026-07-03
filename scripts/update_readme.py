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

START = "<!-- AUTO-GENERATED-PROJECTS:START -->"
END = "<!-- AUTO-GENERATED-PROJECTS:END -->"


def github_get(url: str) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": f"{USERNAME}-profile-readme-updater",
    }

    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"

    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req, timeout=20) as resp:
        if resp.status < 200 or resp.status >= 300:
            raise RuntimeError(f"GitHub API error: HTTP {resp.status}")
        return json.loads(resp.read().decode("utf-8"))


def fetch_repos() -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
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


def repo_score(repo: dict[str, Any]) -> tuple[int, int, str]:
    stars = int(repo.get("stargazers_count") or 0)
    forks = int(repo.get("forks_count") or 0)
    pushed_at = repo.get("pushed_at") or ""
    return stars, forks, pushed_at


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

    result.sort(key=repo_score, reverse=True)
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


def build_generated_block(repos: list[dict[str, Any]]) -> str:
    featured = repos[:6]

    language_counter = Counter()
    for repo in repos:
        language = repo.get("language")
        if language:
            language_counter[language] += 1

    now = dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append(START)
    lines.append("")
    lines.append("### Auto-updated repositories")
    lines.append("")

    if featured:
        for repo in featured:
            lines.append(format_project(repo))
            lines.append("")
    else:
        lines.append("No public repositories found.")
        lines.append("")

    if language_counter:
        lines.append("### Repository language snapshot")
        lines.append("")
        lines.append("| Language | Repositories |")
        lines.append("| --- | ---: |")
        for lang, count in language_counter.most_common(8):
            lines.append(f"| {lang} | {count} |")
        lines.append("")

    lines.append(f"_Last updated: {now}_")
    lines.append("")
    lines.append(END)

    return "\n".join(lines)


def replace_block(readme: str, generated: str) -> str:
    if START not in readme or END not in readme:
        return readme.rstrip() + "\n\n" + generated + "\n"

    before = readme.split(START)[0].rstrip()
    after = readme.split(END, 1)[1].lstrip()

    return before + "\n\n" + generated + "\n\n" + after


def main() -> int:
    if not os.path.exists(README_PATH):
        print(f"README not found: {README_PATH}", file=sys.stderr)
        return 1

    repos = clean_repos(fetch_repos())
    generated = build_generated_block(repos)

    with open(README_PATH, "r", encoding="utf-8") as f:
        old_readme = f.read()

    new_readme = replace_block(old_readme, generated)

    if new_readme == old_readme:
        print("README is already up to date.")
        return 0

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"README updated with {min(len(repos), 6)} featured repositories.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())