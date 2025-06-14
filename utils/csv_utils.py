import csv


def leer_csv(archivo) -> list[list[str]]:
    with open(archivo, newline='') as csvfile:
        rows = []
        reader = csv.reader(csvfile, delimiter='|', quotechar=',')
        for i, row in enumerate(reader):
            if i != 0:
                rows.append(row[0].split(','))
    return rows
