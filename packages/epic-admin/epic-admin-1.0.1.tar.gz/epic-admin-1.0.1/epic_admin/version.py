"""
Version Control helper for automatic numbering for development commits.
Get version number from .git tag in the project folder
When the most recent tag doesn't point to the last commit
(where N counts the number of additional commits after tag, followed by commit signature)
"""
import os
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..',))

def get_version_from_git():
    try:
        return subprocess.check_output(
            ["git", "describe", "--tags", "--always"],
            cwd=BASE_DIR).decode('utf-8').strip()
    except:
        return '?'

VERSION = get_version_from_git()
