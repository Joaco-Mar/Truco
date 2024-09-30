""""Este proyecto va a ser un intento de recrear el juego Argentino Truco"""

import random

def generarCartas(Mazo1, Mazo2):            #Genera las cartas de cada jugador sin que se repitan
    largo=0
    while largo<3:
        Numero=random.choice([i for i in range(1, 13) if i not in [8, 9]])       #Se elige un numero al azar entre 1 y 12, sin incluir el 8 y el 9
        Palo=random.choice(["Espada","Basto","Oro","Copa"])                      #Se elige un palo al azar
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

def main():
    ManoJugador={"Numero":[], "Palo":[]}
    ManoNPC={"Numero":[], "Palo":[]}
    ManoJugador=generarCartas(ManoJugador, ManoNPC)
    ManoNPC=generarCartas(ManoNPC, ManoJugador)
    lenght=len(ManoJugador["Numero"])
    print("Mano del Jugador:")
    for n in range(lenght):
        print(ManoJugador["Numero"][n],ManoJugador["Palo"][n])
    print("\nMano del NPC:")
    for n in range(lenght):
        print(ManoNPC["Numero"][n],ManoNPC["Palo"][n])



if __name__ == "__main__":
    main()