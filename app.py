from flask import Flask, render_template, send_file
import openpyxl

app = Flask(__name__)

# Пути к Excel-файлам
EXCEL_FILE_1 = "static/DataProc.xlsx"
EXCEL_FILE_2 = "static/DataRaw.xlsx"

def read_excel(file_path):
    """Функция для чтения данных из Excel."""
    try:
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active
        return [[cell.value for cell in row] for row in sheet.iter_rows()]
    except FileNotFoundError:
        return [["Файл не найден"]]
    except Exception as e:
        return [[f"Ошибка чтения файла: {e}"]]

@app.route("/index")
def index():
    DataProc = read_excel(EXCEL_FILE_1)
    return render_template("index.html", DataProc=DataProc)

@app.route("/rawdata")
def rawdata():
    DataRaw = read_excel(EXCEL_FILE_2)
    return render_template("rawdata.html", DataRaw=DataRaw)

@app.route("/download/<int:file_id>")
def download(file_id):
    if file_id == 1:
        file_path = EXCEL_FILE_1
    elif file_id == 2:
        file_path = EXCEL_FILE_2
    else:
        return "Файл не найден", 404

    try:
        return send_file(file_path, as_attachment=True, download_name=file_path.split("/")[-1])
    except FileNotFoundError:
        return "Файл не найден", 404

if __name__ == "__main__":
    app.run(debug=True)
