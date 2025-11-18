import csv
import os

ARCHIVO_CSV = "paises.csv"


# ==========================
# Funciones de soporte general
# ==========================

def normalizar_cadena(texto: str) -> str:
    """Devuelve el texto sin espacios al inicio/fin y en minúsculas."""
    return texto.strip().lower()


def pedir_entero_positivo(mensaje: str) -> int:
    """Pide un entero positivo (> 0) al usuario, validando la entrada."""
    while True:
        dato = input(mensaje).strip()
        if dato.isdigit():
            numero = int(dato)
            if numero > 0:
                return numero
        print("❌ Debe ingresar un número entero positivo mayor que 0.")


def pedir_rango_entero(mensaje_min: str, mensaje_max: str):
    """Pide un rango [min, max] de enteros positivos, validando."""
    while True:
        minimo = input(mensaje_min).strip()
        maximo = input(mensaje_max).strip()

        if not (minimo.isdigit() and maximo.isdigit()):
            print("❌ Debe ingresar números enteros positivos en ambos campos.")
            continue

        minimo = int(minimo)
        maximo = int(maximo)

        if minimo <= 0 or maximo <= 0:
            print("❌ Ambos valores deben ser mayores que 0.")
            continue

        if minimo > maximo:
            print("❌ El valor mínimo no puede ser mayor que el máximo.")
            continue

        return minimo, maximo


def pedir_cadena_no_vacia(mensaje: str) -> str:
    """Pide una cadena no vacía al usuario."""
    while True:
        texto = input(mensaje).strip()
        if texto != "":
            return texto
        print("❌ El texto no puede estar vacío.")


# ==========================
# Manejo de archivo CSV
# ==========================

def cargar_paises_desde_csv(nombre_archivo: str) -> list[dict]:
    """
    Lee el archivo CSV y devuelve una lista de diccionarios.
    Se valida:
      - Que el archivo exista.
      - Que tenga las columnas esperadas.
      - Que los campos numéricos sean válidos y positivos.
    Las filas inválidas se ignoran con un mensaje.
    """
    paises: list[dict] = []

    # Validar existencia del archivo
    if not os.path.exists(nombre_archivo):
        print(f"⚠️ No se encontró el archivo '{nombre_archivo}'. Se iniciará con lista vacía.")
        return paises

    # Abrir y leer el CSV
    with open(nombre_archivo, newline="", encoding="utf-8") as f:
        lector = csv.DictReader(f)

        columnas_esperadas = ["nombre", "poblacion", "superficie", "continente"]
        # Validar que estén todas las columnas
        if lector.fieldnames is None:
            print("⚠️ El archivo CSV no tiene encabezado. Se iniciará con lista vacía.")
            return paises

        for col in columnas_esperadas:
            if col not in lector.fieldnames:
                print(f"⚠️ El CSV no tiene la columna requerida '{col}'. Se iniciará con lista vacía.")
                return paises

        # Procesar fila por fila
        for nro_linea, fila in enumerate(lector, start=2):  # 2 = después del encabezado
            nombre = fila["nombre"].strip()
            poblacion_str = fila["poblacion"].strip()
            superficie_str = fila["superficie"].strip()
            continente = fila["continente"].strip()

            # Validar campos de texto
            if nombre == "" or continente == "":
                print(f"⚠️ Línea {nro_linea}: nombre o continente vacío. Fila ignorada.")
                continue

            # Validar que población y superficie sean numéricas
            if not (poblacion_str.isdigit() and superficie_str.isdigit()):
                print(f"⚠️ Línea {nro_linea}: población o superficie no numérica. Fila ignorada.")
                continue

            poblacion = int(poblacion_str)
            superficie = int(superficie_str)

            # Validar que sean valores positivos
            if poblacion <= 0 or superficie <= 0:
                print(f"⚠️ Línea {nro_linea}: población o superficie no positiva. Fila ignorada.")
                continue

            pais = {
                "nombre": nombre,
                "poblacion": poblacion,
                "superficie": superficie,
                "continente": continente
            }
            paises.append(pais)

    return paises


def guardar_paises_en_csv(nombre_archivo: str, paises: list[dict]):
    """
    Guarda la lista de países en el archivo CSV.
    Sobrescribe el archivo completo.
    No usa manejo de excepciones; se asume que el sistema permite escribir.
    """
    campos = ["nombre", "poblacion", "superficie", "continente"]

    if len(paises) == 0:
        print("ℹ️ No hay países cargados. Se creará el archivo solo con el encabezado.")

    with open(nombre_archivo, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=campos)
        escritor.writeheader()
        for pais in paises:
            escritor.writerow(pais)

    print("💾 Datos guardados automáticamente en el archivo CSV.")


