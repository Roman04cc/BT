import tkinter as tk
import calendar
from datetime import datetime  # Корректный импорт

class BusinessTrackerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Business Tracker")

        # Цвета на основе RGB
        self.bg_color = "#C8C8C8"  # RGB(110, 30, 60)
        self.title_color = "#821E28"  # RGB(130, 30, 40)
        self.budget_color = "#FF5050"  # RGB(255, 80, 80)
        self.expense_color = "#C8C8C8"  # RGB(200, 200, 200)

        self.cell_width = 70
        self.cell_height = 50
        self.salary_day = 15  # Установите день зарплаты по умолчанию
        self.salary = 0  # Сумма зарплаты

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.expenses = {}  # Словарь для хранения расходов

        self.setup_ui()
        self.draw_calendar()

    def setup_ui(self):
        self.master.configure(bg=self.bg_color)

        # Создание заголовка
        self.title_label = tk.Label(self.master, text="Календарь Бизнеса", font=("Arial", 16), bg=self.bg_color, fg=self.title_color)
        self.title_label.pack(pady=10)

        # Создание виджетов интерфейса
        self.calendar_frame = tk.Frame(self.master, bg=self.bg_color)
        self.calendar_frame.pack()

        self.calendar_widget = tk.Canvas(self.calendar_frame, width=500, height=400, bg=self.bg_color)
        self.calendar_widget.pack()

        self.month_label = tk.Label(self.master, text=f"{calendar.month_name[self.current_month]} {self.current_year}", font=("Arial", 14), bg=self.bg_color, fg=self.title_color)
        self.month_label.pack(pady=10)

        # Поле для ввода суммы зарплаты
        self.salary_label = tk.Label(self.master, text="Установите сумму зарплаты:", bg=self.bg_color, fg=self.title_color)
        self.salary_label.pack()

        self.salary_entry = tk.Entry(self.master, width=10, bg=self.expense_color)
        self.salary_entry.pack(pady=5)
        self.salary_entry.bind("<Return>", self.set_salary)

        # Поле для ввода дня зарплаты
        self.salary_day_label = tk.Label(self.master, text="Установите день зарплаты (1-31):", bg=self.bg_color, fg=self.title_color)
        self.salary_day_label.pack()

        self.salary_day_entry = tk.Entry(self.master, width=5, bg=self.expense_color)
        self.salary_day_entry.pack(pady=5)
        self.salary_day_entry.bind("<Return>", self.set_salary_day)

        self.button_frame = tk.Frame(self.master, bg=self.bg_color)
        self.button_frame.pack(pady=10)

        self.prev_button = tk.Button(self.button_frame, text="Пред. месяц", command=self.prev_month, width=10, bg=self.title_color, fg="white")
        self.prev_button.pack(side=tk.LEFT, padx=5)

        self.next_button = tk.Button(self.button_frame, text="След. месяц", command=self.next_month, width=10, bg=self.title_color, fg="white")
        self.next_button.pack(side=tk.RIGHT, padx=5)

    def draw_calendar(self):
        self.calendar_widget.delete("all")  # Очистка предыдущего календаря
        days_in_month = calendar.monthrange(self.current_year, self.current_month)[1]
        week_height = 50

        # Заголовки дней недели
        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for idx, day in enumerate(days):
            x = self.cell_width * idx + 5
            self.calendar_widget.create_text(x + self.cell_width / 2, 10, text=day, font=("Arial", 10, 'bold'), fill=self.title_color)

        for day in range(1, days_in_month + 1):
            row = (day + calendar.monthrange(self.current_year, self.current_month)[0]) // 7
            
            col = (day + calendar.monthrange(self.current_year, self.current_month)[0]) % 7
            
            x = self.cell_width * col
            y = week_height + row * self.cell_height

            # Создание ячейки для дня
            self.calendar_widget.create_rectangle(
                x, y, x + self.cell_width, y + self.cell_height, fill=self.bg_color, outline="black"
            )

            # Создание текста с номером дня
            self.calendar_widget.create_text(
                x + self.cell_width / 2,
                y + self.cell_height / 2,
                text=day,
                font=("Arial", 12),
                fill="black",
                anchor=tk.CENTER,
            )

            # Проверяем, является ли этот день днем зарплаты
            if day == self.salary_day:
                self.calendar_widget.create_oval(
                    x + self.cell_width / 2 - 5,
                    y + self.cell_height / 2 - 5,
                    x + self.cell_width / 2 + 5,
                    y + self.cell_height / 2 + 5,
                    fill="#000000",  # Цвет зарплаты
                    outline=""
                )

            # Вычисление дневного бюджета и расходов
            date = f"{self.current_year}-{self.current_month:02d}-{day:02d}"
            daily_budget = self.get_daily_budget(day)
            daily_expenses = self.get_daily_expenses(date)

            if daily_budget > 0:
                self.calendar_widget.create_text(
                    x + 5,
                    y + self.cell_height - 5,
                    text=f"{daily_budget:.2f} ₽",
                    font=("Arial", 8),
                    fill=self.budget_color,
                    anchor=tk.SW,
                )

            if daily_expenses > 0:
                self.calendar_widget.create_text(
                    x + self.cell_width - 5,
                    y + 5,
                    text=f"-{daily_expenses:.2f} ₽",
                    font=("Arial", 8),
                    fill="red",
                    anchor=tk.NE,
                )

    def set_salary(self, event):
        try:
            self.salary = float(self.salary_entry.get())
            self.draw_calendar()  # Обновляем календарь после ввода зарплаты
            self.salary_label.config(text="Установите сумму зарплаты:", fg=self.title_color)
        except ValueError:
            self.salary_label.config(text="Ошибка: введите число.", fg="red")

    def set_salary_day(self, event):
        try:
            self.salary_day = int(self.salary_day_entry.get())
            if 1 <= self.salary_day <= 31:
                self.draw_calendar()
                self.salary_day_label.config(text="Установите день зарплаты (1-31):", fg=self.title_color)
            else:
                self.salary_day_label.config(text="Ошибка: введите число от 1 до 31.", fg="red")
        except ValueError:
            self.salary_day_label.config(text="Ошибка: введите целое число.", fg="red")

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        self.draw_calendar()

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.month_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        self.draw_calendar()

    def get_daily_budget(self, day):
        total_days = (self.days_until_next_salary() + self.salary_day - day) if self.salary_day >= day else (self.days_in_current_month() - day) + self.salary_day
        return self.salary / total_days if total_days > 0 else 0

    def days_until_next_salary(self):
        if self.salary_day is None:
            return 0
        today = datetime.now().day  # Исправлено, теперь правильный импорт
        
        days_in_current_month = calendar.monthrange(self.current_year, self.current_month)[1]
        if today < self.salary_day:
            return self.salary_day - today
        return (days_in_current_month - today) + self.salary_day

    def days_in_current_month(self):
        return calendar.monthrange(self.current_year, self.current_month)[1]

    def get_daily_expenses(self, date):
        return self.expenses.get(date, 0)  # Возвращает 0, если дата не найдена

    def add_expense(self, date, amount):
        if date in self.expenses:
            self.expenses[date] += amount
        else:
            self.expenses[date] = amount


if __name__ == "__main__":
    root = tk.Tk()
    app = BusinessTrackerApp(root)
    root.mainloop()
