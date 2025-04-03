import customtkinter as ctk
from PIL import Image, ImageEnhance
from tkinter import messagebox
import os
from datetime import datetime

# Define the path for the records file (records.txt) in the same directory as the script
FILE_NAME = os.path.join(os.path.dirname(__file__), "records.txt")

# Load background image as a global variable
image_path = os.path.join(os.path.dirname(__file__), "GilasPilipinas.png")
bg_image = Image.open(image_path).convert("RGBA")
opacity = 0.5
alpha = ImageEnhance.Brightness(bg_image.split()[3]).enhance(opacity)
bg_image.putalpha(alpha)
bg_image = ctk.CTkImage(light_image=bg_image, size=(300, 300))

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
        view_window = ctk.CTkToplevel()
        view_window.title("All Records")
        view_window.geometry("800x600") 
        
        text_area = ctk.CTkTextbox(view_window, width=750, height=500) 
        text_area.pack(expand=True, fill="both", padx=10, pady=10) 
        text_area.pack()
        # Format and display each record in the text area
        for record in records:
            id, first, middle, last, birthday, gender = record.strip().split(",")
            full_name = " ".join(filter(None, [first, middle, last]))
            formatted_birthday = format_birthday(birthday)
            text_area.insert(ctk.END, f"ID: {id}\nName: {full_name}\nBirthday: {formatted_birthday}\nGender: {gender}\n\n")
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

    # Create the search UI window
    search_window = ctk.CTkToplevel()
    search_window.title("Search Record")
    search_window.geometry("400x250")
    search_window.attributes('-topmost', True)  # Keep the window on top

    # Add background image
    bg_label = ctk.CTkLabel(search_window, image=bg_image, text="")
    bg_label.place(relwidth=1, relheight=1)

    ctk.CTkLabel(search_window, text="Choose search type:").pack()

    search_option = ctk.StringVar(value="ID")  # Default to ID search

    ctk.CTkRadioButton(search_window, text="By ID", variable=search_option, value="ID").pack()
    ctk.CTkRadioButton(search_window, text="By Name", variable=search_option, value="Name").pack()
    ctk.CTkRadioButton(search_window, text="By Birthday", variable=search_option, value="Birthday").pack()

    ctk.CTkLabel(search_window, text="Enter search term:").pack()
    entry_search = ctk.CTkEntry(search_window)
    entry_search.pack()

    ctk.CTkButton(search_window, text="Search", command=perform_search).pack()

# Function to input first name, middle name, last name, and birthday
def sign_up():
    def submit():
        id = generate_id()
        first = entry_first.get().strip()
        middle = entry_middle.get().strip()
        last = entry_last.get().strip()
        birthday = entry_birthday.get().strip()
        gender = gender_dropdown.get()
        
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
    sign_up_window = ctk.CTkToplevel()
    sign_up_window.title("Sign Up")
    sign_up_window.geometry("600x450")
    sign_up_window.attributes('-topmost', True)  # Keep the window on top
    
    # Add background image
    bg_label = ctk.CTkLabel(sign_up_window, image=bg_image, text="")
    bg_label.place(relwidth=1, relheight=1)

    ctk.CTkLabel(sign_up_window, text="First Name:").pack()
    entry_first = ctk.CTkEntry(sign_up_window)
    entry_first.pack()
    
    ctk.CTkLabel(sign_up_window, text="Middle Name:").pack()
    entry_middle = ctk.CTkEntry(sign_up_window)
    entry_middle.pack()
    
    ctk.CTkLabel(sign_up_window, text="Last Name:").pack()
    entry_last = ctk.CTkEntry(sign_up_window)
    entry_last.pack()
    
    ctk.CTkLabel(sign_up_window, text="Birthday (YYYY-MM-DD):").pack()
    entry_birthday = ctk.CTkEntry(sign_up_window)
    entry_birthday.pack()
    
    ctk.CTkLabel(sign_up_window, text="Gender:").pack()
    gender_dropdown = ctk.CTkComboBox(sign_up_window, values=["Male", "Female", "Other"])
    gender_dropdown.set("Male") 
    gender_dropdown.pack()
    
    submit_button = ctk.CTkButton(sign_up_window, text="Submit", command=submit)
    submit_button.pack(pady=15)
    ctk.CTkButton(sign_up_window, text="Exit", command=sign_up_window.destroy).pack(pady=5)

    
# Main function that builds the root GUI window
def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("User Management System")
    root.geometry("600x450")

    # Add background image to the root window
    bg_label = ctk.CTkLabel(root, image=bg_image, text="")  
    bg_label.place(relwidth=1, relheight=1)

    # Place other widgets on top of the background
    ctk.CTkLabel(root, text="Welcome to the Gilas Pilipinas", font=("Arial", 20)).pack(pady=10)
    
    ctk.CTkButton(root, text="Sign Up", width=200, height=50, command=sign_up, font=("Arial", 15)).pack(pady=5)
    ctk.CTkButton(root, text="View All Records", width=200, height=50, command=view_records, font=("Arial", 15)).pack(pady=5)
    ctk.CTkButton(root, text="Search Record", width=200, height=50, command=search_record, font=("Arial", 15)).pack(pady=5)
    ctk.CTkButton(root, text="Exit", width=200, height=50, command=root.quit, font=("Arial", 15)).pack(pady=5)

    root.mainloop()
    
# Run the main function when the script is executed
if __name__ == "__main__":
    main()
