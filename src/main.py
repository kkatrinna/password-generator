import sys
import os
import tkinter as tk
from tkinter import messagebox, ttk
from pathlib import Path
import importlib.util
import subprocess


def check_dependencies():
    """Проверка наличия необходимых библиотек"""
    required = {
        'pyperclip': 'pyperclip',
        'cryptography': 'cryptography'
    }

    missing = []

    for package, install_name in required.items():
        if importlib.util.find_spec(package) is None:
            missing.append(install_name)

    if missing:
        print("\n" + "=" * 60)
        print("❌ ОТСУТСТВУЮТ ЗАВИСИМОСТИ")
        print("=" * 60)
        print(f"\nНе найдены библиотеки: {', '.join(missing)}")
        print("\n💡 Установите их командой:")
        print(f"\n   pip install {' '.join(missing)}")
        print("\n   или")
        print(f"\n   pip install -r requirements.txt")
        print("\n" + "=" * 60)

        try:
            root = tk.Tk()
            root.withdraw()
            answer = messagebox.askyesno(
                "Установка зависимостей",
                f"❌ Отсутствуют библиотеки: {', '.join(missing)}\n\n"
                "Хотите установить их сейчас?",
                icon='warning'
            )
            root.destroy()

            if answer:
                print("\n📦 Установка зависимостей...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing)
                    print("✅ Зависимости успешно установлены!")
                    return True
                except subprocess.CalledProcessError as e:
                    print(f"❌ Ошибка установки: {e}")
                    return False
            else:
                return False
        except:
            return False

    return True


def setup_environment():
    """Настройка окружения и путей"""
    root_dir = Path(__file__).parent.absolute()

    if str(root_dir) not in sys.path:
        sys.path.insert(0, str(root_dir))

    data_dir = root_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    gitkeep = data_dir / '.gitkeep'
    if not gitkeep.exists():
        gitkeep.touch()

    return root_dir


def show_splash_screen(root):
    """Показать заставку при запуске"""
    splash = tk.Toplevel(root)
    splash.title("")
    splash.geometry("500x300")
    splash.overrideredirect(True)
    splash.configure(bg='#2c3e50')

    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width - 500) // 2
    y = (screen_height - 300) // 2
    splash.geometry(f"+{x}+{y}")

    title_label = tk.Label(
        splash,
        text="🔐",
        font=("Segoe UI", 64),
        bg='#2c3e50',
        fg='#3498db'
    )
    title_label.pack(pady=(40, 10))

    title_label = tk.Label(
        splash,
        text="PASSWORD GENERATOR",
        font=("Segoe UI", 20, "bold"),
        bg='#2c3e50',
        fg='white'
    )
    title_label.pack()

    subtitle_label = tk.Label(
        splash,
        text="Безопасная генерация паролей",
        font=("Segoe UI", 12),
        bg='#2c3e50',
        fg='#bdc3c7'
    )
    subtitle_label.pack(pady=(10, 30))

    style = ttk.Style()
    style.theme_use('clam')
    style.configure(
        "Splash.Horizontal.TProgressbar",
        background='#3498db',
        troughcolor='#34495e',
        borderwidth=0,
        thickness=10
    )

    progress = ttk.Progressbar(
        splash,
        style="Splash.Horizontal.TProgressbar",
        mode='indeterminate',
        length=300
    )
    progress.pack(pady=20)
    progress.start(10)

    version_label = tk.Label(
        splash,
        text="Версия 2.0.0",
        font=("Segoe UI", 9),
        bg='#2c3e50',
        fg='#95a5a6'
    )
    version_label.pack(side=tk.BOTTOM, pady=20)

    author_label = tk.Label(
        splash,
        text="© 2026 Password Generator",
        font=("Segoe UI", 8),
        bg='#2c3e50',
        fg='#7f8c8d'
    )
    author_label.pack(side=tk.BOTTOM)

    splash.after(2000, splash.destroy)

    return splash


