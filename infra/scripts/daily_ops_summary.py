#!/usr/bin/env python3
import json, os, urllib.request
BASE=os.getenv("HARMONIZA_CRM_API_URL","http://127.0.0.1:8000"); TOKEN=os.getenv("HARMONIZA_CRM_API_TOKEN","")
req=urllib.request.Request(f"{BASE}/dashboard/summary", headers={"Authorization": f"Bearer {TOKEN}"})
try:
 d=json.load(urllib.request.urlopen(req, timeout=10)); print(f"CRM Harmoniza — leads {d['leads_total']} | qualificados {d['qualificados']} | agendamentos {d['agendamentos']} | compras {d['compras']} | perdas {d['perdas']}")
except Exception as e: print(f"Erro daily_ops_summary: {e}")
