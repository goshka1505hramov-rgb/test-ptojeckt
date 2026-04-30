import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import os

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.root.geometry("400x550")
        
        self.history_file = "history.json"
        
        # 1. Список предопределённых задач
        self.all_tasks = [
            {"name": "Прочитать главу книги", "type": "Учёба"},
            {"name": "Решить задачу по Python", "type": "Учёба"},
            {"name": "Сделать зарядку", "type": "Спорт"},
            {"name": "Пробежка 3км", "type": "Спорт"},
            {"name": "Разобрать почту", "type": "Работа"},
            {"name": "Подготовить отчет", "type": "Работа"}
        ]
        
        # Загрузка истории при старте
        self.history = self.load_history()
        
        # Интерфейс
        self.setup_ui()

    def setup_ui(self):
        # Выбор категории для фильтрации
        tk.Label(self.root, text="Выберите тип задачи:").pack(pady=5)
        self.filter_var = tk.StringVar(value="Все")
        self.filter_box = ttk.Combobox(self.root, textvariable=self.filter_var, 
                                       values=["Все", "Учёба", "Спорт", "Работа"], state="readonly")
        self.filter_box.pack()

        # Кнопка генерации
        tk.Button(self.root, text="Сгенерировать задачу", command=self.generate_task, bg="#e1e1e1").pack(pady=10)
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12, "bold"), fg="blue", wraplength=350)
        self.result_label.pack(pady=10)

        # Добавление новой задачи
        tk.Label(self.root, text="Добавить свою задачу:", font=("Arial", 10, "bold")).pack(pady=5)
        self.new_task_entry = tk.Entry(self.root, width=30)
        self.new_task_entry.pack()
        self.new_task_type = ttk.Combobox(self.root, values=["Учёба", "Спорт", "Работа"], state="readonly")
        self.new_task_type.pack(pady=5)
        tk.Button(self.root, text="Добавить в список", command=self.add_task).pack()

        # История
        tk.Label(self.root, text="История:", font=("Arial", 10, "bold")).pack(pady=10)
        self.history_list = tk.Listbox(self.root, width=50, height=10)
        self.history_list.pack(padx=10)
        self.update_history_ui()

    def generate_task(self):
        filter_type = self.filter_var.get()
        # Фильтрация
        filtered = [t for t in self.all_tasks if t["type"] == filter_type] if filter_type != "Все" else self.all_tasks
        
        if not filtered:
            messagebox.showwarning("Ошибка", "Нет задач для этой категории!")
            return
            
        task = random.choice(filtered)
        self.result_label.config(text=f"Задача: {task['name']} ({task['type']})")
        
        # Сохранение в историю
        self.history.append(f"{task['name']} ({task['type']})")
        self.save_history()
        self.update_history_ui()

    def add_task(self):
        # 6. Проверка ввода
        name = self.new_task_entry.get().strip()
        t_type = self.new_task_type.get()
        
        if not name:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым!")
            return
        if not t_type:
            messagebox.showerror("Ошибка", "Выберите тип задачи!")
            return
            
        self.all_tasks.append({"name": name, "type": t_type})
        messagebox.showinfo("Успех", f"Задача '{name}' добавлена!")
        self.new_task_entry.delete(0, tk.END)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def update_history_ui(self):
        self.history_list.delete(0, tk.END)
        # Показываем последние 10 задач
        for task in reversed(self.history[-10:]):
            self.history_list.insert(tk.END, task)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()