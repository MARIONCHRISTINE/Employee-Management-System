import tkinter as tk
import sqlite3

# Function to open the GUI
def open_gui():
    root = tk.Tk()
    root.title("Employee Management System")
    root.geometry("600x400")

    # Creating a SQLite database connection and cursor
    db_connection = sqlite3.connect("employee_management.db")
    cursor = db_connection.cursor()

    # Creating the 'employees' table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY,
        name TEXT,
        contact_information TEXT,
        department TEXT
    )''')
    db_connection.commit()

    def add_employee():
        # Creating a new window for adding an employee
        add_employee_window = tk.Toplevel(root)
        add_employee_window.title("Add Employee")

        def add():
            name = name_entry.get()
            contact_information = contact_entry.get()
            department = department_entry.get()

            if not name or not department:
                result_label.config(text="Employee name and department are required.")
                return

            insert_query = "INSERT INTO employees (name, contact_information, department) VALUES (?, ?, ?)"
            cursor.execute(insert_query, (name, contact_information, department))
            db_connection.commit()
            result_label.config(text="Employee added successfully!")

        name_label = tk.Label(add_employee_window, text="Name:")
        name_label.pack()
        name_entry = tk.Entry(add_employee_window)
        name_entry.pack()

        contact_label = tk.Label(add_employee_window, text="Contact Information:")
        contact_label.pack()
        contact_entry = tk.Entry(add_employee_window)
        contact_entry.pack()

        department_label = tk.Label(add_employee_window, text="Department:")
        department_label.pack()
        department_entry = tk.Entry(add_employee_window)
        department_entry.pack()

        add_button = tk.Button(add_employee_window, text="Add Employee", command=add)
        add_button.pack()

        result_label = tk.Label(add_employee_window, text="")
        result_label.pack()

    def remove_employee():
        # Creating a new window for removing an employee
        remove_employee_window = tk.Toplevel(root)
        remove_employee_window.title("Remove Employee")

        def remove():
            identifier = identifier_entry.get()
            if not identifier:
                result_label.config(text="Please provide the name or ID of the employee to remove.")
                return

            select_query = "SELECT employee_id FROM employees WHERE name = ? OR employee_id = ?"
            cursor.execute(select_query, (identifier, identifier))
            result = cursor.fetchone()

            if not result:
                result_label.config(text="Employee not found.")
                return

            employee_id = result[0]
            delete_query = "DELETE FROM employees WHERE employee_id = ?"
            cursor.execute(delete_query, (employee_id,))
            db_connection.commit()
            result_label.config(text="Employee removed successfully!")

        identifier_label = tk.Label(remove_employee_window, text="Name or ID:")
        identifier_label.pack()
        identifier_entry = tk.Entry(remove_employee_window)
        identifier_entry.pack()

        remove_button = tk.Button(remove_employee_window, text="Remove Employee", command=remove)
        remove_button.pack()

        result_label = tk.Label(remove_employee_window, text="")
        result_label.pack()

    def promote_employee():
        # Creating a new window for promoting an employee
        promote_employee_window = tk.Toplevel(root)
        promote_employee_window.title("Promote Employee")

        def promote():
            identifier = identifier_entry.get()
            new_department = new_department_entry.get()
            if not identifier or not new_department:
                result_label.config(text="Please provide the name or ID of the employee to promote and the new department.")
                return

            select_query = "SELECT employee_id FROM employees WHERE name = ? OR employee_id = ?"
            cursor.execute(select_query, (identifier, identifier))
            result = cursor.fetchone()

            if not result:
                result_label.config(text="Employee not found.")
                return

            employee_id = result[0]
            update_query = "UPDATE employees SET department = ? WHERE employee_id = ?"
            cursor.execute(update_query, (new_department, employee_id))
            db_connection.commit()
            result_label.config(text="Employee promoted successfully!")

        identifier_label = tk.Label(promote_employee_window, text="Name or ID:")
        identifier_label.pack()
        identifier_entry = tk.Entry(promote_employee_window)
        identifier_entry.pack()

        new_department_label = tk.Label(promote_employee_window, text="New Department:")
        new_department_label.pack()
        new_department_entry = tk.Entry(promote_employee_window)
        new_department_entry.pack()

        promote_button = tk.Button(promote_employee_window, text="Promote Employee", command=promote)
        promote_button.pack()

        result_label = tk.Label(promote_employee_window, text="")
        result_label.pack()

    def display_employees():
        # Creating a new window to display employees
        display_employees_window = tk.Toplevel(root)
        display_employees_window.title("Employee List")

        select_query = "SELECT * FROM employees"
        cursor.execute(select_query)
        employees = cursor.fetchall()

        if not employees:
            result_label = tk.Label(display_employees_window, text="No employees found.")
            result_label.pack()
        else:
            result_label = tk.Label(display_employees_window, text="Employee List:")
            result_label.pack()
            for employee in employees:
                employee_id, name, contact_information, department = employee
                employee_info = f"Employee ID: {employee_id}, Name: {name}, Contact: {contact_information}, Department: {department}"
                employee_label = tk.Label(display_employees_window, text=employee_info)
                employee_label.pack()

    # Buttons to open different windows
    add_employee_button = tk.Button(root, text="Add Employee", command=add_employee)
    add_employee_button.pack()

    remove_employee_button = tk.Button(root, text="Remove Employee", command=remove_employee)
    remove_employee_button.pack()

    promote_employee_button = tk.Button(root, text="Promote Employee", command=promote_employee)
    promote_employee_button.pack()

    display_employees_button = tk.Button(root, text="Display Employees", command=display_employees)
    display_employees_button.pack()

    # Close the database connection when the main window is closed
    root.protocol("WM_DELETE_WINDOW", lambda: close_connection(root, db_connection))

    root.mainloop()

def close_connection(root, db_connection):
    db_connection.close()
    root.destroy()

if __name__ == "__main__":
    open_gui()
