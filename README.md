# Wirtualny inżynier wyścigowy: analiza telemetrii Assetto Corsa

Projekt z przedmiotu **Programowanie zaawansowane**.

Zbieram telemetrię z gry Assetto Corsa (tor Monza, auto GT3), czyszczę i analizuję dane w pandas, a następnie trenuję modele uczenia maszynowego (scikit-learn), które pokazują, które fragmenty toru najbardziej wpływają na czas okrążenia.

## Etapy
1. Logger telemetrii (shared memory AC → CSV)
2. Zbieranie danych (30–50 okrążeń)
3. Czyszczenie danych (pandas)
4. Analiza i wizualizacja (matplotlib)
5. Model ML: regresja czasu okrążenia, ważność cech
6. Prezentacja wyników

Szczegóły: [PLAN.md](PLAN.md)

## Technologie
Python, pandas, numpy, matplotlib, scikit-learn, Google Colab / Jupyter

## Uruchomienie
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
