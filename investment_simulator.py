import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Clase que modela una inversión y sus cálculos asociados
# ---------------------------------------------------------------------
class Inversion:
    def __init__(self, inversion_inicial, tasa_anual, años, aporte=0, inflacion=0, mensual=False):
        self.inversion_inicial = inversion_inicial  # monto inicial depositado
        self.tasa_anual = tasa_anual                # tasa de interés anual (en decimal)
        self.años = años                            # duración en años
        self.aporte = aporte                        # aporte periódico
        self.inflacion = inflacion                  # tasa de inflación anual (en decimal)
        self.mensual = mensual                      # True si los aportes son mensuales
        self.valor_final = 0                        # aquí guardaremos el valor final calculado
        self.historial = None                       # DataFrame con el historial por periodo

    # -----------------------------------------------------------------
    # Calcula el valor final de la inversión (nominal y ajustado por inflación)
    # -----------------------------------------------------------------
    def calcular_valor_final(self):
        # Ajusta la tasa y periodos si es mensual
        if self.mensual:
            tasa_periodo = self.tasa_anual / 12
            n_periodos = self.años * 12
            aporte = self.aporte
        else:
            tasa_periodo = self.tasa_anual
            n_periodos = self.años
            aporte = self.aporte

        # Fórmula: interés compuesto con aportes periódicos
        valor_final = (
            self.inversion_inicial * (1 + tasa_periodo) ** n_periodos
            + aporte * (((1 + tasa_periodo) ** n_periodos - 1) / tasa_periodo)
        )

        # Ajuste por inflación
        if self.inflacion > 0:
            valor_final_real = valor_final / ((1 + self.inflacion) ** self.años)
        else:
            valor_final_real = valor_final

        self.valor_final = round(valor_final, 2)
        self.historial = self.generar_historial(tasa_periodo, n_periodos, aporte)
        
        # Devuelve el valor ajustado por inflación (real)
        return round(valor_final_real, 2)

    # -----------------------------------------------------------------
    # Genera el historial con el valor acumulado en cada periodo
    # -----------------------------------------------------------------
    def generar_historial(self, tasa_periodo, n_periodos, aporte):
        valores = []                    # lista para almacenar el saldo en cada periodo
        saldo = self.inversion_inicial  # saldo inicial

        for i in range(n_periodos + 1):
            if i > 0:
                # Aplicamos interés y sumamos el aporte
                saldo = saldo * (1 + tasa_periodo) + aporte
            valores.append(round(saldo, 2))

        # Creamos un DataFrame con pandas para representar el historial
        if self.mensual:
            df = pd.DataFrame({"Mes": range(n_periodos + 1), "Valor acumulado": valores})
        else:
            df = pd.DataFrame({"Año": range(n_periodos + 1), "Valor acumulado": valores})

        return df

    # -----------------------------------------------------------------
    # Imprime un resumen con los parámetros y el valor final
    # -----------------------------------------------------------------
    def imprimir_resumen(self):
        if self.valor_final == 0:
            print("Primero debe calcular el valor final.")
            return

        resumen = pd.DataFrame({
            "Inversión inicial": [self.inversion_inicial],
            "Tasa anual": [self.tasa_anual],
            "Años": [self.años],
            "Aporte periódico": [self.aporte],
            "Mensual": [self.mensual],
            "Inflación": [self.inflacion],
            "Valor final": [self.valor_final]
        })
        print("\n📊 Resumen de la inversión:")
        print(resumen)

    # -----------------------------------------------------------------
    # Dibuja la serie temporal del valor acumulado
    # -----------------------------------------------------------------
    def graficar(self, label="Escenario"):
        if self.historial is None:
            print("Debe calcular el valor final primero.")
            return

        if self.mensual:
            x = self.historial["Mes"]
        else:
            x = self.historial["Año"]

        y = self.historial["Valor acumulado"]
        plt.plot(x, y, '-o', label=label)

    # -----------------------------------------------------------------
    # Exporta el historial a un archivo CSV
    # -----------------------------------------------------------------
    def exportar_csv(self, nombre_archivo="historial.csv"):
        if self.historial is not None:
            self.historial.to_csv(nombre_archivo, index=False)
            print(f"📁 Historial exportado a {nombre_archivo}")
        else:
            print("No hay historial para exportar.")


