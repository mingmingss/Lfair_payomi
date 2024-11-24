import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
import json
import os


class CustomStyle:
    def __init__(self):
        self.colors = {
            'primary': '#2196F3',  # Blue
            'secondary': '#757575',  # Gray
            'success': '#4CAF50',  # Green
            'warning': '#FFC107',  # Yellow
            'danger': '#F44336',  # Red
            'light': '#F5F5F5',  # Light Gray
            'dark': '#090909',  # Dark Gray
            'white': '#FFFFFF',
            'background': '#F0F2F5'  # Light blue-gray
        }

        self.fonts = {
            'title': ('Helvetica', 16, 'bold'),
            'subtitle': ('Helvetica', 14, 'bold'),
            'heading': ('Helvetica', 12, 'bold'),
            'body': ('Helvetica', 10),
            'small': ('Helvetica', 9)
        }

        self.apply_style()

    def apply_style(self):
        style = ttk.Style()

        # Configure medinote styles
        style.configure('Main.TFrame', background=self.colors['background'])
        style.configure('Card.TFrame', background=self.colors['white'])

        # Button styles
        style.configure('Primary.TButton',
                        font=self.fonts['body'],
                        background=self.colors['primary'])

        style.configure('Danger.TButton',
                        font=self.fonts['body'],
                        background=self.colors['danger'])

        # Label styles
        style.configure('Title.TLabel',
                        font=self.fonts['title'],
                        background=self.colors['dark'],
                        foreground=self.colors['white'])

        style.configure('Subtitle.TLabel',
                        font=self.fonts['subtitle'],
                        background=self.colors['white'],
                        foreground=self.colors['secondary'])

        style.configure('Heading.TLabel',
                        font=self.fonts['heading'],
                        background=self.colors['dark'],
                        foreground=self.colors['white'])

        style.configure('Body.TLabel',
                        font=self.fonts['body'],
                        background=self.colors['dark'],
                        foreground=self.colors['white'])


class UserInfoDialog:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("사용자 정보 입력")
        self.window.geometry("450x600")
        self.window.configure(bg=CustomStyle().colors['background'])
        self.window.transient(parent)
        self.window.grab_set()

        self.style = CustomStyle()
        self.result = None
        self.create_widgets()

    def create_widgets(self):
        # Main container with padding and background
        main_frame = ttk.Frame(self.window, style='Main.TFrame', padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Card-like container
        card_frame = ttk.Frame(main_frame, style='Card.TFrame', padding="20")
        card_frame.pack(fill=tk.BOTH, expand=True)

        # Title with icon-like emoji
        title_text = "👤 사용자 정보"
        ttk.Label(card_frame,
                  text=title_text,
                  style='Title.TLabel').pack(pady=(0, 20))

        # Subtitle
        ttk.Label(card_frame,
                  text="안전한 약물 복용을 위해\n기본 정보를 입력해주세요.",
                  style='Subtitle.TLabel',
                  justify="center").pack(pady=(0, 30))

        # Input fields
        fields = [
            ("이름", "name", "👤"),
            ("나이", "age", "📅"),
            ("성별", "gender", "⚤"),
            ("키 (cm)", "height", "📏"),
            ("몸무게 (kg)", "weight", "⚖️"),
            ("특이사항\n(알레르기/지병 등)", "notes", "📝")
        ]

        self.entries = {}

        for label, field, icon in fields:
            frame = ttk.Frame(card_frame, style='Card.TFrame')
            frame.pack(fill=tk.X, pady=10)

            # Label with icon
            label_text = f"{icon} {label}"
            ttk.Label(frame,
                      text=label_text,
                      style='Body.TLabel',
                      width=15).pack(side=tk.LEFT)

            if field == "gender":
                self.entries[field] = tk.StringVar(value="남성")
                gender_frame = ttk.Frame(frame, style='Card.TFrame')
                gender_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

                for gender in ["남성", "여성"]:
                    radio = ttk.Radiobutton(gender_frame,
                                            text=gender,
                                            variable=self.entries[field],
                                            value=gender)
                    radio.pack(side=tk.LEFT, padx=10)

            elif field == "notes":
                self.entries[field] = ScrolledText(frame,
                                                   height=4,
                                                   width=30,
                                                   font=self.style.fonts['body'])
                self.entries[field].pack(side=tk.LEFT, fill=tk.X, expand=True)
            else:
                self.entries[field] = ttk.Entry(frame, font=self.style.fonts['body'])
                self.entries[field].pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Buttons
        button_frame = ttk.Frame(card_frame, style='Card.TFrame')
        button_frame.pack(pady=30)

        ttk.Button(button_frame,
                   text="✔️ 저장",
                   style='Primary.TButton',
                   command=self.save).pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame,
                   text="❌ 취소",
                   style='Danger.TButton',
                   command=self.cancel).pack(side=tk.LEFT, padx=5)

    def save(self):
        # 필수 입력 확인
        required_fields = ["name", "age", "height", "weight"]
        for field in required_fields:
            value = self.entries[field].get() if isinstance(self.entries[field], ttk.Entry) else ""
            if not value.strip():
                messagebox.showerror("오류", f"{field.title()}을(를) 입력해주세요.")
                return

        # 숫자 필드 확인
        number_fields = ["age", "height", "weight"]
        for field in number_fields:
            try:
                float(self.entries[field].get())
            except ValueError:
                messagebox.showerror("오류", f"{field.title()}는 숫자로 입력해주세요.")
                return

        # 데이터 수집
        self.result = {
            "name": self.entries["name"].get(),
            "age": int(self.entries["age"].get()),
            "gender": self.entries["gender"].get(),
            "height": float(self.entries["height"].get()),
            "weight": float(self.entries["weight"].get()),
            "notes": self.entries["notes"].get("1.0", tk.END).strip()
        }

        self.window.destroy()

    def cancel(self):
        self.window.destroy()


