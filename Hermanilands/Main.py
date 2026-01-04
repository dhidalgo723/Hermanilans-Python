import random

# mini base de datos de jugadores (media global, nombre, posición)
JUGADORES = [
    # Porteros
    {"nombre": "Thibaut Courtois", "posicion": "POR", "media": 89},
    {"nombre": "Alisson Becker", "posicion": "POR", "media": 89},
    {"nombre": "Ederson", "posicion": "POR", "media": 88},
    {"nombre": "Marc-André ter Stegen", "posicion": "POR", "media": 87},
    
    # defensas
    {"nombre": "Virgil van Dijk", "posicion": "DFC", "media": 90},
    {"nombre": "Ruben Dias", "posicion": "DFC", "media": 88},
    {"nombre": "Marquinhos", "posicion": "DFC", "media": 87},
    {"nombre": "Antonio Rudiger", "posicion": "DFC", "media": 86},
    {"nombre": "Eder Militao", "posicion": "DFC", "media": 85},
    {"nombre": "Kim Min-jae", "posicion": "DFC", "media": 85},
    {"nombre": "Trent Alexander-Arnold", "posicion": "LD", "media": 87},
    {"nombre": "Achraf Hakimi", "posicion": "LD", "media": 86},
    {"nombre": "Kyle Walker", "posicion": "LD", "media": 84},
    {"nombre": "Andrew Robertson", "posicion": "LI", "media": 86},
    {"nombre": "Theo Hernandez", "posicion": "LI", "media": 85},
    {"nombre": "Alphonso Davies", "posicion": "LI", "media": 84},
    
    # mediocampistas
    {"nombre": "Kevin De Bruyne", "posicion": "MC", "media": 91},
    {"nombre": "Jude Bellingham", "posicion": "MC", "media": 90},
    {"nombre": "Rodri", "posicion": "MCD", "media": 90},
    {"nombre": "Luka Modric", "posicion": "MC", "media": 88},
    {"nombre": "Casemiro", "posicion": "MCD", "media": 87},
    {"nombre": "Bruno Fernandes", "posicion": "MCO", "media": 87},
    {"nombre": "Frenkie de Jong", "posicion": "MC", "media": 86},
    {"nombre": "Federico Valverde", "posicion": "MC", "media": 86},
    {"nombre": "Bernardo Silva", "posicion": "MC", "media": 86},
    {"nombre": "Pedri", "posicion": "MC", "media": 85},
    
    # extremos
    {"nombre": "Lionel Messi", "posicion": "ED", "media": 99},
    {"nombre": "Vinicius Jr", "posicion": "EI", "media": 90},
    {"nombre": "Mohamed Salah", "posicion": "ED", "media": 89},
    {"nombre": "Kylian Mbappé", "posicion": "EI", "media": 91},
    {"nombre": "Cristiano Ronaldo", "posicion": "ED", "media": 99},
    {"nombre": "Phil Foden", "posicion": "EI", "media": 87},
    {"nombre": "Leroy Sané", "posicion": "EI", "media": 85},
    {"nombre": "Rafael Leão", "posicion": "EI", "media": 85},
    
    # delanteros
    {"nombre": "Erling Haaland", "posicion": "DC", "media": 91},
    {"nombre": "Harry Kane", "posicion": "DC", "media": 90},
    {"nombre": "Robert Lewandowski", "posicion": "DC", "media": 89},
    {"nombre": "Victor Osimhen", "posicion": "DC", "media": 88},
    {"nombre": "Lautaro Martinez", "posicion": "DC", "media": 87},
    {"nombre": "Darwin Núñez", "posicion": "DC", "media": 84},
]

FORMACIONES = {
    "4-3-3": {"POR": 1, "DEF": 4, "MC": 3, "DEL": 3},
    "4-4-2": {"POR": 1, "DEF": 4, "MC": 4, "DEL": 2},
}

player1 = input("Ingresa el nombre del PRIMER JUGADOR: ")
player2 = input("Ingresa el nombre del SEGUNDO JUGADOR: ")