# ---------------------------------------------------------------------
# Función de interacción: simulación individual
# ---------------------------------------------------------------------
def simulacion_individual():
    print("\n=== Simulación individual ===")
    inversion_inicial = float(input("💰 Inversión inicial: "))
    tasa_anual = float(input("📈 Tasa de interés anual (decimal, ej. 0.05 para 5%): "))
    años = int(input("⏳ Número de años: "))
    aporte = float(input("💵 Aporte periódico (0 si no aplica): "))
    inflacion = float(input("📉 Tasa de inflación anual (0 si no aplica): "))
    mensual = input("📅 ¿Aportes mensuales? (s/n): ").lower() == "s"

    # Creamos y calculamos la inversion
    inversion = Inversion(inversion_inicial, tasa_anual, años, aporte, inflacion, mensual)
    valor_real = inversion.calcular_valor_final()
    inversion.imprimir_resumen()

    print("\n📑 Historial (primeros 12 registros):")
    print(inversion.historial.head(12))

    # Graficar
    inversion.graficar(label="Escenario principal")
    plt.xlabel("Meses" if mensual else "Años")
    plt.ylabel("Valor acumulado")
    plt.title("Crecimiento de la inversión")
    plt.legend()
    plt.show()

    exportar = input("¿Desea exportar el historial a CSV? (s/n): ").lower()
    if exportar == "s":
        inversion.exportar_csv()


# ---------------------------------------------------------------------
# Función que permite comparar varios escenarios
# ---------------------------------------------------------------------
def comparar_escenarios():
    print("\n=== Comparación de escenarios ===")

    escenarios = []  # lista para guardar tuplas (inversion_obj, etiqueta)
    n = int(input("¿Cuántos escenarios desea comparar? "))

    # Recolectamos los datos de cada escenario
    for i in range(n):
        print(f"\n--- Escenario {i+1} ---")
        inversion_inicial = float(input("💰 Inversión inicial: "))
        tasa_anual = float(input("📈 Tasa de interés anual (decimal, ej. 0.05): "))
        años = int(input("⏳ Número de años: "))
        aporte = float(input("💵 Aporte periódico (0 si no aplica): "))
        inflacion = float(input("📉 Tasa de inflación anual (0 si no aplica): "))
        mensual = input("📅 ¿Aportes mensuales? (s/n): ").lower() == "s"

        inv = Inversion(inversion_inicial, tasa_anual, años, aporte, inflacion, mensual)
        inv.calcular_valor_final()
        escenarios.append((inv, f"Escenario {i+1}"))

    # Graficar todos los escenarios juntos
    for inv, label in escenarios:
        inv.graficar(label)

    plt.xlabel("Meses" if escenarios[0][0].mensual else "Años")
    plt.ylabel("Valor acumulado")
    plt.title("Comparación de escenarios de inversión")
    plt.legend()
    plt.show()

    # Exportar a Excel (cada escenario en una hoja)
    exportar = input("¿Desea exportar los escenarios a Excel? (s/n): ").lower()
    if exportar == "s":
        with pd.ExcelWriter("escenarios_inversion.xlsx") as writer:
            for inv, label in escenarios:
                inv.historial.to_excel(writer, sheet_name=label, index=False)
        print("📁 Escenarios exportados a escenarios_inversion.xlsx")


# ---------------------------------------------------------------------
# Bloque principal: menú de interacción
# ---------------------------------------------------------------------
if __name__ == "__main__":
    while True:
        print("\n=== Simulador de Inversiones ===")
        print("1. Simulación individual")
        print("2. Comparar escenarios")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            simulacion_individual()
        elif opcion == "2":
            comparar_escenarios()
        elif opcion == "3":
            print("👋 Gracias por usar el simulador.")
            break
        else:
            print("❌ Opción no válida.")