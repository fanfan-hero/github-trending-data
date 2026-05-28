#!/usr/bin/env python3
import requests, json, re
from datetime import datetime

EXCLUDE = {
    'sponsors','features','about','pricing','marketplace','topics','explore',
    'login','join','settings','orgs','apps','users','repos','search',
    'trending','pulls','issues','notifications','new','organizations','github',
    'readme','license','blob','tree','commit','compare','releases','packages',
    'actions','projects','security','pulse','graphs','network','wiki','stargazers',
    'watchers','forks','site','contact','enterprise','team'
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

resp = requests.get("https://github.com/trending?since=daily", headers=headers, timeout=30)
html = resp.text

all_links = re.findall(r'href="/([a-zA-Z0-9_-]+/[a-zA-Z0-9_.-]+)"', html)
repos = []
seen = set()
for l in all_links:
    owner = l.split('/')[0]
    if owner not in EXCLUDE and l not in seen:
        seen.add(l)
        repos.append(l)

daily_gains = re.findall(r'([\d,]+)\s+stars today', html)

projects = []
for i, name in enumerate(repos):
    gain = int(daily_gains[i].replace(',', '')) if i < len(daily_gains) else 0
    projects.append({"name": name, "daily_gain": gain})

data = {
    "updated_at": datetime.utcnow().isoformat() + "Z",
    "projects": projects
}

with open("trending.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Saved {} projects, updated at {}".format(len(projects), data["updated_at"]))
