import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import subprocess
from encrypt import encrypt_file
from decrypt import decrypt_file
from utils import check_password_strength, get_file_hash, log_action, get_history

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureShield - File Encryption System")
        self.root.geometry("800x600")
        self.root.minsize(600, 450)
        self.root.configure(bg="#f0f4f7")

        # Style ttk components
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure("TNotebook", background="#f0f4f7", borderwidth=0)
        style.configure("TNotebook.Tab", background="#dcdde1", padding=[20, 8], font=("Helvetica", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", "#ffffff")], foreground=[("selected", "#2c3e50")])
        
        style.configure("Treeview", font=("Helvetica", 9), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 10, "bold"), background="#dcdde1", foreground="#2c3e50")

        self.selected_file = tk.StringVar()
        self.password = tk.StringVar()
        self.show_password = tk.BooleanVar(value=False)

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=70)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame, text="🔒 SecureShield File Encryption", 
            fg="white", bg="#2c3e50", font=("Helvetica", 18, "bold")
        ).pack(pady=20)

        # Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=20)

        # Tab 1: Operations
        self.ops_frame = tk.Frame(self.notebook, bg="#ffffff", padx=40, pady=30)
        self.notebook.add(self.ops_frame, text="Encrypt / Decrypt")
        self.setup_ops_tab()

        # Tab 2: History
        self.history_frame = tk.Frame(self.notebook, bg="#ffffff", padx=30, pady=30)
        self.notebook.add(self.history_frame, text="History")
        self.setup_history_tab()

    def setup_ops_tab(self):
        self.ops_frame.columnconfigure(0, weight=1)
        self.ops_frame.columnconfigure(1, weight=0)

        # File Selection
        tk.Label(self.ops_frame, text="Select File:", bg="#ffffff", font=("Helvetica", 11, "bold"), fg="#2c3e50").grid(row=0, column=0, sticky="w", pady=(10, 5))
        
        file_entry = tk.Entry(self.ops_frame, textvariable=self.selected_file, font=("Helvetica", 11), state="readonly", relief="solid", bd=1)
        file_entry.grid(row=1, column=0, sticky="ew", padx=(0, 15), ipady=6)
        
        tk.Button(
            self.ops_frame, text="Browse...", command=self.browse_file, 
            bg="#3498db", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=15, pady=6, cursor="hand2"
        ).grid(row=1, column=1)

        # Password Input
        tk.Label(self.ops_frame, text="Enter Password:", bg="#ffffff", font=("Helvetica", 11, "bold"), fg="#2c3e50").grid(row=2, column=0, sticky="w", pady=(25, 5))
        
        self.pass_entry = tk.Entry(self.ops_frame, textvariable=self.password, font=("Helvetica", 11), show="*", relief="solid", bd=1)
        self.pass_entry.grid(row=3, column=0, sticky="ew", padx=(0, 15), ipady=6)

        tk.Checkbutton(
            self.ops_frame, text="Show", variable=self.show_password, 
            command=self.toggle_password, bg="#ffffff", font=("Helvetica", 10), cursor="hand2", fg="#2c3e50"
        ).grid(row=3, column=1, sticky="w")

        # Buttons Frame
        btn_frame = tk.Frame(self.ops_frame, bg="#ffffff")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=40)

        tk.Button(
            btn_frame, text="Encrypt File", command=self.handle_encrypt, 
            bg="#e74c3c", fg="white", font=("Helvetica", 12, "bold"), 
            width=16, pady=10, relief="flat", cursor="hand2"
        ).pack(side="left", padx=15)

        tk.Button(
            btn_frame, text="Decrypt File", command=self.handle_decrypt, 
            bg="#27ae60", fg="white", font=("Helvetica", 12, "bold"), 
            width=16, pady=10, relief="flat", cursor="hand2"
        ).pack(side="left", padx=15)

        # Status Label
        self.status_label = tk.Label(
            self.ops_frame, text="Ready", fg="#7f8c8d", bg="#ffffff", font=("Helvetica", 10, "italic")
        )
        self.status_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Integrity Check Info
        self.integrity_label = tk.Label(
            self.ops_frame, text="", fg="#34495e", bg="#ffffff", font=("Courier", 10)
        )
        self.integrity_label.grid(row=6, column=0, columnspan=2)

    def setup_history_tab(self):
        # Treeview frame
        tree_frame = tk.Frame(self.history_frame, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Treeview for history
        columns = ("timestamp", "action", "filename")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("timestamp", text="Date & Time")
        self.tree.heading("action", text="Action")
        self.tree.heading("filename", text="File Name")
        
        self.tree.column("timestamp", width=160, stretch=False)
        self.tree.column("action", width=100, stretch=False)
        self.tree.column("filename", width=350, stretch=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Context Menu / Buttons
        btn_frame = tk.Frame(self.history_frame, bg="#ffffff")
        btn_frame.pack(fill="x", side="bottom")

        tk.Button(
            btn_frame, text="Open File Location", command=self.open_selected_location,
            bg="#9b59b6", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=15, pady=8, cursor="hand2"
        ).pack(side="right")

        tk.Button(
            btn_frame, text="Refresh History", command=self.refresh_history,
            bg="#95a5a6", fg="white", font=("Helvetica", 10, "bold"), relief="flat", padx=15, pady=8, cursor="hand2"
        ).pack(side="right", padx=(0, 15))

        self.refresh_history()

    def refresh_history(self):
        # Clear current tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load and insert data
        history = get_history()
        for entry in history:
            self.tree.insert("", "end", values=(entry["timestamp"], entry["action"], entry["filename"]), tags=(entry["output_path"],))

    def open_selected_location(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a history entry first.")
            return
        
        # Retrieve output_path from tags
        tags = self.tree.item(selected[0], "tags")
        if tags:
            file_path = tags[0]
            if os.path.exists(file_path):
                # Highlight file in explorer
                subprocess.run(['explorer', '/select,', os.path.normpath(file_path)])
            else:
                messagebox.showerror("Error", "File no longer exists at this location.")

    def toggle_password(self):
        if self.show_password.get():
            self.pass_entry.config(show="")
        else:
            self.pass_entry.config(show="*")

    def browse_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.selected_file.set(filename)
            file_hash = get_file_hash(filename)
            self.integrity_label.config(text=f"SHA-256: {file_hash[:32]}...")

    def handle_encrypt(self):
        file_path = self.selected_file.get()
        password = self.password.get()

        if not file_path or not password:
            messagebox.showwarning("Warning", "Please select a file and enter a password.")
            return

        is_strong, msg = check_password_strength(password)
        if not is_strong:
            if not messagebox.askyesno("Weak Password", f"{msg}\n\nDo you still want to proceed?"):
                return

        try:
            self.status_label.config(text="Encrypting...", fg="#e67e22")
            self.root.update_idletasks()
            
            output_path = encrypt_file(file_path, password)
            
            # Log action
            log_action("Encrypted", file_path, output_path)
            self.refresh_history()

            self.status_label.config(text=f"Encrypted: {os.path.basename(output_path)}", fg="#27ae60")
            messagebox.showinfo("Success", f"File encrypted successfully!\nSaved to: {output_path}")
        except Exception as e:
            self.status_label.config(text="Encryption Failed", fg="#c0392b")
            messagebox.showerror("Error", str(e))

    def handle_decrypt(self):
        file_path = self.selected_file.get()
        password = self.password.get()

        if not file_path or not password:
            messagebox.showwarning("Warning", "Please select a file and enter a password.")
            return

        try:
            self.status_label.config(text="Decrypting...", fg="#e67e22")
            self.root.update_idletasks()
            
            output_path = decrypt_file(file_path, password)
            
            # Log action
            log_action("Decrypted", file_path, output_path)
            self.refresh_history()

            self.status_label.config(text=f"Decrypted: {os.path.basename(output_path)}", fg="#27ae60")
            messagebox.showinfo("Success", f"File decrypted successfully!\nSaved to: {output_path}")
        except Exception as e:
            self.status_label.config(text="Decryption Failed", fg="#c0392b")
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
