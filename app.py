from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)

def leer_csv(archivo) -> list[list[str]]:
    with open(archivo, newline='') as csvfile:
        rows = []
        reader = csv.reader(csvfile, delimiter='|', quotechar=',')
        for i, row in enumerate(reader):
            if i != 0:
                rows.append(row[0].split(','))
    return rows

def promedio_general_materia(detalle_alumnos, materias) -> list[int, int]:
    cantidad_alumnos_materia = []
    acumulador_notas_materia = []
    promedio_general_materia = []

    for n in enumerate(materias):
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
    lambda_mayor = lambda x: True if int(x[1][5]) >= nota else False
    alumnos_filtrados = []
    for n in enumerate(detalle_alumnos):
        if lambda_mayor(n):
            alumnos_filtrados.append(n)
    return alumnos_filtrados

def alumno_aprobo(detalle_alumno) -> bool:
    return (int(detalle_alumno[2]) >= 4 and int(detalle_alumno[3]) >= 4 and int(detalle_alumno[4]) >= 4)

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

def existe_alumno_en_la_lista(lista:str, alumno:str) -> bool:
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

def ordenar_por_nombre(detalle_alumnos):
    return detalle_alumnos

def alumnos_con_nota_final_mayor_por_materia(detalle_alumnos, nota):
    lista =[]
    for alumno in detalle_alumnos:
        if int(alumno[5]) >= nota:
            lista.append([alumno[0], alumno[1], alumno[5]])
    return lista

@app.route('/', methods=['GET'])
def informe():
    materias = leer_csv('materias.csv')
    detalle_alumnos = leer_csv('calificaciones.csv')

    promedio_por_materia = promedio_general_materia(detalle_alumnos, materias)

    alumnos_con_nota_mayor = alumnos_con_nota_final_mayor_a(detalle_alumnos, nota=4)
    alumnos_con_nota_mayor_ordenados = ordenar_por_nombre(alumnos_con_nota_mayor)

    cantidad_aprobados_desaprobados = aprobados_desaprobados_por_materia(detalle_alumnos, materias)

    alumnos_que_recursan_materias = alumnos_con_materias_para_recursar(detalle_alumnos)

    alumnos_promocionados_por_materia = alumnos_con_nota_final_mayor_por_materia(detalle_alumnos, nota=8)

    return render_template('informe.html',
                           detalle_alumnos=detalle_alumnos,
                           promedio_por_materia=promedio_por_materia,
                           alumnos_con_nota_mayor=alumnos_con_nota_mayor_ordenados,
                           cantidad_aprobados_desaprobados=cantidad_aprobados_desaprobados,
                           alumnos_que_recursan_materias=alumnos_que_recursan_materias,
                           alumnos_promocionados_por_materia=alumnos_promocionados_por_materia,
                           materias=materias)


@app.route('/crear_alumno', methods=['POST', 'GET'])
def crear_alumno():
    if request.method == 'POST':

        nombre = request.form.get("nombre")
        materia = request.form.get("materia")

        nota1 = int(request.form.get("nota1"))
        nota2 = int(request.form.get("nota2"))
        nota3 = int(request.form.get("nota3"))

        notaPromedio = (nota1 + nota2 + nota3) // 3

        nuevoAlumno = [nombre, materia, nota1, nota2, nota3, notaPromedio]
        with open("calificaciones.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(nuevoAlumno)

        return redirect("/")
    else:
        materias = []
        with open('materias.csv', newline='') as materiasfile:
            materias_reader = csv.reader(materiasfile, delimiter='|', quotechar=',')
            for i, row in enumerate(materias_reader):
                if i != 0:
                    materias.append(row[0].split(','))

        return render_template('crear_alumno.html', materias=materias)


@app.route('/borrar_alumno', methods=['POST'])
def borrar_alumno():
    return


if __name__=="__main__":
    app.run(debug=True)

