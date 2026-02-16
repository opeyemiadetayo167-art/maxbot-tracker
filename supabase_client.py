import requests
import os

SUPABASE_URL = os.environ.get('SUPABASE_URL', 'https://fwwfgwnqrnchjizyzzhd.supabase.co')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3M6ZSI6ImFub24iLCJpYXQiOjE3NzA5NDg1NjAsImV4cCI6MjA4NjUyNDU2MH0.uKtpcmqQaJBzAM80LwVUT84G4V8pglyRY3VcUGuiwoQ')

HEADERS = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
    'Content-Type': 'application/json'
}

def supabase_select(table, filters=None):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    params = filters if filters else {}
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json() if response.status_code == 200 else []

def supabase_insert(table, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code in [200, 201]

def supabase_update(table, filters, data):
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    response = requests.patch(url, headers=HEADERS, params=filters, json=data)
    return response.status_code == 200