class PasswordGeneratorQuickApp:
    """Упрощенная версия приложения только для генерации паролей"""

    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Генератор паролей")
        self.root.geometry("700x600")
        self.root.minsize(650, 550)
        self.root.configure(bg='#f0f0f0')

        try:
            from src.generator import generator
            self.generator = generator
        except ImportError:
            from generator import PasswordGenerator
            self.generator = PasswordGenerator()

        self.current_password = None
        self.setup_ui()

        self.center_window()

        self.generate_password()

    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def setup_ui(self):
        """Создание интерфейса"""
        main_frame = tk.Frame(self.root, bg='#f0f0f0', padx=30, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            main_frame,
            text="🔐 ГЕНЕРАТОР ПАРОЛЕЙ",
            font=("Segoe UI", 18, "bold"),
            bg='#f0f0f0',
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))

        settings_frame = tk.LabelFrame(
            main_frame,
            text=" Настройки пароля ",
            font=("Segoe UI", 11, "bold"),
            bg='#f0f0f0',
            fg='#34495e',
            padx=20,
            pady=15,
            relief=tk.GROOVE,
            bd=2
        )
        settings_frame.pack(fill=tk.X, pady=(0, 20))

        length_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        length_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            length_frame,
            text="📏 Длина пароля:",
            font=("Segoe UI", 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)

        self.length_var = tk.IntVar(value=12)

        length_spinbox = tk.Spinbox(
            length_frame,
            from_=4,
            to=64,
            textvariable=self.length_var,
            font=("Segoe UI", 10),
            width=10,
            relief=tk.SUNKEN,
            bd=1,
            command=self.generate_password
        )
        length_spinbox.pack(side=tk.LEFT, padx=(15, 10))

        for length in [8, 12, 16, 20, 24]:
            btn = tk.Button(
                length_frame,
                text=str(length),
                font=("Segoe UI", 9),
                width=3,
                bg='#ecf0f1',
                fg='#2c3e50',
                relief=tk.RAISED,
                bd=1,
                cursor='hand2',
                command=lambda l=length: self.set_length(l)
            )
            btn.pack(side=tk.LEFT, padx=2)

        chars_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        chars_frame.pack(fill=tk.X, pady=(15, 5))

        tk.Label(
            chars_frame,
            text="🔤 Наборы символов:",
            font=("Segoe UI", 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(anchor=tk.W)

        checkboxes_frame = tk.Frame(settings_frame, bg='#f0f0f0')
        checkboxes_frame.pack(fill=tk.X, padx=(20, 0), pady=(5, 0))

        left_col = tk.Frame(checkboxes_frame, bg='#f0f0f0')
        left_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.use_lowercase = tk.BooleanVar(value=True)
        self.use_uppercase = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)

        tk.Checkbutton(
            left_col,
            text="Строчные буквы (a-z)",
            variable=self.use_lowercase,
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#2c3e50',
            activebackground='#f0f0f0',
            cursor='hand2',
            command=self.generate_password
        ).pack(anchor=tk.W, pady=2)

        tk.Checkbutton(
            left_col,
            text="Заглавные буквы (A-Z)",
            variable=self.use_uppercase,
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#2c3e50',
            activebackground='#f0f0f0',
            cursor='hand2',
            command=self.generate_password
        ).pack(anchor=tk.W, pady=2)

        tk.Checkbutton(
            left_col,
            text="Цифры (0-9)",
            variable=self.use_digits,
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#2c3e50',
            activebackground='#f0f0f0',
            cursor='hand2',
            command=self.generate_password
        ).pack(anchor=tk.W, pady=2)

        right_col = tk.Frame(checkboxes_frame, bg='#f0f0f0')
        right_col.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.use_symbols = tk.BooleanVar(value=True)
        self.exclude_ambiguous = tk.BooleanVar(value=False)

        tk.Checkbutton(
            right_col,
            text="Спецсимволы (!@#$%)",
            variable=self.use_symbols,
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#2c3e50',
            activebackground='#f0f0f0',
            cursor='hand2',
            command=self.generate_password
        ).pack(anchor=tk.W, pady=2)

        tk.Checkbutton(
            right_col,
            text="Исключить похожие (Il1O0)",
            variable=self.exclude_ambiguous,
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#2c3e50',
            activebackground='#f0f0f0',
            cursor='hand2',
            command=self.generate_password
        ).pack(anchor=tk.W, pady=2)

        result_frame = tk.LabelFrame(
            main_frame,
            text=" Сгенерированный пароль ",
            font=("Segoe UI", 11, "bold"),
            bg='#f0f0f0',
            fg='#34495e',
            padx=20,
            pady=15,
            relief=tk.GROOVE,
            bd=2
        )
        result_frame.pack(fill=tk.BOTH, expand=True)

        password_display_frame = tk.Frame(result_frame, bg='#f0f0f0')
        password_display_frame.pack(fill=tk.X, pady=(10, 15))

        self.password_var = tk.StringVar()

        password_entry = tk.Entry(
            password_display_frame,
            textvariable=self.password_var,
            font=("Courier New", 16, "bold"),
            justify=tk.CENTER,
            state='readonly',
            readonlybackground='white',
            bd=2,
            relief=tk.SUNKEN,
            fg='#2c3e50'
        )
        password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)

        copy_btn = tk.Button(
            password_display_frame,
            text="📋 Копировать",
            font=("Segoe UI", 10, "bold"),
            bg='#3498db',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=15,
            cursor='hand2',
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side=tk.RIGHT, padx=(10, 0))

        generate_btn = tk.Button(
            result_frame,
            text="🔄 СГЕНЕРИРОВАТЬ НОВЫЙ ПАРОЛЬ",
            font=("Segoe UI", 12, "bold"),
            bg='#2ecc71',
            fg='white',
            relief=tk.RAISED,
            bd=2,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.generate_password
        )
        generate_btn.pack(pady=(0, 15))
        info_frame = tk.Frame(result_frame, bg='#f0f0f0')
        info_frame.pack(fill=tk.X)

        strength_frame = tk.Frame(info_frame, bg='#f0f0f0')
        strength_frame.pack(fill=tk.X, pady=5)

        tk.Label(
            strength_frame,
            text="Сложность:",
            font=("Segoe UI", 10),
            bg='#f0f0f0',
            fg='#2c3e50'
        ).pack(side=tk.LEFT)

        self.strength_label = tk.Label(
            strength_frame,
            text="—",
            font=("Segoe UI", 10, "bold"),
            bg='#f0f0f0'
        )
        self.strength_label.pack(side=tk.LEFT, padx=(10, 0))

        self.strength_bar = ttk.Progressbar(
            info_frame,
            length=300,
            mode='determinate',
            style="Strength.Horizontal.TProgressbar"
        )
        self.strength_bar.pack(fill=tk.X, pady=5)

        self.length_info = tk.Label(
            info_frame,
            text="",
            font=("Segoe UI", 9),
            bg='#f0f0f0',
            fg='#7f8c8d'
        )
        self.length_info.pack(pady=(5, 0))

    def set_length(self, length):
        """Установка длины пароля"""
        self.length_var.set(length)
        self.generate_password()

    def generate_password(self):
        """Генерация пароля"""
        try:
            if not any([
                self.use_lowercase.get(),
                self.use_uppercase.get(),
                self.use_digits.get(),
                self.use_symbols.get()
            ]):
                self.use_lowercase.set(True)

            password = self.generator.generate_password(
                length=self.length_var.get(),
                use_lowercase=self.use_lowercase.get(),
                use_uppercase=self.use_uppercase.get(),
                use_digits=self.use_digits.get(),
                use_symbols=self.use_symbols.get(),
                exclude_ambiguous=self.exclude_ambiguous.get()
            )

            self.current_password = password
            self.password_var.set(password)

            rating, feedback, color, score = self.generator.check_strength(password)

            self.strength_label.config(text=rating, fg=color)
            self.strength_bar['value'] = (score / 9) * 100

            style = ttk.Style()
            style.theme_use('clam')
            style.configure(
                "Strength.Horizontal.TProgressbar",
                background=color,
                troughcolor='#e0e0e0',
                borderwidth=0,
                thickness=15
            )

            # Информация о длине
            self.length_info.config(
                text=f"Длина: {len(password)} символов | "
                     f"Уникальных символов: {len(set(password))}"
            )

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сгенерировать пароль:\n{e}")

    def copy_to_clipboard(self):
        """Копирование пароля в буфер обмена"""
        if self.current_password:
            try:
                import pyperclip
                pyperclip.copy(self.current_password)

                self.show_copy_feedback()

            except ImportError:
                self.root.clipboard_clear()
                self.root.clipboard_append(self.current_password)

                messagebox.showinfo(
                    "Успех",
                    "✅ Пароль скопирован в буфер обмена!"
                )
            except Exception as e:
                messagebox.showerror(
                    "Ошибка",
                    f"❌ Не удалось скопировать пароль:\n{e}"
                )

    def show_copy_feedback(self):
        """Показать всплывающее уведомление о копировании"""
        popup = tk.Toplevel(self.root)
        popup.title("")
        popup.geometry("250x100")
        popup.overrideredirect(True)
        popup.configure(bg='#2ecc71')

        x = self.root.winfo_x() + self.root.winfo_width() // 2 - 125
        y = self.root.winfo_y() + self.root.winfo_height() // 2 - 50
        popup.geometry(f"+{x}+{y}")

        tk.Label(
            popup,
            text="✅",
            font=("Segoe UI", 32),
            bg='#2ecc71',
            fg='white'
        ).pack(pady=(10, 0))

        tk.Label(
            popup,
            text="Пароль скопирован!",
            font=("Segoe UI", 12, "bold"),
            bg='#2ecc71',
            fg='white'
        ).pack(pady=(5, 0))

        popup.after(1500, popup.destroy)


