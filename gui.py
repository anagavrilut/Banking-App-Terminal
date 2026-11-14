
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import database


# ==================================================
# CONFIGURATION
# ==================================================

BG = "#080E1C"
SIDEBAR = "#0D1728"
PANEL = "#111D31"
PANEL_LIGHT = "#192A42"
BORDER = "#29445F"

CYAN = "#42DFFF"
PURPLE = "#A78BFA"
GREEN = "#40E6A0"
RED = "#FF647C"

WHITE = "#F0F7FF"
TEXT = "#A5B8CE"
MUTED = "#647B98"

USERS = {
    "admin": "1234",
    "user": "0000"
}

root = tk.Tk()
root.title("Crest Bank")
root.geometry("1200x800")
root.minsize(950, 680)
root.configure(bg=BG)

current_user = {"name": ""}


# ==================================================
# DATABASE OPERATIONS
# ==================================================

def get_transactions():
    return database.get_transactions()


def update_transaction(transaction_id, day, amount, transaction_type):
    connection = sqlite3.connect("crest_bank.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET day = ?, amount = ?, type = ?
        WHERE id = ?
    """, (day, amount, transaction_type, transaction_id))

    connection.commit()
    connection.close()


def delete_transaction(transaction_id):
    connection = sqlite3.connect("crest_bank.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()


# ==================================================
# FINANCIAL CALCULATIONS
# ==================================================

def calculate_balance(transactions):
    return sum(
        t[2] if t[3] == "intrare" else -t[2]
        for t in transactions
    )


def calculate_income(transactions):
    return sum(
        t[2] for t in transactions
        if t[3] == "intrare"
    )


def calculate_expenses(transactions):
    return sum(
        t[2] for t in transactions
        if t[3] == "iesire"
    )


# ==================================================
# REUSABLE UI FUNCTIONS
# ==================================================

def label(parent, text, size=10, color=WHITE, bold=False):
    return tk.Label(
        parent,
        text=text,
        font=("Arial", size, "bold" if bold else "normal"),
        bg=parent.cget("bg"),
        fg=color
    )


def button(parent, text, command, color=CYAN, fg=BG):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=color,
        activeforeground=fg,
        font=("Arial", 9, "bold"),
        relief="flat",
        cursor="hand2",
        padx=14,
        pady=9
    )


def create_entry(parent, width=20):
    return tk.Entry(
        parent,
        width=width,
        font=("Arial", 11),
        bg=PANEL_LIGHT,
        fg=WHITE,
        insertbackground=CYAN,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=CYAN
    )


# ==================================================
# LOGIN SCREEN
# ==================================================

def show_login():

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=BG)

    center = tk.Frame(root, bg=BG)
    center.place(relx=0.5, rely=0.5, anchor="center")

    label(
        center, "◈", 55, CYAN, True
    ).pack()

    label(
        center, "CREST BANK", 27, WHITE, True
    ).pack(pady=(5, 5))

    label(
        center, "SECURE LOGIN", 9, CYAN, True
    ).pack(pady=(0, 30))

    card = tk.Frame(
        center,
        bg=PANEL,
        padx=35,
        pady=35,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card.pack()

    label(card, "USERNAME", 9, TEXT, True).pack(anchor="w")

    username = create_entry(card, 30)
    username.pack(ipady=10, pady=(8, 20))

    label(card, "PASSWORD", 9, TEXT, True).pack(anchor="w")

    password = create_entry(card, 30)
    password.config(show="*")
    password.pack(ipady=10, pady=(8, 25))

    attempts = {"count": 0}

    def login():

        name = username.get().strip()
        secret = password.get()

        if name in USERS and USERS[name] == secret:

            current_user["name"] = name
            show_application()

        else:

            attempts["count"] += 1
            password.delete(0, tk.END)

            if attempts["count"] >= 3:
                messagebox.showerror(
                    "Access denied",
                    "Too many failed attempts."
                )
                root.destroy()

            else:
                messagebox.showerror(
                    "Login failed",
                    f"Incorrect credentials.\n"
                    f"Attempts remaining: {3 - attempts['count']}"
                )

    button(
        card,
        "LOGIN",
        login
    ).pack(fill="x", ipady=3)

    password.bind(
        "<Return>",
        lambda event: login()
    )

    username.bind(
        "<Return>",
        lambda event: password.focus()
    )

    username.focus()


# ==================================================
# MAIN APPLICATION
# ==================================================

def show_application():

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=BG)

    style = ttk.Style()
    style.theme_use("clam")

    # Main layout
    sidebar = tk.Frame(root, bg=SIDEBAR, width=220)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    workspace = tk.Frame(root, bg=BG)
    workspace.pack(side="left", fill="both", expand=True)

    # ==================================================
    # SIDEBAR
    # ==================================================

    logo = tk.Frame(sidebar, bg=SIDEBAR)
    logo.pack(fill="x", padx=18, pady=25)

    label(logo, "◈", 29, CYAN, True).pack(side="left")

    label(logo, "CREST BANK", 15, WHITE, True).pack(
        side="left", padx=8
    )

    tk.Frame(
        sidebar,
        bg=BORDER,
        height=1
    ).pack(fill="x", padx=15, pady=10)

    label(
        sidebar, "MAIN MENU", 8, MUTED, True
    ).pack(anchor="w", padx=22, pady=(15, 10))

    # Page container
    page = tk.Frame(workspace, bg=BG)
    page.pack(fill="both", expand=True)

    def clear_page():

        for widget in page.winfo_children():
            widget.destroy()

    def nav_button(text, command, selected=False):

        color = PANEL_LIGHT if selected else SIDEBAR
        fg = CYAN if selected else TEXT

        tk.Button(
            sidebar,
            text=text,
            command=command,
            bg=color,
            fg=fg,
            activebackground=PANEL_LIGHT,
            activeforeground=CYAN,
            relief="flat",
            font=("Arial", 10, "bold"),
            anchor="w",
            padx=20,
            pady=13,
            cursor="hand2"
        ).pack(fill="x", padx=12, pady=3)

    # ==================================================
    # TOP BAR
    # ==================================================

    topbar = tk.Frame(
        workspace,
        bg=PANEL,
        height=65
    )

    topbar.pack(fill="x")
    topbar.pack_propagate(False)

    page_title = tk.Label(
        topbar,
        text="DASHBOARD",
        font=("Arial", 14, "bold"),
        bg=PANEL,
        fg=WHITE
    )
    page_title.pack(side="left", padx=25, pady=20)

    user_label = tk.Label(
        topbar,
        text=f"● {current_user['name'].upper()}",
        font=("Arial", 9, "bold"),
        bg=PANEL,
        fg=GREEN
    )
    user_label.pack(side="right", padx=25)

    tk.Frame(
        workspace,
        bg=CYAN,
        height=2
    ).pack(fill="x")

    # ==================================================
    # DASHBOARD
    # ==================================================

    def show_dashboard():

        clear_page()
        page_title.config(text="DASHBOARD")

        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=25, pady=22)

        label(
            content, "FINANCIAL OVERVIEW", 19, WHITE, True
        ).pack(anchor="w", pady=(0, 20))

        # Financial cards
        cards = tk.Frame(content, bg=BG)
        cards.pack(fill="x", pady=(0, 25))

        def create_card(title, color, icon):

            card = tk.Frame(
                cards,
                bg=PANEL,
                highlightbackground=BORDER,
                highlightthickness=1,
                height=125
            )
            card.pack_propagate(False)

            tk.Frame(
                card,
                bg=color,
                height=3
            ).pack(fill="x")

            inner = tk.Frame(card, bg=PANEL)
            inner.pack(fill="both", expand=True, padx=15, pady=10)

            label(inner, icon, 16, color, True).pack(anchor="w")
            label(inner, title, 9, TEXT, True).pack(anchor="w")

            value = tk.Label(
                inner,
                text="0.00 RON",
                font=("Arial", 18, "bold"),
                bg=PANEL,
                fg=color
            )
            value.pack(anchor="w", pady=5)

            return card, value

        balance_card, balance_value = create_card(
            "TOTAL BALANCE", CYAN, "◈"
        )

        income_card, income_value = create_card(
            "TOTAL INCOME", GREEN, "↗"
        )

        expense_card, expense_value = create_card(
            "TOTAL EXPENSES", RED, "↘"
        )

        for card in [balance_card, income_card, expense_card]:
            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

        # Recent transactions
        label(
            content, "RECENT TRANSACTIONS", 12, WHITE, True
        ).pack(anchor="w", pady=(5, 12))

        recent_frame = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        recent_frame.pack(fill="both", expand=True)

        columns = ("ID", "DAY", "AMOUNT", "TYPE")

        recent_table = ttk.Treeview(
            recent_frame,
            columns=columns,
            show="headings",
            height=7
        )

        configure_table(recent_table)

        for col in columns:
            recent_table.heading(col, text=col)

        for col in columns:
            recent_table.column(col, anchor="center", width=130)

        recent_table.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        def refresh():

            transactions = get_transactions()

            balance_value.config(
                text=f"{calculate_balance(transactions):,.2f} RON"
            )

            income_value.config(
                text=f"{calculate_income(transactions):,.2f} RON"
            )

            expense_value.config(
                text=f"{calculate_expenses(transactions):,.2f} RON"
            )

            for item in recent_table.get_children():
                recent_table.delete(item)

            for t in transactions[-8:][::-1]:

                recent_table.insert(
                    "",
                    "end",
                    values=(
                        t[0],
                        t[1],
                        f"{t[2]:.2f} RON",
                        "Income" if t[3] == "intrare" else "Expense"
                    ),
                    tags=(t[3],)
                )

        refresh()

        # Simple activity chart
        chart_title = tk.Frame(content, bg=BG)
        chart_title.pack(fill="x", pady=(20, 8))

        label(
            chart_title, "INCOME VS EXPENSES", 11, WHITE, True
        ).pack(anchor="w")

        chart = tk.Canvas(
            content,
            height=95,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground=BORDER
        )
        chart.pack(fill="x")

        transactions = get_transactions()
        income = calculate_income(transactions)
        expenses = calculate_expenses(transactions)

        maximum = max(income, expenses, 1)

        chart_width = 400

        chart.create_text(
            15, 20,
            text="Income",
            anchor="w",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

        chart.create_rectangle(
            110, 12,
            110 + chart_width * income / maximum,
            30,
            fill=GREEN,
            outline=""
        )

        chart.create_text(
            15, 55,
            text="Expenses",
            anchor="w",
            fill=RED,
            font=("Arial", 9, "bold")
        )

        chart.create_rectangle(
            110, 47,
            110 + chart_width * expenses / maximum,
            65,
            fill=RED,
            outline=""
        )

        chart.create_text(
            530, 21,
            text=f"{income:,.2f} RON",
            fill=GREEN,
            font=("Arial", 9, "bold")
        )

        chart.create_text(
            530, 56,
            text=f"{expenses:,.2f} RON",
            fill=RED,
            font=("Arial", 9, "bold")
        )

    # ==================================================
    # TABLE STYLING
    # ==================================================

    def configure_table(table):

        style.configure(
            "Treeview",
            background=PANEL,
            foreground=WHITE,
            fieldbackground=PANEL,
            rowheight=35,
            borderwidth=0,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=PANEL_LIGHT,
            foreground=CYAN,
            font=("Arial", 9, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#24415D")],
            foreground=[("selected", WHITE)]
        )

        table.tag_configure("intrare", foreground=GREEN)
        table.tag_configure("iesire", foreground=RED)

    # ==================================================
    # TRANSACTIONS PAGE
    # ==================================================

    def show_transactions():

        clear_page()
        page_title.config(text="TRANSACTIONS")

        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=25, pady=22)

        label(
            content, "TRANSACTION MANAGEMENT", 18, WHITE, True
        ).pack(anchor="w", pady=(0, 20))

        # Search bar
        search_frame = tk.Frame(content, bg=PANEL, padx=12, pady=12)
        search_frame.pack(fill="x", pady=(0, 15))

        search_entry = create_entry(search_frame, 35)
        search_entry.pack(side="left", ipady=8)

        # Table
        table_frame = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "DAY", "AMOUNT", "TYPE")

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        configure_table(table)

        for col in columns:
            table.heading(col, text=col)

        for col in columns:
            table.column(col, anchor="center", width=140)

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=table.yview
        )

        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True, padx=8, pady=8)
        scrollbar.pack(side="right", fill="y", pady=8)

        def load_table():

            for item in table.get_children():
                table.delete(item)

            query = search_entry.get().lower().strip()

            for t in get_transactions():

                transaction_type = (
                    "Income" if t[3] == "intrare" else "Expense"
                )

                values = (
                    t[0],
                    t[1],
                    f"{t[2]:.2f} RON",
                    transaction_type
                )

                searchable = " ".join(map(str, values)).lower()

                if query and query not in searchable:
                    continue

                table.insert(
                    "",
                    "end",
                    values=values,
                    tags=(t[3],)
                )

        button(
            search_frame,
            "SEARCH",
            load_table
        ).pack(side="left", padx=10)

        button(
            search_frame,
            "CLEAR",
            lambda: (
                search_entry.delete(0, tk.END),
                load_table()
            ),
            PANEL_LIGHT,
            WHITE
        ).pack(side="left")

        search_entry.bind(
            "<Return>",
            lambda event: load_table()
        )

        # Transaction actions
        actions = tk.Frame(content, bg=BG)
        actions.pack(fill="x", pady=15)

        def selected_id():

            selected = table.selection()

            if not selected:
                messagebox.showwarning(
                    "No selection",
                    "Please select a transaction first."
                )
                return None

            return int(table.item(selected[0], "values")[0])

        def open_editor(edit=True):

            transaction_id = selected_id()

            if transaction_id is None:
                return

            transaction = next(
                (t for t in get_transactions() if t[0] == transaction_id),
                None
            )

            if transaction is None:
                return

            popup = tk.Toplevel(root)
            popup.title("Edit Transaction" if edit else "Transaction Details")
            popup.geometry("360x350")
            popup.configure(bg=PANEL)
            popup.transient(root)
            popup.grab_set()

            tk.Label(
                popup,
                text="EDIT TRANSACTION",
                font=("Arial", 15, "bold"),
                bg=PANEL,
                fg=CYAN
            ).pack(pady=20)

            tk.Label(
                popup,
                text="Day",
                bg=PANEL,
                fg=TEXT
            ).pack()

            day_field = create_entry(popup, 20)
            day_field.pack(ipady=7, pady=6)
            day_field.insert(0, str(transaction[1]))

            tk.Label(
                popup,
                text="Amount (RON)",
                bg=PANEL,
                fg=TEXT
            ).pack()

            amount_field = create_entry(popup, 20)
            amount_field.pack(ipady=7, pady=6)
            amount_field.insert(0, str(transaction[2]))

            tk.Label(
                popup,
                text="Type",
                bg=PANEL,
                fg=TEXT
            ).pack()

            type_field = ttk.Combobox(
                popup,
                values=["Income", "Expense"],
                state="readonly",
                width=18
            )

            type_field.pack(pady=8)
            type_field.set(
                "Income" if transaction[3] == "intrare" else "Expense"
            )

            def save():

                try:

                    day = int(day_field.get())
                    amount = float(amount_field.get())

                    if not 1 <= day <= 31 or amount <= 0:
                        raise ValueError

                    transaction_type = (
                        "intrare" if type_field.get() == "Income"
                        else "iesire"
                    )

                    update_transaction(
                        transaction_id,
                        day,
                        amount,
                        transaction_type
                    )

                    popup.destroy()
                    load_table()

                    messagebox.showinfo(
                        "Success",
                        "Transaction updated successfully."
                    )

                except ValueError:
                    messagebox.showerror(
                        "Invalid input",
                        "Check the day and amount."
                    )

            button(
                popup,
                "SAVE CHANGES",
                save
            ).pack(fill="x", padx=30, pady=15)

        def remove_transaction():

            transaction_id = selected_id()

            if transaction_id is None:
                return

            confirm = messagebox.askyesno(
                "Delete transaction",
                "Are you sure you want to delete this transaction?"
            )

            if confirm:

                delete_transaction(transaction_id)
                load_table()

                messagebox.showinfo(
                    "Deleted",
                    "Transaction deleted successfully."
                )

        button(
            actions,
            "EDIT SELECTED",
            lambda: open_editor(),
            CYAN
        ).pack(side="left", padx=5)

        button(
            actions,
            "DELETE SELECTED",
            remove_transaction,
            RED,
            WHITE
        ).pack(side="left", padx=5)

        load_table()

    # ==================================================
    # SETTINGS PAGE
    # ==================================================

    def show_settings():

        clear_page()
        page_title.config(text="SETTINGS")

        content = tk.Frame(page, bg=BG)
        content.pack(fill="both", expand=True, padx=25, pady=25)

        label(
            content, "ACCOUNT SETTINGS", 18, WHITE, True
        ).pack(anchor="w", pady=(0, 20))

        account = tk.Frame(
            content,
            bg=PANEL,
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=25,
            pady=25
        )
        account.pack(fill="x")

        label(account, "ACCOUNT INFORMATION", 11, CYAN, True).pack(
            anchor="w", pady=(0, 20)
        )

        label(account, "Username", 9, MUTED).pack(anchor="w")
        label(account, current_user["name"], 13, WHITE, True).pack(
            anchor="w", pady=(4, 15)
        )

        label(account, "Application", 9, MUTED).pack(anchor="w")
        label(account, "Crest Bank", 13, WHITE, True).pack(
            anchor="w", pady=(4, 15)
        )

        label(account, "Storage", 9, MUTED).pack(anchor="w")
        label(account, "SQLite Database", 13, WHITE, True).pack(
            anchor="w", pady=(4, 15)
        )

        label(account, "Theme", 9, MUTED).pack(anchor="w")
        label(account, "Dark Futuristic", 13, CYAN, True).pack(
            anchor="w", pady=(4, 15)
        )

        button(
            content,
            "LOG OUT",
            show_login,
            RED,
            WHITE
        ).pack(anchor="w", pady=20)

        label(
            content,
            "CREST BANK  |  PYTHON DESKTOP APPLICATION",
            9,
            MUTED
        ).pack(anchor="w", pady=15)

    # ==================================================
    # SIDEBAR NAVIGATION
    # ==================================================

    nav_button(
        "◈   Dashboard",
        show_dashboard,
        True
    )

    nav_button(
        "⇄   Transactions",
        show_transactions
    )

    nav_button(
        "⚙   Settings",
        show_settings
    )

    tk.Frame(sidebar, bg=SIDEBAR).pack(
        fill="both",
        expand=True
    )

    tk.Frame(
        sidebar,
        bg=BORDER,
        height=1
    ).pack(fill="x", padx=15, pady=10)

    label(
        sidebar,
        current_user["name"].upper(),
        10,
        CYAN,
        True
    ).pack(anchor="w", padx=22, pady=5)

    nav_button(
        "↪   Logout",
        show_login
    )

    # Initial page
    show_dashboard()


database.create_table()

show_login()

root.mainloop()
