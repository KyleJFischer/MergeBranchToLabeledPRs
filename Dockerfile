# If all you need is Python 3, use:
FROM python:3.8

# If you need Python 3 and the GitHub CLI, then use:
# FROM cicirello/pyaction:4

# If Python 3 + git is sufficient, then use:
# FROM cicirello/pyaction:3

# To pull from the GitHub Container Registry instead, use one of these:
# FROM ghcr.io/cicirello/pyaction-lite:3
# FROM ghcr.io/cicirello/pyaction:4
# FROM ghcr.io/cicirello/pyaction:3

COPY entrypoint.py /entrypoint.py
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/entrypoint.py"]
