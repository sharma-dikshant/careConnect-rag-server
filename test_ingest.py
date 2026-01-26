import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8080"
PRESIGNED_URL = "<PRESIGNED_URL>"

def test_ingest():
    print(f"Testing ingestion from: {PRESIGNED_URL[:50]}...")
    payload = {
        "file_url": PRESIGNED_URL,
        "doctor_id": "doc_123",
        "patient_id": "pat_456"
    }

    try:
        response = requests.post(f"{BASE_URL}/ingest", json=payload)
        response.raise_for_status()
        data = response.json()
        print("Ingestion Successful!")
        print(json.dumps(data, indent=2))
        return True
    except requests.exceptions.HTTPError as e:
        print(f"Ingestion Failed: {e}")
        try:
          print(f"Response: {response.text}")
        except:
          pass
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def test_query():
    print("\nTesting query...")
    query_text = "What is Care Connect?"
    payload = {
        "query": query_text,
        "doctor_id": "doc_123",
        "patient_id": "pat_456",
        "limit": 10
    }

    try:
        response = requests.post(f"{BASE_URL}/query", json=payload)
        response.raise_for_status()
        results = response.json()
        print("Query Successful!")
        print(json.dumps(results, indent=2))
        # print(f"Found {len(results)} results for query: '{query_text}'")
        # for i, res in enumerate(results):
        #     print(f"-- Result {i+1} --")
        #     print(f"Source: {res.get('source_file')}")
        #     print(f"Content: {res.get('content')[:200]}...")  # Truncate content for display
        return True
    except requests.exceptions.HTTPError as e:
        print(f"Query Failed: {e}")
        try:
           print(f"Response: {response.text}")
        except:
           pass
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    if test_ingest():
        # Give a small delay to ensure DB commit if needed, though requests are synchronous
        time.sleep(1)
        test_query()
