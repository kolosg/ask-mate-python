import csv


def read_data_from_csv(filename, data_list):
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for line in reader:
            data_list.append(line)

    return data_list

def write_data_to_csv(filename, fields, data_list):
    with open(filename, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        for data in data_list:
            if filename == "templates/question.csv":
                writer.writerow({'id': data['id'], 'submission_time': data['submission_time'], 'view_number': data['view_number'],
                                     'vote_number': data['vote_number'], 'title': data['title'], 'message': data['message'], 'image': data['image']})
            else:
                writer.writerow({'id': data['id'], 'submission_time': data['submission_time'], 'vote_number': data['vote_number'],
                     'question_id': data['question_id'], 'message': data['message'], 'image': data['image']})


def append_data_to_csv(filename, fields, new_id, current_date, title_or_question_id, message):
    with open(filename, "a") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        if filename == "templates/question.csv":
            writer.writerow({'id': new_id, 'submission_time': current_date, 'view_number': 1, 'vote_number': 0,
                             'title': title_or_question_id, 'message': message, 'image': ""})
        else:
            writer.writerow({'id': new_id, 'submission_time': current_date, 'vote_number': 0,
                             'question_id': title_or_question_id, 'message': message, 'image': ""})
