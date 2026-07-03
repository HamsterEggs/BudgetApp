from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
import sqlite3
import os
import datetime


CATEGORY_OPTIONS = ["Rent", "Going Out", "Food", "Gym", "Meds", "Misc", "Hobbies", "Uni", "Income", "Savings"]


class MainWidget(BoxLayout):
    pass


class BudgetAndroidApp(App):
    def build(self):
        self.title = "Budget App"
        # DB in user_data_dir so it persists on device
        self.db_path = os.path.join(self.user_data_dir, "budget_data.db")
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()

        root = BoxLayout(orientation='vertical', padding=8, spacing=8)

        form = GridLayout(cols=4, size_hint_y=None, height=160, spacing=6)

        self.date_input = TextInput(text=datetime.date.today().isoformat(), multiline=False)
        self.type_spinner = Spinner(text='Expense', values=['Expense', 'Income'], size_hint_x=None, width=140)
        self.amount_input = TextInput(hint_text='Amount', input_filter='float', multiline=False)
        self.category_spinner = Spinner(text=CATEGORY_OPTIONS[0], values=CATEGORY_OPTIONS, size_hint_x=None, width=160)
        self.desc_input = TextInput(hint_text='Description', multiline=False)

        form.add_widget(Label(text='Date'))
        form.add_widget(self.date_input)
        form.add_widget(Label(text='Type'))
        form.add_widget(self.type_spinner)

        form.add_widget(Label(text='Amount'))
        form.add_widget(self.amount_input)
        form.add_widget(Label(text='Category'))
        form.add_widget(self.category_spinner)

        form.add_widget(Label(text='Description'))
        form.add_widget(self.desc_input)
        form.add_widget(Widget())
        add_btn = Button(text='Add Transaction')
        add_btn.bind(on_press=self.add_transaction)
        form.add_widget(add_btn)

        root.add_widget(form)

        self.totals_label = Label(text='Income: $0.00   Expense: $0.00   Balance: $0.00   Saved: $0.00', size_hint_y=None, height=30)
        root.add_widget(self.totals_label)

        self.list_layout = GridLayout(cols=1, size_hint_y=None)
        self.list_layout.bind(minimum_height=self.list_layout.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.list_layout)
        root.add_widget(scroll)

        self.refresh_transactions()

        return root

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS transactions ("
                "id INTEGER PRIMARY KEY, "
                "date TEXT NOT NULL, "
                "type TEXT NOT NULL, "
                "amount REAL NOT NULL, "
                "category TEXT NOT NULL, "
                "description TEXT, "
                "year_month TEXT NOT NULL"
                ")"
            )

    def add_transaction(self, instance):
        date_text = self.date_input.text.strip()
        tx_type = self.type_spinner.text
        amount_text = self.amount_input.text.strip()
        category = self.category_spinner.text
        description = self.desc_input.text.strip()

        try:
            datetime.datetime.strptime(date_text, "%Y-%m-%d")
        except Exception:
            date_text = datetime.date.today().isoformat()

        try:
            amount = float(amount_text)
        except Exception:
            return

        year_month = date_text[:7]
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO transactions (date, type, amount, category, description, year_month) VALUES (?, ?, ?, ?, ?, ?)",
                (date_text, tx_type, amount, category, description, year_month),
            )

        self.amount_input.text = ''
        self.desc_input.text = ''
        self.refresh_transactions()

    def refresh_transactions(self):
        self.list_layout.clear_widgets()
        txs = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT date, type, amount, category, description FROM transactions ORDER BY date DESC")
            txs = cursor.fetchall()

        income_total = 0.0
        expense_total = 0.0
        saved_total = 0.0
        for row in txs:
            date, tx_type, amount, category, description = row
            if tx_type == 'Income':
                income_total += amount
            else:
                expense_total += abs(amount)
            if category == 'Savings':
                saved_total += amount
            lbl = Label(text=f"{date} | {tx_type} | ${amount:.2f} | {category} | {description}", size_hint_y=None, height=30)
            self.list_layout.add_widget(lbl)

        balance = income_total - expense_total
        self.totals_label.text = f"Income: ${income_total:.2f}   Expense: ${expense_total:.2f}   Balance: ${balance:.2f}   Saved: ${saved_total:.2f}"


if __name__ == '__main__':
    BudgetAndroidApp().run()
