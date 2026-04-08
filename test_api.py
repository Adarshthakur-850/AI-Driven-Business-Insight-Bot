import requests
import json
import time

API_URL = "http://localhost:8000"

def test_home():
    try:
        response = requests.get(f"{API_URL}/")
        assert response.status_code == 200
        print("✅ Home endpoint is up.")
    except Exception as e:
        print(f"❌ Home endpoint failed: {e}")

def test_ask_mock():
    # Test a query that should trigger the mock SQL generation (or real if API key set)
    payload = {"question": "Show total revenue by country"}
    try:
        response = requests.post(f"{API_URL}/ask", json=payload)
        if response.status_code == 200:
            data = response.json()
            # Verify structure
            assert "data" in data
            assert "sql" in data
            assert "kpis" in data
            
            # Verify data content (should have results from sample data)
            if data["data"]:
                print(f"✅ Query successful. Rows returned: {len(data['data'])}")
                print(f"   SQL: {data['sql']}")
                print(f"   KPIs: {data['kpis']}")
            else:
                print("⚠️ Query returned no data (DB might be empty or query invalid).")
        else:
            print(f"❌ Ask endpoint failed with status {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Ask endpoint connection failed: {e}")

if __name__ == "__main__":
    print("Waiting for API to stabilize...")
    time.sleep(2)
    test_home()
    test_ask_mock()
