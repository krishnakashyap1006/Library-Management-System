# Library Management System

Yeh version aapke original program ko teen layers mein rakhta hai:

- `schema.sql`: database aur tables
- `db.py`: MySQL connection, commit, rollback aur close
- `books.py`, `students.py`, `transactions.py`: database operations
- `app.py`: menu aur user input

## 1. Database banana

MySQL Workbench mein `schema.sql` open karke poori file run karein. Ya MySQL command line se:

```powershell
mysql -u root -p < schema.sql
```

Isse `lib_management` database aur `books`, `students`, `transactions` tables banengi.

## 2. Python package install karna

Is folder mein PowerShell kholkar:

```powershell
py -m pip install -r requirements.txt
```

### `ModuleNotFoundError` aaye to

Agar error `No module named 'mysql'` hai, to isi Python interpreter mein package install karein:

```powershell
py -m pip install --user mysql-connector-python
py -c "import mysql.connector; print('mysql connector OK')"
```

Agar error `No module named 'db'`, `books`, ya `students` hai, to `app.py` ko isi folder se run karein. Ye sab `.py` files ek hi folder mein honi chahiye:

```powershell
cd "C:\Users\Krishna\Documents\Codex\2026-09-24\i\outputs\library_management"
py app.py
```

VS Code use kar rahe hain to wahi interpreter select karein jisme upar wala `py -m pip install` command chala hai.

## 3. MySQL credentials set karna

Password ko code mein hard-code na karein. PowerShell mein apni values set karein:

```powershell
$env:MYSQL_HOST = "127.0.0.1"
$env:MYSQL_PORT = "3306"
$env:MYSQL_USER = "root"
$env:MYSQL_PASSWORD = "aapka_mysql_password"
$env:MYSQL_DATABASE = "lib_management"
```

## 4. Program run karna

```powershell
py app.py
```

## Files ek doosre se kaise connect hoti hain

`app.py` functions ko import karta hai. `books.py`, `students.py` aur `transactions.py` database work ke liye `db.py` ka `db_session()` use karti hain. Har operation ke successful hone par commit hota hai; error par rollback hota hai.

Issue karte waqt `transactions` mein ek row banti hai aur `books.quantity` ek kam hoti hai. Return karte waqt usi transaction row ka status `returned` hota hai aur stock ek badhta hai. Isliye return ke liye `transaction_id` use hota hai.

## Aapke original code mein important problems

- `return_book()` mein `UPDATE` ke baad `fetchone()` kiya gaya tha; `UPDATE` result fetch nahi hota.
- Transaction mein student ka naam rakhne se duplicate aur spelling mismatch ho sakta hai; ab `student_id` foreign key hai.
- `date` ke liye `%y` do-digit year deta tha; ab MySQL ka `CURDATE()` use ho raha hai.
- Credentials input/code mein rakhne ke bajay environment variables se liye ja rahe hain.
- `FOR UPDATE` aur commit/rollback se issue/return ke beech stock mismatch ka risk kam hota hai.

## Aage ke enhancements

- Book search, student search aur pagination
- Late return par fine calculation
- Admin/login roles
- CSV/PDF reports aur dashboard
- Logging aur automated database backup
- Tkinter ya web UI
