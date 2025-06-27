from flask import session, flash

from utils.csv_utils import add_row_csv


def calcular_promedio_general_materia(detalle_alumnos, materias) -> list[int]:
    cantidad_alumnos_materia = []
    acumulador_notas_materia = []
    promedio_general_materia = []

    for _ in range(len(materias)):
        cantidad_alumnos_materia.append(0)
        acumulador_notas_materia.append(0)
        promedio_general_materia.append(0)


    for n in enumerate(detalle_alumnos):
        cantidad_alumnos_materia[int(n[1][1]) - 1] += 1
        acumulador_notas_materia[int(n[1][1]) - 1] += int(n[1][5])

    for n in enumerate(materias):
        if cantidad_alumnos_materia[n[0] - 1] != 0:
            promedio = acumulador_notas_materia[n[0] - 1] // cantidad_alumnos_materia[n[0] - 1]
            promedio_general_materia[n[0] - 1] = [n[0], promedio]
        else:
            promedio_general_materia[n[0] - 1] = [n[0], 0]

    return promedio_general_materia

def alumnos_con_nota_final_mayor_a(detalle_alumnos, nota=4) -> list[list[str]]:
    alumnos_filtrados = []
    for alumno in detalle_alumnos:
        # Verifica si la nota final (columna 5) es mayor o igual a la nota indicada
        if int(alumno[5]) >= nota:
            alumnos_filtrados.append(alumno)
    return alumnos_filtrados

def alumno_aprobo(detalle_alumno) -> bool:
    return int(detalle_alumno[2]) >= 4 and int(detalle_alumno[3]) >= 4 and int(detalle_alumno[4]) >= 4

def aprobados_desaprobados_por_materia(detalle_alumnos, materias) -> list[list[int]]:
    reporte_por_materia = []
    for materia in materias:
        reporte_por_materia.append([materia[0], 0, 0])

    for alumno in detalle_alumnos:
        if alumno_aprobo(alumno):
            reporte_por_materia[int(alumno[1]) - 1][1] += 1
        else:
            reporte_por_materia[int(alumno[1]) - 1][2] += 1

    return reporte_por_materia

def existe_alumno_en_la_lista(lista:list[str], alumno:str) -> bool:
    for n in lista:
        if n == alumno:
            return True
    return False

def alumnos_con_materias_para_recursar(detalle_alumnos) -> list[str]:
    lista = []
    for alumno in detalle_alumnos:
        if not alumno_aprobo(alumno) and not existe_alumno_en_la_lista(lista, alumno[0]):
            lista.append(alumno[0])
    return lista

def alumnos_con_nota_final_mayor_por_materia(detalle_alumnos, nota):
    lista =[]
    for alumno in detalle_alumnos:
        if int(alumno[5]) >= nota:
            lista.append([alumno[0], alumno[1], alumno[5]])
    return lista

def alumnos_con_una_nota_menor_a(detalle_alumnos):
    alumnos_filtrados = []
    for alumno in detalle_alumnos:
        if int(alumno[2]) < 4 or int(alumno[3]) < 4 or int(alumno[4]) < 4:
            alumnos_filtrados.append(alumno)
    return alumnos_filtrados

def calcular_promedio_alumno(alumno: list[str]) -> list[str]:
    alumno_completo = alumno.copy()
    alumno_completo.append(str((int(alumno[2]) + int(alumno[3]) + int(alumno[4])) // 3))
    return alumno_completo

def generar_promedios(reporte_crudo) -> list[list[str]]:
    reporte_final=[]
    for alumno in reporte_crudo:
        reporte_final.append(calcular_promedio_alumno(alumno))
    return reporte_final

def agregar_alumno(alumno) -> None:
    if alumno_valido(alumno):
        add_row_csv(session['reporte_path'], calcular_promedio_alumno(alumno))

def alumno_valido(alumno) -> bool:
    try:
        nota1 = int(alumno[2])
        nota2 = int(alumno[3])
        nota3 = int(alumno[4])
    except ValueError:
        flash("Algunas notas no se ingresaron por contener caracteres indebidos. \nLas notas deben ser valores enteros", 'danger')
        return False
    if not (0 <= int(alumno[2]) <= 10 and  0 <= int(alumno[3]) <= 10 and 0 <= int(alumno[4]) <= 10):
        flash("Algunos registros no se ingresaron.\nVerifique que los valores esten entre 0 y 10.", 'warning')
        return False

    return True