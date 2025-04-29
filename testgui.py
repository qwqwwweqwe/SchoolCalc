from tkinter import *
from tkinter import ttk, messagebox
import json
import os

win = Tk()
win.state('zoomed')
win.resizable(False, False)
win.title("SchoolCalc")
win.geometry("750x700")
win.configure(bg="#F5F5F5")

main_font = ("Verdana", 14)
title_font = ("Verdana", 24, "bold")
bold_font = ("Verdana", 14, "bold")
bg_color = "#F5F5F5"
text_color = "#333333"
button_color = "#10B981"
button_text = "#FFFFFF"
label_bg = "#FFFFFF"
label_text = "#6B7280"
entry_bg = "#FFFFFF"
entry_text = "#333333"
accent_color = "#F59E0B"

style = ttk.Style()
style.configure("TCombobox", fieldbackground=entry_bg, foreground=entry_text, font=main_font)
style.configure("Treeview", background="#E5E7EB", foreground=text_color, font=main_font, rowheight=30)
style.configure("Treeview.Heading", background="#D1D5DB", foreground=text_color, font=bold_font)

subjects = ["Інформатика", "Історія України", "Алгебра", "Англійська мова", "Біологія","Всесвітня історія", "Географія", "Геометрія", "Математика", "Мистецтво","Технології", "Українська література", "Українська мова", "Фізика","Фізична культура", "Хімія"]
grade_types = ["Звичайна", "Контрольна", "Лабораторна", "Зошит", "Самостійна","Тематичне оцінювання", "Перевірка ДЗ", "Проєкт", "Усний залік","Письмовий залік", "Модульна робота", "Підсумкова оцінка"]

title_label = Label(win, text="Журнал Оцінок", font=title_font, bg=label_bg, fg=accent_color)
title_label.place(relx=0.1, rely=0.05)

subject_label = Label(win, text="Предмет:", font=bold_font, bg=label_bg, fg=label_text)
subject_label.place(relx=0.1, rely=0.15)

subject_combo = ttk.Combobox(win, values=subjects, state="readonly", width=25)
subject_combo.place(relx=0.25, rely=0.15)

grade_type_label = Label(win, text="Тип оцінки:", font=bold_font, bg=label_bg, fg=label_text)
grade_type_label.place(relx=0.1, rely=0.20)

grade_type_combo = ttk.Combobox(win, values=grade_types, state="readonly", width=25)
grade_type_combo.place(relx=0.25, rely=0.20)

grade_label = Label(win, text="Оцінка:", font=bold_font, bg=label_bg, fg=label_text)
grade_label.place(relx=0.1, rely=0.25)

grade_entry = Entry(win, font=main_font, width=25, bg=entry_bg, fg=entry_text, bd=2, relief="flat")
grade_entry.place(relx=0.25, rely=0.25)

add_grade_button = Button(win, text="Додати оцінку", font=main_font, bg=button_color, fg=button_text, bd=0, relief="flat", padx=10, pady=5)
add_grade_button.place(relx=0.25, rely=0.35)

new_subject_label = Label(win, text="Новий предмет:", font=bold_font, bg=label_bg, fg=label_text)
new_subject_label.place(relx=0.1, rely=0.45)

new_subject_entry = Entry(win, font=main_font, width=25, bg=entry_bg, fg=entry_text, bd=2, relief="flat")
new_subject_entry.place(relx=0.25, rely=0.45)

add_subject_button = Button(win, text="Додати предмет", font=main_font, bg=button_color, fg=button_text, bd=0, relief="flat", padx=10, pady=5)
add_subject_button.place(relx=0.25, rely=0.55)

tree_label = Label(win, text="Ваші оцінки", font=bold_font, bg=label_bg, fg=label_text)
tree_label.place(relx=0.1, rely=0.65)

tree = ttk.Treeview(win, columns=("Subject", "GradeType", "Grade", "Average"), show="headings", height=8)
tree.heading("Subject", text="Предмет")
tree.heading("GradeType", text="Тип оцінки")
tree.heading("Grade", text="Оцінка")
tree.heading("Average", text="Середня")
tree.column("Subject", width=200, anchor="w")
tree.column("GradeType", width=150, anchor="center")
tree.column("Grade", width=80, anchor="center")
tree.column("Average", width=80, anchor="center")
tree.place(relx=0.1, rely=0.65, relwidth=0.8, relheight=0.3)
tree.tag_configure("oddrow", background="#F3F4F6")
tree.tag_configure("evenrow", background="#E5E7EB")
tree.tag_configure("subject_row", background="#FBBF24", foreground="#FFFFFF", font=bold_font)

