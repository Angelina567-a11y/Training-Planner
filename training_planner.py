import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "trainings.json"

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.data = []

        self.load_data()

        self.create_widgets()
        self.populate_table()

    def create_widgets(self):
        # Ввод данных
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame)
        self.date_entry.grid(row=0, column=1)

        tk.Label(frame, text="Тип тренировки:").grid(row=1, column=0)
        self.type_entry = tk.Entry(frame)
        self.type_entry.grid(row=1, column=1)

        tk.Label(frame, text="Длительность (мин):").grid(row=2, column=0)
        self.duration_entry = tk.Entry(frame)
        self.duration_entry.grid(row=2, column=1)

        # Кнопка добавления
        add_btn = tk.Button(frame, text="Добавить тренировку", command=self.add_training)
        add_btn.grid(row=3, column=0, columnspan=2, pady=5)

        # Таблица
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(padx=10, pady=10)

        # Фильтр
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(padx=10, pady=10)

        tk.Label(filter_frame, text="Фильтр по типу:").grid(row=0, column=0)
        self.type_filter = tk.Entry(filter_frame)
        self.type_filter.grid(row=0, column=1)
        tk.Button(filter_frame, text="Применить", command=self.filter_type).grid(row=0, column=2)

        tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=1, column=0)
        self.date_filter = tk.Entry(filter_frame)
        self.date_filter.grid(row=1, column=1)
        tk.Button(filter_frame, text="Применить", command=self.filter_date).grid(row=1, column=2)

        tk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).grid(row=2, column=0, columnspan=3, pady=5)

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = []

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def populate_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if data is None:
            data = self.data
        for item in data:
            self.tree.insert("", "end", values=(item['date'], item['type'], item['duration']))

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_duration(self, duration_text):
        try:
            return int(duration_text) > 0
        except ValueError:
            return False

    def add_training(self):
        date = self.date_entry.get()
        t_type = self.type_entry.get()
        duration = self.duration_entry.get()

        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        if not self.validate_duration(duration):
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        self.data.append({"date": date, "type": t_type, "duration": duration})
        self.save_data()
        self.populate_table()

        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)

    def filter_type(self):
        t_type = self.type_filter.get()
        filtered = [item for item in self.data if item['type'] == t_type]
        self.populate_table(filtered)

    def filter_date(self):
        date_filter = self.date_filter.get()
        if not self.validate_date(date_filter):
            messagebox.showerror("Ошибка", "Некорректный формат даты фильтра.")
            return
        filtered = [item for item in self.data if item['date'] == date_filter]
        self.populate_table(filtered)

    def reset_filters(self):
        self.populate_table()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
