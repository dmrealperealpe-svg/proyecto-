"""
SplitFácil - Prototipo de escritorio (Tkinter)
Aplicación para dividir gastos compartidos en grupos.

Cómo ejecutarlo en VS Code:
1. Asegúrate de tener Python instalado (tkinter viene incluido).
2. Abre este archivo y presiona el botón ▷ "Run Python File".

Este es un prototipo: los datos viven en memoria mientras la app
está abierta (no hay base de datos todavía). Al cerrar la ventana
se pierden los cambios, tal como un MVP de práctica.
"""

import tkinter as tk
from tkinter import ttk, messagebox

# ---------------------------------------------------------------------------
# Colores (mismo lenguaje visual que el prototipo web)
# ---------------------------------------------------------------------------
PAPER = "#F7F4EC"
PAPER_2 = "#EFEADC"
INK = "#1E2422"
INK_SOFT = "#55605C"
TEAL = "#2F6F62"
TEAL_DEEP = "#204B42"
GOLD = "#C99A46"
DEBT = "#B65C4A"
CREDIT = "#2F6F62"
CARD_BG = "#FFFDF8"
LINE = "#DBD4C1"

FONT_TITLE = ("Georgia", 20, "bold")
FONT_SUB = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 10, "bold")
FONT_BODY = ("Segoe UI", 11)
FONT_AMOUNT = ("Georgia", 14, "bold")


def fmt(amount):
    """Formatea un número como moneda colombiana simple: $1.200.000"""
    return "$" + f"{round(amount):,}".replace(",", ".")


# ---------------------------------------------------------------------------
# "Base de datos" en memoria
# ---------------------------------------------------------------------------
class AppState:
    def __init__(self):
        self.user = None  # {"name": ..., "email": ...}
        self.groups = [
            {
                "id": "g1",
                "name": "Apartamento 5B",
                "members": ["Tú", "Camila", "Jorge"],
                "expenses": [
                    {"desc": "Arriendo de septiembre", "amount": 1200000, "paid_by": "Camila", "settled": False},
                    {"desc": "Mercado quincenal", "amount": 185000, "paid_by": "Tú", "settled": False},
                    {"desc": "Internet y servicios", "amount": 210000, "paid_by": "Jorge", "settled": True},
                ],
            },
            {
                "id": "g2",
                "name": "Viaje a la costa",
                "members": ["Tú", "Laura", "Andrés", "Camila"],
                "expenses": [
                    {"desc": "Hospedaje 3 noches", "amount": 980000, "paid_by": "Laura", "settled": False},
                    {"desc": "Gasolina ida y vuelta", "amount": 260000, "paid_by": "Tú", "settled": False},
                ],
            },
        ]

    def compute_balances(self, group):
        """Devuelve {miembro: balance} — positivo = le deben, negativo = debe."""
        balances = {m: 0.0 for m in group["members"]}
        for exp in group["expenses"]:
            if exp["settled"]:
                continue
            share = exp["amount"] / len(group["members"])
            for m in group["members"]:
                if m == exp["paid_by"]:
                    balances[m] += exp["amount"] - share
                else:
                    balances[m] -= share
        return balances

    def user_balance_in_group(self, group):
        return self.compute_balances(group).get("Tú", 0.0)

    def total_user_balance(self):
        return sum(self.user_balance_in_group(g) for g in self.groups)

    def get_group(self, group_id):
        return next((g for g in self.groups if g["id"] == group_id), None)


STATE = AppState()


# ---------------------------------------------------------------------------
# Ventana principal: controla el cambio de pantallas
# ---------------------------------------------------------------------------
class SplitFacilApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SplitFácil")
        self.geometry("880x600")
        self.minsize(720, 520)
        self.configure(bg=PAPER)

        self.active_group_id = None
        self.container = tk.Frame(self, bg=PAPER)
        self.container.pack(fill="both", expand=True)

        self.show_login()

    def clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        LoginScreen(self.container, self).pack(fill="both", expand=True)

    def show_register(self):
        self.clear()
        RegisterScreen(self.container, self).pack(fill="both", expand=True)

    def show_dashboard(self):
        self.clear()
        DashboardScreen(self.container, self).pack(fill="both", expand=True)

    def show_group(self, group_id):
        self.active_group_id = group_id
        self.clear()
        GroupScreen(self.container, self, group_id).pack(fill="both", expand=True)

    def logout(self):
        STATE.user = None
        self.show_login()


