import time
import os

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def es_capicua(n):
    s = str(n)
    return s == s[::-1]

def es_feliz(n, max_iter=100):
    def suma_cuadrados_digitos(x):
        return sum(int(d)**2 for d in str(x))
    
    visitados = set()
    while n != 1 and max_iter > 0:
        n = suma_cuadrados_digitos(n)
        if n in visitados:
            return False
        visitados.add(n)
        max_iter -= 1
    return n == 1

def main():
    # Asegúrate de que exista el archivo de origen
    input_file = "/app-data/numbers.txt"
    output_file = "/app-data/classified.txt"

    # Creamos el archivo de salida, si no existe
    if not os.path.exists(output_file):
        open(output_file, "w").close()

    # Llevaremos un marcador para saber cuál fue la última línea procesada
    last_position = 0

    while True:
        # Abrimos el archivo en modo lectura
        with open(input_file, "r") as f_in:
            # Movemos el cursor a la última posición leída
            f_in.seek(last_position)

            # Leemos nuevas líneas (nuevos números)
            lines = f_in.readlines()

            # Actualizamos la posición (para la próxima iteración)
            last_position = f_in.tell()

        # Procesamos cada número nuevo
        if lines:
            with open(output_file, "a") as f_out:
                for line in lines:
                    line = line.strip()
                    if line.isdigit():
                        num = int(line)
                        # Clasificación
                        primo = es_primo(num)
                        capicua = es_capicua(num)
                        feliz = es_feliz(num)
                        # Escribimos el resultado en el output_file
                        # Formato: num, primo, capicua, feliz
                        f_out.write(f"{num},{primo},{capicua},{feliz}\n")

        # Espera un segundo antes de revisar nuevas líneas
        time.sleep(1)

if __name__ == "__main__":
    main()