# ==========================
# Operaciones de la aplicación
# ==========================

def agregar_pais(paises: list[dict]):
    """Agrega un nuevo país a la lista, validando que no haya campos vacíos."""
    print("\n=== Agregar país ===")
    nombre = pedir_cadena_no_vacia("Nombre del país: ")
    poblacion = pedir_entero_positivo("Población (entero positivo): ")
    superficie = pedir_entero_positivo("Superficie en km² (entero positivo): ")
    continente = pedir_cadena_no_vacia("Continente: ")

    nuevo = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
    paises.append(nuevo)
    print(f"✅ País '{nombre}' agregado correctamente.")
    # Guardado automático
    guardar_paises_en_csv(ARCHIVO_CSV, paises)


def buscar_paises_por_nombre(paises: list[dict], termino: str) -> list[dict]:
    """Devuelve los países cuyo nombre contiene el término (búsqueda parcial, sin distinción de mayúsculas)."""
    termino_norm = normalizar_cadena(termino)
    resultados = []
    for pais in paises:
        if termino_norm in normalizar_cadena(pais["nombre"]):
            resultados.append(pais)
    return resultados


def actualizar_pais(paises: list[dict]):
    """Actualiza población y superficie de un país seleccionado por búsqueda de nombre."""
    print("\n=== Actualizar país ===")
    termino = pedir_cadena_no_vacia("Ingrese el nombre (o parte del nombre) del país a actualizar: ")

    resultados = buscar_paises_por_nombre(paises, termino)
    if not resultados:
        print("❌ No se encontraron países que coincidan con la búsqueda.")
        return

    print("\nPaíses encontrados:")
    for i, pais in enumerate(resultados, start=1):
        print(f"{i}. {pais['nombre']} - Población: {pais['poblacion']} - Superficie: {pais['superficie']} km²")

    while True:
        opcion = input("Seleccione el número del país a actualizar (o 0 para cancelar): ").strip()
        if opcion.isdigit():
            num_opcion = int(opcion)
            if num_opcion == 0:
                print("🔙 Operación cancelada.")
                return
            if 1 <= num_opcion <= len(resultados):
                pais_seleccionado = resultados[num_opcion - 1]
                break
        print("❌ Opción inválida.")

    print(f"\nActualizando '{pais_seleccionado['nombre']}'")
    nueva_poblacion = pedir_entero_positivo("Nueva población: ")
    nueva_superficie = pedir_entero_positivo("Nueva superficie en km²: ")

    pais_seleccionado["poblacion"] = nueva_poblacion
    pais_seleccionado["superficie"] = nueva_superficie
    print("✅ Datos actualizados correctamente.")
    # Guardado automático
    guardar_paises_en_csv(ARCHIVO_CSV, paises)


def opcion_buscar_pais(paises: list[dict]):
    """Opción de menú para buscar un país y mostrar resultados."""
    print("\n=== Buscar país por nombre ===")
    termino = pedir_cadena_no_vacia("Ingrese el nombre (o parte del nombre) del país: ")
    resultados = buscar_paises_por_nombre(paises, termino)

    if not resultados:
        print("❌ No se encontraron países con ese criterio.")
        return

    print("\nResultados de la búsqueda:")
    mostrar_lista_paises(resultados)


def filtrar_por_continente(paises: list[dict]):
    """Filtra países por continente."""
    print("\n=== Filtrar países por continente ===")
    continente = pedir_cadena_no_vacia("Ingrese el continente: ")
    continente_norm = normalizar_cadena(continente)

    filtrados = [p for p in paises if normalizar_cadena(p["continente"]) == continente_norm]

    if not filtrados:
        print("❌ No se encontraron países en ese continente.")
        return

    print(f"\nPaíses en el continente '{continente}':")
    mostrar_lista_paises(filtrados)


def filtrar_por_rango_poblacion(paises: list[dict]):
    """Filtra países por rango de población."""
    print("\n=== Filtrar países por rango de población ===")
    minimo, maximo = pedir_rango_entero("Población mínima: ", "Población máxima: ")

    filtrados = [p for p in paises if minimo <= p["poblacion"] <= maximo]

    if not filtrados:
        print("❌ No se encontraron países dentro de ese rango de población.")
        return

    print(f"\nPaíses con población entre {minimo} y {maximo}:")
    mostrar_lista_paises(filtrados)


