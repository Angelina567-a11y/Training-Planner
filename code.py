import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []

        self.create_widgets()

    def create_widgets(self):
        # Ввод данных
        frame_input = tk.Frame(self.root)
        frame_input.pack(padx=10, pady=5)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=2)
        self.entry_date = tk.Entry(frame_input)
        self.entry_date.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=2)
        self.entry_type = tk.Entry(frame_input)
        self.entry_type.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_input, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=2)
        self.entry_duration = tk.Entry(frame_input)
        self.entry_duration.grid(row=2, column=1, padx=5, pady=2)

        btn_add = tk.Button(frame_input, text="Добавить тренировку", command=self.add_training)
        btn_add.grid(row=3, column=0, columnspan=2, pady=5)

        # Поля фильтрации
        frame_filter = tk.Frame(self.root)
        frame_filter.pack(padx=10, pady=5)

        tk.Label(frame_filter, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5)
        self.filter_date = tk.Entry(frame_filter)
        self.filter_date.grid(row=0, column=1, padx=5)

        tk.Label(frame_filter, text="Фильтр по типу:").grid(row=0, column=2, padx=5)
        self.filter_type = tk.Entry(frame_filter)
        self.filter_type.grid(row=0, column=3, padx=5)

        btn_filter = tk.Button(frame_filter, text="Фильтровать", command=self.apply_filter)
        btn_filter.grid(row=0, column=4, padx=5)

        btn_reset = tk.Button(frame_filter, text="Сбросить фильтр", command=self.reset_filter)
        btn_reset.grid(row=0, column=5, padx=5)

        # Таблица тренировок
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность, мин")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Кнопки для сохранения/загрузки
        frame_file = tk.Frame(self.root)
        frame_file.pack(padx=10, pady=5)

        btn_save = tk.Button(frame_file, text="Сохранить в JSON", command=self.save_to_json)
        btn_save.pack(side=tk.LEFT, padx=5)

        btn_load = tk.Button(frame_file, text="Загрузить из JSON", command=self.load_from_json)
        btn_load.pack(side=tk.LEFT, padx=5)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def add_training(self):
        date_str = self.entry_date.get().strip()
        t_type = self.entry_type.get().strip()
        duration_str = self.entry_duration.get().strip()

        # Валидация
        if not self.validate_date(date_str):
            messagebox.showerror("Ошибка", "Некорректный формат даты.")
            return
        if not t_type:
            messagebox.showerror("Ошибка", "Введите тип тренировки.")
            return
        if not duration_str.isdigit() or int(duration_str) <= 0:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
            return

        training = {
            "date": date_str,
            "type": t_type,
            "duration": int(duration_str)
        }
        self.trainings.append(training)
        self.update_table(self.trainings)
        self.clear_entries()

    def clear_entries(self):
        self.entry_date.delete(0, tk.END)
        self.entry_type.delete(0, tk.END)
        self.entry_duration.delete(0, tk.END)

    def update_table(self, trainings):
        self.tree.delete(*self.tree.get_children())
        for t in trainings:
            self.tree.insert("", tk.END, values=(t["date"], t["type"], t["duration"]))

    def save_to_json(self):
        filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены.")

    def load_from_json(self):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                self.trainings = json.load(f)
            self.update_table(self.trainings)

    def apply_filter(self):
        date_filter = self.filter_date.get().strip()
        type_filter = self.filter_type.get().strip().lower()

        filtered = self.trainings
        if date_filter:
            if not self.validate_date(date_filter):
                messagebox.showerror("Ошибка", "Некорректный формат даты фильтра.")
                return
            filtered = [t for t in filtered if t["date"] == date_filter]
        if type_filter:
            filtered = [t for t in filtered if type_filter in t["type"].lower()]

        self.update_table(filtered)

    def reset_filter(self):
        self.filter_date.delete(0, tk.END)
        self.filter_type.delete(0, tk.END)
        self.update_table(self.trainings)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()