import csv


def read_data_from_csv(filename, data_list):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            data_list.append(line)

    return data_list

def write_data_to_csv(filename, fields):
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerow()


def append_question_to_csv(filename, fields, new_id, current_date, title, message):
    with open(filename, "a") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writerow({'id': new_id, 'submission_time': current_date, 'view_number': 1, 'vote_number': 0,
                         'title': title, 'message': message, 'image': ""})