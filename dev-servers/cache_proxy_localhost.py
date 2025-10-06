# mitmproxy addon: disk-backed response cache + replay
# RUN:
# mitmproxy -s cache_proxy_localhost.py --listen-port 8085
# mitmproxy -s "$PATH_CLI_UTILS/servers/cache_proxy_localhost.py" --listen-port 8085
# LEGACY:
# Usage: mitmproxy -s cache_proxy_localhost.py --listen-port 8085


# from mitmproxy import http, ctx
import os, hashlib, json
from urllib.parse import urlparse, parse_qs

CACHE_DIR = os.path.expanduser("~/.cache/mitmproxy-responses")
BYPASS_HEADER = "x-cache-bypass"    # set to "1" or "true" to force live fetch
REFRESH_PARAM = "__refresh_cache"   # ?__refresh_cache=1 to refresh

def ensure_cache_dir():
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR, exist_ok=True)

def key_for_request(req: http.Request) -> str:
    # create a deterministic key from method + full url (including query)
    s = f"{req.method} {req.url}"
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def meta_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.meta.json")

def body_path(key: str) -> str:
    return os.path.join(CACHE_DIR, f"{key}.body")

def is_local_host(host: str) -> bool:
    # avoid caching local development hosts - adjust as needed
    if not host:
        return False
    host_lower = host.lower()
    if host_lower.endswith(".localhost") or host_lower in ("localhost", "127.0.0.1"):
        return True
    if host_lower.startswith("10.") or host_lower.startswith("192.168.") or host_lower.startswith("172."):
        return True
    return False

def should_bypass(flow: http.HTTPFlow) -> bool:
    # header-based bypass
    hv = flow.request.headers.get(BYPASS_HEADER, "")
    if hv and hv.lower() in ("1", "true", "yes"):
        return True
    # query param-based refresh
    q = parse_qs(urlparse(flow.request.url).query)
    if REFRESH_PARAM in q:
        return True
    return False

def load_cached_response(key: str):
    mp = meta_path(key)
    bp = body_path(key)
    if not (os.path.exists(mp) and os.path.exists(bp)):
        return None
    try:
        with open(mp, "r", encoding="utf-8") as f:
            meta = json.load(f)
        with open(bp, "rb") as f:
            body = f.read()
        return meta, body
    except Exception as e:
        ctx.log.warn(f"Failed to load cache {key}: {e}")
        return None

def save_response_to_cache(key: str, resp: http.Response):
    mp = meta_path(key)
    bp = body_path(key)
    meta = {
        "status_code": resp.status_code,
        "reason": resp.reason,
        "headers": dict(resp.headers),
        "http_version": resp.http_version
    }
    try:
        with open(mp, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
        with open(bp, "wb") as f:
            # resp.content is bytes
            f.write(resp.content or b"")
        ctx.log.info(f"Saved cache: {key} -> {mp}, {bp}")
    except Exception as e:
        ctx.log.warn(f"Failed to save cache {key}: {e}")

class CacheProxy:
    def __init__(self):
        ensure_cache_dir()
        ctx.log.info(f"Cache dir: {CACHE_DIR}")

    def request(self, flow: http.HTTPFlow):
        # Decide early whether to intercept or not.
        host = flow.request.host
        if is_local_host(host):
            # don't touch local dev servers
            return
        if should_bypass(flow):
            # bypass this request - let it go live
            flow.request.headers.pop(BYPASS_HEADER, None)
            return

        k = key_for_request(flow.request)
        cached = load_cached_response(k)
        if cached:
            meta, body = cached
            headers = meta.get("headers", {})
            status = meta.get("status_code", 200)
            reason = meta.get("reason", "")
            # Build a response object and short-circuit
            flow.response = http.HTTPResponse.make(
                status,
                body,
                headers
            )
            ctx.log.info(f"Replayed cached response for {flow.request.method} {flow.request.url}")
            # stop the request from going out
            return

    def response(self, flow: http.HTTPFlow):
        # Only cache external responses; skip failed status codes optionally
        host = flow.request.host
        if is_local_host(host):
            return
        # optionally, skip large or streaming responses here by inspecting headers
        key = key_for_request(flow.request)
        # Save the response to disk (overwrite existing). You might add conditions (status==200 etc).
        try:
            save_response_to_cache(key, flow.response)
        except Exception as e:
            ctx.log.warn(f"Error saving cache for {flow.request.url}: {e}")


addons = [
    CacheProxy()
]
