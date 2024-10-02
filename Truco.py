""""Este proyecto va a ser un intento de recrear el juego Argentino Truco"""

import random

def generarCartas(Mazo1, Mazo2):            #Genera las cartas de cada jugador sin que se repitan
    largo=0
    while largo<3:
        Numero=random.choice([i for i in range(1, 13) if i not in [8, 9]])       #Se elige un numero al azar entre 1 y 12, sin incluir el 8 y el 9
        Palo=random.choice(["⚔️","🪵","🪙","🍷"])                      #Se elige un palo al azar
        Mazo={"Numero":[Numero], "Palo":[Palo]}
        valido=True
        i=0
        while valido and i<len(Mazo1["Numero"]):                                               #Se verifica que la carta no este en la mano de ninguno de los jugadores
            if Numero == Mazo1["Numero"][i] and Palo == Mazo1["Palo"][i]:
                valido=False
            i+=1
        i=0
        while valido and i<len(Mazo2["Numero"]):                                               #Se verifica que la carta no este en la mano de ninguno de los jugadores
            if Numero == Mazo2["Numero"][i] and Palo == Mazo2["Palo"][i]:
                valido=False
            i+=1
        if valido:
            Mazo1["Numero"].append(Mazo["Numero"][0])
            Mazo1["Palo"].append(Mazo["Palo"][0])
            #print(Mazo["Numero"][0],Mazo["Palo"][0])                               imprime las cartas que se generan en vivo
            largo+=1
    return Mazo1

def jugar(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,ganadosJugador,ganadosNPC,parda):
    terminado=False
    try:
        def turnoJugador(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,envido):
            if mano == 1:
                envido = input("¿Quieres cantar envido? (S/N):").upper()
                if envido == "S":
                    eleccion=random.choice(["S", "N"])
                    if eleccion=="S":
                        print("El NPC🤖 aceptó el envido.")
                        puntajeJugador,puntajeNPC=envido(ManoJugador,ManoNPC,puntajeJugador,puntajeNPC,Arranca)
                    else:
                        print("El NPC🤖 NO acepto el envido.")
            carta = elegirCarta(ManoJugador)
            print("\nJugaste la carta:", ManoJugador["Numero"][carta-1], ManoJugador["Palo"][carta-1])
            return ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,envido,carta

        def turnoNPC(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,envido):
            if mano == 1 and envido != "S":
                envido = random.choice(["S", "N"])
                if envido == "S":
                    eleccion=(input("El NPC🤖 cantó envido, ¿Quieres aceptar? (S/N):"))
                    if eleccion=="S":
                        puntajeJugador,puntajeNPC=envido(ManoJugador,ManoNPC,puntajeJugador,puntajeNPC,Arranca)
            cartaNPC = random.choice([i for i in range(len(ManoNPC["Numero"]))])
            print("El NPC🤖 jugó la carta:", ManoNPC["Numero"][cartaNPC-1], ManoNPC["Palo"][cartaNPC-1])
            return ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,envido,cartaNPC

        envido = "N"

        if Arranca:  # Turno jugador primero
            print("\nTurno del Jugador")
            ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,envido,carta=turnoJugador(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,envido)
            print("\nTurno del NPC🤖")
            ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,envido,cartaNPC=turnoNPC(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,envido)
        else:  # Turno NPC primero
            print("\nTurno del NPC🤖")
            ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,envido,carta=turnoNPC(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,envido)
            print("\nTurno del Jugador")
            ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,envido,cartaNPC=turnoJugador(mano,ManoJugador, ManoNPC,Arranca,puntajeJugador,puntajeNPC,envido)
        
        if ManoJugador["Numero"][carta-1] > ManoNPC["Numero"][cartaNPC-1]:
            print("El Jugador gana la ronda")
            ganadosJugador+=1
            Arranca=True
        elif ManoJugador["Numero"][carta-1] < ManoNPC["Numero"][cartaNPC-1]:
            print("El NPC🤖 gana la ronda")
            ganadosNPC+=1
            Arranca=False
        else:
            print("Se empardó la mano")
            parda=True
            ganadosJugador+=1
            ganadosNPC+=1

        #FALTA CONSIDERAR SI EMPARDO DOS VECES SEGUIDAS
        if ganadosJugador==2:
            print("El Jugador gana la mano")
            puntajeJugador+=1
            terminado=True

        elif ganadosNPC==2:
            print("El NPC🤖 gana la mano")
            puntajeNPC+=1
            terminado=True

        ManoJugador["Numero"].pop(carta-1)
        ManoJugador["Palo"].pop(carta-1)
        ManoNPC["Numero"].pop(cartaNPC-1)
        ManoNPC["Palo"].pop(cartaNPC-1)

        return puntajeJugador, puntajeNPC,ganadosJugador,ganadosNPC,Arranca,parda,terminado
    
    except KeyboardInterrupt:
        print("\nGracias por jugar")
        print("\nPuntaje Jugador:", puntajeJugador)
        print("Puntaje NPC🤖:", puntajeNPC)
        exit()


def elegirCarta(Cartas):
    print("Ingrese la carta de quieres jugar 1 -",len(Cartas["Numero"]), ":",end="")
    carta=int(input())
    while carta<1 or carta>len(Cartas["Numero"]):
        print("Carta invalida, ingrese una carta", ":", end="")
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

def envido(ManoJugador, ManoNPC,puntajeJugador,puntajeNPC,arranca):
    envidoJugador = calcularEnvido(ManoJugador)
    envidoNPC = calcularEnvido(ManoNPC)
    print(f"\nPuntos de envido - Jugador: {envidoJugador}, NPC🤖: {envidoNPC}")
    
    if envidoJugador > envidoNPC or (envidoJugador == envidoNPC and arranca):
        print("El jugador gana el envido")
        puntajeJugador += 2
    elif envidoJugador < envidoNPC or (envidoJugador == envidoNPC and not arranca):
        print("El NPC🤖 gana el envido")
        puntajeNPC += 2
    return puntajeJugador, puntajeNPC


    

def main():
    puntajeJugador=0
    puntajeNPC=0
    mano=1
    modoAdmin=input("¿Desea jugar en modo administrador? (S/N):")
    terminado=True
    ganadosJugador=0
    ganadosNPC=0
    parda=False

    while puntajeJugador<15 and puntajeNPC<15:
        if terminado:
            arrancaJugador=random.choice([True,False])
            ManoJugador={"Numero":[], "Palo":[]}
            ManoNPC={"Numero":[], "Palo":[]}
            ganadosJugador=0
            ganadosNPC=0
            parda=False

            ManoJugador=generarCartas(ManoJugador, ManoNPC)
            ManoNPC=generarCartas(ManoNPC, ManoJugador)

            terminado=False

        lenght=len(ManoJugador["Numero"])
        print("Mano del Jugador:")
        for n in range(lenght):
            print(ManoJugador["Numero"][n],ManoJugador["Palo"][n])
        if modoAdmin=="S":
            print("\nMano del NPC🤖:")
            for n in range(lenght):
                print(ManoNPC["Numero"][n],ManoNPC["Palo"][n])            

        puntajeJugador, puntajeNPC,ganadosJugador,ganadosNPC,arrancaJugador,parda,terminado=jugar(mano,ManoJugador, ManoNPC,arrancaJugador,puntajeJugador,puntajeNPC,ganadosJugador,ganadosNPC,parda)

        print("\nPuntaje Jugador:", puntajeJugador)
        print("Puntaje NPC🤖:", puntajeNPC)
        mano+=1

if __name__ == "__main__":
    main()