# getter de categoria de posicion
def obtener_categoria_posicion(pos):
    """Convierte posiciones específicas en categorías generales"""
    if pos == "POR":
        return "POR"
    elif pos in ["DFC", "LD", "LI"]:
        return "DEF"
    elif pos in ["MC", "MCD", "MCO"]:
        return "MC"
    elif pos in ["EI", "ED", "DC"]:
        return "DEL"
    return None

# funcion que muestra los jugadores que quedan
def mostrar_jugadores_disponibles(disponibles, categoria=None):
    """Muestra los jugadores disponibles, opcionalmente filtrados por categoría"""
    # creacion de lista de jugadores filtrados
    jugadores_filtrados = []
    
    # enumerate añade un contador automatico a la lista
    # recorre cada jugador disponible con su numero de posicion
    for idx, j in enumerate(disponibles):
        # obtiene la categoria del jugador (POR, DEF, MC o DEL)
        cat = obtener_categoria_posicion(j["posicion"])
        # si no hay filtro o el jugador es de la categoria buscada
        if categoria is None or cat == categoria:
        # guarda el numero y el jugador en la lista filtrada
            jugadores_filtrados.append((idx, j))
    
    # si no esta en jugadores filtrados
    if not jugadores_filtrados:
        print(f"No hay jugadores disponibles en la categoría {categoria}")
        return []
    
    # muestra los jugadores disponibles
    print("\nJugadores disponibles:")
    for idx, j in jugadores_filtrados:
        print(f"{idx}. {j['nombre']} - {j['posicion']} (Media: {j['media']})")
    
    return jugadores_filtrados

# elige al jugador
def elegir_jugador(jugador_num, disponibles, categoria, plantilla, formacion):
    """Permite a un jugador elegir un futbolista"""
    # obtiene cuantos jugadores se necesitan de esa categoría segun la formación elegida
    requerido = formacion[categoria]
    # los actuales seran iguales a la suma de la cantidad de jugadores en plantilla de esa posicion
    actuales = sum(1 for j in plantilla if obtener_categoria_posicion(j["posicion"]) == categoria)
    
    # si todavia no llegas a los requeridos, sigues jugando
    if actuales >= requerido:
        print(f"Ya tienes todos los {categoria} necesarios ({requerido})")
        return None
    
    # sigue al proximo jugador
    print(f"\n--- Turno del Jugador {jugador_num} ---")
    # muestra la categoria elegida y los jugadores que te faltan
    print(f"Categoría: {categoria} (Tienes {actuales}/{requerido})")
    
    jugadores_filtrados = mostrar_jugadores_disponibles(disponibles, categoria)
    
    if not jugadores_filtrados:
        return None
    
    while True:
        try:
            eleccion = int(input("Elige el número del jugador: "))
            jugador_elegido = disponibles[eleccion]
            
            # Verificar que sea de la categoría correcta
            if obtener_categoria_posicion(jugador_elegido["posicion"]) == categoria:
                return jugador_elegido
            else:
                print("Ese jugador no pertenece a la categoría actual.")
        except (ValueError, IndexError):
            print("Opción inválida. Intenta de nuevo.")

# funcion de media
def calcular_media_equipo(plantilla):
    """Calcula la media global del equipo"""
    # si la longitud de la plantilla es igual a 0
    if len(plantilla) == 0:
        return 0 # devuelve 0
    # sino recorre cada jugador de la plantilla extrae sus datos, los suma y devuelve el numero de jugadores que tiene y los que le faltan
    return sum(j["media"] for j in plantilla) / len(plantilla)

# funcion que muestra la plantilla
def mostrar_plantilla(jugador_num, plantilla, formacion):
    """Muestra la plantilla actual de un jugador"""
    print(f"\n=== Plantilla del Jugador {jugador_num} ===")
    print(f"Formación: {formacion}")
    
    # muestra las categorias
    categorias = ["POR", "DEF", "MC", "DEL"]
    for cat in categorias:
        jugadores_cat = [j for j in plantilla if obtener_categoria_posicion(j["posicion"]) == cat]
        print(f"\n{cat}:")
        for j in jugadores_cat:
            print(f"  - {j['nombre']} ({j['posicion']}) - Media: {j['media']}")

