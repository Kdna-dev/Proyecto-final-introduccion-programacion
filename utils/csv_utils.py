import csv

def add_csv(archivo) -> None:
    with open(archivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Nombre','Materia','Nota1','Nota2','Nota3','Promedio'])

def add_row_csv(archivo, nuevo_alumno: list[str]) -> None:
    with open(archivo, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(nuevo_alumno)

def leer_csv(archivo) -> list[list[str]]:
    with open(archivo, newline='') as csvfile:
        rows = []
        reader = csv.reader(csvfile, delimiter='|', quotechar=',')
        for i, row in enumerate(reader):
            if i != 0:
                rows.append(row[0].split(','))
    return rows

def empty_csv(archivo) -> None:
    with open(archivo, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Nombre', 'Materia', 'Nota1', 'Nota2', 'Nota3', 'Promedio'])