from flask import Flask, render_template, request, redirect
from utils.csv_utils import leer_csv, add_row_csv
from utils.sort_utils import ordenar_por_nota_final, ordenar_materias_por_nombre, ordenar_por_nombre_y_nota, \
    ordenar_por_nombre
from gestion_alumnos.gestion_alumnos import aprobados_desaprobados_por_materia, \
    alumnos_con_nota_final_mayor_por_materia, alumnos_con_materias_para_recursar, \
    calcular_promedio_general_materia, alumnos_con_una_nota_menor_a

import csv
app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def informe():

    orden = request.form.get('filtro', 'nombre')  # 'nombre', 'nota' o 'materia'
    materias = leer_csv('materias.csv')
    detalle_alumnos = leer_csv('calificaciones.csv')

    if request.method == 'POST':
        nota_minima = int(request.form.get("nota_minima")) if request.form.get("nota_minima").isdigit() else 0
        alumnos_promocionados_por_materia = alumnos_con_nota_final_mayor_por_materia(detalle_alumnos, nota_minima)
    else:
        alumnos_promocionados_por_materia = alumnos_con_nota_final_mayor_por_materia(detalle_alumnos, nota=8)

    alumnos_que_recursan_materias = alumnos_con_materias_para_recursar(detalle_alumnos)

    #Ordenamientos generales
    if orden == 'nombre':
        detalle_ordenado = ordenar_por_nombre_y_nota(detalle_alumnos.copy())
    elif orden == 'nota':
        detalle_ordenado = ordenar_por_nota_final(detalle_alumnos.copy())
    elif orden == 'materia':
        materias_ordenadas = ordenar_materias_por_nombre(materias.copy())
        detalle_ordenado = []
        for materia in materias_ordenadas:
            for alumno in detalle_alumnos:
                if materias[int(alumno[1]) - 1][1] == materia[1]:
                    detalle_ordenado.append(alumno)
    else:
        detalle_ordenado = detalle_alumnos.copy()
        # Reordenar promedio_por_materia por nombre de materia
    promedio_por_materia= calcular_promedio_general_materia(detalle_alumnos, materias)
    promedio_ordenado = []
    materias_ordenadas = ordenar_materias_por_nombre(materias.copy())

    for materia in materias_ordenadas:
        id_materia = int(materia[0])
        for promedio in promedio_por_materia:
            if promedio[0] == id_materia:
                promedio_ordenado.append(promedio)
                break
    # Cantidad aprobados y desaprobados por materia (orden por ID original)
    cantidad_aprobados_desaprobados = aprobados_desaprobados_por_materia(detalle_alumnos, materias)

    # Reordenar lista de aprobados/desaprobados según nombre de materia
    cantidad_ordenada = []
    materias_ordenadas = ordenar_materias_por_nombre(materias.copy())

    for materia in materias_ordenadas:
        id_materia = int(materia[0])
        for item in cantidad_aprobados_desaprobados:
            if int(item[0]) == id_materia:
                cantidad_ordenada.append(item)
                break



    alumnos_una_nota_menor = alumnos_con_una_nota_menor_a(detalle_alumnos)
    alumnos_una_nota_menor_ordenados = ordenar_por_nombre(alumnos_una_nota_menor)
    alumnos_ordenados_combinado = ordenar_por_nombre_y_nota(detalle_alumnos.copy())
    cantidad_aprobados_desaprobados = cantidad_ordenada

    return render_template(
    'informe.html',
    materias=materias,
    detalle_alumnos=detalle_ordenado,
    promedio_por_materia=promedio_ordenado,
    cantidad_aprobados_desaprobados=cantidad_aprobados_desaprobados,
    alumnos_que_recursan_materias=alumnos_que_recursan_materias,
    alumnos_ordenados_combinado=alumnos_ordenados_combinado,
    alumnos_promocionados_por_materia=alumnos_promocionados_por_materia,
    orden=orden,
    alumnos_una_nota_menor_ordenados=alumnos_una_nota_menor_ordenados

)



@app.route('/crear_alumno', methods=['POST', 'GET'])
def crear_alumno():
    if request.method == 'POST':

        nombre = request.form.get("nombre")
        materia = request.form.get("materia")

        nota1 = int(request.form.get("nota1"))
        nota2 = int(request.form.get("nota2"))
        nota3 = int(request.form.get("nota3"))

        nota_promedio = (nota1 + nota2 + nota3) // 3

        nuevo_alumno = [nombre, materia, nota1, nota2, nota3, nota_promedio]

        add_row_csv(nuevo_alumno)

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

