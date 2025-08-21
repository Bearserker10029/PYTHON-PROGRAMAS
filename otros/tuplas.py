if __name__ == "__main__":
    # Tupla de días de la semana
    días=[(1,"lunes"),(2,"martes"),(3,"miércoles"),(4,"jueves"),(5,"viernes"),(6,"sábado"),(7,"domingo")]

    día=int(input("Ingrese el día: "))

    if día < 1 or día > 7:
        print("Día inválido")
    else:
        print("El día es:", días[día-1][1])