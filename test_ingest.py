import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
PRESIGNED_URL = "https://careconnect-bucket.s3.ap-south-1.amazonaws.com/uploads/appointments/2/2/6680bc06-cf97-474b-85f5-c0525953206f_Emergency_Consultation_Sample.pdf?response-content-disposition=inline&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Security-Token=IQoJb3JpZ2luX2VjENP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCmFwLXNvdXRoLTEiRzBFAiEA3wV%2BLnWnfzC8LqKkG0LcI%2BhM0QeO3ARyRAiESkKRUf8CICAz5DH6oQzr0h3Ma%2FYVwMhkLDvdl0HBfFOmxWg9g0FCKsIDCJz%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMMzM3NjA4Mzg2NDkwIgzsRJiXlmFBQIgJ%2FSMqlgN0NbPTdwpTrbkZI%2F1cPcRaMvFCpOh%2FuKPD8v1iQn6sYoSYIdKpJtD6I1Z1BY2OaSFVsz7%2Bac3F%2FPVs57WKNNESR8ObHHOKIgu8daOWCuqu6VYu%2BzDaP%2FMzw%2FfwYUz4OWCHrasl0kjSXVvqVM7GQzIVTBTSQYTLFnMtTvBmxe520PVGWN4%2FRAtu9CGdgz5%2B5jvQMP%2F0UzZUNeK2J2vKFkTrdGr%2BBvpg5q912Rw2ype4bJBkIuBYY1mn30ckmuU7seAIHBpBBa5j31QPEeoAKPtb7ab1wmXzcGVTGBfBBqzMqkKstkNU0Xz9Raq9u4vqqsxrLJu7Nk7PkG%2FDyZ41ibkPsaF8rCWReq1QDAThO1655OLjkj4IQlUkdSODrYeGCeVaZIW5CMffF96ukbJ50bF4xgKAbWuNbGx2UHVxR3PLwN9pXya3BNnMH3gQECDGeG%2FoPRkSlSG7LMRkjMPROpTkNdMsR80Q1OLasE%2F5LHA7fuVp5VpEdptnDJKax%2F4fLLAoCcaDUTpSk1R098GNuGn25V6RlR05MJ7%2B%2B84GOt4CrllSyYAHx0R%2FSyQU5%2Bl2Pks7DFZpHOkR%2BUngcgJvFcLD5SSiiRvcGmBgIeSy6P6Aoch5wjkehkogBxWmD8oK%2F2Ahh2tAZofD7K9UTDdOqmsEN%2FWNr9%2BVgqXcbkq5CZQwwSLGkbUKw2sgsMqiV4snC3mmm72xT7r1qgaRjEh3Uhx0TIjCGcNFbVvtLTD%2Bn6cPgaXrf5QBCwQ%2FIEzNAWfNmP1HVCSOhADVQUPFD1GSE%2Fn0tbEmYgh7bXqcnDbmnS87WPTffc%2FS3KEnxAzc%2BHHs%2FRXRYcAvsaDiON7cCqkmxwPhOKcZMmkSDfRt5DYdZgny3slsoSAOYX3idXEn8DygCNU6bgwJ8HKu3IQJ%2BGYq6aXcRQRTBLXjDxnIJI9Wr1NyMipOwhhw%2BRnhrXArfBKE70U1IzsyyJa1TosamvqbicpMCsCGdmoa32BUXxUV%2BwlmHn78R%2FIyzE%2F3eRfI%2Bg4%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAU5GYHE65KIQJSKH7%2F20260415%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20260415T030218Z&X-Amz-Expires=43200&X-Amz-SignedHeaders=host&X-Amz-Signature=8a9416f97bf6b6424d7d8557c04b6527ab05b1bcd8a93675c1840a26bb785fc7"


def test_ingest():
    print(f"Testing ingestion from: {PRESIGNED_URL[:50]}...")
    payload = {
        "file_url": PRESIGNED_URL,
        "doctor_id": "1",
        "patient_id": "1"
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
        "doctor_id": "1",
        "patient_id": "1",
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
