import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# Mini base de datos de jugadores
JUGADORES = [
    # Porteros
    {"nombre": "Thibaut Courtois", "posicion": "POR", "media": 89},
    {"nombre": "Alisson Becker", "posicion": "POR", "media": 89},
    {"nombre": "Ederson", "posicion": "POR", "media": 88},
    {"nombre": "Marc-André ter Stegen", "posicion": "POR", "media": 87},
    # Defensas
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
    # Mediocampistas
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
    # Extremos
    {"nombre": "Lionel Messi", "posicion": "ED", "media": 99},
    {"nombre": "Vinicius Jr", "posicion": "EI", "media": 90},
    {"nombre": "Mohamed Salah", "posicion": "ED", "media": 89},
    {"nombre": "Kylian Mbappé", "posicion": "EI", "media": 91},
    {"nombre": "Cristiano Ronaldo", "posicion": "ED", "media": 99},
    {"nombre": "Phil Foden", "posicion": "EI", "media": 87},
    {"nombre": "Leroy Sané", "posicion": "EI", "media": 85},
    {"nombre": "Rafael Leão", "posicion": "EI", "media": 85},
    # Delanteros
    {"nombre": "Erling Haaland", "posicion": "DC", "media": 91},
    {"nombre": "Harry Kane", "posicion": "DC", "media": 90},
    {"nombre": "Robert Lewandowski", "posicion": "DC", "media": 89},
    {"nombre": "Victor Osimhen", "posicion": "DC", "media": 88},
    {"nombre": "Lautaro Martinez", "posicion": "DC", "media": 87},
    {"nombre": "Darwin Núñez", "posicion": "DC", "media": 84},
]

# Diccionario de formaciones disponibles
FORMACIONES = {
    "4-3-3": {"POR": 1, "DEF": 4, "MC": 3, "DEL": 3},
    "4-4-2": {"POR": 1, "DEF": 4, "MC": 4, "DEL": 2},
}

# Convierte posición específica a categoría general
def obtener_categoria_posicion(pos):
    if pos == "POR":
        return "POR"
    elif pos in ["DFC", "LD", "LI"]:
        return "DEF"
    elif pos in ["MC", "MCD", "MCO"]:
        return "MC"
    elif pos in ["EI", "ED", "DC"]:
        return "DEL"
    return None

# Calcula la media del equipo
def calcular_media_equipo(plantilla):
    if len(plantilla) == 0:
        return 0
    return sum(j["media"] for j in plantilla) / len(plantilla)