scrollbar = ttk.Scrollbar(win, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.place(relx=0.9, rely=0.65, relheight=0.3)


edit_button = Button(win, text="Редагувати оцінку", font=main_font, bg=button_color, fg=button_text, bd=0, relief="flat", padx=10, pady=5)
edit_button.place(relx=0.5, rely=0.20)

delete_button = Button(win, text="Видалити оцінку", font=main_font, bg=button_color, fg=button_text, bd=0, relief="flat", padx=10, pady=5)
delete_button.place(relx=0.65, rely=0.20)

average_label = Label(win, text="Загальний середній бал: 0", font=title_font, bg=label_bg, fg=accent_color)
average_label.place(relx=0.5, rely=0.05)




grades_data = {}
grade_indices = {}
def load_grades():
    global grades_data, subjects
    with open("grades.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    subjects = data.get("subjects", subjects)
    subject_combo["values"] = subjects
    raw_grades = data.get("grades", {})
    grades_data.clear()
    for subject, grades in raw_grades.items():
        grades_data[subject] = [("Звичайна", str(g)) for g in grades] if grades else []

def save_grades():
    data = {
        "subjects": subjects,
        "grades": {
            subject: [int(g[1]) for g in grades]
            for subject, grades in grades_data.items()
        }
    }
    with open("grades.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def validate_grade(grade):
    return grade.isdigit() and 1 <= int(grade) <= 12

def calculate_subject_average(subject):
    if subject in grades_data and grades_data[subject]:
        return round(sum(int(g[1]) for g in grades_data[subject]) / len(grades_data[subject]), 2)
    return 0

def calculate_total_average():
    all_grades = [(gtype, int(grade)) for grades in grades_data.values() for gtype, grade in grades]
    if not all_grades:
        return 0
    
    weights = {"Контрольна": 0.3,"Лабораторна": 0.25,"Тематичне оцінювання": 0.2,"Модульна робота": 0.15,"Підсумкова оцінка": 0.1,"Звичайна": 0.05,"Зошит": 0.05,"Самостійна": 0.05,"Перевірка ДЗ": 0.05,"Проєкт": 0.1,"Усний залік": 0.05,"Письмовий залік": 0.05}
    total_weighted_sum = sum(grade * weights.get(gtype, 0.05) for gtype, grade in all_grades)
    total_weight = sum(weights.get(gtype, 0.05) for gtype, _ in all_grades)
    
    return round(total_weighted_sum / total_weight, 2) if total_weight > 0 else 0

def update_tree():
    tree.delete(*tree.get_children())
    grade_indices.clear()
    row_index = 0
    for subject in sorted(grades_data.keys()):
        if not grades_data[subject]:
            continue
        avg = calculate_subject_average(subject)
        tree.insert("", "end", values=(subject, "", "", avg), tags=("subject_row",))
        idx = 0
        for gtype, grade in grades_data[subject]:
            tag = "oddrow" if row_index % 2 else "evenrow"
            item_id = tree.insert("", "end", values=(subject, gtype, grade, ""), tags=(tag,))
            grade_indices[item_id] = (subject, idx)
            row_index += 1
            idx += 1
    average_label.config(text=f"Загальний середній бал: {calculate_total_average()}")


def add_grade():
    subject = subject_combo.get()
    gtype = grade_type_combo.get()
    grade = grade_entry.get()
    if not subject or not gtype or not grade:
        messagebox.showerror("Помилка", "Заповніть усі поля!")
        return
    if not validate_grade(grade):
        messagebox.showerror("Помилка", "Оцінка має бути числом від 1 до 12!")
        return
    grades_data.setdefault(subject, []).append((gtype, grade))
    update_tree()
    save_grades()
    grade_entry.delete(0, END)
    grade_type_combo.set("")

def add_new_subject():
    name = new_subject_entry.get().strip()
    if not name:
        messagebox.showerror("Помилка", "Введіть назву предмета!")
        return
    if name in subjects:
        messagebox.showerror("Помилка", "Такий предмет вже існує!")
        return
    subjects.append(name)
    subject_combo["values"] = subjects
    grades_data[name] = []
    new_subject_entry.delete(0, END)
    save_grades()
    messagebox.showinfo("Успіх", f"Предмет '{name}' додано!")

def edit_grade():
    selected = tree.selection()
    if not selected or not tree.item(selected[0])["values"][1]:
        messagebox.showerror("Помилка", "Виберіть оцінку для редагування!")
        return
    item_id = selected[0]
    if item_id not in grade_indices:
        messagebox.showerror("Помилка", "Не вдалося знайти дані оцінки!")
        return
    subject, idx = grade_indices[item_id]
    old_type, old_grade = grades_data[subject][idx]

    edit_win = Toplevel(win)
    edit_win.title("Редагувати оцінку")
    edit_win.geometry("400x300")

    subject_var = StringVar(value=subject)
    type_var = StringVar(value=old_type)
    grade_var = StringVar(value=old_grade)

    ttk.Combobox(edit_win, textvariable=subject_var, values=subjects, state="readonly").pack(pady=10)
    ttk.Combobox(edit_win, textvariable=type_var, values=grade_types, state="readonly").pack(pady=10)
    Entry(edit_win, textvariable=grade_var).pack(pady=10)

    def save_changes():
        new_subject = subject_var.get()
        new_type = type_var.get()
        new_grade = grade_var.get()
        if not new_subject or not new_type or not new_grade:
            messagebox.showerror("Помилка", "Заповніть усі поля!")
            return
        if not validate_grade(new_grade):
            messagebox.showerror("Помилка", "Оцінка має бути числом від 1 до 12!")
            return
        if subject != new_subject:
            grades_data.setdefault(new_subject, []).append((new_type, new_grade))
            grades_data[subject].pop(idx)
            if not grades_data[subject]:
                del grades_data[subject]
        else:
            grades_data[subject][idx] = (new_type, new_grade)
        update_tree()
        save_grades()
        edit_win.destroy()

    Button(edit_win, text="Зберегти", command=save_changes).pack(pady=20)

def delete_grade():
    selected = tree.selection()
    if not selected or not tree.item(selected[0])["values"][1]:
        messagebox.showerror("Помилка", "Виберіть оцінку для видалення!")
        return
    item_id = selected[0]
    if item_id not in grade_indices:
        messagebox.showerror("Помилка", "Не вдалося знайти дані оцінки!")
        return
    subject, idx = grade_indices[item_id]
    grades_data[subject].pop(idx)
    if not grades_data[subject]:
        del grades_data[subject]
    update_tree()
    save_grades()


load_grades()
update_tree()
add_grade_button.config(command=add_grade)
add_subject_button.config(command=add_new_subject)
edit_button.config(command=edit_grade)
delete_button.config(command=delete_grade)
win.mainloop()