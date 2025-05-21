import requests
import json

BASE_URL = "http://localhost:8000"

def test_predict():
    print("\nTestando endpoint /predict:")
    data = {
        "title": "Mickey 17",
        "year": 2025,
        "categorias": ["oscar_nominated", "oscar_winner", "globe_nominated", "globe_winner"]
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print("Resposta:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_top10():
    print("\nTestando endpoint /top10 para cada categoria:")
    categorias = ["oscar_nominated", "oscar_winner", "globe_nominated", "globe_winner"]
    
    for categoria in categorias:
        print(f"\nTop 10 para {categoria}:")
        response = requests.get(f"{BASE_URL}/top10?categoria={categoria}")
        print(f"Status: {response.status_code}")
        print("Resposta:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("Iniciando testes da API...")
    test_predict()
    test_top10() 