import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter.font import Font
import pyperclip
from generator import generator
from vault import vault


class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Генератор и Хранитель Паролей")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)

        self.setup_styles()

        self.current_password = None
        self.vault_unlocked = False
        self.master_password = None

        self.create_widgets()

        self.check_vault()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.colors = {
            'bg': '#f5f5f5',
            'fg': '#333333',
            'accent': '#4CAF50',
            'weak': '#f44336',
            'medium': '#FF9800',
            'strong': '#2196F3',
            'very_strong': '#4CAF50'
        }

        self.root.configure(bg=self.colors['bg'])

        self.title_font = Font(family="Helvetica", size=16, weight="bold")
        self.password_font = Font(family="Courier", size=14, weight="bold")
        self.normal_font = Font(family="Helvetica", size=10)

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.generator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.generator_frame, text="🎲 Генератор")
        self.setup_generator_tab()

        self.vault_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.vault_frame, text="🔒 Хранилище")
        self.setup_vault_tab()

        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Настройки")
        self.setup_settings_tab()

    def setup_generator_tab(self):
        main_frame = ttk.Frame(self.generator_frame, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title = ttk.Label(
            main_frame,
            text="🎲 Генератор безопасных паролей",
            font=self.title_font
        )
        title.pack(pady=(0, 20))

        settings_frame = ttk.LabelFrame(main_frame, text="Настройки", padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 20))

        length_frame = ttk.Frame(settings_frame)
        length_frame.pack(fill=tk.X, pady=5)

        ttk.Label(length_frame, text="Длина пароля:").pack(side=tk.LEFT)
        self.length_var = tk.IntVar(value=12)
        length_spinbox = ttk.Spinbox(
            length_frame,
            from_=4,
            to=64,
            textvariable=self.length_var,
            width=10,
            state="readonly"
        )
        length_spinbox.pack(side=tk.LEFT, padx=(10, 0))

        ttk.Label(length_frame, text="Быстрый выбор:").pack(side=tk.LEFT, padx=(20, 5))
        for length in [8, 12, 16, 20, 24]:
            btn = ttk.Button(
                length_frame,
                text=str(length),
                width=3,
                command=lambda l=length: self.length_var.set(l)
            )
            btn.pack(side=tk.LEFT, padx=2)

        chars_frame = ttk.Frame(settings_frame)
        chars_frame.pack(fill=tk.X, pady=10)

        ttk.Label(chars_frame, text="Наборы символов:").pack(anchor=tk.W)

        chars_options_frame = ttk.Frame(chars_frame)
        chars_options_frame.pack(fill=tk.X, padx=(20, 0), pady=5)

        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            chars_options_frame,
            text="Строчные буквы (a-z)",
            variable=self.use_lowercase
        ).pack(anchor=tk.W)

        ttk.Checkbutton(
            chars_options_frame,
            text="Заглавные буквы (A-Z)",
            variable=self.use_uppercase
        ).pack(anchor=tk.W)

        ttk.Checkbutton(
            chars_options_frame,
            text="Цифры (0-9)",
            variable=self.use_digits
        ).pack(anchor=tk.W)

        ttk.Checkbutton(
            chars_options_frame,
            text="Спецсимволы (!@#$%)",
            variable=self.use_symbols
        ).pack(anchor=tk.W)

        ttk.Checkbutton(
            chars_options_frame,
            text="Исключить похожие (Il1O0)",
            variable=self.exclude_ambiguous
        ).pack(anchor=tk.W, pady=(5, 0))

        level_frame = ttk.Frame(settings_frame)
        level_frame.pack(fill=tk.X, pady=10)

        ttk.Label(level_frame, text="Готовые уровни:").pack(anchor=tk.W)

        level_buttons_frame = ttk.Frame(level_frame)
        level_buttons_frame.pack(fill=tk.X, padx=(20, 0), pady=5)

        for level in ["Низкий", "Средний", "Высокий", "Очень высокий"]:
            btn = ttk.Button(
                level_buttons_frame,
                text=level,
                command=lambda l=level: self.set_level(l)
            )
            btn.pack(side=tk.LEFT, padx=2)

        generate_btn = ttk.Button(
            main_frame,
            text="🔑 Сгенерировать пароль",
            command=self.generate_password,
            style='Accent.TButton'
        )
        generate_btn.pack(pady=10)

        result_frame = ttk.LabelFrame(main_frame, text="Результат", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))

        password_frame = ttk.Frame(result_frame)
        password_frame.pack(fill=tk.X, pady=(0, 10))

        self.password_var = tk.StringVar(value="Нажмите кнопку для генерации")
        password_entry = ttk.Entry(
            password_frame,
            textvariable=self.password_var,
            font=self.password_font,
            state="readonly",
            justify=tk.CENTER
        )
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))

        copy_btn = ttk.Button(
            password_frame,
            text="📋 Копировать",
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side=tk.RIGHT)
        strength_frame = ttk.Frame(result_frame)
        strength_frame.pack(fill=tk.X, pady=10)

        ttk.Label(strength_frame, text="Сложность:").pack(side=tk.LEFT)
        self.strength_label = ttk.Label(
            strength_frame,
            text="—",
            font=Font(weight="bold")
        )
        self.strength_label.pack(side=tk.LEFT, padx=(10, 0))

        self.strength_bar = ttk.Progressbar(
            result_frame,
            length=200,
            mode='determinate'
        )
        self.strength_bar.pack(fill=tk.X, pady=5)

        self.analysis_text = scrolledtext.ScrolledText(
            result_frame,
            height=6,
            font=self.normal_font,
            state=tk.DISABLED,
            wrap=tk.WORD
        )
        self.analysis_text.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    def setup_vault_tab(self):
        self.login_frame = ttk.Frame(self.vault_frame, padding="20")
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            self.login_frame,
            text="🔒 Защищенное хранилище паролей",
            font=self.title_font
        ).pack(pady=(0, 30))

        password_frame = ttk.Frame(self.login_frame)
        password_frame.pack(pady=10)

        ttk.Label(password_frame, text="Мастер-пароль:").pack(side=tk.LEFT)
        self.master_password_var = tk.StringVar()
        master_entry = ttk.Entry(
            password_frame,
            textvariable=self.master_password_var,
            show="•",
            width=30
        )
        master_entry.pack(side=tk.LEFT, padx=(10, 0))

        button_frame = ttk.Frame(self.login_frame)
        button_frame.pack(pady=20)

        ttk.Button(
            button_frame,
            text="🔓 Разблокировать",
            command=self.unlock_vault
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🆕 Создать хранилище",
            command=self.create_vault
        ).pack(side=tk.LEFT, padx=5)

        self.vault_content_frame = ttk.Frame(self.vault_frame)

        columns = ("Сервис", "Логин", "Пароль", "Заметки", "Создан", "Изменен")
        self.password_tree = ttk.Treeview(
            self.vault_content_frame,
            columns=columns,
            show="headings",
            height=15
        )

        for col in columns:
            self.password_tree.heading(col, text=col)
            self.password_tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(
            self.vault_content_frame,
            orient=tk.VERTICAL,
            command=self.password_tree.yview
        )
        self.password_tree.configure(yscrollcommand=scrollbar.set)

        self.password_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        control_frame = ttk.Frame(self.vault_content_frame)
        control_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            control_frame,
            text="➕ Добавить",
            command=self.add_password_dialog
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            control_frame,
            text="✏️ Редактировать",
            command=self.edit_password_dialog
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            control_frame,
            text="🗑️ Удалить",
            command=self.delete_password
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            control_frame,
            text="📋 Копировать",
            command=self.copy_password
        ).pack(side=tk.LEFT, padx=2)

        ttk.Button(
            control_frame,
            text="🔒 Заблокировать",
            command=self.lock_vault
        ).pack(side=tk.RIGHT, padx=2)

    def setup_settings_tab(self):
        """Настройки приложения"""
        settings_frame = ttk.Frame(self.settings_frame, padding="20")
        settings_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            settings_frame,
            text="⚙️ Настройки приложения",
            font=self.title_font
        ).pack(pady=(0, 20))


        gen_settings = ttk.LabelFrame(settings_frame, text="Генератор", padding="15")
        gen_settings.pack(fill=tk.X, pady=10)

        self.auto_copy = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            gen_settings,
            text="Автоматически копировать пароль в буфер обмена",
            variable=self.auto_copy
        ).pack(anchor=tk.W, pady=2)

        self.close_after_copy = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            gen_settings,
            text="Закрывать окно после копирования пароля",
            variable=self.close_after_copy
        ).pack(anchor=tk.W, pady=2)

        vault_settings = ttk.LabelFrame(settings_frame, text="Хранилище", padding="15")
        vault_settings.pack(fill=tk.X, pady=10)

        self.auto_lock = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            vault_settings,
            text="Автоматически блокировать хранилище через",
            variable=self.auto_lock
        ).pack(anchor=tk.W, pady=2)

        lock_time_frame = ttk.Frame(vault_settings)
        lock_time_frame.pack(anchor=tk.W, padx=(20, 0), pady=2)

        self.lock_time = tk.IntVar(value=5)
        ttk.Spinbox(
            lock_time_frame,
            from_=1,
            to=30,
            textvariable=self.lock_time,
            width=5
        ).pack(side=tk.LEFT)
        ttk.Label(lock_time_frame, text="минут").pack(side=tk.LEFT, padx=(5, 0))

        about_frame = ttk.LabelFrame(settings_frame, text="О программе", padding="15")
        about_frame.pack(fill=tk.X, pady=10)

        about_text = """
 Генератор и Хранитель Паролей

Безопасный генератор паролей с шифрованным хранилищем.
Использует современные алгоритмы шифрования.

Разработано на Python с использованием Tkinter
и библиотеки cryptography.
        """

        ttk.Label(
            about_frame,
            text=about_text,
            justify=tk.LEFT
        ).pack(anchor=tk.W)

    def generate_password(self):
        """Генерация пароля"""
        password = generator.generate_password(
            length=self.length_var.get(),
            use_lowercase=self.use_lowercase.get(),
            use_uppercase=self.use_uppercase.get(),
            use_digits=self.use_digits.get(),
            use_symbols=self.use_symbols.get(),
            exclude_ambiguous=self.exclude_ambiguous.get()
        )

        self.current_password = password
        self.password_var.set(password)

        rating, feedback, color, score = generator.check_strength(password)

        self.strength_label.config(text=rating, foreground=color)
        self.strength_bar['value'] = (score / 9) * 100

        self.analysis_text.config(state=tk.NORMAL)
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(1.0, f"Оценка: {rating}\n\n")
        for item in feedback:
            self.analysis_text.insert(tk.END, f"• {item}\n")
        self.analysis_text.config(state=tk.DISABLED)

        if self.auto_copy.get():
            self.copy_to_clipboard()

    def set_level(self, level):
        """Установка уровня сложности"""
        config = generator.LEVELS[level]

        self.use_lowercase.set(config["lowercase"])
        self.use_uppercase.set(config["uppercase"])
        self.use_digits.set(config["digits"])
        self.use_symbols.set(config["symbols"])

        avg_length = (config["min_length"] + config["max_length"]) // 2
        self.length_var.set(avg_length)

    def copy_to_clipboard(self):
        """Копирование в буфер обмена"""
        if self.current_password:
            pyperclip.copy(self.current_password)
            messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

            if self.close_after_copy.get():
                self.root.after(100, self.root.iconify)

    def check_vault(self):
        """Проверка существования хранилища"""
        import os
        if not os.path.exists('data/vault.dat'):
            self.login_frame.tkraise()

    def unlock_vault(self):
        """Разблокировка хранилища"""
        master_password = self.master_password_var.get()
        if not master_password:
            messagebox.showwarning("Предупреждение", "Введите мастер-пароль!")
            return

        if vault.unlock_vault(master_password):
            self.vault_unlocked = True
            self.master_password = master_password
            self.vault_content_frame.pack(fill=tk.BOTH, expand=True)
            self.login_frame.pack_forget()
            self.refresh_password_list()
            messagebox.showinfo("Успех", "Хранилище разблокировано!")
        else:
            messagebox.showerror("Ошибка", "Неверный мастер-пароль!")

    def create_vault(self):
        """Создание нового хранилища"""
        master_password = self.master_password_var.get()
        if not master_password:
            messagebox.showwarning("Предупреждение", "Введите мастер-пароль!")
            return

        if len(master_password) < 8:
            messagebox.showwarning(
                "Предупреждение",
                "Мастер-пароль должен содержать минимум 8 символов!"
            )
            return

        if vault.create_vault(master_password):
            self.vault_unlocked = True
            self.master_password = master_password
            self.vault_content_frame.pack(fill=tk.BOTH, expand=True)
            self.login_frame.pack_forget()
            messagebox.showinfo("Успех", "Хранилище успешно создано!")
        else:
            messagebox.showerror("Ошибка", "Не удалось создать хранилище!")

    def lock_vault(self):
        """Блокировка хранилища"""
        vault.lock_vault()
        self.vault_unlocked = False
        self.master_password = None
        self.vault_content_frame.pack_forget()
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        self.master_password_var.set("")

    def refresh_password_list(self):
        """Обновление списка паролей"""
        for item in self.password_tree.get_children():
            self.password_tree.delete(item)

        passwords = vault.get_passwords()
        for pwd in passwords:
            self.password_tree.insert(
                "",
                tk.END,
                iid=pwd['id'],
                values=(
                    pwd['service'],
                    pwd['username'],
                    "••••••••",
                    pwd['notes'][:30] + "..." if len(pwd['notes']) > 30 else pwd['notes'],
                    pwd['created_at'],
                    pwd['updated_at']
                )
            )

    def add_password_dialog(self):
        """Диалог добавления пароля"""
        dialog = tk.Toplevel(self.root)
        dialog.title("➕ Добавить пароль")
        dialog.geometry("500x400")
        dialog.resizable(False, False)

        ttk.Label(dialog, text="Добавление нового пароля",
                  font=self.title_font).pack(pady=20)

        frame = ttk.Frame(dialog, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Сервис:").grid(row=0, column=0, sticky=tk.W, pady=5)
        service_entry = ttk.Entry(frame, width=40)
        service_entry.grid(row=0, column=1, padx=(10, 0), pady=5)

        ttk.Label(frame, text="Логин:").grid(row=1, column=0, sticky=tk.W, pady=5)
        username_entry = ttk.Entry(frame, width=40)
        username_entry.grid(row=1, column=1, padx=(10, 0), pady=5)

        ttk.Label(frame, text="Пароль:").grid(row=2, column=0, sticky=tk.W, pady=5)
        password_entry = ttk.Entry(frame, width=40)
        password_entry.grid(row=2, column=1, padx=(10, 0), pady=5)

        ttk.Button(
            frame,
            text="🎲 Сгенерировать",
            command=lambda: password_entry.insert(0, generator.generate_by_level("Высокий"))
        ).grid(row=2, column=2, padx=(10, 0), pady=5)

        ttk.Label(frame, text="Заметки:").grid(row=3, column=0, sticky=tk.W, pady=5)
        notes_text = scrolledtext.ScrolledText(frame, width=40, height=5)
        notes_text.grid(row=3, column=1, padx=(10, 0), pady=5)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=3, pady=20)

        def save():
            service = service_entry.get().strip()
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            notes = notes_text.get(1.0, tk.END).strip()

            if not all([service, username, password]):
                messagebox.showwarning("Предупреждение", "Заполните все обязательные поля!")
                return

            if vault.add_password(service, username, password, notes):
                self.refresh_password_list()
                dialog.destroy()
                messagebox.showinfo("Успех", "Пароль сохранен!")
            else:
                messagebox.showerror("Ошибка", "Не удалось сохранить пароль!")

        ttk.Button(button_frame, text="Сохранить", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_password(self):
        """Удаление пароля"""
        selected = self.password_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пароль для удаления!")
            return

        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить этот пароль?"):
            if vault.delete_password(int(selected[0])):
                self.refresh_password_list()
                messagebox.showinfo("Успех", "Пароль удален!")

    def copy_password(self):
        """Копирование пароля"""
        selected = self.password_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите пароль!")
            return

        passwords = vault.get_passwords()
        for pwd in passwords:
            if pwd['id'] == int(selected[0]):
                pyperclip.copy(pwd['password'])
                messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
                break


def main():
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()