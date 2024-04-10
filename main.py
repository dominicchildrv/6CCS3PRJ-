import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from threading import Thread
from subprocess import Popen
from database import PacmanDatabase
from booleanFormula import BooleanFormula
from graphConverter import cnf_to_graph
from mapEngine import generate_map
from mapToLayout import Layout
import os

class PacmanUI:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("Pacman can be NP Hard!")
        self.root.geometry("1920x1080")

        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(expand=True, fill='both')

        self.boolean_formula = BooleanFormula()

        self.show_main_menu()

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_frame()

        label = tk.Label(self.content_frame, text="Welcome to Pacman!", font=("Arial", 14))
        label.pack(pady=10)

        # Re-create the formula label here to ensure it's always fresh and correctly placed
        self.formula_label = tk.Label(self.content_frame, text="", font=("Arial", 12), wraplength=800)
        self.formula_label.pack(pady=10)


        add_clause_button = tk.Button(self.content_frame, text="Add Clause to Boolean Formula", command=self.add_clause, font=("Arial", 12))
        add_clause_button.pack(pady=10)

        layout_name_label = tk.Label(self.content_frame, text="Layout Name:", font=("Arial", 12))
        layout_name_label.pack(pady=5)
        self.layout_name_entry = tk.Entry(self.content_frame, font=("Arial", 12))
        self.layout_name_entry.pack(pady=5)

        self.ghosts_var = tk.StringVar()
        ghosts_label = tk.Label(self.content_frame, text="Ghosts:", font=("Arial", 12))
        ghosts_label.pack(pady=5)
        ghosts_dropdown = ttk.Combobox(self.content_frame, textvariable=self.ghosts_var, font=("Arial", 12))
        ghosts_dropdown['values'] = (0, 1, 2, 3, 4)
        ghosts_dropdown['state'] = 'readonly'  # Prevent typing a value
        ghosts_dropdown.pack(pady=5)

        generate_reset_button = tk.Button(self.content_frame, text="Generate Layout & Reset", command=self.generate_and_reset_layout, font=("Arial", 12))
        generate_reset_button.pack(pady=10)


        view_db_button = tk.Button(self.content_frame, text="View Levels", command=self.show_database, font=("Arial", 12))
        view_db_button.pack(pady=10)

        self.update_formula_label()

    def start_game(self, name):

        self.show_main_menu()
        # Example function for starting the game with a specific level
        def run_game():
            command = ['python3', 'pacman.py', '-l', name]
            process = Popen(command)
            process.wait()
            self.show_main_menu()  # Return to main menu after game

        for widget in self.content_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="disabled")

        game_thread = Thread(target=run_game, daemon=True)
        game_thread.start()

    def show_database(self):
        self.clear_frame()

        back_button = tk.Button(self.content_frame, text="Back", command=self.show_main_menu, font=("Arial", 12))
        back_button.pack(pady=10)

        # Setup the tree view with proper headings
        self.tree = ttk.Treeview(self.content_frame)
        self.tree['columns'] = ('ID', 'Layout Name', 'Ghosts', 'High Score', 'Last Score', 'Beaten')

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column('ID', anchor=tk.CENTER, width=80)
        self.tree.column('Layout Name', anchor=tk.CENTER, width=120)
        self.tree.column('Ghosts', anchor=tk.CENTER, width=80)
        self.tree.column('High Score', anchor=tk.CENTER, width=80)
        self.tree.column('Last Score', anchor=tk.CENTER, width=80)
        self.tree.column('Beaten', anchor=tk.CENTER, width=80)

        self.tree.heading('ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('Layout Name', text='Layout Name', anchor=tk.W)
        self.tree.heading('Ghosts', text='Ghosts', anchor=tk.CENTER)
        self.tree.heading('High Score', text='High Score', anchor=tk.CENTER)
        self.tree.heading('Last Score', text='Last Score', anchor=tk.CENTER)
        self.tree.heading('Beaten', text='Beaten', anchor=tk.CENTER)

        self.tree.pack(expand=True, fill='both')

        data = self.db.get_all_layouts()
        for row in data:
            beaten_status = "Beaten" if row[5] == 1 else "Not Beaten"  # Adjust this index if necessary
            # Update the row data with the modified 'beaten_status' before inserting it into the tree view
            modified_row = row[:5] + (beaten_status,)
            self.tree.insert('', tk.END, values=modified_row)

        delete_button = tk.Button(self.content_frame, text="Delete Selected Level", command=self.delete_selected_level, font=("Arial", 12))
        delete_button.pack(pady=10)

        def on_double_click(event):
            item = self.tree.selection()[0]
            level_name = self.tree.item(item, 'values')[1]  # Assuming the level name is the second value
            self.start_game(level_name)

        self.tree.bind("<Double-1>", on_double_click)



    def add_clause(self):
        literals = simpledialog.askstring("Input", "Enter literals separated by spaces (e.g., x1 ~x2 x3):", parent=self.root)
        if literals:
            clause = literals.split()
            added_successfully = self.boolean_formula.add_clause(*clause)
            if added_successfully:
                messagebox.showinfo("Info", "Clause added to the formula.")
                self.update_formula_label()
            else:
                messagebox.showerror("Error", "Invalid literal(s) entered. Clause was not added.")

    def update_formula_label(self):
        # Converts the Boolean formula to a string and updates the formula label
        formula_str = " AND ".join(["(" + " OR ".join(clause) + ")" for clause in self.boolean_formula.return_clause_list()])
        self.formula_label.config(text="Boolean Formula: " + formula_str)

    def generate_and_reset_layout(self):
        layoutName = self.layout_name_entry.get().strip()  # Trim whitespace
        numOfGhosts = self.ghosts_var.get()

          
        if not self.boolean_formula.clauses:
            messagebox.showwarning("Warning", "No Boolean formula provided. Please add at least one clause.")
            return

        # Check if layout name is provided
        if not layoutName:
            messagebox.showwarning("Warning", "A level needs a name. Please enter a name for the level.")
            return
        
        if not numOfGhosts:
            messagebox.showwarning("Warning", "Please select the number of ghosts for the level.")
            return

        booleanFormula = self.boolean_formula

        # Assuming cnf_to_graph, generate_map, and Layout handle the creation and saving of the layout
        graph = cnf_to_graph(booleanFormula)
        map = generate_map(graph)
        layout = Layout(map, int(numOfGhosts), self.db, layoutName)
        layout.save_layout()

        # Clear the input fields and Boolean formula
        self.boolean_formula.clauses.clear()
        self.layout_name_entry.delete(0, tk.END)
        self.ghosts_var.set('')
        self.update_formula_label()

        # Notify the user that the layout was generated and parameters have been reset
        messagebox.showinfo("Info", "Layout generated and parameters reset.")


    def delete_selected_level(self):
        selected_item = self.tree.selection()  # Get selected item in the treeview
        if selected_item:
            item = self.tree.item(selected_item)
            level_id, level_name, _, _, _, _ = item['values']  # Assuming the level name is the second value in the 'values' list
            self.db.delete_layout_by_id(level_id)  # Call the method to delete layout from database
            
            # Construct the path to the layout file
            layout_file_path = os.path.join("pacman_utils", "layouts", f"{level_name}.lay")
            try:
                # Attempt to delete the layout file
                os.remove(layout_file_path)
                messagebox.showinfo("Info", f"Selected level and layout file '{level_name}.lay' have been deleted.")
            except OSError as e:
                # If the file does not exist or an error occurs, show a warning
                messagebox.showwarning("Warning", f"Could not delete layout file '{level_name}.lay'.\n{e}")
            
            self.tree.delete(selected_item)  # Remove the item from the treeview
        else:
            messagebox.showwarning("Warning", "No level selected.")



if __name__ == "__main__":
    db = PacmanDatabase('pacman_layouts.db')  # Ensure this is defined correctly
    root = tk.Tk()
    app = PacmanUI(root, db)
    root.mainloop()
