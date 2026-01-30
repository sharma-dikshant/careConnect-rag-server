import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8080"
PRESIGNED_URL = "https://bucket-whatsapp-clone.s3.ap-south-1.amazonaws.com/globals/1/d45b6557-fd97-4d6f-ad99-231c6ce0e1fb_Care%20Connect%20Full%20Srs.pdf?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEHAaCmFwLXNvdXRoLTEiSDBGAiEA1aq7dY24Mxkpg5abwLAZM8ccimpsrtf8d%2FR6j9PQrUYCIQDlkwQTkfms29IBfStHw2sFYhgXAxOLcGY%2FQrDWHph78Cq5Awg5EAAaDDYyNDU3MTI4NTE4MiIMeMdryzlgDfy1jEzyKpYDVxpgOlQ%2FJdzZsBhPcJ4bQvksVphcurq21X5CH6NsF8E0dSuOyZq%2FhxPD%2BJu29mEC68WL4nVnx3jFr0YsnF6sgszhIsU2ptBqvaUujHXmWu%2BgfMIr6zWSefuDH6V3zIRUoPCgp%2F9U7PySrnYmUz9X%2FuK0wwQGVC%2BkpN%2BtfmQfKHHWgTbTxdmN1oTDCvkmBnb%2FZrGYuuWT7UfB82c33E6BySAhTv0eBncPv8eAwknX9aUB62dxLUGGJF67rYn95G%2BwMO0TR3mxSfRohoWcW%2BS%2BUoaEVOAP7%2F%2Bm6ZfovnrFLOEitmzQLi2mxsaK2b9BeJRfsx3riFgx3dqYATP%2BI88Fh70l9CxFM7%2B0cotJtH2nvIqOioTxQqFg50hU4gHPZsONFJF%2BZsjXsn9wcLEpaIjWWK2VkT8Ng9%2FcFEsd2S3LAdbHjCFB8Z%2FcXH3%2FNMoeWwr4EXlj9uOY%2FQbi7E1hvjRMKIWvOGgGAk4SXYBfX0YIfFrFKC27BVtMB0RobXz%2B6RyCMwLeY0EXpsYj40dtI6oAaKRv7rQk7DCv1tvLBjrdAinFjo4OIYMS5kbBK0v9LNCSgsZrlpkMLoUnonktk6UCIC38RPsEh1LGMcdwMdIOoSRfPyEJDFWVvoZ1lSLZXGOj3riuXK3sERyZLu30wpgr8aoXbDrqlR0DzA0quBEnnpG5Ke2j%2B0lIkYT4lE%2FO0bKml1Nef7AgjSIxR74mC29I%2FxPrbWZD5QNCXy%2BBUDA%2FY83RGbfLdJvx88KAG1iWcSY2T4Jfm88jh5UO4VA0uS0bz8qfGiUwz1wKeevVWcZ7zuGM9n8HvnHyAwdGAEXwVV9zYCSvtZ95Cada87DsF03EMdzHP8D689FBxvLNVaBUKmoAiYJeZb7%2FpEU89ciDbLOGHXbM2cI7uEqxPmueiGobCrsW0Jd%2FiANbPcwI1fQlUDFOBAUYHLz6vzyIQwEVbNAkcQz25j%2FyaDgYL1XyswXy1fR%2FDTNNQyTlEnDSuI5qRt3oQUlnLk8wcHnebfc%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAZC22ZP27O4XNGP4K%2F20260126%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20260126T082148Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=d85ed48be6f4f6fdbe11106834d4bda2531a15e30b75aa330befa17314cea328"

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
        data = response.json()
        print("Query Successful!")
        print("-" * 40)
        print(f"Answer: {data.get('answer')}")
        print("-" * 40)
        print("Sources:")
        for i, res in enumerate(data.get('sources', [])):
            print(f"-- Source {i+1} --")
            print(f"Source File: {res.get('source_file')}")
            print(f"Content: {res.get('content')[:200]}...")
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
