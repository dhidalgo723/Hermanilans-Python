import random
import tkinter as tk
from tkinter import messagebox, simpledialog

# mini base de datos de jugadores
JUGADORES = [
    # porteros
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

# diccionario de formaciones disponibles
FORMACIONES = {
    "4-3-3": {"POR": 1, "DEF": 4, "MC": 3, "DEL": 3},
    "4-4-2": {"POR": 1, "DEF": 4, "MC": 4, "DEL": 2},
}

# convierte posicion especifica a categoria general
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

# calcula la media del equipo
def calcular_media_equipo(plantilla):
    if len(plantilla) == 0:
        return 0
    return sum(j["media"] for j in plantilla) / len(plantilla)

# clase principal del juego con interfaz grafica
class JuegoDraftGUI:
    def __init__(self, root):
        self.root = root  # ventana principal
        self.root.title("Draft Futbolistico")  # titulo de la ventana
        
        # pone la ventana en pantalla completa
        self.root.state('zoomed')  # windows
        # si estas en linux o mac usa: self.root.attributes('-zoomed', True)
        
        self.root.configure(bg="#2E7D32")  # color de fondo verde
        
        # variables del juego
        self.player1 = ""  # nombre del jugador 1
        self.player2 = ""  # nombre del jugador 2
        self.formacion1 = ""  # formacion elegida por jugador 1
        self.formacion2 = ""  # formacion elegida por jugador 2
        self.plantilla1 = []  # lista de jugadores del equipo 1
        self.plantilla2 = []  # lista de jugadores del equipo 2
        self.disponibles = JUGADORES.copy()  # copia de jugadores disponibles
        self.turnos = []  # lista de turnos del draft
        self.turno_actual = 0  # indice del turno actual
        
        # variables para navegacion con teclado
        self.jugadores_frames = []  # lista de frames de jugadores
        self.indice_seleccionado = 0  # indice del jugador seleccionado con teclado
        
        # inicia con la pantalla de nombres
        self.pantalla_nombres()
    
    # pantalla inicial para ingresar nombres
    def pantalla_nombres(self):
        self.limpiar_pantalla()  # limpia la ventana
        
        # frame contenedor principal
        frame = tk.Frame(self.root, bg="#2E7D32")
        frame.pack(expand=True)
        
        # titulo del juego
        tk.Label(frame, text="🏆 DRAFT FUTBOLISTICO 🏆", 
                font=("Arial", 32, "bold"), bg="#2E7D32", fg="white").pack(pady=30)
        
        # label para jugador 1
        tk.Label(frame, text="Nombre del Jugador 1:", 
                font=("Arial", 18), bg="#2E7D32", fg="white").pack(pady=5)
        # campo de entrada para nombre jugador 1
        self.entry_player1 = tk.Entry(frame, font=("Arial", 18), width=30)
        self.entry_player1.pack(pady=5)
        
        # label para jugador 2
        tk.Label(frame, text="Nombre del Jugador 2:", 
                font=("Arial", 18), bg="#2E7D32", fg="white").pack(pady=5)
        # campo de entrada para nombre jugador 2
        self.entry_player2 = tk.Entry(frame, font=("Arial", 18), width=30)
        self.entry_player2.pack(pady=5)
        
        # boton para continuar
        tk.Button(frame, text="Continuar", font=("Arial", 18, "bold"),
                 bg="#FFC107", fg="black", command=self.guardar_nombres,
                 width=20, height=2).pack(pady=40)
    
    # guarda los nombres y va a seleccion de formaciones
    def guardar_nombres(self):
        self.player1 = self.entry_player1.get().strip()  # obtiene nombre jugador 1
        self.player2 = self.entry_player2.get().strip()  # obtiene nombre jugador 2
        
        # valida que ambos nombres esten completos
        if not self.player1 or not self.player2:
            messagebox.showwarning("Error", "Ambos jugadores deben ingresar su nombre")
            return
        
        self.pantalla_formaciones()  # va a siguiente pantalla
    
    # pantalla de seleccion de formaciones
    def pantalla_formaciones(self):
        self.limpiar_pantalla()  # limpia la ventana
        
        # frame contenedor
        frame = tk.Frame(self.root, bg="#2E7D32")
        frame.pack(expand=True)
        
        # titulo
        tk.Label(frame, text="Seleccion de Formaciones", 
                font=("Arial", 28, "bold"), bg="#2E7D32", fg="white").pack(pady=30)
        
        # seccion jugador 1
        tk.Label(frame, text=f"🔵 {self.player1}", 
                font=("Arial", 20, "bold"), bg="#2E7D32", fg="#64B5F6").pack(pady=15)
        
        # frame para botones de formacion jugador 1
        frame_form1 = tk.Frame(frame, bg="#2E7D32")
        frame_form1.pack(pady=10)
        
        # boton 4-3-3 para jugador 1
        tk.Button(frame_form1, text="4-3-3\n1 POR • 4 DEF • 3 MC • 3 DEL", 
                 font=("Arial", 16), bg="#1976D2", fg="white",
                 command=lambda: self.seleccionar_formacion(1, "4-3-3"),
                 width=30, height=4).pack(side=tk.LEFT, padx=10)
        
        # boton 4-4-2 para jugador 1
        tk.Button(frame_form1, text="4-4-2\n1 POR • 4 DEF • 4 MC • 2 DEL", 
                 font=("Arial", 16), bg="#1976D2", fg="white",
                 command=lambda: self.seleccionar_formacion(1, "4-4-2"),
                 width=30, height=4).pack(side=tk.LEFT, padx=10)
        
        # seccion jugador 2
        tk.Label(frame, text=f"🔴 {self.player2}", 
                font=("Arial", 20, "bold"), bg="#2E7D32", fg="#EF5350").pack(pady=15)
        
        # frame para botones de formacion jugador 2
        frame_form2 = tk.Frame(frame, bg="#2E7D32")
        frame_form2.pack(pady=10)
        
        # boton 4-3-3 para jugador 2
        tk.Button(frame_form2, text="4-3-3\n1 POR • 4 DEF • 3 MC • 3 DEL", 
                 font=("Arial", 16), bg="#C62828", fg="white",
                 command=lambda: self.seleccionar_formacion(2, "4-3-3"),
                 width=30, height=4).pack(side=tk.LEFT, padx=10)
        
        # boton 4-4-2 para jugador 2
        tk.Button(frame_form2, text="4-4-2\n1 POR • 4 DEF • 4 MC • 2 DEL", 
                 font=("Arial", 16), bg="#C62828", fg="white",
                 command=lambda: self.seleccionar_formacion(2, "4-4-2"),
                 width=30, height=4).pack(side=tk.LEFT, padx=10)
        
        # label para mostrar formaciones seleccionadas
        self.label_formaciones = tk.Label(frame, text="", 
                                         font=("Arial", 16), bg="#2E7D32", fg="white")
        self.label_formaciones.pack(pady=25)
        
        # boton para iniciar draft (deshabilitado inicialmente)
        self.btn_iniciar = tk.Button(frame, text="¡Iniciar Draft!", 
                                     font=("Arial", 18, "bold"), bg="#FFC107", fg="black",
                                     command=self.iniciar_draft, width=25, height=3,
                                     state=tk.DISABLED)
        self.btn_iniciar.pack(pady=15)
    
    # guarda la formacion seleccionada
    def seleccionar_formacion(self, jugador, formacion):
        if jugador == 1:
            self.formacion1 = formacion  # guarda formacion jugador 1
        else:
            self.formacion2 = formacion  # guarda formacion jugador 2
        
        # actualiza el texto de formaciones seleccionadas
        texto = ""
        if self.formacion1:
            texto += f"🔵 {self.player1}: {self.formacion1}\n"
        if self.formacion2:
            texto += f"🔴 {self.player2}: {self.formacion2}"
        self.label_formaciones.config(text=texto)
        
        # habilita boton de iniciar si ambos eligieron
        if self.formacion1 and self.formacion2:
            self.btn_iniciar.config(state=tk.NORMAL)
    
    # genera los turnos del draft e inicia el juego
    def iniciar_draft(self):
        form1 = FORMACIONES[self.formacion1]  # obtiene estructura formacion 1
        form2 = FORMACIONES[self.formacion2]  # obtiene estructura formacion 2
        
        # genera turnos por categoria
        categorias = ["POR", "DEF", "MC", "DEL"]
        self.turnos = []
        
        for cat in categorias:  # para cada categoria
            turnos_cat = []  # lista temporal de turnos de esta categoria
            max_picks = max(form1[cat], form2[cat])  # maximo de picks en esta categoria
            
            # crea turnos para cada pick
            for pick in range(max_picks):
                if pick < form1[cat]:  # si jugador 1 necesita mas
                    turnos_cat.append((1, cat))  # añade turno jugador 1
                if pick < form2[cat]:  # si jugador 2 necesita mas
                    turnos_cat.append((2, cat))  # añade turno jugador 2
            
            random.shuffle(turnos_cat)  # mezcla turnos de esta categoria
            self.turnos.extend(turnos_cat)  # añade a lista general de turnos
        
        self.turno_actual = 0  # resetea contador de turnos
        self.pantalla_draft()  # va a pantalla de draft
    
    # pantalla principal del draft
    def pantalla_draft(self):
        self.limpiar_pantalla()  # limpia la ventana
        
        # si ya no hay mas turnos, mostrar resultados
        if self.turno_actual >= len(self.turnos):
            self.pantalla_resultados()
            return
        
        jugador_num, categoria = self.turnos[self.turno_actual]  # obtiene turno actual
        jugador_nombre = self.player1 if jugador_num == 1 else self.player2  # nombre del jugador
        color = "#490C6C" if jugador_num == 1 else "#09737C"  # color segun jugador
        
        # frame superior con informacion del turno
        frame_top = tk.Frame(self.root, bg=color)
        frame_top.pack(fill=tk.X, pady=10)
        
        # muestra turno actual y jugador
        tk.Label(frame_top, text=f"Turno {self.turno_actual + 1}/{len(self.turnos)}", 
                font=("Arial", 14), bg=color, fg="white").pack()
        tk.Label(frame_top, text=f"🎯 Turno de: {jugador_nombre}", 
                font=("Arial", 20, "bold"), bg=color, fg="white").pack(pady=5)
        tk.Label(frame_top, text=f"Categoria: {categoria}", 
                font=("Arial", 16), bg=color, fg="white").pack()
        
        # contador de jugadores seleccionados
        contador = tk.Frame(self.root, bg="#2E7D32")
        contador.pack(pady=5)
        tk.Label(contador, text=f"🔵 {self.player1}: {len(self.plantilla1)}/11", 
                font=("Arial", 14), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(contador, text=f"🔴 {self.player2}: {len(self.plantilla2)}/11", 
                font=("Arial", 14), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        
        # barra de busqueda centrada
        frame_busqueda = tk.Frame(self.root, bg="#2E7D32")
        frame_busqueda.pack(pady=10)
        
        # contenedor interno para centrar
        busqueda_centro = tk.Frame(frame_busqueda, bg="#2E7D32")
        busqueda_centro.pack()
        
        tk.Label(busqueda_centro, text="🔍 Buscar jugador:", 
                font=("Arial", 14), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=5)
        
        # campo de entrada para busqueda
        self.entry_busqueda = tk.Entry(busqueda_centro, font=("Arial", 14), width=30)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        # cuando escribe en la busqueda, actualiza la lista
        self.entry_busqueda.bind('<KeyRelease>', lambda e: self.actualizar_lista_jugadores(jugador_num, categoria))
        
        # frame con scroll para lista de jugadores
        frame_lista = tk.Frame(self.root, bg="#2E7D32")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # canvas y scrollbar para scroll vertical
        self.canvas = tk.Canvas(frame_lista, bg="#2E7D32", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2E7D32")
        
        # configura el scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # habilita scroll con la rueda del mouse
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # windows
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)  # linux scroll arriba
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)  # linux scroll abajo
        
        # guarda datos del turno para usar en navegacion con teclado
        self.jugador_num_actual = jugador_num
        self.categoria_actual = categoria
        
        # actualiza la lista de jugadores
        self.actualizar_lista_jugadores(jugador_num, categoria)
        
        # empaqueta canvas y scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # vincula las teclas de navegacion
        self.root.bind('<Up>', self.mover_seleccion_arriba)
        self.root.bind('<Down>', self.mover_seleccion_abajo)
        self.root.bind('<Return>', self.seleccionar_con_enter)
    
    # funcion para scroll con la rueda del mouse
    def _on_mousewheel(self, event):
        # windows y macos
        if event.num == 4 or event.delta > 0:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            self.canvas.yview_scroll(1, "units")
    
    # actualiza la lista de jugadores segun la busqueda
    def actualizar_lista_jugadores(self, jugador_num, categoria):
        # limpia los frames anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # obtiene el texto de busqueda
        texto_busqueda = self.entry_busqueda.get().lower().strip()
        
        # filtra jugadores disponibles por categoria
        jugadores_filtrados = [j for j in self.disponibles 
                              if obtener_categoria_posicion(j["posicion"]) == categoria]
        
        # si hay texto de busqueda, filtra por nombre
        if texto_busqueda:
            jugadores_filtrados = [j for j in jugadores_filtrados 
                                  if texto_busqueda in j["nombre"].lower()]
        
        # reinicia la lista de frames y el indice
        self.jugadores_frames = []
        self.indice_seleccionado = 0
        
        # si no hay jugadores disponibles
        if not jugadores_filtrados:
            tk.Label(self.scrollable_frame, text="No hay jugadores disponibles", 
                    font=("Arial", 16), bg="#B30909", fg="white").pack(pady=20)
        else:
            # crea boton para cada jugador disponible
            for idx, jugador in enumerate(jugadores_filtrados):
                # frame para cada jugador
                frame_jugador = tk.Frame(self.scrollable_frame, bg="white", relief=tk.RAISED, bd=2)
                frame_jugador.pack(fill=tk.X, padx=5, pady=3)
                
                # guarda el frame y el jugador
                self.jugadores_frames.append({
                    'frame': frame_jugador,
                    'jugador': jugador
                })
                
                # informacion del jugador
                info_frame = tk.Frame(frame_jugador, bg="white")
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=8)
                
                tk.Label(info_frame, text=jugador["nombre"], 
                        font=("Arial", 14, "bold"), bg="white", anchor="w").pack(anchor="w")
                tk.Label(info_frame, text=f"{jugador['posicion']}", 
                        font=("Arial", 12), bg="white", fg="gray", anchor="w").pack(anchor="w")
                
                # media del jugador con estrella
                media_frame = tk.Frame(frame_jugador, bg="white")
                media_frame.pack(side=tk.RIGHT, padx=10)
                
                tk.Label(media_frame, text="⭐", font=("Arial", 16), bg="white").pack(side=tk.LEFT)
                tk.Label(media_frame, text=str(jugador["media"]), 
                        font=("Arial", 18, "bold"), bg="white").pack(side=tk.LEFT)
                
                # boton para seleccionar jugador
                tk.Button(frame_jugador, text="¡Lo Quiero!", bg="#4CAF50", fg="white",
                         font=("Arial", 12, "bold"), 
                         command=lambda j=jugador: self.seleccionar_jugador(j, jugador_num, categoria)
                         ).pack(side=tk.RIGHT, padx=10)
            
            # resalta el primer jugador
            if self.jugadores_frames:
                self.resaltar_jugador(0)
    
    # resalta el jugador seleccionado con teclado
    def resaltar_jugador(self, indice):
        # quita el resaltado de todos
        for item in self.jugadores_frames:
            item['frame'].configure(bg="white", bd=2)
        
        # resalta el jugador actual
        if 0 <= indice < len(self.jugadores_frames):
            self.jugadores_frames[indice]['frame'].configure(bg="#FFE082", bd=4)
            
            # hace scroll automatico para que el jugador seleccionado sea visible
            self.canvas.yview_moveto(indice / len(self.jugadores_frames))
    
    # mueve la seleccion hacia arriba con flecha arriba
    def mover_seleccion_arriba(self, event):
        if self.jugadores_frames and self.indice_seleccionado > 0:
            self.indice_seleccionado -= 1
            self.resaltar_jugador(self.indice_seleccionado)
    
    # mueve la seleccion hacia abajo con flecha abajo
    def mover_seleccion_abajo(self, event):
        if self.jugadores_frames and self.indice_seleccionado < len(self.jugadores_frames) - 1:
            self.indice_seleccionado += 1
            self.resaltar_jugador(self.indice_seleccionado)
    
    # selecciona el jugador resaltado con enter
    def seleccionar_con_enter(self, event):
        if self.jugadores_frames and 0 <= self.indice_seleccionado < len(self.jugadores_frames):
            jugador = self.jugadores_frames[self.indice_seleccionado]['jugador']
            self.seleccionar_jugador(jugador, self.jugador_num_actual, self.categoria_actual)
    
    # selecciona un jugador en el draft
    def seleccionar_jugador(self, jugador, jugador_num, categoria):
        plantilla = self.plantilla1 if jugador_num == 1 else self.plantilla2  # obtiene plantilla
        formacion = FORMACIONES[self.formacion1 if jugador_num == 1 else self.formacion2]  # obtiene formacion
        
        # verifica limite de la categoria
        actuales = sum(1 for j in plantilla if obtener_categoria_posicion(j["posicion"]) == categoria)
        if actuales >= formacion[categoria]:
            messagebox.showwarning("Error", f"Ya tienes todos los {categoria} necesarios")
            return
        
        # añade jugador a la plantilla correspondiente
        if jugador_num == 1:
            self.plantilla1.append(jugador)
        else:
            self.plantilla2.append(jugador)
        
        # elimina jugador de disponibles
        self.disponibles.remove(jugador)
        
        # avanza al siguiente turno
        self.turno_actual += 1
        
        # desvincula eventos del teclado antes de cambiar de pantalla
        self.root.unbind('<Up>')
        self.root.unbind('<Down>')
        self.root.unbind('<Return>')
        
        self.pantalla_draft()
    
    # pantalla de resultados finales
    def pantalla_resultados(self):
        self.limpiar_pantalla()  # limpia la ventana
        
        # desvincula eventos del mouse
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")
        
        # calcula medias de ambos equipos
        media1 = calcular_media_equipo(self.plantilla1)
        media2 = calcular_media_equipo(self.plantilla2)
        
        # determina ganador
        if media1 > media2:
            ganador = self.player1
            color_ganador = "#490C6C"
        elif media2 > media1:
            ganador = self.player2
            color_ganador = "#09737C"
        else:
            ganador = "¡Empate!"
            color_ganador = "#544310"
        
        # frame superior con resultado
        frame_top = tk.Frame(self.root, bg=color_ganador)
        frame_top.pack(fill=tk.X, pady=10)
        
        tk.Label(frame_top, text="🏆 RESULTADOS FINALES 🏆", 
                font=("Arial", 28, "bold"), bg=color_ganador, fg="white").pack(pady=10)
        tk.Label(frame_top, text=f"¡{ganador}!", 
                font=("Arial", 24, "bold"), bg=color_ganador, fg="white").pack(pady=5)
        
        # muestra medias de ambos equipos
        medias_frame = tk.Frame(self.root, bg="#2E7D32")
        medias_frame.pack(pady=10)
        
        tk.Label(medias_frame, text=f"🔵 {self.player1}: {media1:.2f}", 
                font=("Arial", 18, "bold"), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        tk.Label(medias_frame, text=f"🔴 {self.player2}: {media2:.2f}", 
                font=("Arial", 18, "bold"), bg="#2E7D32", fg="white").pack(side=tk.LEFT, padx=20)
        
        # frame con scroll para mostrar plantillas
        frame_plantillas = tk.Frame(self.root, bg="#2E7D32")
        frame_plantillas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(frame_plantillas, bg="#2E7D32", highlightthickness=0)
        scrollbar = tk.Scrollbar(frame_plantillas, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas, bg="#2E7D32")
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # habilita scroll con la rueda del mouse en resultados
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # muestra plantilla jugador 1
        self.mostrar_plantilla_gui(scrollable, self.player1, self.plantilla1, self.formacion1, "#1976D2")
        
        # muestra plantilla jugador 2
        self.mostrar_plantilla_gui(scrollable, self.player2, self.plantilla2, self.formacion2, "#C62828")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # boton para jugar de nuevo
        tk.Button(self.root, text="Jugar de Nuevo", font=("Arial", 18, "bold"),
                 bg="#FFC107", fg="black", command=self.reiniciar_juego,
                 width=25, height=3).pack(pady=15)
    
    # muestra una plantilla en la interfaz
    def mostrar_plantilla_gui(self, parent, nombre, plantilla, formacion, color):
        frame = tk.Frame(parent, bg="white", relief=tk.RAISED, bd=3)
        frame.pack(fill=tk.X, padx=5, pady=10)
        
        # header con nombre y formacion
        header = tk.Frame(frame, bg=color)
        header.pack(fill=tk.X)
        tk.Label(header, text=f"{nombre} - {formacion}", 
                font=("Arial", 18, "bold"), bg=color, fg="white").pack(pady=10)
        
        # agrupa jugadores por categoria
        categorias = ["POR", "DEF", "MC", "DEL"]
        for cat in categorias:
            jugadores_cat = [j for j in plantilla if obtener_categoria_posicion(j["posicion"]) == cat]
            if jugadores_cat:
                # label de categoria
                tk.Label(frame, text=f"⚽ {cat}", font=("Arial", 14, "bold"), 
                        bg="white", anchor="w").pack(anchor="w", padx=10, pady=5)
                # lista de jugadores de esta categoria
                for j in jugadores_cat:
                    tk.Label(frame, text=f"  • {j['nombre']} ({j['posicion']}) - ⭐{j['media']}", 
                            font=("Arial", 12), bg="white", anchor="w").pack(anchor="w", padx=20)
    
    # reinicia el juego
    def reiniciar_juego(self):
        # desvincula todos los eventos del mouse
        try:
            self.canvas.unbind_all("<MouseWheel>")
            self.canvas.unbind_all("<Button-4>")
            self.canvas.unbind_all("<Button-5>")
        except:
            pass
        
        self.player1 = ""
        self.player2 = ""
        self.formacion1 = ""
        self.formacion2 = ""
        self.plantilla1 = []
        self.plantilla2 = []
        self.disponibles = JUGADORES.copy()
        self.turnos = []
        self.turno_actual = 0
        self.jugadores_frames = []
        self.indice_seleccionado = 0
        self.pantalla_nombres()  # vuelve a pantalla inicial
    
    # limpia todos los widgets de la ventana
    def limpiar_pantalla(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# inicia la aplicacion
if __name__ == "__main__":
    root = tk.Tk()  # crea ventana principal
    app = JuegoDraftGUI(root)  # crea instancia del juego
    root.mainloop()  # ejecuta el loop de la interfaz