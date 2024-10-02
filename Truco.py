""""Este proyecto va a ser un intento de recrear el juego Argentino Truco"""

import random
import time

# Función para imprimir texto lentamente
def imprimir_lento(texto, velocidad=0.02):
    for char in texto:
        print(char, end='', flush=True)
        time.sleep(velocidad)
    print()  # Para asegurar un salto de línea al final del texto

def generarCartas(Mazo1, Mazo2):  # Genera las cartas de cada jugador sin que se repitan
    largo = 0
    while largo < 3:
        Numero = random.choice([i for i in range(1, 13) if i not in [8, 9]])  # Se elige un numero al azar entre 1 y 12, sin incluir el 8 y el 9
        Palo = random.choice(["⚔️", "🪵", "🪙", "🍷"])  # Se elige un palo al azar
        Mazo = {"Numero": [Numero], "Palo": [Palo]}
        valido = True
        i = 0
        while valido and i < len(Mazo1["Numero"]):  # Se verifica que la carta no este en la mano de ninguno de los jugadores
            if Numero == Mazo1["Numero"][i] and Palo == Mazo1["Palo"][i]:
                valido = False
            i += 1
        i = 0
        while valido and i < len(Mazo2["Numero"]):  # Se verifica que la carta no este en la mano de ninguno de los jugadores
            if Numero == Mazo2["Numero"][i] and Palo == Mazo2["Palo"][i]:
                valido = False
            i += 1
        if valido:
            Mazo1["Numero"].append(Mazo["Numero"][0])
            Mazo1["Palo"].append(Mazo["Palo"][0])
            largo += 1
    return Mazo1

def jugar(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, ganadosJugador, ganadosNPC, parda):
    terminado = False
    try:
        def turnoJugador(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, envido):
            if mano == 1 and envido != "S":
                imprimir_lento("¿Quieres cantar envido? (S/N):")
                envido = input().upper()
                if envido == "S":
                    eleccion = random.choice(["S", "N"])
                    if eleccion == "S":
                        imprimir_lento("El NPC🤖 aceptó el envido.")
                        puntajeJugador, puntajeNPC = envidoFunc(ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, Arranca)
                    else:
                        imprimir_lento("El NPC🤖 NO acepto el envido.")
            carta = elegirCarta(ManoJugador)
            imprimir_lento(f"\nJugaste la carta: {ManoJugador['Numero'][carta - 1]} {ManoJugador['Palo'][carta - 1]}")
            return ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, envido, carta

        def turnoNPC(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, envido):
            if mano == 1 and envido != "S":
                envido = random.choice(["S", "N"])
                if envido == "S":
                    imprimir_lento(f"El NPC🤖 cantó envido, ¿Quieres aceptar? (S/N):")
                    eleccion = input()
                    if eleccion == "S":
                        puntajeJugador, puntajeNPC = envidoFunc(ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, Arranca)
            cartaNPC = random.choice([i for i in range(len(ManoNPC["Numero"]))])
            imprimir_lento(f"El NPC🤖 jugó la carta: {ManoNPC['Numero'][cartaNPC - 1]} {ManoNPC['Palo'][cartaNPC - 1]}")
            return ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, envido, cartaNPC

        envido = "N"

        if Arranca:  # Turno jugador primero
            imprimir_lento("\nTurno del Jugador")
            ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, envido, carta = turnoJugador(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, envido)
            imprimir_lento("\nTurno del NPC🤖")
            ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, envido, cartaNPC = turnoNPC(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, envido)
        else:  # Turno NPC primero
            imprimir_lento("\nTurno del NPC🤖")
            ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, envido, carta = turnoNPC(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, envido)
            imprimir_lento("\nTurno del Jugador")
            ManoJugador, ManoNPC, puntajeJugador, puntajeNPC, envido, cartaNPC = turnoJugador(mano, ManoJugador, ManoNPC, Arranca, puntajeJugador, puntajeNPC, envido)

        valorJugador = valorCarta({"Numero": ManoJugador["Numero"][carta - 1], "Palo": ManoJugador["Palo"][carta - 1]})
        valorNPC = valorCarta({"Numero": ManoNPC["Numero"][cartaNPC - 1], "Palo": ManoNPC["Palo"][cartaNPC - 1]})

        if valorJugador > valorNPC:
            imprimir_lento("El Jugador gana la ronda\n")
            ganadosJugador += 1
            Arranca = True
        elif valorJugador < valorNPC:
            imprimir_lento("El NPC🤖 gana la ronda\n")
            ganadosNPC += 1
            Arranca = False
        else:
            imprimir_lento("Se empardó la ronda\n")
            parda = True
            ganadosJugador += 1
            ganadosNPC += 1

        if ganadosJugador == 2:
            imprimir_lento("El Jugador gana la mano\n")
            puntajeJugador += 1
            terminado = True

        elif ganadosNPC == 2:
            imprimir_lento("El NPC🤖 gana la mano\n")
            puntajeNPC += 1
            terminado = True

        ManoJugador["Numero"].pop(carta - 1)
        ManoJugador["Palo"].pop(carta - 1)
        ManoNPC["Numero"].pop(cartaNPC - 1)
        ManoNPC["Palo"].pop(cartaNPC - 1)

        return puntajeJugador, puntajeNPC, ganadosJugador, ganadosNPC, Arranca, parda, terminado

    except KeyboardInterrupt:
        imprimir_lento("\nGracias por jugar")
        imprimir_lento(f"\nPuntaje Jugador: {puntajeJugador}")
        imprimir_lento(f"Puntaje NPC🤖: {puntajeNPC}")
        exit()

    except ValueError:
        imprimir_lento("Ingresa bien los valores plis.")