# Clase principal del juego con interfaz gráfica
class JuegoDraftGUI:
    def __init__(self, root):
        self.root = root  # Ventana principal
        self.root.title("Draft Futbolístico")  # Título de la ventana
        self.root.geometry("600x700")  # Tamaño de la ventana
        self.root.configure(bg="#2E7D32")  # Color de fondo verde
        
        # Variables del juego
        self.player1 = ""  # Nombre del jugador 1
        self.player2 = ""  # Nombre del jugador 2
        self.formacion1 = ""  # Formación elegida por jugador 1
        self.formacion2 = ""  # Formación elegida por jugador 2
        self.plantilla1 = []  # Lista de jugadores del equipo 1
        self.plantilla2 = []  # Lista de jugadores del equipo 2
        self.disponibles = JUGADORES.copy()  # Copia de jugadores disponibles
        self.turnos = []  # Lista de turnos del draft
        self.turno_actual = 0  # Índice del turno actual
        
        # Inicia con la pantalla de nombres
        self.pantalla_nombres()
    
    # Pantalla inicial para ingresar nombres
    def pantalla_nombres(self):
        self.limpiar_pantalla()  # Limpia la ventana
        
        # Frame contenedor principal
        frame = tk.Frame(self.root, bg="#2E7D32")
        frame.pack(expand=True)
        
        # Título del juego
        tk.Label(frame, text="🏆 DRAFT FUTBOLÍSTICO 🏆", 
                font=("Arial", 24, "bold"), bg="#2E7D32", fg="white").pack(pady=20)
        
        # Label para jugador 1
        tk.Label(frame, text="Nombre del Jugador 1:", 
                font=("Arial", 14), bg="#2E7D32", fg="white").pack(pady=5)
        # Campo de entrada para nombre jugador 1
        self.entry_player1 = tk.Entry(frame, font=("Arial", 14), width=25)
        self.entry_player1.pack(pady=5)
        
        # Label para jugador 2
        tk.Label(frame, text="Nombre del Jugador 2:", 
                font=("Arial", 14), bg="#2E7D32", fg="white").pack(pady=5)
        # Campo de entrada para nombre jugador 2
        self.entry_player2 = tk.Entry(frame, font=("Arial", 14), width=25)
        self.entry_player2.pack(pady=5)
        
        # Botón para continuar
        tk.Button(frame, text="Continuar", font=("Arial", 14, "bold"),
                 bg="#FFC107", fg="black", command=self.guardar_nombres,
                 width=20, height=2).pack(pady=30)
    
    # Guarda los nombres y va a selección de formaciones
    def guardar_nombres(self):
        self.player1 = self.entry_player1.get().strip()  # Obtiene nombre jugador 1
        self.player2 = self.entry_player2.get().strip()  # Obtiene nombre jugador 2
        
        # Valida que ambos nombres estén completos
        if not self.player1 or not self.player2:
            messagebox.showwarning("Error", "Ambos jugadores deben ingresar su nombre")
            return
        
        self.pantalla_formaciones()  # Va a siguiente pantalla
    
    # Pantalla de selección de formaciones
    def pantalla_formaciones(self):
        self.limpiar_pantalla()  # Limpia la ventana
        
        # Frame contenedor
        frame = tk.Frame(self.root, bg="#2E7D32")
        frame.pack(expand=True)
        
        # Título
        tk.Label(frame, text="Selección de Formaciones", 
                font=("Arial", 20, "bold"), bg="#2E7D32", fg="white").pack(pady=20)
        
        # Sección Jugador 1
        tk.Label(frame, text=f"🔵 {self.player1}", 
                font=("Arial", 16, "bold"), bg="#2E7D32", fg="#64B5F6").pack(pady=10)
        
        # Frame para botones de formación jugador 1
        frame_form1 = tk.Frame(frame, bg="#2E7D32")
        frame_form1.pack(pady=5)
        
        # Botón 4-3-3 para jugador 1
        tk.Button(frame_form1, text="4-3-3\n1 POR • 4 DEF • 3 MC • 3 DEL", 
                 font=("Arial", 12), bg="#1976D2", fg="white",
                 command=lambda: self.seleccionar_formacion(1, "4-3-3"),
                 width=25, height=3).pack(side=tk.LEFT, padx=5)
        
        # Botón 4-4-2 para jugador 1
        tk.Button(frame_form1, text="4-4-2\n1 POR • 4 DEF • 4 MC • 2 DEL", 
                 font=("Arial", 12), bg="#1976D2", fg="white",
                 command=lambda: self.seleccionar_formacion(1, "4-4-2"),
                 width=25, height=3).pack(side=tk.LEFT, padx=5)
        
        # Sección Jugador 2
        tk.Label(frame, text=f"🔴 {self.player2}", 
                font=("Arial", 16, "bold"), bg="#2E7D32", fg="#EF5350").pack(pady=10)
        
        # Frame para botones de formación jugador 2
        frame_form2 = tk.Frame(frame, bg="#2E7D32")
        frame_form2.pack(pady=5)
        
        # Botón 4-3-3 para jugador 2
        tk.Button(frame_form2, text="4-3-3\n1 POR • 4 DEF • 3 MC • 3 DEL", 
                 font=("Arial", 12), bg="#C62828", fg="white",
                 command=lambda: self.seleccionar_formacion(2, "4-3-3"),
                 width=25, height=3).pack(side=tk.LEFT, padx=5)
        
        # Botón 4-4-2 para jugador 2
        tk.Button(frame_form2, text="4-4-2\n1 POR • 4 DEF • 4 MC • 2 DEL", 
                 font=("Arial", 12), bg="#C62828", fg="white",
                 command=lambda: self.seleccionar_formacion(2, "4-4-2"),
                 width=25, height=3).pack(side=tk.LEFT, padx=5)
        
        # Label para mostrar formaciones seleccionadas
        self.label_formaciones = tk.Label(frame, text="", 
                                         font=("Arial", 12), bg="#2E7D32", fg="white")
        self.label_formaciones.pack(pady=20)
        
        # Botón para iniciar draft (deshabilitado inicialmente)
        self.btn_iniciar = tk.Button(frame, text="¡Iniciar Draft!", 
                                     font=("Arial", 14, "bold"), bg="#FFC107", fg="black",
                                     command=self.iniciar_draft, width=20, height=2,
                                     state=tk.DISABLED)
        self.btn_iniciar.pack(pady=10)
    
    # Guarda la formación seleccionada
    def seleccionar_formacion(self, jugador, formacion):
        if jugador == 1:
            self.formacion1 = formacion  # Guarda formación jugador 1
        else:
            self.formacion2 = formacion  # Guarda formación jugador 2
        
        # Actualiza el texto de formaciones seleccionadas
        texto = ""
        if self.formacion1:
            texto += f"🔵 {self.player1}: {self.formacion1}\n"
        if self.formacion2:
            texto += f"🔴 {self.player2}: {self.formacion2}"
        self.label_formaciones.config(text=texto)
        
        # Habilita botón de iniciar si ambos eligieron
        if self.formacion1 and self.formacion2:
            self.btn_iniciar.config(state=tk.NORMAL)
    
    # Genera los turnos del draft e inicia el juego
    def iniciar_draft(self):
        form1 = FORMACIONES[self.formacion1]  # Obtiene estructura formación 1
        form2 = FORMACIONES[self.formacion2]  # Obtiene estructura formación 2
        
        # Genera turnos por categoría
        categorias = ["POR", "DEF", "MC", "DEL"]
        self.turnos = []
        
        for cat in categorias:  # Para cada categoría
            turnos_cat = []  # Lista temporal de turnos de esta categoría
            max_picks = max(form1[cat], form2[cat])  # Máximo de picks en esta categoría
            
            # Crea turnos para cada pick
            for pick in range(max_picks):
                if pick < form1[cat]:  # Si jugador 1 necesita más
                    turnos_cat.append((1, cat))  # Añade turno jugador 1
                if pick < form2[cat]:  # Si jugador 2 necesita más
                    turnos_cat.append((2, cat))  # Añade turno jugador 2
            
            random.shuffle(turnos_cat)  # Mezcla turnos de esta categoría
            self.turnos.extend(turnos_cat)  # Añade a lista general de turnos
        
        self.turno_actual = 0  # Resetea contador de turnos
        self.pantalla_draft()  # Va a pantalla de draft
    
    # Pantalla principal del draft
    def pantalla_draft(self):
        self.limpiar_pantalla()  # Limpia la ventana
        
        # Si ya no hay más turnos, mostrar resultados
        if self.turno_actual >= len(self.turnos):
            self.pantalla_resultados()
            return
        
        jugador_num, categoria = self.turnos[self.turno_actual]  # Obtiene turno actual
        jugador_nombre = self.player1 if jugador_num == 1 else self.player2  # Nombre del jugador
        color = "#490C6C" if jugador_num == 1 else "#09737C"  # Color según jugador
        
        # Frame superior con información del turno
        frame_top = tk.Frame(self.root, bg=color)
        frame_top.pack(fill=tk.X, pady=10)
        
        # Muestra turno actual y jugador
        tk.Label(frame_top, text=f"Turno {self.turno_actual + 1}/{len(self.turnos)}", 
                font=("Arial", 12), bg=color, fg="white").pack()
        tk.Label(frame_top, text=f"🎯 Turno de: {jugador_nombre}", 
                font=("Arial", 16, "bold"), bg=color, fg="white").pack(pady=5)
        tk.Label(frame_top, text=f"Categoría: {categoria}", 
                font=("Arial", 14), bg=color, fg="white").pack()
        
        # Contador de jugadores seleccionados
        contador = tk.Frame(self.root, bg="#2E7D32")
        contador.pack(pady=5)
        tk.Label(contador, text=f"🔵 {self.player1}: {len(self.plantilla1)}/11", 
                font=("Arial", 12), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(contador, text=f"🔴 {self.player2}: {len(self.plantilla2)}/11", 
                font=("Arial", 12), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        
        # Frame con scroll para lista de jugadores
        frame_lista = tk.Frame(self.root, bg="#2E7D32")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas y scrollbar para scroll vertical
        canvas = tk.Canvas(frame_lista, bg="#2E7D32", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#2E7D32")
        
        # Configura el scroll
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Filtra jugadores disponibles por categoría
        jugadores_filtrados = [j for j in self.disponibles 
                              if obtener_categoria_posicion(j["posicion"]) == categoria]
        
        # Si no hay jugadores disponibles
        if not jugadores_filtrados:
            tk.Label(scrollable_frame, text="No hay jugadores disponibles", 
                    font=("Arial", 14), bg="#B30909", fg="white").pack(pady=20)
        else:
            # Crea botón para cada jugador disponible
            for jugador in jugadores_filtrados:
                # Frame para cada jugador
                frame_jugador = tk.Frame(scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
                frame_jugador.pack(fill=tk.X, padx=5, pady=3)
                
                # Información del jugador
                info_frame = tk.Frame(frame_jugador, bg="white")
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                
                tk.Label(info_frame, text=jugador["nombre"], 
                        font=("Arial", 12, "bold"), bg="white", anchor="w").pack(anchor="w")
                tk.Label(info_frame, text=f"{jugador['posicion']}", 
                        font=("Arial", 10), bg="white", fg="gray", anchor="w").pack(anchor="w")
                
                # Media del jugador con estrella
                media_frame = tk.Frame(frame_jugador, bg="white")
                media_frame.pack(side=tk.RIGHT, padx=10)
                
                tk.Label(media_frame, text="⭐", font=("Arial", 14), bg="white").pack(side=tk.LEFT)
                tk.Label(media_frame, text=str(jugador["media"]), 
                        font=("Arial", 16, "bold"), bg="white").pack(side=tk.LEFT)
                
                # Botón para seleccionar jugador
                tk.Button(frame_jugador, text="¡Lo Quiero!", bg="#4CAF50", fg="white",
                         font=("Arial", 10, "bold"), 
                         command=lambda j=jugador: self.seleccionar_jugador(j, jugador_num, categoria)
                         ).pack(side=tk.RIGHT, padx=10)
        
        # Empaqueta canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    # Selecciona un jugador en el draft
    def seleccionar_jugador(self, jugador, jugador_num, categoria):
        plantilla = self.plantilla1 if jugador_num == 1 else self.plantilla2  # Obtiene plantilla
        formacion = FORMACIONES[self.formacion1 if jugador_num == 1 else self.formacion2]  # Obtiene formación
        
        # Verifica límite de la categoría
        actuales = sum(1 for j in plantilla if obtener_categoria_posicion(j["posicion"]) == categoria)
        if actuales >= formacion[categoria]:
            messagebox.showwarning("Error", f"Ya tienes todos los {categoria} necesarios")
            return
        
        # Añade jugador a la plantilla correspondiente
        if jugador_num == 1:
            self.plantilla1.append(jugador)
        else:
            self.plantilla2.append(jugador)
        
        # Elimina jugador de disponibles
        self.disponibles.remove(jugador)
        
        # Avanza al siguiente turno
        self.turno_actual += 1
        self.pantalla_draft()
    
    # Pantalla de resultados finales
    def pantalla_resultados(self):
        self.limpiar_pantalla()  # Limpia la ventana
        
        # Calcula medias de ambos equipos
        media1 = calcular_media_equipo(self.plantilla1)
        media2 = calcular_media_equipo(self.plantilla2)
        
        # Determina ganador
        if media1 > media2:
            ganador = self.player1
            color_ganador = "#490C6C"
        elif media2 > media1:
            ganador = self.player2
            color_ganador = "#09737C"
        else:
            ganador = "¡Empate!"
            color_ganador = "#544310"
        
        # Frame superior con resultado
        frame_top = tk.Frame(self.root, bg=color_ganador)
        frame_top.pack(fill=tk.X, pady=10)
        
        tk.Label(frame_top, text="🏆 RESULTADOS FINALES 🏆", 
                font=("Arial", 20, "bold"), bg=color_ganador, fg="white").pack(pady=10)
        tk.Label(frame_top, text=f"¡{ganador}!", 
                font=("Arial", 18, "bold"), bg=color_ganador, fg="white").pack(pady=5)
        
        # Muestra medias de ambos equipos
        medias_frame = tk.Frame(self.root, bg="#2E7D32")
        medias_frame.pack(pady=10)
        
        tk.Label(medias_frame, text=f"🔵 {self.player1}: {media1:.2f}", 
                font=("Arial", 14, "bold"), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(medias_frame, text=f"🔴 {self.player2}: {media2:.2f}", 
                font=("Arial", 14, "bold"), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        
        # Frame con scroll para mostrar plantillas
        frame_plantillas = tk.Frame(self.root, bg="#2E7D32")
        frame_plantillas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame_plantillas, bg="#2E7D32", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_plantillas, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#2E7D32")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Muestra plantilla jugador 1
        self.mostrar_plantilla_gui(scrollable, self.player1, self.plantilla1, self.formacion1, "#1976D2")
        
        # Muestra plantilla jugador 2
        self.mostrar_plantilla_gui(scrollable, self.player2, self.plantilla2, self.formacion2, "#C62828")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botón para jugar de nuevo
        tk.Button(self.root, text="Jugar de Nuevo", font=("Arial", 14, "bold"),
                 bg="#FFC107", fg="black", command=self.reiniciar_juego,
                 width=20, height=2).pack(pady=10)
    
    # Muestra una plantilla en la interfaz
    def mostrar_plantilla_gui(self, parent, nombre, plantilla, formacion, color):
        frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=3)
        frame.pack(fill=tk.X, padx=5, pady=10)
        
        # Header con nombre y formación
        header = tk.Frame(frame, bg=color)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"{nombre} - {formacion}", 
                font=("Arial", 14, "bold"), bg=color, fg="white").pack(pady=8)
        
        # Agrupa jugadores por categoría
        categorias = ["POR", "DEF", "MC", "DEL"]
        for cat in categorias:
            jugadores_cat = [j for j in plantilla if obtener_categoria_posicion(j["posicion"]) == cat]
            if jugadores_cat:
                # Label de categoría
                tk.Label(frame, text=f"⚽ {cat}", font=("Arial", 12, "bold"), 
                        bg="white", anchor="w").pack(anchor="w", padx=10, pady=5)
                # Lista de jugadores de esta categoría
                for j in jugadores_cat:
                    tk.Label(frame, text=f"  • {j['nombre']} ({j['posicion']}) - ⭐{j['media']}", 
                            font=("Arial", 10), bg="white", anchor="w").pack(anchor="w", padx=20)
    
    # Reinicia el juego
    def reiniciar_juego(self):
        self.player1 = ""
        self.player2 = ""
        self.formacion1 = ""
        self.formacion2 = ""
        self.plantilla1 = []
        self.plantilla2 = []
        self.disponibles = JUGADORES.copy()
        self.turnos = []
        self.turno_actual = 0
        self.pantalla_nombres()  # Vuelve a pantalla inicial
    
    # Limpia todos los widgets de la ventana
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Inicia la aplicación
if __name__ == "__main__":
    root = tk.Tk()  # Crea ventana principal
    app = JuegoDraftGUI(root)  # Crea instancia del juego
    root.mainloop()  # Ejecuta el loop de la interfaz