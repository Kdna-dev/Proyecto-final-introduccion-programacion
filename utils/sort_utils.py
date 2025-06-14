def ordenar_por_nombre_y_nota(detalle_alumnos):
    n = len(detalle_alumnos)

    # Ordenamos usando el algoritmo de burbuja
    for i in range(n):
        for j in range(0, n - i - 1):
            # Compara primero por nombre (alumno[0]) y luego por la nota final (alumno[5])
            # Convertimos el nombre a minúsculas para una comparación insensible a mayúsculas
            nombre_1 = detalle_alumnos[j][0].lower()
            nombre_2 = detalle_alumnos[j + 1][0].lower()
            nota_1 = int(detalle_alumnos[j][5])
            nota_2 = int(detalle_alumnos[j + 1][5])

            # Si el nombre del primer alumno es mayor, intercambiamos
            if nombre_1 > nombre_2:
                detalle_alumnos[j], detalle_alumnos[j + 1] = detalle_alumnos[j + 1], detalle_alumnos[j]
            # Si los nombres son iguales, comparamos las notas finales
            elif nombre_1 == nombre_2:
                if nota_1 < nota_2:
                    detalle_alumnos[j], detalle_alumnos[j + 1] = detalle_alumnos[j + 1], detalle_alumnos[j]

    return detalle_alumnos


def ordenar_por_nota_final(detalle_alumnos):
    n = len(detalle_alumnos)
    for i in range(n-1):
        indice = i
        for j in range(i + 1, n):
            if int(detalle_alumnos[indice][5]) > int(detalle_alumnos[j][5]):
                indice = j
        detalle_alumnos[i], detalle_alumnos[indice] = intercambiar(detalle_alumnos[i], detalle_alumnos[indice])
    return detalle_alumnos

def intercambiar(alumno_1, alumno_2):
    alumno_aux = alumno_1.copy()
    alumno_1 = alumno_2.copy()
    alumno_2 = alumno_aux.copy()

    return alumno_1, alumno_2

def ordenar_por_nombre(detalle_alumnos):
    n = len(detalle_alumnos)
    for i in range(n):
        for j in range(0, n - i - 1):
            if detalle_alumnos[j][0].lower() > detalle_alumnos[j + 1][0].lower():
                detalle_alumnos[j], detalle_alumnos[j + 1] = detalle_alumnos[j + 1], detalle_alumnos[j]
    return detalle_alumnos

def ordenar_materias_por_nombre(materias):
    n = len(materias)
    for i in range(n):
        for j in range(0, n - i - 1):
            nombre1 = materias[j][1].lower()
            nombre2 = materias[j + 1][1].lower()
            if nombre1 > nombre2:
                materias[j], materias[j + 1] = materias[j + 1], materias[j]
    return materias