def filtrar_por_rango_superficie(paises: list[dict]):
    """Filtra países por rango de superficie."""
    print("\n=== Filtrar países por rango de superficie ===")
    minimo, maximo = pedir_rango_entero("Superficie mínima (km²): ", "Superficie máxima (km²): ")

    filtrados = [p for p in paises if minimo <= p["superficie"] <= maximo]

    if not filtrados:
        print("❌ No se encontraron países dentro de ese rango de superficie.")
        return

    print(f"\nPaíses con superficie entre {minimo} y {maximo} km²:")
    mostrar_lista_paises(filtrados)


def ordenar_paises(paises: list[dict]):
    """Ordena la lista de países según criterio elegido por el usuario."""
    print("\n=== Ordenar países ===")
    print("1) Ordenar por nombre")
    print("2) Ordenar por población")
    print("3) Ordenar por superficie")
    opcion = input("Elija una opción: ").strip()

    if opcion not in ("1", "2", "3"):
        print("❌ Opción inválida.")
        return

    print("\nTipo de orden:")
    print("1) Ascendente")
    print("2) Descendente")
    orden = input("Elija una opción: ").strip()

    if orden == "1":
        reverso = False
    elif orden == "2":
        reverso = True
    else:
        print("❌ Opción de orden inválida.")
        return

    if opcion == "1":
        clave = "nombre"
    elif opcion == "2":
        clave = "poblacion"
    else:
        clave = "superficie"

    paises_ordenados = sorted(paises, key=lambda p: p[clave], reverse=reverso)

    print("\nPaíses ordenados:")
    mostrar_lista_paises(paises_ordenados)


def mostrar_estadisticas(paises: list[dict]):
    """Muestra estadísticas básicas del conjunto de países."""
    print("\n=== Estadísticas ===")
    if not paises:
        print("❌ No hay países cargados para calcular estadísticas.")
        return

    # País con mayor y menor población
    pais_max_pob = max(paises, key=lambda p: p["poblacion"])
    pais_min_pob = min(paises, key=lambda p: p["poblacion"])

    # Promedios
    total_poblacion = sum(p["poblacion"] for p in paises)
    total_superficie = sum(p["superficie"] for p in paises)
    cantidad = len(paises)

    promedio_poblacion = total_poblacion / cantidad
    promedio_superficie = total_superficie / cantidad

    # Cantidad de países por continente
    conteo_continentes: dict[str, int] = {}
    for p in paises:
        cont = p["continente"]
        if cont in conteo_continentes:
            conteo_continentes[cont] += 1
        else:
            conteo_continentes[cont] = 1

    print(f"🧍 País con mayor población: {pais_max_pob['nombre']} ({pais_max_pob['poblacion']})")
    print(f"🧍 País con menor población: {pais_min_pob['nombre']} ({pais_min_pob['poblacion']})")
    print(f"📊 Promedio de población: {promedio_poblacion:.2f}")
    print(f"📏 Promedio de superficie: {promedio_superficie:.2f} km²")
    print("\n🌍 Cantidad de países por continente:")
    for cont, cant in conteo_continentes.items():
        print(f"   - {cont}: {cant}")


def mostrar_lista_paises(paises: list[dict]):
    """Muestra una lista de países en formato legible."""
    if not paises:
        print("   (Lista vacía)")
        return

    for p in paises:
        print(
            f"- {p['nombre']} | Población: {p['poblacion']} | "
            f"Superficie: {p['superficie']} km² | Continente: {p['continente']}"
        )


# ==========================
# Menú principal
# ==========================

def mostrar_menu():
    print("\n===============================")
    print("   Gestión de Datos de Países  ")
    print("===============================")
    print("1) Agregar país")
    print("2) Actualizar datos de un país")
    print("3) Buscar país por nombre")
    print("4) Filtrar países por continente")
    print("5) Filtrar países por rango de población")
    print("6) Filtrar países por rango de superficie")
    print("7) Ordenar países")
    print("8) Mostrar estadísticas")
    print("0) Salir")
    print("===============================")


def main():
    paises = cargar_paises_desde_csv(ARCHIVO_CSV)

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            agregar_pais(paises)
        elif opcion == "2":
            actualizar_pais(paises)
        elif opcion == "3":
            opcion_buscar_pais(paises)
        elif opcion == "4":
            filtrar_por_continente(paises)
        elif opcion == "5":
            filtrar_por_rango_poblacion(paises)
        elif opcion == "6":
            filtrar_por_rango_superficie(paises)
        elif opcion == "7":
            ordenar_paises(paises)
        elif opcion == "8":
            mostrar_estadisticas(paises)
        elif opcion == "0":
            # Guardado final por las dudas
            guardar_paises_en_csv(ARCHIVO_CSV, paises)
            print("👋 Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("❌ Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