# ---------------------------------------------------------------------------
# Pantalla: Login
# ---------------------------------------------------------------------------
class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=PAPER)
        self.app = app

        card = tk.Frame(self, bg=PAPER)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="SplitFácil", font=("Georgia", 26, "bold"), bg=PAPER, fg=TEAL_DEEP).pack(pady=(0, 4))
        tk.Label(card, text="Divide gastos en grupo sin hacer cuentas de cabeza.",
                 font=FONT_SUB, bg=PAPER, fg=INK_SOFT).pack(pady=(0, 24))

        form = tk.Frame(card, bg=CARD_BG, padx=32, pady=28, highlightbackground=LINE, highlightthickness=1)
        form.pack()

        tk.Label(form, text="Iniciar sesión", font=FONT_TITLE, bg=CARD_BG, fg=INK).pack(anchor="w")
        tk.Label(form, text="Entra para ver tus grupos y balances.", font=FONT_SUB,
                 bg=CARD_BG, fg=INK_SOFT).pack(anchor="w", pady=(0, 18))

        tk.Label(form, text="Correo electrónico", font=FONT_LABEL, bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")
        self.email_entry = tk.Entry(form, font=FONT_BODY, width=32, relief="solid", bd=1)
        self.email_entry.pack(pady=(2, 12), ipady=4)

        tk.Label(form, text="Contraseña", font=FONT_LABEL, bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")
        self.pass_entry = tk.Entry(form, font=FONT_BODY, width=32, relief="solid", bd=1, show="•")
        self.pass_entry.pack(pady=(2, 4), ipady=4)

        self.error_label = tk.Label(form, text="", font=FONT_SUB, bg=CARD_BG, fg=DEBT)
        self.error_label.pack(anchor="w", pady=(0, 8))

        tk.Button(form, text="Iniciar sesión", font=FONT_LABEL, bg=TEAL, fg="white",
                  activebackground=TEAL_DEEP, activeforeground="white", relief="flat",
                  padx=10, pady=8, command=self.login).pack(fill="x", pady=(10, 14))

        footer = tk.Frame(form, bg=CARD_BG)
        footer.pack()
        tk.Label(footer, text="¿No tienes cuenta?", font=FONT_SUB, bg=CARD_BG, fg=INK_SOFT).pack(side="left")
        tk.Button(footer, text="Crear una", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEAL,
                  relief="flat", bd=0, cursor="hand2", command=app.show_register).pack(side="left", padx=4)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.pass_entry.get()
        if not email or not password:
            self.error_label.config(text="Revisa tu correo y contraseña.")
            return
        # Prototipo: no hay backend real, cualquier credencial válida entra.
        display_name = email.split("@")[0].capitalize()
        STATE.user = {"name": display_name, "email": email}
        self.app.show_dashboard()


# ---------------------------------------------------------------------------
# Pantalla: Registro
# ---------------------------------------------------------------------------
class RegisterScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=PAPER)
        self.app = app

        card = tk.Frame(self, bg=PAPER)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(card, text="SplitFácil", font=("Georgia", 26, "bold"), bg=PAPER, fg=TEAL_DEEP).pack(pady=(0, 4))
        tk.Label(card, text="Regístrate en menos de un minuto.", font=FONT_SUB,
                 bg=PAPER, fg=INK_SOFT).pack(pady=(0, 24))

        form = tk.Frame(card, bg=CARD_BG, padx=32, pady=28, highlightbackground=LINE, highlightthickness=1)
        form.pack()

        tk.Label(form, text="Crear cuenta", font=FONT_TITLE, bg=CARD_BG, fg=INK).pack(anchor="w", pady=(0, 18))

        tk.Label(form, text="Nombre", font=FONT_LABEL, bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")
        self.name_entry = tk.Entry(form, font=FONT_BODY, width=32, relief="solid", bd=1)
        self.name_entry.pack(pady=(2, 12), ipady=4)

        tk.Label(form, text="Correo electrónico", font=FONT_LABEL, bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")
        self.email_entry = tk.Entry(form, font=FONT_BODY, width=32, relief="solid", bd=1)
        self.email_entry.pack(pady=(2, 12), ipady=4)

        tk.Label(form, text="Contraseña (mínimo 6 caracteres)", font=FONT_LABEL, bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")
        self.pass_entry = tk.Entry(form, font=FONT_BODY, width=32, relief="solid", bd=1, show="•")
        self.pass_entry.pack(pady=(2, 4), ipady=4)

        self.error_label = tk.Label(form, text="", font=FONT_SUB, bg=CARD_BG, fg=DEBT)
        self.error_label.pack(anchor="w", pady=(0, 8))

        tk.Button(form, text="Crear cuenta", font=FONT_LABEL, bg=TEAL, fg="white",
                  activebackground=TEAL_DEEP, activeforeground="white", relief="flat",
                  padx=10, pady=8, command=self.register).pack(fill="x", pady=(10, 14))

        footer = tk.Frame(form, bg=CARD_BG)
        footer.pack()
        tk.Label(footer, text="¿Ya tienes cuenta?", font=FONT_SUB, bg=CARD_BG, fg=INK_SOFT).pack(side="left")
        tk.Button(footer, text="Iniciar sesión", font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=TEAL,
                  relief="flat", bd=0, cursor="hand2", command=app.show_login).pack(side="left", padx=4)

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.pass_entry.get()
        if not name or not email or len(password) < 6:
            self.error_label.config(text="Completa todos los campos (contraseña de 6+ caracteres).")
            return
        STATE.user = {"name": name, "email": email}
        self.app.show_dashboard()


# ---------------------------------------------------------------------------
# Pantalla: Dashboard (lista de grupos)
# ---------------------------------------------------------------------------
class DashboardScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=PAPER)
        self.app = app

        # Header
        header = tk.Frame(self, bg=PAPER, pady=14, padx=24)
        header.pack(fill="x")
        tk.Label(header, text="SplitFácil", font=("Georgia", 16, "bold"), bg=PAPER, fg=INK).pack(side="left")
        right = tk.Frame(header, bg=PAPER)
        right.pack(side="right")
        tk.Label(right, text=f"Hola, {STATE.user['name']}", font=FONT_SUB, bg=PAPER, fg=INK_SOFT).pack(side="left", padx=(0, 12))
        tk.Button(right, text="Salir", font=FONT_SUB, bg=PAPER, fg=INK_SOFT, relief="flat",
                  cursor="hand2", command=app.logout).pack(side="left")
        tk.Frame(self, bg=LINE, height=1).pack(fill="x")

        # Balance total
        total = STATE.total_user_balance()
        banner = tk.Frame(self, bg=CARD_BG, highlightbackground=LINE, highlightthickness=1, padx=20, pady=16)
        banner.pack(fill="x", padx=24, pady=20)
        label = "En total, te deben" if total >= 0 else "En total, debes"
        color = CREDIT if total >= 0 else DEBT
        tk.Label(banner, text=label, font=FONT_SUB, bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")
        tk.Label(banner, text=fmt(abs(total)), font=("Georgia", 20, "bold"), bg=CARD_BG, fg=color).pack(anchor="w")

        # Lista de grupos
        tk.Label(self, text="Tus grupos", font=("Georgia", 14, "bold"), bg=PAPER, fg=INK).pack(anchor="w", padx=24)

        list_frame = tk.Frame(self, bg=PAPER)
        list_frame.pack(fill="both", expand=True, padx=24, pady=(10, 20))

        for group in STATE.groups:
            self.build_group_card(list_frame, group)

    def build_group_card(self, parent, group):
        bal = STATE.user_balance_in_group(group)
        color = CREDIT if bal >= 0 else DEBT
        tag = "te deben" if bal >= 0 else "debes"

        card = tk.Frame(parent, bg=CARD_BG, highlightbackground=LINE, highlightthickness=1,
                         padx=18, pady=14, cursor="hand2")
        card.pack(fill="x", pady=6)

        left = tk.Frame(card, bg=CARD_BG)
        left.pack(side="left", fill="x", expand=True)
        tk.Label(left, text=group["name"], font=("Segoe UI", 12, "bold"), bg=CARD_BG, fg=INK).pack(anchor="w")
        tk.Label(left, text=f'{len(group["members"])} integrantes · {len(group["expenses"])} gastos',
                 font=("Segoe UI", 9), bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")

        right = tk.Frame(card, bg=CARD_BG)
        right.pack(side="right")
        tk.Label(right, text=fmt(abs(bal)), font=FONT_AMOUNT, bg=CARD_BG, fg=color).pack(anchor="e")
        tk.Label(right, text=tag, font=("Segoe UI", 9), bg=CARD_BG, fg=INK_SOFT).pack(anchor="e")

        def open_group(event=None, gid=group["id"]):
            self.app.show_group(gid)

        for widget in (card, left, right):
            widget.bind("<Button-1>", open_group)
        for child in left.winfo_children() + right.winfo_children():
            child.bind("<Button-1>", open_group)


# ---------------------------------------------------------------------------
# Pantalla: Detalle de grupo (balances + gastos + agregar gasto)
# ---------------------------------------------------------------------------
class GroupScreen(tk.Frame):
    def __init__(self, parent, app, group_id):
        super().__init__(parent, bg=PAPER)
        self.app = app
        self.group = STATE.get_group(group_id)

        header = tk.Frame(self, bg=PAPER, pady=14, padx=24)
        header.pack(fill="x")
        tk.Button(header, text="← Tus grupos", font=FONT_SUB, bg=PAPER, fg=INK_SOFT, relief="flat",
                  cursor="hand2", command=app.show_dashboard).pack(side="left")
        tk.Button(header, text="Salir", font=FONT_SUB, bg=PAPER, fg=INK_SOFT, relief="flat",
                  cursor="hand2", command=app.logout).pack(side="right")
        tk.Frame(self, bg=LINE, height=1).pack(fill="x")

        body = tk.Frame(self, bg=PAPER, padx=24, pady=16)
        body.pack(fill="both", expand=True)

        tk.Label(body, text=self.group["name"], font=("Georgia", 18, "bold"), bg=PAPER, fg=INK).pack(anchor="w")
        tk.Label(body, text=", ".join(self.group["members"]), font=FONT_SUB, bg=PAPER, fg=INK_SOFT).pack(anchor="w", pady=(0, 16))

        # Balances
        tk.Label(body, text="Balances", font=("Georgia", 13, "bold"), bg=PAPER, fg=INK).pack(anchor="w", pady=(0, 6))
        self.balances_frame = tk.Frame(body, bg=PAPER)
        self.balances_frame.pack(fill="x", pady=(0, 16))

        # Gastos
        expenses_header = tk.Frame(body, bg=PAPER)
        expenses_header.pack(fill="x")
        tk.Label(expenses_header, text="Gastos", font=("Georgia", 13, "bold"), bg=PAPER, fg=INK).pack(side="left")
        tk.Button(expenses_header, text="+ Agregar gasto", font=FONT_LABEL, bg=TEAL, fg="white",
                  relief="flat", padx=12, pady=4, cursor="hand2", command=self.open_add_expense).pack(side="right")

        self.expenses_frame = tk.Frame(body, bg=PAPER)
        self.expenses_frame.pack(fill="both", expand=True, pady=(10, 0))

        self.refresh()

    def refresh(self):
        for w in self.balances_frame.winfo_children():
            w.destroy()
        for w in self.expenses_frame.winfo_children():
            w.destroy()

        balances = STATE.compute_balances(self.group)
        for member, bal in balances.items():
            color = CREDIT if bal >= 0 else DEBT
            if abs(bal) < 1:
                text = "está al día"
            else:
                text = f"le deben {fmt(bal)}" if bal >= 0 else f"debe {fmt(abs(bal))}"
            row = tk.Frame(self.balances_frame, bg=CARD_BG, highlightbackground=LINE, highlightthickness=1,
                            padx=14, pady=8)
            row.pack(fill="x", pady=3)
            tk.Label(row, text=member, font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=INK).pack(side="left")
            tk.Label(row, text=text, font=FONT_SUB, bg=CARD_BG, fg=color).pack(side="right")

        if not self.group["expenses"]:
            tk.Label(self.expenses_frame, text="Aún no hay gastos. Registra el primero.",
                     font=FONT_SUB, bg=PAPER, fg=INK_SOFT).pack(pady=20)
            return

        for exp in self.group["expenses"]:
            row = tk.Frame(self.expenses_frame, bg=CARD_BG, highlightbackground=LINE, highlightthickness=1,
                            padx=16, pady=10)
            row.pack(fill="x", pady=4)

            left = tk.Frame(row, bg=CARD_BG)
            left.pack(side="left", fill="x", expand=True)
            tk.Label(left, text=exp["desc"], font=("Segoe UI", 10, "bold"), bg=CARD_BG, fg=INK).pack(anchor="w")
            tk.Label(left, text=f'Pagó {exp["paid_by"]} · partes iguales', font=("Segoe UI", 9),
                     bg=CARD_BG, fg=INK_SOFT).pack(anchor="w")

            right = tk.Frame(row, bg=CARD_BG)
            right.pack(side="right")
            tk.Label(right, text=fmt(exp["amount"]), font=("Georgia", 12, "bold"), bg=CARD_BG, fg=INK).pack(anchor="e")

            btn_text = "Pagado ✓" if exp["settled"] else "Marcar pagado"
            btn_color = CREDIT if exp["settled"] else INK_SOFT

            def toggle(e=exp):
                e["settled"] = not e["settled"]
                self.refresh()

            tk.Button(right, text=btn_text, font=("Segoe UI", 8), fg=btn_color, bg=CARD_BG,
                      relief="solid", bd=1, cursor="hand2", command=toggle).pack(anchor="e", pady=(4, 0))

    def open_add_expense(self):
        win = tk.Toplevel(self)
        win.title("Nuevo gasto")
        win.configure(bg=PAPER)
        win.geometry("340x320")
        win.transient(self.app)
        win.grab_set()

        pad = tk.Frame(win, bg=PAPER, padx=20, pady=20)
        pad.pack(fill="both", expand=True)

        tk.Label(pad, text="Nuevo gasto", font=FONT_TITLE, bg=PAPER, fg=INK).pack(anchor="w", pady=(0, 14))

        tk.Label(pad, text="Descripción", font=FONT_LABEL, bg=PAPER, fg=INK_SOFT).pack(anchor="w")
        desc_entry = tk.Entry(pad, font=FONT_BODY, relief="solid", bd=1)
        desc_entry.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(pad, text="Monto (COP)", font=FONT_LABEL, bg=PAPER, fg=INK_SOFT).pack(anchor="w")
        amount_entry = tk.Entry(pad, font=FONT_BODY, relief="solid", bd=1)
        amount_entry.pack(fill="x", pady=(2, 10), ipady=4)

        tk.Label(pad, text="¿Quién pagó?", font=FONT_LABEL, bg=PAPER, fg=INK_SOFT).pack(anchor="w")
        paid_by_var = tk.StringVar(value=self.group["members"][0])
        paid_by_menu = ttk.Combobox(pad, textvariable=paid_by_var, values=self.group["members"], state="readonly")
        paid_by_menu.pack(fill="x", pady=(2, 4))

        error_label = tk.Label(pad, text="", font=FONT_SUB, bg=PAPER, fg=DEBT)
        error_label.pack(anchor="w", pady=(4, 4))

        def save():
            desc = desc_entry.get().strip()
            amount_text = amount_entry.get().strip()
            if not desc or not amount_text:
                error_label.config(text="Completa la descripción y el monto.")
                return
            try:
                amount = float(amount_text)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                error_label.config(text="El monto debe ser un número mayor a 0.")
                return

            self.group["expenses"].append({
                "desc": desc,
                "amount": amount,
                "paid_by": paid_by_var.get(),
                "settled": False,
            })
            win.destroy()
            self.refresh()

        btns = tk.Frame(pad, bg=PAPER)
        btns.pack(fill="x", pady=(14, 0))
        tk.Button(btns, text="Cancelar", font=FONT_LABEL, bg=PAPER, fg=INK_SOFT,
                  relief="solid", bd=1, command=win.destroy).pack(side="left", expand=True, fill="x", padx=(0, 6))
        tk.Button(btns, text="Guardar", font=FONT_LABEL, bg=TEAL, fg="white",
                  relief="flat", command=save).pack(side="left", expand=True, fill="x", padx=(6, 0))


if __name__ == "__main__":
    app = SplitFacilApp()
    app.mainloop()