def main():
    """Главная функция запуска"""
    print("\n" + "=" * 60)
    print("🔐 ЗАПУСК ГЕНЕРАТОРА ПАРОЛЕЙ")
    print("=" * 60)

    project_dir = setup_environment()
    print(f"📁 Проект: {project_dir}")
    print(f"📁 Данные: {project_dir / 'data'}")

    if not check_dependencies():
        print("\n❌ Невозможно запустить приложение без зависимостей.")
        print("💡 Установите зависимости и попробуйте снова.")
        input("\nНажмите Enter для выхода...")
        sys.exit(1)

    try:
        root = tk.Tk()

        try:
            splash = show_splash_screen(root)
        except Exception as e:
            print(f"⚠️ Не удалось показать заставку: {e}")

        print("\n✅ Запуск графического интерфейса...")
        app = PasswordGeneratorQuickApp(root)

        def on_closing():
            if messagebox.askyesno(
                    "Выход",
                    "Вы уверены, что хотите выйти?",
                    icon='question'
            ):
                print("\n👋 Программа завершена")
                root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        def on_key_press(event):
            if event.keysym == 'Escape':
                on_closing()
            elif event.keysym == 'F5':
                app.generate_password()
            elif event.state == 4 and event.keysym == 'c':  # Ctrl+C
                app.copy_to_clipboard()
            elif event.state == 4 and event.keysym == 'g':  # Ctrl+G
                app.generate_password()

        root.bind('<Escape>', on_key_press)
        root.bind('<F5>', lambda e: app.generate_password())
        root.bind('<Control-c>', lambda e: app.copy_to_clipboard())
        root.bind('<Control-g>', lambda e: app.generate_password())

        print("\n" + "=" * 60)
        print("✅ ПРИЛОЖЕНИЕ УСПЕШНО ЗАПУЩЕНО!")
        print("=" * 60)
        print("\n📌 ГОРЯЧИЕ КЛАВИШИ:")
        print("   • F5         - Сгенерировать пароль")
        print("   • Ctrl+C     - Копировать пароль")
        print("   • Ctrl+G     - Сгенерировать новый")
        print("   • Escape     - Выход")
        print("\n" + "=" * 60)

        root.mainloop()

    except ImportError as e:
        print(f"\n❌ Ошибка импорта: {e}")
        print("\n💡 Проверьте структуру проекта:")
        print("   password-generator/")
        print("   ├── main.py (текущий файл)")
        print("   ├── src/")
        print("   │   ├── generator.py")
        print("   │   └── utils.py")
        print("   └── requirements.txt")
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Ошибка запуска",
                f"❌ Не удалось загрузить компоненты приложения:\n\n{e}\n\n"
                f"Проверьте структуру проекта."
            )
            root.destroy()
        except:
            pass

        input("\nНажмите Enter для выхода...")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {e}")
        import traceback
        traceback.print_exc()

        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Критическая ошибка",
                f"❌ Произошла непредвиденная ошибка:\n\n{e}\n\n"
                f"Подробности в консоли."
            )
            root.destroy()
        except:
            pass

        input("\nНажмите Enter для выхода...")
        sys.exit(1)


