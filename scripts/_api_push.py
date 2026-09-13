import base64
import json
import subprocess
import sys
import urllib.request

# 用法: python _api_push.py "commit message" 文件1 文件2 ...
# 不带参数时默认推送 layouts/partials/extend_head.html
REPO = "combig/combig.github.io"
MESSAGE = sys.argv[1] if len(sys.argv) > 1 else "Update site"
FILES = sys.argv[2:] if len(sys.argv) > 2 else ["layouts/partials/extend_head.html"]

# 从 Git Credential Manager 取 token（不打印）
raw = subprocess.run(
    ["git", "credential-manager", "get"],
    input="protocol=https\nhost=github.com\n\n",
    capture_output=True, text=True, check=True,
).stdout
TOKEN = [l.split("=", 1)[1] for l in raw.splitlines() if l.startswith("password=")][0]

opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def api(method, path, body=None):
    req = urllib.request.Request(
        f"https://api.github.com{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "workbuddy",
        },
    )
    with opener.open(req, timeout=30) as r:
        data = r.read()
    return json.loads(data) if data else {}


ref = api("GET", f"/repos/{REPO}/git/ref/heads/main")
base_sha = ref["object"]["sha"]
base_commit = api("GET", f"/repos/{REPO}/git/commits/{base_sha}")
base_tree = base_commit["tree"]["sha"]
print("remote main:", base_sha[:10], "tree:", base_tree[:10])

entries = []
for path in FILES:
    with open(path, "rb") as f:
        content_b64 = base64.b64encode(f.read()).decode()
    blob = api("POST", f"/repos/{REPO}/git/blobs",
               {"content": content_b64, "encoding": "base64"})
    print("blob:", path, blob["sha"][:10])
    entries.append({"path": path, "mode": "100644", "type": "blob", "sha": blob["sha"]})

tree = api("POST", f"/repos/{REPO}/git/trees", {
    "base_tree": base_tree,
    "tree": entries,
})
print("tree:", tree["sha"][:10])

commit = api("POST", f"/repos/{REPO}/git/commits", {
    "message": MESSAGE,
    "tree": tree["sha"],
    "parents": [base_sha],
})
print("commit:", commit["sha"][:10])

api("PATCH", f"/repos/{REPO}/git/refs/heads/main", {"sha": commit["sha"]})
print("ref updated -> main is now", commit["sha"][:12])
print("API_COMMIT_SHA=" + commit["sha"])
