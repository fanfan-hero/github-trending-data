#!/usr/bin/env python3
import requests, json, re
from datetime import datetime

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

resp = requests.get("https://github.com/trending?since=daily", headers=headers, timeout=30)
html = resp.text

repo_names = re.findall(r'<h2[^>]*>\s*<a\s+href="/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)"', html)
daily_gains = re.findall(r'([\d,]+)\s+stars today', html)

projects = []
for i, name in enumerate(repo_names[:25]):
    gain = int(daily_gains[i].replace(',', '')) if i < len(daily_gains) else 0
    projects.append({"name": name, "daily_gain": gain})

data = {
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "projects": projects
}

with open("trending.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved {} projects, updated at {}".format(len(projects), data["updated_at"]))