def quick_generate():
    """Быстрая генерация пароля из командной строки"""
    try:
        from src.generator import generator
    except ImportError:
        try:
            from generator import PasswordGenerator
            generator = PasswordGenerator()
        except ImportError:
            print("❌ Ошибка: Не найден модуль генератора")
            return

    password = generator.generate_by_level("Высокий", 16)
    print(f"\n🔐 Сгенерированный пароль: \033[92m{password}\033[0m")
    print(f"📋 Длина: {len(password)} символов")

    # Копируем в буфер обмена
    try:
        import pyperclip
        pyperclip.copy(password)
        print("✅ Пароль скопирован в буфер обмена!")
    except:
        try:
            import tkinter as tk
            root = tk.Tk()
            root.withdraw()
            root.clipboard_clear()
            root.clipboard_append(password)
            root.destroy()
            print("✅ Пароль скопирован в буфер обмена!")
        except:
            print("⚠️ Не удалось скопировать пароль")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="🔐 Генератор безопасных паролей",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python main.py              # Запуск графического интерфейса
  python main.py --quick      # Быстрая генерация пароля в консоли
  python main.py --length 20  # Пароль длиной 20 символов
  python main.py --no-symbols # Пароль без спецсимволов
  python main.py --copy       # Сгенерировать и скопировать
        """
    )

    parser.add_argument(
        '--quick', '-q',
        action='store_true',
        help='Быстрая генерация пароля в консоли'
    )

    parser.add_argument(
        '--length', '-l',
        type=int,
        default=16,
        help='Длина пароля (по умолчанию: 16)'
    )

    parser.add_argument(
        '--no-symbols',
        action='store_true',
        help='Без спецсимволов'
    )

    parser.add_argument(
        '--no-digits',
        action='store_true',
        help='Без цифр'
    )

    parser.add_argument(
        '--copy', '-c',
        action='store_true',
        help='Копировать в буфер обмена'
    )

    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='Показать версию'
    )

    args = parser.parse_args()

    if args.version:
        print("🔐 Password Generator v2.0.0")
        print("© 2026 Все права защищены")
        sys.exit(0)

    if args.quick:
        quick_generate()
        sys.exit(0)

    main()