def elegirCarta(Cartas):
    imprimir_lento(f"Ingrese la carta de quieres jugar 1 -{len(Cartas["Numero"])}")
    carta=int(input())
    while carta<1 or carta>len(Cartas["Numero"]):
        imprimir_lento("Carta invalida, ingrese una carta:")
        carta=int(input())
    return carta

def calcularEnvido(Mano):
    # Diccionario con los valores de las cartas para el envido
    valores_envido = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 10: 0, 11: 0, 12: 0}
    
    # Separar las cartas por palos
    palos = {}
    for i in range(len(Mano["Numero"])):
        palo = Mano["Palo"][i]
        numero = Mano["Numero"][i]
        if palo not in palos:
            palos[palo] = []
        palos[palo].append(valores_envido[numero])

    # Calcular el envido (dos cartas del mismo palo suman 20 + el valor de las cartas)
    max_envido = 0
    for palo, valores in palos.items():
        if len(valores) > 1:  # Si hay al menos dos cartas del mismo palo
            valores.sort(reverse=True)
            envido_palo = 20 + valores[0] + valores[1]
        else:  # Si solo hay una carta de ese palo
            envido_palo = valores[0]
        max_envido = max(max_envido, envido_palo)
    
    return max_envido

def envidoFunc(ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,arranca):
    envidoJugador = calcularEnvido(ManoJugador)
    envidoNPC = calcularEnvido(ManoNPC)
    print(f"\nPuntos de envido - Jugador: {envidoJugador}, NPC🤖: {envidoNPC}")
    
    if envidoJugador > envidoNPC or (envidoJugador == envidoNPC and arranca):
        imprimir_lento("El jugador gana el envido\n")
        puntajeJugador += 2
    elif envidoJugador < envidoNPC or (envidoJugador == envidoNPC and not arranca):
        imprimir_lento("El NPC🤖 gana el envido\n")
        puntajeNPC += 2
    return puntajeJugador, puntajeNPC

def valorCarta(carta):
    numero = carta["Numero"]
    palo = carta["Palo"]

    # Definimos los valores de las cartas según las reglas del Truco
    valores = {
        "⚔️": {
            1:14,
            7:12,
            3:10,
            2:9,
            12:7,
            11:6,
            10:5,
            6:3,
            5:2,
            4:1,

        }, 
        "🪵": {
            1:13,
            3:10,
            2:9,
            12:7,
            11:6,
            10:5,
            7:4,
            6:3,
            5:2,
            4:1,
        }, 
        "🪙":{
            7:11,
            3:10,
            2:9,
            1:8,
            12:7,
            11:6,
            10:5,
            6:3,
            5:2,
            4:1,

        }, 
        "🍷":{
            3:10,
            2:9,
            1:8,
            12:7,
            11:6,
            10:5,
            7:4,
            6:3,
            5:2,
            4:1,
        }
    }
    return valores.get(palo, {}).get(numero, 0)  # Retornamos 0 para cartas no válidas

    

def main():
    puntajeJugador=0
    puntajeNPC=0
    mano=1
    modoAdmin=input("¿Desea jugar en modo administrador? (S/N):")
    terminado=True
    ganadosJugador=0
    ganadosNPC=0
    parda=False
    arrancaJugador=random.choice([True,False])

    while puntajeJugador<15 and puntajeNPC<15:
        if terminado:
            arrancaJugador=random.choice([True,False])
            ManoJugador={"Numero":[], "Palo":[]}
            ManoNPC={"Numero":[], "Palo":[]}
            ganadosJugador=0
            ganadosNPC=0
            parda=False
            mano=1

            ManoJugador=generarCartas(ManoJugador, ManoNPC)
            ManoNPC=generarCartas(ManoNPC, ManoJugador)

            imprimir_lento(f"\nPuntaje Jugador: {puntajeJugador}")
            imprimir_lento(f"Puntaje NPC🤖: {puntajeNPC}\n")

            terminado=False

        lenght=len(ManoJugador["Numero"])
        imprimir_lento("Mano del Jugador:")
        for n in range(lenght):
            imprimir_lento(f"{ManoJugador["Numero"][n]}{ManoJugador["Palo"][n]}")
        if modoAdmin=="S":
            imprimir_lento("\nMano del NPC🤖:")
            for n in range(lenght):
                imprimir_lento(f"{ManoNPC["Numero"][n]}{ManoNPC["Palo"][n]}")       

        puntajeJugador, puntajeNPC,ganadosJugador,ganadosNPC,arrancaJugador,parda,terminado=jugar(mano,ManoJugador, ManoNPC,arrancaJugador,puntajeJugador,puntajeNPC,ganadosJugador,ganadosNPC,parda)
        mano+=1

if __name__ == "__main__":
    main()