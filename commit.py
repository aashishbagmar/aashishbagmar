"""
Generate backdated git commits for the GitHub contribution graph.

Use a dedicated empty PUBLIC repo — not your profile README repo.
Commits only appear on your graph if the repo is public (or private
contributions are enabled in GitHub profile settings).

Run:  python commit.py
Push: git push origin main
"""

import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

COMMIT_COUNT = 150
START_DATE = datetime(2026, 1, 1)
END_DATE = datetime.now().replace(hour=23, minute=59, second=59, microsecond=0)
TRACK_FILE = "activity.log"
TIMEZONE = "+0530"
DRY_RUN = False


def run_git(args: list[str], env: dict[str, str] | None = None) -> None:
    subprocess.run(
        ["git", *args],
        env=env,
        check=True,
        cwd=Path.cwd(),
    )


def random_commit_dates(count: int, start: datetime, end: datetime) -> list[datetime]:
    if start > end:
        raise ValueError(f"START_DATE ({start.date()}) must be on or before END_DATE ({end.date()})")

    span_seconds = int((end - start).total_seconds())
    dates = []
    for _ in range(count):
        offset = random.randint(0, span_seconds)
        hour = random.randint(9, 22)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        day = start + timedelta(seconds=offset)
        dates.append(day.replace(hour=hour, minute=minute, second=second, microsecond=0))

    dates.sort()
    return dates


def commit_at(when: datetime, index: int, total: int) -> None:
    track_path = Path(TRACK_FILE)
    with track_path.open("a", encoding="utf-8") as file:
        file.write(f"{when.isoformat()} commit #{index}\n")

    date_str = when.strftime(f"%Y-%m-%d %H:%M:%S {TIMEZONE}")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    message = f"activity: {when.strftime('%Y-%m-%d')}"

    if DRY_RUN:
        print(f"[dry-run] {index}/{total} {date_str}  {message}")
        return

    run_git(["add", TRACK_FILE])
    run_git(["commit", "-m", message], env=env)
    print(f"Committed {index}/{total}  {when.strftime('%Y-%m-%d %H:%M')}")


def ensure_git_repo() -> None:
    if not Path(".git").exists():
        print("Error: not a git repository. cd into your target repo first.", file=sys.stderr)
        sys.exit(1)

    result = subprocess.run(["git", "config", "user.email"], capture_output=True, text=True)
    if not result.stdout.strip():
        print("Error: git user.email is not set.", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    if Path.cwd().name == "aashishbagmar" or "Git_Profile" in str(Path.cwd()):
        print(
            "Warning: you are in your profile repo. Prefer a dedicated empty repo:\n"
            "  mkdir contribution-bot && cd contribution-bot\n"
            "  git init && git remote add origin <your-empty-repo-url>\n"
        )

    ensure_git_repo()

    dates = random_commit_dates(COMMIT_COUNT, START_DATE, END_DATE)
    print(
        f"Creating {COMMIT_COUNT} commits between "
        f"{START_DATE.date()} and {END_DATE.date()}..."
    )

    for i, when in enumerate(dates, start=1):
        commit_at(when, i, COMMIT_COUNT)

    print("Done.")
    if not DRY_RUN:
        print("Push when ready:  git push origin main")


if __name__ == "__main__":
    main()