class MedicationBanner(ttk.Frame):
    def __init__(self, parent, medication_data, manager, **kwargs):
        super().__init__(parent, **kwargs)
        self.medication_data = medication_data
        self.manager = manager
        self.style = CustomStyle()

        # Card-like container
        self.configure(style='Card.TFrame', padding="15")

        # Main content frame
        content_frame = ttk.Frame(self, style='Card.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Header with product name and time
        header_frame = ttk.Frame(content_frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X)

        # Product name with pill icon
        name_frame = ttk.Frame(header_frame, style='Card.TFrame')
        name_frame.pack(side=tk.LEFT)

        ttk.Label(name_frame,
                  text="💊 " + medication_data['Product Name'],
                  style='Heading.TLabel').pack(side=tk.LEFT)

        # Time with clock icon (only if notification time is set)
        if pd.notna(medication_data['Notification Time']):
            time_frame = ttk.Frame(header_frame, style='Card.TFrame')
            time_frame.pack(side=tk.RIGHT)

            notification_status = "🔔" if medication_data.get('Notifications_Enabled', True) else "🔕"
            time_text = f"{notification_status} 복용시간: {medication_data['Notification Time']}"
            ttk.Label(time_frame,
                      text=time_text,
                      style='Body.TLabel').pack(side=tk.RIGHT)

        # Medication details
        details_frame = ttk.Frame(content_frame, style='Card.TFrame')
        details_frame.pack(fill=tk.X, pady=(10, 0))

        # Icons for different types of information
        info_text = f"🧬 주요성분: {medication_data['Main Ingredient']}\n"
        info_text += f"✨ 효능: {medication_data['Effectiveness']}\n"
        info_text += f"📝 복용방법: {medication_data['How to Take It']}\n"
        info_text += f"⚠️ 주의사항: {medication_data['Medications to Avoid']}"

        ttk.Label(details_frame,
                  text=info_text,
                  style='Body.TLabel',
                  wraplength=400).pack(fill=tk.X)

        # Action buttons
        button_frame = ttk.Frame(content_frame, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame,
                   text="🔍 상세정보",
                   style='Primary.TButton',
                   command=self.show_details).pack(side=tk.LEFT, padx=2)

        ttk.Button(button_frame,
                   text="⏰ 시간변경",
                   style='Primary.TButton',
                   command=self.change_time).pack(side=tk.LEFT, padx=2)

        ttk.Button(button_frame,
                   text="🗑️ 삭제",
                   style='Danger.TButton',
                   command=self.delete_medication).pack(side=tk.LEFT, padx=2)

    def show_details(self):
        details_window = tk.Toplevel(self)
        details_window.title(f"약물 상세 정보 - {self.medication_data['Product Name']}")
        details_window.geometry("600x400")
        details_window.configure(bg=self.style.colors['background'])

        # Card-like container
        card_frame = ttk.Frame(details_window, style='Card.TFrame', padding="20")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        ttk.Label(card_frame,
                  text=f"💊 {self.medication_data['Product Name']}",
                  style='Title.TLabel').pack(pady=(0, 20))

        # Scrollable text area with styling
        info_text = ScrolledText(card_frame,
                                 font=self.style.fonts['body'],
                                 wrap=tk.WORD,
                                 height=15)
        info_text.pack(fill=tk.BOTH, expand=True)

        # Add content with icons
        for key, value in self.medication_data.items():
            if key != 'index':
                icon = self.get_icon_for_field(key)
                info_text.insert(tk.END, f"{icon} {key}: {value}\n\n")

        info_text.configure(state='disabled')

    def get_icon_for_field(self, field):
        icons = {
            'Product Name': '💊',
            'Company Name': '🏢',
            'Main Ingredient': '🧬',
            'Effectiveness': '✨',
            'How to Take It': '📝',
            'Precautions': '⚠️',
            'Warnings': '⛔',
            'Medications to Avoid': '❌',
            'Major Side Effects': '🚫',
            'Storage Instructions': '📦',
            'Notification Time': '⏰'
        }
        return icons.get(field, '📌')

    def change_time(self):
        time_window = tk.Toplevel(self)
        time_window.title("복용 시간 설정")
        time_window.geometry("400x550")
        time_window.configure(bg=self.style.colors['background'])

        # Card-like container
        card_frame = ttk.Frame(time_window, style='Card.TFrame', padding="20")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        ttk.Label(card_frame,
                  text="⏰ 복용 시간 설정",
                  style='Title.TLabel').pack(pady=(0, 20))

        # Enable/Disable notifications
        notifications_var = tk.BooleanVar(value=pd.notna(self.medication_data['Notification Time']))
        notifications_check = ttk.Checkbutton(
            card_frame,
            text="알림 설정",
            variable=notifications_var,
            style='Primary.TCheckbutton'
        )
        notifications_check.pack(pady=(0, 10))

        # Time input frame
        time_frame = ttk.Frame(card_frame, style='Card.TFrame')
        time_frame.pack(fill=tk.X, pady=10)

        ttk.Label(time_frame,
                  text="복용 시간:",
                  style='Body.TLabel').pack()
        time_entry = ttk.Entry(time_frame, font=self.style.fonts['body'])
        time_entry.pack(pady=5)

        # 기존 시간이 있으면 입력
        if pd.notna(self.medication_data['Notification Time']):
            time_entry.insert(0, self.medication_data['Notification Time'])

        ttk.Label(time_frame,
                  text="형식: HH:MM (예: 09:00)\n알림을 받지 않으려면 비워두세요",
                  style='Body.TLabel',
                  justify='center').pack()

        # Condition selection
        condition_frame = ttk.Frame(card_frame, style='Card.TFrame')
        condition_frame.pack(fill=tk.X, pady=20)

        ttk.Label(condition_frame,
                  text="복용 조건:",
                  style='Body.TLabel').pack()

        current_condition = self.medication_data.get('Taking_Condition', '식후')
        condition_var = tk.StringVar(value=current_condition)

        conditions = {
            '식전': '식사하기 30분 전에 복용하세요.',
            '식후': '식사 직후에 복용하세요.',
            '공복': '식사와 식사 사이 충분한 시간이 지난 후 복용하세요.\n(보통 식사 2시간 후)'
        }

        for condition in conditions.keys():
            ttk.Radiobutton(condition_frame,
                            text=condition,
                            variable=condition_var,
                            value=condition).pack(padx=5, pady=5)

        # Explanation label
        explanation_label = ttk.Label(card_frame,
                                      text=conditions[current_condition],
                                      style='Body.TLabel',
                                      wraplength=350)
        explanation_label.pack(pady=10)

        def update_explanation(*args):
            selected = condition_var.get()
            if selected in conditions:
                explanation_label.config(text=conditions[selected])

        condition_var.trace('w', update_explanation)

        def save_new_time():
            time_str = time_entry.get().strip()
            notifications_enabled = notifications_var.get()

            if time_str:  # 시간이 입력된 경우
                try:
                    datetime.strptime(time_str, "%H:%M")
                except ValueError:
                    messagebox.showerror("오류", "올바른 시간 형식을 입력하세요 (HH:MM)")
                    return
            else:  # 시간이 입력되지 않은 경우
                time_str = None

            updates = {
                'Notification Time': time_str,
                'Taking_Condition': condition_var.get(),
                'Notifications_Enabled': notifications_enabled
            }

            self.manager.update_medication(
                self.medication_data['Product Name'],
                updates
            )

            time_window.destroy()
            success_msg = "복용 설정이 변경되었습니다."
            if not time_str:
                success_msg += "\n알림 시간이 설정되지 않았습니다."
            messagebox.showinfo("성공", success_msg)

        ttk.Button(card_frame,
                   text="✔️ 저장",
                   style='Primary.TButton',
                   command=save_new_time).pack(pady=20)

    def delete_medication(self):
        if messagebox.askyesno("확인", "이 약물을 삭제하시겠습니까?"):
            self.manager.delete_medication(self.medication_data['Product Name'])
            self.destroy()


class MedicationManager:
    def __init__(self, root):
        self.root = root
        self.root.title("복용 약물 관리")
        self.root.geometry("800x600")
        self.style = CustomStyle()
        self.root.configure(bg=self.style.colors['background'])

        # 사용자 정보 로드 또는 입력 받기
        self.load_or_create_user_info()

        # 데이터 로드
        try:
            self.medication_db = pd.read_excel('medications.xlsx')
        except FileNotFoundError:
            self.medication_db = pd.DataFrame(columns=[
                'Product Name', 'Company Name', 'Main Ingredient',
                'Effectiveness', 'How to Take It', 'Precautions',
                'Warnings', 'Medications to Avoid', 'Major Side Effects',
                'Storage Instructions'
            ])

        try:
            self.my_medications = pd.read_excel('my_medications.xlsx')
        except FileNotFoundError:
            self.my_medications = pd.DataFrame(columns=[
                'Product Name', 'Company Name', 'Main Ingredient',
                'Effectiveness', 'How to Take It', 'Precautions',
                'Warnings', 'Medications to Avoid', 'Major Side Effects',
                'Storage Instructions', 'Notification Time', 'Notifications_Enabled'
            ])

        self.create_main_screen()
        self.check_notifications()

    def load_or_create_user_info(self):
        if os.path.exists('user_info.json'):
            with open('user_info.json', 'r', encoding='utf-8') as f:
                self.user_info = json.load(f)
        else:
            dialog = UserInfoDialog(self.root)
            self.root.wait_window(dialog.window)

            if dialog.result is None:
                messagebox.showwarning("경고", "사용자 정보는 필수입니다.")
                self.root.quit()
                return

            self.user_info = dialog.result
            with open('user_info.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_info, f, ensure_ascii=False, indent=2)

    def create_main_screen(self):
        # Main container with background
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # User info card
        user_card = ttk.Frame(self.main_frame, style='Card.TFrame', padding="20")
        user_card.pack(fill=tk.X, pady=(0, 20))

        # User info header
        user_header = ttk.Frame(user_card, style='Card.TFrame')
        user_header.pack(fill=tk.X)

        ttk.Label(user_header,
                  text=f"👤 {self.user_info['name']}님의 복용 약물",
                  style='Title.TLabel').pack(side=tk.LEFT)

        ttk.Button(user_header,
                   text="✏️ 정보 수정",
                   style='Primary.TButton',
                   command=self.edit_user_info).pack(side=tk.RIGHT)

        # User details
        user_details = f"나이: {self.user_info['age']}세 | " \
                       f"성별: {self.user_info['gender']} | " \
                       f"키: {self.user_info['height']}cm | " \
                       f"몸무게: {self.user_info['weight']}kg"
        ttk.Label(user_card,
                  text=user_details,
                  style='Body.TLabel').pack(pady=(10, 0))

        # Add medication button
        ttk.Button(self.main_frame,
                   text="➕ 복용 약물 추가",
                   style='Primary.TButton',
                   command=self.show_add_screen).pack(pady=(0, 20))

        # Scrollable frame for medications
        self.create_scrollable_frame()
        self.update_medication_list()

    def edit_user_info(self):
        dialog = UserInfoDialog(self.root)

        # 현재 정보로 필드 채우기
        for field, value in self.user_info.items():
            if field == "notes":
                dialog.entries[field].insert("1.0", str(value))
            elif field == "gender":
                dialog.entries[field].set(value)
            else:
                dialog.entries[field].insert(0, str(value))

        self.root.wait_window(dialog.window)

        if dialog.result:
            self.user_info = dialog.result
            with open('user_info.json', 'w', encoding='utf-8') as f:
                json.dump(self.user_info, f, ensure_ascii=False, indent=2)

            # 메인 화면 새로고침
            self.main_frame.destroy()
            self.create_main_screen()

    def create_scrollable_frame(self):
        # Create canvas
        self.canvas = tk.Canvas(self.main_frame,
                                bg=self.style.colors['background'],
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.main_frame,
                                  orient=tk.VERTICAL,
                                  command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Main.TFrame')

        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0),
                                  window=self.scrollable_frame,
                                  anchor="nw",
                                  width=self.canvas.winfo_width())

        # Update canvas width when medinote frame is resized
        def on_frame_configure(event):
            canvas_width = event.width - scrollbar.winfo_width()
            self.canvas.itemconfig(1, width=canvas_width)

        self.main_frame.bind('<Configure>', on_frame_configure)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def show_add_screen(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("복용 약물 추가")
        add_window.geometry("600x500")
        add_window.configure(bg=self.style.colors['background'])

        # Main card container
        card_frame = ttk.Frame(add_window, style='Card.TFrame', padding="20")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        ttk.Label(card_frame,
                  text="➕ 복용 약물 추가",
                  style='Title.TLabel').pack(pady=(0, 20))

        # Search frame
        search_frame = ttk.Frame(card_frame, style='Card.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(search_frame,
                  text="🔍 약물 검색:",
                  style='Body.TLabel').pack(side=tk.LEFT, padx=(0, 10))

        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame,
                                 textvariable=search_var,
                                 font=self.style.fonts['body'])
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Treeview for search results
        columns = ('제품명', '주요 성분', '효능')
        search_tree = ttk.Treeview(card_frame,
                                   columns=columns,
                                   show='headings',
                                   height=10)

        for col in columns:
            search_tree.heading(col, text=col)
            search_tree.column(col, width=120)

        search_tree.pack(fill=tk.BOTH, expand=True, pady=10)

        def search_medications(*args):
            search_text = search_var.get().lower()
            for item in search_tree.get_children():
                search_tree.delete(item)

            for _, row in self.medication_db.iterrows():
                if (search_text in str(row['Product Name']).lower() or
                        search_text in str(row['Main Ingredient']).lower() or
                        search_text in str(row['Effectiveness']).lower()):
                    search_tree.insert('', tk.END, values=(
                        row['Product Name'],
                        row['Main Ingredient'],
                        row['Effectiveness']
                    ))

        search_var.trace('w', search_medications)

        def add_selected_medication():
            selected_item = search_tree.selection()
            if not selected_item:
                messagebox.showwarning("경고", "약물을 선택해주세요.")
                return

            selected_values = search_tree.item(selected_item)['values']
            selected_name = selected_values[0]

            if not self.my_medications[
                self.my_medications['Product Name'] == selected_name
            ].empty:
                messagebox.showwarning("경고", "이미 추가된 약물입니다.")
                return

            medication_info = self.medication_db[
                self.medication_db['Product Name'] == selected_name
                ].iloc[0]

            self.set_notification_time(medication_info, add_window)

        ttk.Button(card_frame,
                   text="✔️ 선택 약물 추가",
                   style='Primary.TButton',
                   command=add_selected_medication).pack(pady=10)

    def set_notification_time(self, medication_info, parent_window):
        time_window = tk.Toplevel(parent_window)
        time_window.title("복용 시간 설정")
        time_window.geometry("400x550")
        time_window.configure(bg=self.style.colors['background'])

        # Card container
        card_frame = ttk.Frame(time_window, style='Card.TFrame', padding="20")
        card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title
        ttk.Label(card_frame,
                  text="⏰ 복용 시간 설정",
                  style='Title.TLabel').pack(pady=(0, 20))

        # Enable/Disable notifications
        notifications_var = tk.BooleanVar(value=True)
        notifications_check = ttk.Checkbutton(
            card_frame,
            text="알림 설정",
            variable=notifications_var,
            style='Primary.TCheckbutton'
        )
        notifications_check.pack(pady=(0, 10))

        # Time input frame
        time_frame = ttk.Frame(card_frame, style='Card.TFrame')
        time_frame.pack(fill=tk.X, pady=10)

        ttk.Label(time_frame,
                  text="복용 시간:",
                  style='Body.TLabel').pack()
        time_entry = ttk.Entry(time_frame, font=self.style.fonts['body'])
        time_entry.pack(pady=5)

        ttk.Label(time_frame,
                  text="형식: HH:MM (예: 09:00)\n알림을 받지 않으려면 비워두세요",
                  style='Body.TLabel',
                  justify='center').pack()

        # Condition selection
        condition_frame = ttk.Frame(card_frame, style='Card.TFrame')
        condition_frame.pack(fill=tk.X, pady=20)

        ttk.Label(condition_frame,
                  text="복용 조건:",
                  style='Body.TLabel').pack()

        condition_var = tk.StringVar(value='식후')

        conditions = {
            '식전': '식사하기 30분 전에 복용하세요.',
            '식후': '식사 직후에 복용하세요.',
            '공복': '식사와 식사 사이 충분한 시간이 지난 후 복용하세요.\n(보통 식사 2시간 후)'
        }

        for condition in conditions.keys():
            ttk.Radiobutton(condition_frame,
                            text=condition,
                            variable=condition_var,
                            value=condition).pack(padx=5, pady=5)

        # Explanation label
        explanation_label = ttk.Label(card_frame,
                                      text=conditions['식후'],
                                      style='Body.TLabel',
                                      wraplength=350)
        explanation_label.pack(pady=10)

        def update_explanation(*args):
            selected = condition_var.get()
            if selected in conditions:
                explanation_label.config(text=conditions[selected])

        condition_var.trace('w', update_explanation)

        def save_with_time():
            time_str = time_entry.get().strip()
            notifications_enabled = notifications_var.get()

            if time_str:  # If time is provided
                try:
                    datetime.strptime(time_str, "%H:%M")
                except ValueError:
                    messagebox.showerror("오류", "올바른 시간 형식을 입력하세요 (HH:MM)")
                    return
            else:  # If no time is provided
                time_str = None

            medication_info_dict = medication_info.to_dict()
            medication_info_dict['Notification Time'] = time_str
            medication_info_dict['Taking_Condition'] = condition_var.get()
            medication_info_dict['Notifications_Enabled'] = notifications_enabled

            self.my_medications = pd.concat([
                self.my_medications,
                pd.DataFrame([medication_info_dict])
            ], ignore_index=True)

            self.my_medications.to_excel('my_medications.xlsx', index=False)
            self.update_medication_list()

            time_window.destroy()
            parent_window.destroy()

            success_msg = "약물이 추가되었습니다."
            if not time_str:
                success_msg += "\n알림 시간이 설정되지 않았습니다."
            messagebox.showinfo("성공", success_msg)

        ttk.Button(card_frame,
                   text="✔️ 저장",
                   style='Primary.TButton',
                   command=save_with_time).pack(pady=20)

    def update_medication_list(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for _, medication in self.my_medications.iterrows():
            banner = MedicationBanner(self.scrollable_frame,
                                      medication,
                                      self)
            banner.pack(fill=tk.X, padx=5, pady=5)

    def update_medication(self, product_name, updates):
        mask = self.my_medications['Product Name'] == product_name
        for field, value in updates.items():
            self.my_medications.loc[mask, field] = value
        self.my_medications.to_excel('my_medications.xlsx', index=False)
        self.update_medication_list()

        def delete_medication(self, product_name):
            self.my_medications = self.my_medications[
                self.my_medications['Product Name'] != product_name
                ]
            self.my_medications.to_excel('my_medications.xlsx', index=False)

    def delete_medication(self, product_name):
        """약물을 삭제하는 메소드"""
        try:
            # 해당 약물을 제외한 데이터만 남김
            self.my_medications = self.my_medications[
                self.my_medications['Product Name'] != product_name
                ]
            # 파일 저장 - 직접 파일명 사용
            self.my_medications.to_excel('my_medications.xlsx', index=False)
            # UI 업데이트
            self.update_medication_list()

            messagebox.showinfo("성공", f"{product_name}이(가) 삭제되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", f"약물 삭제 중 오류가 발생했습니다: {str(e)}")

    def check_notifications(self):
        current_time = datetime.now().strftime("%H:%M")
        for _, medication in self.my_medications.iterrows():
            # Only check medications with enabled notifications and set times
            if (medication.get('Notifications_Enabled', True) and
                    pd.notna(medication['Notification Time']) and
                    medication['Notification Time'] == current_time):
                # Create styled notification window
                notif_window = tk.Toplevel(self.root)
                notif_window.title("복용 알림")
                notif_window.geometry("400x300")
                notif_window.configure(bg=self.style.colors['background'])

                # Card container
                card_frame = ttk.Frame(notif_window, style='Card.TFrame', padding="20")
                card_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

                # Notification icon and title
                ttk.Label(card_frame,
                          text="⏰ 복용 시간 알림",
                          style='Title.TLabel').pack(pady=(0, 20))

                # Medication name
                ttk.Label(card_frame,
                          text=f"💊 {medication['Product Name']}",
                          style='Heading.TLabel').pack(pady=(0, 10))

                # Taking condition
                if 'Taking_Condition' in medication:
                    condition_text = {
                        '식전': '식사하기 30분 전에 복용하세요.',
                        '식후': '식사 직후에 복용하세요.',
                        '공복': '식사와 식사 사이 충분한 시간이 지난 후 복용하세요.'
                    }.get(medication['Taking_Condition'], '')

                    if condition_text:
                        ttk.Label(card_frame,
                                  text=condition_text,
                                  style='Body.TLabel',
                                  wraplength=300).pack(pady=(0, 10))

                # How to take it
                ttk.Label(card_frame,
                          text=f"📝 {medication['How to Take It']}",
                          style='Body.TLabel',
                          wraplength=300).pack(pady=(0, 20))

                # Close button
                ttk.Button(card_frame,
                           text="✔️ 확인",
                           style='Primary.TButton',
                           command=notif_window.destroy).pack()

        self.root.after(60000, self.check_notifications)

        def edit_user_info(self):
            dialog = UserInfoDialog(self.root)

            # Fill current info
            for field, value in self.user_info.items():
                if field == "notes":
                    dialog.entries[field].insert("1.0", str(value))
                elif field == "gender":
                    dialog.entries[field].set(value)
                else:
                    dialog.entries[field].insert(0, str(value))

            self.root.wait_window(dialog.window)

            if dialog.result:
                self.user_info = dialog.result
                with open('user_info.json', 'w', encoding='utf-8') as f:
                    json.dump(self.user_info, f, ensure_ascii=False, indent=2)

                # Refresh medinote screen
                self.main_frame.destroy()
                self.create_main_screen()


def main():
    root = tk.Tk()
    root.title("복용 약물 관리")

    # Set window icon (if available)
    try:
        root.iconbitmap('pill_icon.ico')
    except:
        pass  # Icon file not found

    # Set minimum window size
    root.minsize(800, 600)

    # Center window on screen
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    app = MedicationManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
