import tkinter as tk
from tkinter import messagebox, ttk
import os
from datetime import datetime

# Define the path for the records file (records.txt) in the same directory as the script
FILE_NAME = os.path.join(os.path.dirname(__file__), "records.txt")
# Function to save a new user record into the records.txt file
def save_record(id, first, middle, last, birthday, gender):
    try:
        # Check if the file exists and read existing records to avoid duplicates
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                records = file.readlines()
            
            # Create new record entry
            new_entry = f"{id},{first},{middle},{last},{birthday},{gender}\n"
            if new_entry in records:
                messagebox.showerror("Error", "Record already exists!")
                return
        # Append the new record to the file
        with open(FILE_NAME, "a") as file:
            file.write(new_entry)
        messagebox.showinfo("Success", "Record saved successfully!")
    
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save record: {e}")
        
# Function that will generate id automatically
def generate_id():
    # Contermeasures when there is no file or anything in the database
    if not os.path.exists(FILE_NAME):
        return "00001"

    with open(FILE_NAME, "r") as file:
        records = file.readlines()

    if not records:
        return "00001"

    # Find the highest id and assign the next number to that id
    ids = [int(record.split(",")[0]) for record in records if record.strip()]
    new_id = max(ids) + 1
    return f"{new_id:05d}"  # Format as five-digit string
        
# Function to validate user input before saving
def validate_input(first, middle, last, birthday):
    # Ensure required fields are not empty
    if not all([first, last, birthday]):
        return "All fields except middle name are required!"
    # Ensure names only contain letters
    if not first.replace(" ", "").isalpha() or not last.replace(" ", "").isalpha() or (middle and not middle.replace(" ", "").isalpha()):
        return "First, middle, and last names should only contain letters!"
    # Ensure birthday is in correct YYYY-MM-DD format
    try:
        datetime.strptime(birthday, "%Y-%m-%d")
    except ValueError:
        return "Invalid birthday format! Use YYYY-MM-DD."
    return None

# Format birthday to a readable date string
def format_birthday(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%B %d, %Y")
    except ValueError:
        return date_str
    
# Function to view all saved records
def view_records():
    try:
        if not os.path.exists(FILE_NAME):
            messagebox.showinfo("Info", "No records found.")
            return
        
        with open(FILE_NAME, "r") as file:
            records = file.readlines()
        
        if not records:
            messagebox.showinfo("Info", "No records found.")
            return
        # Create a new window to display records
        view_window = tk.Toplevel()
        view_window.title("All Records")
        view_window.geometry("600x450")
        
        text_area = tk.Text(view_window, width=70, height=20)
        text_area.pack()
        # Format and display each record in the text area
        for record in records:
            id, first, middle, last, birthday, gender = record.strip().split(",")
            full_name = " ".join(filter(None, [first, middle, last]))
            formatted_birthday = format_birthday(birthday)
            text_area.insert(tk.END, f"ID: {id}\nName: {full_name}\nBirthday: {formatted_birthday}\nGender: {gender}\n\n")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read records: {e}")
        
# Function to search for a record by ID, Name, or Birthday
def search_record():
    def perform_search():
        keyword = entry_search.get().strip().lower()
        search_type = search_option.get()  # Either "ID", "Name", or "Birthday"

        try:
            if not os.path.exists(FILE_NAME):
                messagebox.showinfo("Info", "No records found.")
                search_window.destroy()
                return
            
            with open(FILE_NAME, "r") as file:
                records = file.readlines()

            # Perform search based on the selected type
            if search_type == "ID":
                results = [record for record in records if record.strip().split(",")[0] == keyword]
            elif search_type == "Name":
                results = [record for record in records if keyword in " ".join(record.strip().split(",")[1:4]).lower()]
            else:  # Search by Birthday
                results = [record for record in records if record.strip().split(",")[4] == keyword]

            # Display search results
            if results:
                result_text = "\n".join(
                    [
                        f"ID: {rec.strip().split(',')[0]}\n"
                        f"Name: {' '.join(filter(None, rec.strip().split(',')[1:4]))}\n"
                        f"Birthday: {format_birthday(rec.strip().split(',')[4])}\n"
                        f"Gender: {rec.strip().split(',')[5]}\n"
                        for rec in results
                    ]
                )
                messagebox.showinfo("Search Results", result_text)
            else:
                messagebox.showinfo("Search Results", "No matching records found.")

        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {e}")

        finally:
            search_window.destroy()

    # Create the search UI window
    search_window = tk.Toplevel()
    search_window.title("Search Record")
    search_window.geometry("400x250")

    tk.Label(search_window, text="Choose search type:").pack()

    search_option = tk.StringVar(value="ID")  # Default to ID search

    tk.Radiobutton(search_window, text="By ID", variable=search_option, value="ID", indicatoron=True).pack()
    tk.Radiobutton(search_window, text="By Name", variable=search_option, value="Name", indicatoron=True).pack()
    tk.Radiobutton(search_window, text="By Birthday", variable=search_option, value="Birthday", indicatoron=True).pack()

    tk.Label(search_window, text="Enter search term:").pack()
    entry_search = tk.Entry(search_window)
    entry_search.pack()

    tk.Button(search_window, text="Search", command=perform_search).pack()


def sign_up():
    def submit():
        id = generate_id()
        first = entry_first.get().strip()
        middle = entry_middle.get().strip()
        last = entry_last.get().strip()
        birthday = entry_birthday.get().strip()
        gender = gender_var.get()
        
        # Validate the inputs
        error = validate_input(first, middle, last, birthday)
        if error:
            messagebox.showerror("Error", error)
            sign_up_window.destroy()  
            return

        # Save the record with the assigned ID
        save_record(id, first, middle, last, birthday, gender)
        sign_up_window.destroy()
        
    # Create the Sign Up UI form
    sign_up_window = tk.Toplevel()
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("600x450")
    
    tk.Label(sign_up_window, text="First Name:").pack()
    entry_first = tk.Entry(sign_up_window)
    entry_first.pack()
    
    tk.Label(sign_up_window, text="Middle Name:").pack()
    entry_middle = tk.Entry(sign_up_window)
    entry_middle.pack()
    
    tk.Label(sign_up_window, text="Last Name:").pack()
    entry_last = tk.Entry(sign_up_window)
    entry_last.pack()
    
    tk.Label(sign_up_window, text="Birthday (YYYY-MM-DD):").pack()
    entry_birthday = tk.Entry(sign_up_window)
    entry_birthday.pack()
    
    tk.Label(sign_up_window, text="Gender:").pack()
    gender_var = tk.StringVar()
    gender_dropdown = ttk.Combobox(sign_up_window, textvariable=gender_var, values=["Male", "Female", "Other"])
    gender_dropdown.pack()
    gender_dropdown.current(0)  # Default to first item
    
    tk.Button(sign_up_window, text="Submit", command=submit).pack()
    
# Main function that builds the root GUI window
def main():
    root = tk.Tk()
    root.title("User Management System")
    root.geometry("600x450")
    
    # Main menu buttons
    tk.Label(root, text="Welcome to the System", font=("Arial", 12)).pack(pady=10)
    
    tk.Button(root, text="Sign Up", width=20, command=sign_up).pack(pady=5)
    tk.Button(root, text="View All Records", width=20, command=view_records).pack(pady=5)
    tk.Button(root, text="Search Record", width=20, command=search_record).pack(pady=5)
    tk.Button(root, text="Exit", width=20, command=root.quit).pack(pady=5)
    
    root.mainloop()
    
# Run the main function when the script is executed
if __name__ == "__main__":
    main()