# main
def main():
    print("=" * 50)
    print("JUEGO DE DRAFT DE FUTBOLISTAS")
    print("=" * 50)
    
    # seleccion de formaciones
    print("\nFormaciones disponibles:")
    for nombre, detalle in FORMACIONES.items():
        print(f"- {nombre}: {detalle['POR']} POR, {detalle['DEF']} DEF, {detalle['MC']} MC, {detalle['DEL']} DEL")
    
    # si elige la formacion 1, o no elige bien
    formacion1 = input(f"\n {player1}, elige tu formación (4-3-3 o 4-4-2): ").strip()
    while formacion1 not in FORMACIONES:
        formacion1 = input("Formación inválida. Elige 4-3-3 o 4-4-2: ").strip()
    
    # si elige la formacion 2, o no elige bien
    formacion2 = input(f"{player2}, elige tu formación (4-3-3 o 4-4-2): ").strip()
    while formacion2 not in FORMACIONES:
        formacion2 = input("Formación inválida. Elige 4-3-3 o 4-4-2: ").strip()
    
    plantilla1 = []
    plantilla2 = []
    disponibles = JUGADORES.copy()
    
    form1 = FORMACIONES[formacion1]
    form2 = FORMACIONES[formacion2]
    
    # crear orden de draft por categorías
    categorias = ["POR", "DEF", "MC", "DEL"]
    turnos = []
    
    for cat in categorias:
        # para cada categoría, crear turnos y mezclarlos solo dentro de esa categoría
        turnos_categoria = []
        max_picks = max(form1[cat], form2[cat])
        for pick in range(max_picks):
            if pick < form1[cat]:
                turnos_categoria.append((1, cat))
            if pick < form2[cat]:
                turnos_categoria.append((2, cat))
        
        # mezclar solo los turnos de esta categoría antes de añadirlos
        random.shuffle(turnos_categoria)
        turnos.extend(turnos_categoria)
    
    print(f"\nSe realizarán {len(turnos)} selecciones en total.")
    input("Presiona Enter para comenzar el draft...")
    
    # escoger plantillas
    for turno_num, (jugador, categoria) in enumerate(turnos, 1):
        print(f"\n{'='*50}")
        print(f"TURNO {turno_num}/{len(turnos)}")
        print(f"{'='*50}")
        
        if jugador == 1:
            jugador_elegido = elegir_jugador(1, disponibles, categoria, plantilla1, form1)
            if jugador_elegido:
                plantilla1.append(jugador_elegido)
                disponibles.remove(jugador_elegido)
                print(f"\n {player1} seleccionó a {jugador_elegido['nombre']}")
        else:
            jugador_elegido = elegir_jugador(2, disponibles, categoria, plantilla2, form2)
            if jugador_elegido:
                plantilla2.append(jugador_elegido)
                disponibles.remove(jugador_elegido)
                print(f"\n {player2} seleccionó a {jugador_elegido['nombre']}")
    
    # muestra los resultados finales
    print("\n" + "="*50)
    print("RESULTADOS FINALES...")
    print("="*50)
    
    mostrar_plantilla(1, plantilla1, formacion1)
    mostrar_plantilla(2, plantilla2, formacion2)
    
    media1 = calcular_media_equipo(plantilla1)
    media2 = calcular_media_equipo(plantilla2)
    
    print("\n" + "="*50)
    input("EL GANADOR ES....")
    print("="*50)
    
    if media1 > media2:
        print(f"🏆 ¡{player1} GANA! (Media: {media1:.2f} vs {media2:.2f})")
    elif media2 > media1:
        print(f"🏆 ¡{player2} GANA! (Media: {media2:.2f} vs {media1:.2f})")
    else:
        print(f"🤝 ¡EMPATE! (Ambos con media: {media1:.2f})")

if __name__ == "__main__":
    main()