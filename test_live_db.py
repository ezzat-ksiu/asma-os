import urllib.request
import json

url = 'https://cazlpsbwjrgxscctfoqn.supabase.co/rest/v1/operational_gates?select=*'
headers = {
    'apikey': 'sb_publishable_ymPtWABOYRMsXyqXHv3tzQ_mDz95Tlc',
    'Authorization': 'Bearer sb_publishable_ymPtWABOYRMsXyqXHv3tzQ_mDz95Tlc'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode('utf-8'))
        print('🎉 LIVE SUPABASE DATA READ SUCCESSFUL!')
        print(f'Retrieved {len(data)} operational gates from live database:')
        for g in data:
            print(f"  - [{g.get('gate_id')}] {g.get('name')}: {g.get('status')}")
except Exception as e:
    print('❌ Read Error:', e)
