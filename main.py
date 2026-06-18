import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# PDF EXPORT IMPORTS
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


class BudgetTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Budget Tracker")
        self.root.geometry("750x600")
        self.root.configure(bg="#f4f6f8")

        self.transactions = []

        # TITLE
        title = tk.Label(
            root,
            text="Student Budget Tracker",
            font=("Arial", 22, "bold"),
            bg="#f4f6f8",
            fg="#1f4e79"
        )
        title.pack(pady=10)

        # BALANCE DISPLAY
        self.balance_var = tk.StringVar()
        self.balance_var.set("Current Balance: ₦0.00")

        balance_label = tk.Label(
            root,
            textvariable=self.balance_var,
            font=("Arial", 16, "bold"),
            bg="#d9edf7",
            fg="#0c5460",
            padx=15,
            pady=10
        )
        balance_label.pack(pady=10)

        # INPUT FRAME
        input_frame = tk.Frame(root, bg="#f4f6f8")
        input_frame.pack(pady=10)

        # DESCRIPTION
        tk.Label(
            input_frame,
            text="Description",
            bg="#f4f6f8"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.description_entry = tk.Entry(
            input_frame,
            width=20
        )
        self.description_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        # AMOUNT
        tk.Label(
            input_frame,
            text="Amount (₦)",
            bg="#f4f6f8"
        ).grid(row=0, column=2, padx=5, pady=5)

        self.amount_entry = tk.Entry(
            input_frame,
            width=15
        )
        self.amount_entry.grid(
            row=0,
            column=3,
            padx=5,
            pady=5
        )

        # TYPE
        tk.Label(
            input_frame,
            text="Type",
            bg="#f4f6f8"
        ).grid(row=0, column=4, padx=5, pady=5)

        self.type_var = tk.StringVar(value="Expense")

        type_menu = ttk.Combobox(
            input_frame,
            textvariable=self.type_var,
            values=["Income", "Expense"],
            state="readonly",
            width=12
        )

        type_menu.grid(
            row=0,
            column=5,
            padx=5,
            pady=5
        )

        # ADD BUTTON
        add_button = tk.Button(
            root,
            text="Add Transaction",
            command=self.add_transaction,
            bg="#28a745",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )

        add_button.pack(pady=10)

        # TRANSACTION TABLE
        columns = (
            "Date",
            "Description",
            "Type",
            "Amount"
        )

        self.tree = ttk.Treeview(
            root,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(pady=10)

        # DELETE BUTTON
        delete_button = tk.Button(
            root,
            text="Delete Selected",
            command=self.delete_transaction,
            bg="#dc3545",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )

        delete_button.pack(pady=5)

        # PDF EXPORT BUTTON
        export_button = tk.Button(
            root,
            text="Export PDF Report",
            command=self.export_pdf,
            bg="#007bff",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5
        )

        export_button.pack(pady=5)

    def add_transaction(self):

        description = self.description_entry.get()
        amount_text = self.amount_entry.get()
        transaction_type = self.type_var.get()

        if not description or not amount_text:
            messagebox.showerror(
                "Input Error",
                "Please fill in all fields."
            )
            return

        try:
            amount = float(amount_text)

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Amount must be a number."
            )
            return

        date = datetime.now().strftime("%Y-%m-%d")

        transaction = {
            "date": date,
            "description": description,
            "type": transaction_type,
            "amount": amount
        }

        self.transactions.append(transaction)

        self.tree.insert(
            "",
            tk.END,
            values=(
                date,
                description,
                transaction_type,
                f"₦{amount:,.2f}"
            )
        )

        self.update_balance()
        self.clear_inputs()

    def delete_transaction(self):

        selected_item = self.tree.selection()

        if not selected_item:
            messagebox.showwarning(
                "Selection Error",
                "Please select a transaction to delete."
            )
            return

        item_index = self.tree.index(selected_item)

        self.tree.delete(selected_item)

        del self.transactions[item_index]

        self.update_balance()

    def update_balance(self):

        balance = 0

        for transaction in self.transactions:

            if transaction["type"] == "Income":
                balance += transaction["amount"]

            else:
                balance -= transaction["amount"]

        self.balance_var.set(
            f"Current Balance: ₦{balance:,.2f}"
        )

    def export_pdf(self):

        if not self.transactions:
            messagebox.showwarning(
                "No Data",
                "There are no transactions to export."
            )
            return

        pdf = SimpleDocTemplate(
            "budget_report.pdf"
        )

        styles = getSampleStyleSheet()

        report = []

        report.append(
            Paragraph(
                "Student Budget Report",
                styles["Title"]
            )
        )

        report.append(Spacer(1, 12))

        balance = 0

        for transaction in self.transactions:

            if transaction["type"] == "Income":
                balance += transaction["amount"]

            else:
                balance -= transaction["amount"]

        report.append(
            Paragraph(
                f"Current Balance: ₦{balance:,.2f}",
                styles["Heading2"]
            )
        )

        report.append(Spacer(1, 12))

        for transaction in self.transactions:

            line = (
                f"{transaction['date']} | "
                f"{transaction['description']} | "
                f"{transaction['type']} | "
                f"₦{transaction['amount']:,.2f}"
            )

            report.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )

        pdf.build(report)

        messagebox.showinfo(
            "Success",
            "PDF exported successfully!\n\nSaved as budget_report.pdf"
        )

    def clear_inputs(self):

        self.description_entry.delete(
            0,
            tk.END
        )

        self.amount_entry.delete(
            0,
            tk.END
        )

        self.type_var.set("Expense")


if __name__ == "__main__":

    root = tk.Tk()

    app = BudgetTracker(root)

    root.mainloop()
