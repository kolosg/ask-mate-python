import csv


def read_data_from_csv(filename, data_list):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            data_list.append(line)

    return data_list
