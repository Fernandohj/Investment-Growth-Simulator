# Investment Growth Simulator

A Python script to simulate and analyze investment growth, factoring in compound interest, periodic contributions, and inflation.

## Features

* Calculates the future value of an investment with compound interest.
* Allows for periodic contributions (either annual or monthly).
* Adjusts the final value for an inflation rate to show real purchasing power.
* **Single Simulation:** Analyzes one scenario, shows the historical data, and generates a plot.
* **Scenario Comparison:** Plots multiple simulations (e.g., different interest rates) on a single chart.
* **Data Export:**
    * Single simulation: Exports history to a `.csv` file.
    * Scenario comparison: Exports each scenario to a separate sheet in an `.xlsx` file.

## Setup

1.  Download or clone this repository:
    ```bash
    git clone [https://github.com/Fernandohj/Investment-Growth-Simulator.git](https://github.com/Fernandohj/Investment-Growth-Simulator.git)
    cd Investment-Growth-Simulator
    ```

2.  (Recommended) Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the simulator, execute the `investment_simulator.py` script from your terminal:

```bash
python investment_simulator.py
````

An interactive menu will appear:

```
=== Simulador de Inversiones ===
1. Simulación individual
2. Comparar escenarios
3. Salir
Seleccione una opción:
```

Follow the on-screen prompts to enter your simulation data.

```
```
