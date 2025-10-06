from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'hello_world'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_students_from_file():
    """Чтение списка студентов из файла"""
    students = []
    try:
        with open('students.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line: # Пропускаем пустые строки
                    students.append(line)
    except FileNotFoundError:
        students = ["Файл students.txt не найден"]
    except Exception as e:
        students = [f"Ошибка при чтении файла: {str(e)}"]

    return students

def add_students_to_file(student_name):
    try:
        with open('students.txt', 'a', encoding='utf-8') as file:
            file.write(student_name + '\n')
        return True
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
        return False

@app.route('/del_student', methods=['GET', 'POST'])
def del_student():
    message = None
    message_type = None
    if request.method == 'POST':
        student = request.form.get('student_name', '').strip()
        if del_student_from_file(student):
            message = f"Студент '{student}' успешно удален!"
            message_type = 'success'
        else:
            message = "Ошибка при удалении студента"
            message_type = 'error'

    return render_template('del_student.html', message=message, message_type=message_type)

# функция удаления студента
def del_student_from_file(student):
    students = []
    try:
        with open('students.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line: # Пропускаем пустые строки
                    students.append(line)
            students.remove(student)
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")
        return False
    file1 = open('students.txt', 'w', encoding='utf-8')
    for student in students:
        file1.write(student + '\n')
    file1.close()
    return True
# функция удаления студента

@app_route('/import_student', methods=['GET', 'POST'])
def import_student():
    message = ''
    message_type = ''
    if request.method == 'POST':
        if 'file' not in request.files:
            message = 'Файл не отправлен'
            message_type = 'error'
        else:
            file = request.files['file']
            if file.filename == '':
                message = 'Файл не выбран'
                message_type = 'error'
            elif file and allowed_file(file.filename):
                try:
                    filename = (file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    message = f'Файл "{filename}" успешно загружен'
                    message_type = 'success'
                except Exception as e:
                    message = f'Ошибка при загрузке файла: {str(e)}'
                    message_type = 'error'
            else:
                message = 'Разрешены только файлы .txt'
                message_type = 'error'

    return render_template('import_students.html', message=message, message_type=message_type)


@app.route('/')
def index():
    """
    Главная страница со списком студентов

    Returns:
        rendered template: HTML страница со списком студентов
    """
    students = read_students_from_file()
    return render_template('index.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)