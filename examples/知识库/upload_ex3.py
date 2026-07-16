#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exercise 3 step 4: 通过脚本将 ex3_docs 下的文档上传到指定知识库。
用法: TOKEN=xxx DID=xxx python upload_ex3.py
"""
import os
import sys
import json
import urllib.request

BASE = "http://localhost:5001/v1"
TOKEN = os.environ.get("TOKEN", "")
DID = os.environ.get("DID", "")
DOC_DIR = os.environ.get("DOC_DIR", r"C:\ai\RuyiDify\examples\知识库\ex3_docs")
# 仅上传尚未手动上传的格式（docx / pdf）；md 已手动上传
TARGETS = ["Dify学习资料.docx", "Dify学习资料.pdf"]


def upload(filename: str) -> dict:
    path = os.path.join(DOC_DIR, filename)
    boundary = "----ex3boundary"
    parts = []
    # file part
    with open(path, "rb") as f:
        data = f.read()
    parts.append(
        ("--%s\r\n" % boundary).encode()
        + ('Content-Disposition: form-data; name="file"; filename="%s"\r\n' % filename).encode()
        + b"Content-Type: application/octet-stream\r\n\r\n"
        + data + b"\r\n"
    )
    meta = json.dumps({
        "indexing_technique": "high_quality",
        "doc_form": "text_model",
        "doc_language": "Chinese",
        "process_rule": {"mode": "automatic"},
    }).encode("utf-8")
    parts.append(
        ("--%s\r\n" % boundary).encode()
        + b'Content-Disposition: form-data; name="data"\r\n'
        + b"Content-Type: application/json\r\n\r\n"
        + meta + b"\r\n"
    )
    body = b"".join(parts) + ("--%s--\r\n" % boundary).encode()
    req = urllib.request.Request(
        f"{BASE}/datasets/{DID}/document/create-by-file",
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


if __name__ == "__main__":
    if not TOKEN or not DID:
        print("need TOKEN and DID env vars"); sys.exit(1)
    for fn in TARGETS:
        try:
            r = upload(fn)
            doc = r.get("document", {})
            print(f"{fn}: HTTP OK | batch={doc.get('batch')} | status={doc.get('indexing_status')}")
        except Exception as e:
            print(f"{fn}: FAIL {e}")
