import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os

class SchoolCalc:
    def __init__(self, root):
        self.root = root
        self.root.title("SchoolCalc")
        self.root.geometry("750x700")
        self.root.configure(bg="#0F111A")
        
        self.heading_font = ("Segoe UI", 13, "bold")
        self.normal_font = ("Segoe UI", 11)
        self.bold_font = ("Segoe UI", 11, "bold")
        self.large_font = ("Segoe UI", 16, "bold")
        self.title_font = ("Segoe UI", 20, "bold")

        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.bg_color = "#0F111A"
        self.primary_color = "#1A237E"
        self.secondary_color = "#131A2B"
        self.accent_color = "#F44336"
        self.text_color = "#ECEFF1"
        self.field_bg = "#1E2132"
        self.highlight_color = "#3F51B5"
        self.success_color = "#43A047"
        
        self.configure_styles()
        
        self.data_file = "grades.json"
        self.data = {}
        self.subjects = []
        self.default_subjects = ["Українська мова", "Українська література", "Англійська мова", "Математика", "Алгебра", "Геометрія", "Фізика", "Хімія", "Біологія", "Історія України", "Всесвітня історія", "Географія", "Інформатика", "Фізична культура", "Мистецтво", "Технології"]
        self.load_data()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)

        self.create_interface()
        
        self.update_subject_combo()
        self.update_tree()
        
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.grade_entry.bind("<Return>", lambda event: self.add_grade())
        self.new_subject_entry.bind("<Return>", lambda event: self.add_subject())
        
        self.edit_button.state(["disabled"])
        self.delete_button.state(["disabled"])
    
    def configure_styles(self):
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("TLabel", background=self.bg_color, foreground=self.text_color, font=self.normal_font)
        self.style.configure("Heading.TLabel", background=self.bg_color, foreground=self.text_color, font=self.heading_font)
        self.style.configure("Title.TLabel", background=self.bg_color, foreground=self.accent_color, font=self.title_font)
        
        self.style.configure("TButton", background=self.primary_color, foreground=self.text_color, 
                            font=self.bold_font, padding=8, borderwidth=0)
        self.style.map("TButton", background=[('active', self.highlight_color), ('pressed', self.highlight_color)],
                      foreground=[('active', self.text_color)])
        
        self.style.configure("Primary.TButton", background=self.accent_color, foreground=self.text_color, 
                            font=self.bold_font, padding=10)
        self.style.map("Primary.TButton", background=[('active', '#E53935'), ('pressed', '#C62828')])

        self.style.configure("Danger.TButton", background="#D32F2F", foreground=self.text_color, 
                            font=self.bold_font, padding=10)
        self.style.map("Danger.TButton", background=[('active', '#F44336'), ('pressed', '#B71C1C')])
        
        self.style.configure("Success.TButton", background=self.success_color, foreground=self.text_color, 
                            font=self.bold_font, padding=10)
        self.style.map("Success.TButton", background=[('active', '#4CAF50'), ('pressed', '#2E7D32')])
        
        self.style.configure("TCombobox", background=self.field_bg, foreground=self.text_color, 
                            font=self.normal_font, fieldbackground=self.field_bg, padding=10)
        self.style.map("TCombobox", fieldbackground=[('readonly', self.field_bg)],
                      selectbackground=[('readonly', self.primary_color)])
        
        self.style.configure("TEntry", fieldbackground=self.field_bg, foreground=self.text_color, 
                            font=self.normal_font, padding=10)
        
        self.style.configure("Treeview", background=self.secondary_color, foreground=self.text_color, 
                            font=self.normal_font, rowheight=38, fieldbackground=self.secondary_color)
        self.style.configure("Treeview.Heading", background=self.primary_color, foreground=self.text_color, 
                            font=self.bold_font, padding=10)
        self.style.map("Treeview.Heading", background=[('active', self.highlight_color)])
        
        self.style.configure("TSeparator", background=self.accent_color)
        
        self.style.configure("Vertical.TScrollbar", background=self.primary_color, troughcolor=self.bg_color, 
                            borderwidth=0, arrowsize=16)
        self.style.map("Vertical.TScrollbar", background=[('active', self.highlight_color)])
    
    def create_interface(self):
        title_frame = ttk.Frame(self.root, padding="20 20 20 5")
        title_frame.grid(row=0, column=0, sticky="ew")
        title_label = ttk.Label(title_frame, text="Журнал Оцінок", style="Title.TLabel")
        title_label.pack(anchor="center")
        
        separator_title = ttk.Separator(self.root, orient="horizontal")
        separator_title.grid(row=1, column=0, sticky="ew", padx=20)

        input_frame = ttk.Frame(self.root, padding="30 20 30 15")
        input_frame.grid(row=2, column=0, sticky="new")
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Предмет:", style="Heading.TLabel").grid(row=0, column=0, padx=(0, 15), pady=10, sticky="w")
        self.subject_combo = ttk.Combobox(input_frame, values=self.subjects, state="readonly", width=30)
        self.subject_combo.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

        ttk.Label(input_frame, text="Оцінка:", style="Heading.TLabel").grid(row=1, column=0, padx=(0, 15), pady=10, sticky="w")
        self.grade_entry = ttk.Entry(input_frame, width=30)
        self.grade_entry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

        self.add_grade_button = ttk.Button(input_frame, text="Додати оцінку", command=self.add_grade, style="Primary.TButton")
        self.add_grade_button.grid(row=2, column=0, columnspan=2, padx=5, pady=(20, 10))

        separator = ttk.Separator(input_frame, orient="horizontal")
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=20)
        
        ttk.Label(input_frame, text="Новий предмет:", style="Heading.TLabel").grid(row=4, column=0, padx=(0, 15), pady=10, sticky="w")
        self.new_subject_entry = ttk.Entry(input_frame, width=30)
        self.new_subject_entry.grid(row=4, column=1, padx=5, pady=10, sticky="ew")
        self.add_subject_button = ttk.Button(input_frame, text="Додати предмет", command=self.add_subject, style="Success.TButton")
        self.add_subject_button.grid(row=5, column=0, columnspan=2, padx=5, pady=15)

        tree_frame = ttk.Frame(self.root, padding="30 10 30 15")
        tree_frame.grid(row=3, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(1, weight=1)
        
        ttk.Label(tree_frame, text="Ваші оцінки", style="Heading.TLabel").grid(row=0, column=0, sticky="w", pady=(5, 15))

        tree_container = ttk.Frame(tree_frame, borderwidth=1, relief="solid")
        tree_container.grid(row=1, column=0, sticky="nsew")
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_container, columns=("Subject", "Grade", "Average"), show="headings", height=10)
        self.tree.heading("Subject", text="Предмет")
        self.tree.heading("Grade", text="Оцінка")
        self.tree.heading("Average", text="Середня")
        self.tree.column("Subject", width=320, anchor="w")
        self.tree.column("Grade", width=100, anchor="center")
        self.tree.column("Average", width=100, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.tag_configure('oddrow', background="#1E2132")
        self.tree.tag_configure('evenrow', background="#181D2A")
        self.tree.tag_configure('subject_row', background="#1A237E", font=self.bold_font)

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        button_frame = ttk.Frame(self.root, padding="30 15 30 15")
        button_frame.grid(row=4, column=0, sticky="ew")
        button_frame.columnconfigure((0, 1), weight=1)

        self.edit_button = ttk.Button(button_frame, text="Редагувати оцінку", command=self.edit_grade)
        self.edit_button.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")

        self.delete_button = ttk.Button(button_frame, text="Видалити оцінку", command=self.delete_grade, style="Danger.TButton")
        self.delete_button.grid(row=0, column=1, padx=(10, 0), pady=5, sticky="ew")

        info_frame = ttk.Frame(self.root, padding="30 20 30 25")
        info_frame.grid(row=5, column=0, sticky="ew")
        info_frame.columnconfigure(0, weight=1)
        
        separator_avg = ttk.Separator(info_frame, orient="horizontal")
        separator_avg.grid(row=0, column=0, sticky="ew", pady=10)

        self.average_label = ttk.Label(info_frame, text="Загальний середній бал: 0", anchor="center", font=self.large_font, foreground=self.accent_color)
        self.average_label.grid(row=1, column=0, sticky="ew", pady=15)

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item_id = selected[0]
            item_values = self.tree.item(item_id, 'values')
            if len(item_values) >= 3 and item_values[1]:
                self.edit_button.state(["!disabled"])
                self.delete_button.state(["!disabled"])
            else:
                self.edit_button.state(["disabled"])
                self.delete_button.state(["disabled"])
        else:
            self.edit_button.state(["disabled"])
            self.delete_button.state(["disabled"])

    def add_subject(self):
        new_subject = self.new_subject_entry.get().strip()
        if new_subject:
            if new_subject not in self.subjects:
                self.subjects.append(new_subject)
                self.subjects.sort()
                if new_subject not in self.data["grades"]:
                    self.data["grades"][new_subject] = []
                self.update_subject_combo()
                self.save_data()
                self.new_subject_entry.delete(0, tk.END)
                messagebox.showinfo("Успіх", f"Предмет '{new_subject}' додано.", parent=self.root)
            else:
                messagebox.showwarning("Дублікат", f"Предмет '{new_subject}' вже існує.", parent=self.root)
        else:
            messagebox.showerror("Помилка", "Назва предмета не може бути порожньою.", parent=self.root)

    def update_subject_combo(self):
         self.subject_combo['values'] = self.subjects
         if self.subjects:
             current_selection = self.subject_combo.get()
             if current_selection in self.subjects:
                 self.subject_combo.set(current_selection)
             else:
                 self.subject_combo.current(0)
         else:
             self.subject_combo.set('')

    def add_grade(self):
        subject = self.subject_combo.get()
        grade_str = self.grade_entry.get().strip()
        if not subject:
            messagebox.showerror("Помилка", "Будь ласка, виберіть або додайте предмет спочатку.", parent=self.root)
            return
        if not grade_str:
             messagebox.showerror("Помилка", "Будь ласка, введіть оцінку.", parent=self.root)
             return

        try:
            grade = int(grade_str)
            if 1 <= grade <= 12:
                if subject not in self.data["grades"]:
                    self.data["grades"][subject] = []
                self.data["grades"][subject].append(grade)
                self.save_data()
                self.update_tree()
                self.grade_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Помилка", "Оцінка повинна бути цілим числом від 1 до 12.", parent=self.root)
        except ValueError:
            messagebox.showerror("Помилка", "Недійсний формат оцінки. Будь ласка, введіть ціле число.", parent=self.root)

    def edit_grade(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Помилка вибору", "Будь ласка, виберіть оцінку для редагування.", parent=self.root)
            return

        item_id = selected_items[0]
        item_values = self.tree.item(item_id, 'values')
        
        if len(item_values) < 3 or not item_values[1]:
            messagebox.showwarning("Помилка вибору", "Будь ласка, виберіть оцінку для редагування.", parent=self.root)
            return
            
        subject = item_values[0]
        original_grade_str = item_values[1]

        try:
            original_grade = int(original_grade_str)
            grade_list = self.data["grades"][subject]
            try:
                original_index = self.tree.item(item_id, 'tags')[1]
                original_index = int(original_index)
                if grade_list[original_index] != original_grade:
                     raise ValueError("Невідповідність оцінки - дані можуть бути несинхронізовані")
            except (IndexError, ValueError, TypeError):
                 original_index = grade_list.index(original_grade)

            new_grade_str = simpledialog.askstring("Редагувати оцінку", f"Введіть нову оцінку для {subject}:",
                                                   initialvalue=original_grade_str, parent=self.root)

            if new_grade_str is not None:
                try:
                    new_grade = int(new_grade_str.strip())
                    if 1 <= new_grade <= 12:
                        self.data["grades"][subject][original_index] = new_grade
                        self.save_data()
                        self.update_tree()
                        messagebox.showinfo("Успіх", "Оцінку успішно оновлено.", parent=self.root)
                    else:
                        messagebox.showerror("Помилка", "Оцінка повинна бути цілим числом від 1 до 12.", parent=self.root)
                except ValueError:
                    messagebox.showerror("Помилка", "Недійсний формат оцінки. Будь ласка, введіть ціле число.", parent=self.root)
        except (IndexError, ValueError, KeyError) as e:
             messagebox.showerror("Помилка", f"Не вдалося обробити вибрану оцінку: {e}\nДані можуть бути несумісними.", parent=self.root)

    def delete_grade(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Помилка вибору", "Будь ласка, виберіть оцінку для видалення.", parent=self.root)
            return

        item_id = selected_items[0]
        item_values = self.tree.item(item_id, 'values')
        
        if len(item_values) < 3 or not item_values[1]:
            messagebox.showwarning("Помилка вибору", "Будь ласка, виберіть оцінку для видалення.", parent=self.root)
            return
            
        subject = item_values[0]
        grade_to_delete_str = item_values[1]

        confirm = messagebox.askyesno("Підтвердження видалення",
                                      f"Ви впевнені, що хочете видалити оцінку '{grade_to_delete_str}' для предмета '{subject}'?",
                                      parent=self.root)

        if confirm:
            try:
                grade_to_delete = int(grade_to_delete_str)
                grade_list = self.data["grades"][subject]

                try:
                    original_index = self.tree.item(item_id, 'tags')[1]
                    original_index = int(original_index)
                    if grade_list[original_index] != grade_to_delete:
                         raise ValueError("Невідповідність оцінки - дані можуть бути несинхронізовані")
                    del grade_list[original_index]
                except (IndexError, ValueError, TypeError):
                    grade_list.remove(grade_to_delete)

                self.save_data()
                self.update_tree()
                messagebox.showinfo("Успіх", "Оцінку успішно видалено.", parent=self.root)
            except (IndexError, ValueError, KeyError) as e:
                 messagebox.showerror("Помилка", f"Не вдалося виконати видалення: {e}", parent=self.root)

    def calculate_average(self, grades):
        if not grades:
            return 0
        try:
            return round(sum(grades) / len(grades))
        except (ValueError, TypeError):
            return 0

    def calculate_overall_average(self):
        total_grades = []
        if "grades" in self.data:
            for subject in self.data["grades"]:
                total_grades.extend(self.data["grades"][subject])
        return self.calculate_average(total_grades)

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        if "grades" in self.data:
            row_index = 0
            sorted_subjects = sorted(self.data["grades"].keys())
            
            for subject in sorted_subjects:
                grades = self.data["grades"][subject]
                
                if grades:
                    subject_avg = self.calculate_average(grades)
                    
                    subject_id = self.tree.insert("", tk.END, 
                                               values=(subject, "", f"{subject_avg}"), 
                                               tags=('subject_row'))
                    row_index += 1
                    
                    for idx, grade in enumerate(grades):
                        try:
                            tag = 'evenrow' if row_index % 2 == 0 else 'oddrow'
                            self.tree.insert("", tk.END, 
                                          values=(subject, f"{grade}", ""), 
                                          tags=(tag, str(idx)))
                            row_index += 1
                        except (ValueError, TypeError):
                            pass

        overall_average = self.calculate_overall_average()
        self.average_label.config(text=f"Загальний середній бал: {overall_average}")
        
        if not self.tree.get_children():
            self.edit_button.state(["disabled"])
            self.delete_button.state(["disabled"])

    def load_data(self):
        default_data = {"subjects": self.default_subjects, "grades": {}}
        
        if not os.path.exists(self.data_file):
            self.data = default_data
            self.subjects = self.data["subjects"][:]
            self.save_data()
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                loaded_data = json.load(f)

            if isinstance(loaded_data, dict) and \
               "subjects" in loaded_data and isinstance(loaded_data["subjects"], list) and \
               "grades" in loaded_data and isinstance(loaded_data["grades"], dict):
                self.data = loaded_data
                self.subjects = self.data.get("subjects", [])
                for subj in self.subjects:
                    if subj not in self.data["grades"]:
                        self.data["grades"][subj] = []
                grade_keys = list(self.data["grades"].keys())
                for key in grade_keys:
                    if key not in self.subjects:
                         self.subjects.append(key)

                self.subjects.sort()
            else:
                self.backup_and_reset_data()

        except (json.JSONDecodeError, IOError) as e:
            self.backup_and_reset_data()

        if "grades" not in self.data or not isinstance(self.data["grades"], dict):
            self.data["grades"] = {}
        if "subjects" not in self.data or not isinstance(self.data["subjects"], list):
             self.data["subjects"] = sorted(list(self.data.get("grades", {}).keys()))
        self.subjects = self.data["subjects"]

    def backup_and_reset_data(self):
        default_data = {"subjects": self.default_subjects, "grades": {}}
        
        if os.path.exists(self.data_file):
            try:
                backup_file = self.data_file + ".bak"
                os.rename(self.data_file, backup_file)
            except OSError as backup_err:
                messagebox.showerror("Помилка створення резервної копії", f"Не вдалося створити резервну копію: {backup_err}", parent=self.root)
        
        self.data = default_data
        self.subjects = self.data["subjects"][:]
        self.save_data()

    def save_data(self):
        self.data["subjects"] = sorted(list(set(self.subjects)))
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
        except IOError as e:
             messagebox.showerror("Помилка збереження", f"Не вдалося зберегти дані у {self.data_file}: {e}", parent=self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolCalc(root)
    root.mainloop()