#!/usr/bin/env python3
import json, os, urllib.request
BASE=os.getenv("HARMONIZA_CRM_API_URL","http://127.0.0.1:8000"); TOKEN=os.getenv("HARMONIZA_CRM_API_TOKEN","")
req=urllib.request.Request(f"{BASE}/ops/followups-overdue", headers={"Authorization": f"Bearer {TOKEN}"})
try:
 data=json.load(urllib.request.urlopen(req, timeout=10)); print(f"Follow-ups vencidos: {data.get('count',0)}")
except Exception as e: print(f"Erro audit_followups: {e}")
