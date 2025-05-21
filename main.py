import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk, filedialog
import math
import pyperclip
import json
from string import Template

class ModernVHDLCodeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("VHDL Code Generator")
        self.root.state('zoomed')
        
        # Set root background color
        self.root.configure(bg='#FFF0DC')  # Light Beige background

        # Configure modern style
        self.configure_styles()

        # Create main container with matching background
        self.main_container = ttk.Frame(self.root, style='Main.TFrame')
        self.main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Create header
        self.create_header()

        # Create content area
        self.create_content_area()

        # Create parameter frame
        self.param_frame = ttk.LabelFrame(self.main_container, text="Component Parameters", padding=15)
        self.param_frame.pack(fill='x', pady=10)

        # Create buttons
        self.create_buttons()

        # Create code display
        self.create_code_display()

        # Initialize parameters
        self.params = {}
        self.update_params()

        # Bind right-click to context menu
        self.root.bind('<Button-3>', self.create_context_menu)

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("VHDL Code Generator Help")
        help_window.geometry("900x700")
        
        # Configure style for help window
        style = ttk.Style()
        help_frame = ttk.Frame(help_window, padding="20")
        help_frame.pack(fill='both', expand=True)
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(help_frame)
        notebook.pack(fill='both', expand=True, pady=(0, 10))

        # GUI Guide Tab (New First Tab)
        gui_guide = ttk.Frame(notebook, padding=10)
        notebook.add(gui_guide, text='واجهة البرنامج')
        
        gui_text = scrolledtext.ScrolledText(gui_guide, wrap=tk.WORD, font=('Segoe UI', 11))
        gui_text.pack(fill='both', expand=True)
        gui_text.insert('1.0', """
دليل واجهة المستخدم (GUI):

▼ القسم العلوي (شريط العنوان):
   ┌──────────────────────────────────────┐
   │  VHDL Code Generator    [Help]       │ ← زر المساعدة في أعلى اليمين
   └──────────────────────────────────────┘

▼ قسم التكوين (Configuration):
   ┌──────────────────────────────────────┐
   │ Component Configuration:             │
   │ ▶ Select Component: [قائمة منسدلة]   │ ← اختيار نوع المكون
   │ ▶ Code Type: [Function/Procedure]    │ ← اختيار نوع الكود
   └──────────────────────────────────────┘

▼ قسم الأسماء (Names):
   ┌──────────────────────────────────────┐
   │ Name Configuration:                  │
   │ ▶ Entity Name: [حقل إدخال]           │ ← اسم الكيان
   │ ▶ Architecture Name: [حقل إدخال]     │ ← اسم البنية
   │ ▶ Function Name: [حقل إدخال]         │ ← اسم الدالة
   └──────────────────────────────────────┘

▼ قسم المعلمات (Parameters):
   ┌──────────────────────────────────────┐
   │ Component Parameters:                │
   │ [تظهر الحقول حسب المكون المختار]     │ ← معلمات خاصة بكل مكون
   └──────────────────────────────────────┘

▼ أزرار التحكم (Control Buttons):
   ┌──────────────────────────────────────┐
   │ [Generate Code] [Clear] [Save] [Copy]│
   └──────────────────────────────────────┘
   • Generate Code: إنشاء الكود
   • Clear: مسح الكود
   • Save: حفظ في ملف
   • Copy: نسخ للحافظة

▼ منطقة عرض الكود (Code Display):
   ┌──────────────────────────────────────┐
   │                                      │
   │ [منطقة عرض الكود المُنشأ]            │ ← الكود VHDL المُنشأ
   │                                      │
   └──────────────────────────────────────┘

ملاحظات مهمة عن الواجهة:
• جميع الحقول مطلوبة ويجب ملؤها
• يتغير قسم المعلمات تلقائياً حسب المكون المختار
• يمكن تكبير نافذة البرنامج للحصول على عرض أفضل للكود
• شريط التمرير يظهر تلقائياً عند الحاجة
• يمكن تحديد الكود باستخدام الماوس أو Ctrl+A

تلميحات سريعة:
• حرك المؤشر فوق الحقول للحصول على تلميحات إضافية
• الألوان المختلفة تساعد في تمييز الأقسام المختلفة
• الأخطاء تظهر في رسائل منبثقة واضحة
• يمكن تعديل حجم أقسام الواجهة عن طريق السحب
""")

        # Make gui_text read-only
        gui_text.configure(state='disabled')
        
        # Add other existing tabs
        getting_started = ttk.Frame(notebook, padding=10)
        notebook.add(getting_started, text='البداية')
        
        start_text = scrolledtext.ScrolledText(getting_started, wrap=tk.WORD, font=('Segoe UI', 11))
        start_text.pack(fill='both', expand=True)
        start_text.insert('1.0', """
مرحباً بك في برنامج توليد شفرة VHDL!

الخطوات الأساسية لاستخدام البرنامج:

1. اختيار المكون (Component):
   • انقر على القائمة المنسدلة "Select Component"
   • اختر المكون الذي تريد إنشاء كود له
   • مثال: اختر "MUX" لإنشاء مضاعف (multiplexer)

2. إدخال الأسماء:
   • Entity Name: اسم الكيان (مثل: my_mux)
   • Architecture Name: اسم البنية (مثل: my_arch)
   • Function/Procedure Name: اسم الدالة (مثل: my_func)
   
   ملاحظة: يجب أن تبدأ الأسماء بحرف وتحتوي فقط على حروف وأرقام وشرطة سفلية (_)

3. إدخال المعلمات:
   • ستظهر حقول إدخال مختلفة حسب المكون المختار
   • أدخل القيم المطلوبة (سنشرح كل مكون بالتفصيل في علامة التبويب "المكونات")

4. توليد الكود:
   • انقر على زر "Generate Code"
   • سيظهر الكود في النافذة السفلية
   • يمكنك نسخ الكود أو حفظه في ملف

5. الأزرار الإضافية:
   • Clear Code: لمسح الكود المولد
   • Save to File: لحفظ الكود في ملف
   • Copy to Clipboard: لنسخ الكود إلى الحافظة
""")
        
        # Components Tab
        components = ttk.Frame(notebook, padding=10)
        notebook.add(components, text='Components')
        
        comp_text = scrolledtext.ScrolledText(components, wrap=tk.WORD, font=('Segoe UI', 11))
        comp_text.pack(fill='both', expand=True)
        comp_text.insert('1.0', """
شرح تفصيلي للمكونات:

1. المضاعف (MUX):
   • ما هو؟ دائرة تختار إشارة واحدة من عدة إشارات دخل
   • المعلمات المطلوبة:
     - Number of inputs: عدد المدخلات (يجب أن يكون 2، 4، 8، 16، ...)
     - Width of channels: عرض كل قناة بالبت
   • مثال عملي:
     - Number of inputs: 4
     - Width of channels: 8
     → سينشئ مضاعف 4×1 مع قنوات عرض 8 بت

2. موزع (DeMUX):
   • ما هو؟ دائرة توجه إشارة دخل واحدة إلى أحد المخارج المتعددة
   • المعلمات المطلوبة:
     - Number of outputs: عدد المخارج (يجب أن يكون 2، 4، 8، 16، ...)
     - Width of channels: عرض كل قناة بالبت
   • مثال عملي:
     - Number of outputs: 4
     - Width of channels: 8
     → سينشئ موزع 1×4 مع قنوات عرض 8 بت

3. المشفر (Decoder):
   • ما هو؟ يحول الشفرة الثنائية إلى إشارات منفصلة
   • المعلمات المطلوبة:
     - Width: عرض الدخل بالبت
   • مثال عملي:
     - Width: 3
     → سينشئ مشفر مع 3 مدخلات و 8 مخارج (2^3)

4. المرمز (Encoder):
   • ما هو؟ يحول الإشارات المنفصلة إلى شفرة ثنائية
   • المعلمات المطلوبة:
     - Width: عرض المخرج بالبت
   • مثال عملي:
     - Width: 3
     → سينشئ مرمز مع 8 مدخلات (2^3) و 3 مخارج

5. سجل الإزاحة (Shift Register):
   • ما هو؟ سجل يخزن البيانات ويمكنه إزاحتها
   • المعلمات المطلوبة:
     - Width: عدد البتات في السجل
     - Type: نوع السجل (SIPO/PISO)
   • مثال عملي:
     - Width: 8
     - Type: Serial-In Parallel-Out
     → سينشئ سجل إزاحة 8 بت

6. ذاكرة SRAM:
   • ما هي؟ ذاكرة قراءة/كتابة سريعة
   • المعلمات المطلوبة:
     - Address Width: عرض العنوان (يحدد حجم الذاكرة)
     - Data Width: عرض البيانات
   • مثال عملي:
     - Address Width: 4
     - Data Width: 8
     → سينشئ ذاكرة بحجم 16 موقع (2^4)، كل موقع 8 بت

7. مقسم التردد (Clock Divider):
   • ما هو؟ دائرة تقسم تردد الساعة
   • المعلمات المطلوبة:
     - Division Factor: معامل القسمة
   • مثال عملي:
     - Division Factor: 4
     → سيقسم تردد الساعة على 4
""")
        
        # Tips and Tricks Tab
        tips = ttk.Frame(notebook, padding=10)
        notebook.add(tips, text='Tips & Tricks')
        
        tips_text = scrolledtext.ScrolledText(tips, wrap=tk.WORD, font=('Segoe UI', 11))
        tips_text.pack(fill='both', expand=True)
        tips_text.insert('1.0', """
نصائح وحيل مفيدة:

1. اختيار الأسماء:
   • استخدم أسماء وصفية تدل على وظيفة المكون
   • تجنب الأسماء المحجوزة في VHDL مثل: signal, process, entity
   • أمثلة جيدة:
     - my_mux_4bit
     - data_decoder
     - freq_divider_10

2. تحديد الأحجام:
   • اختر أصغر حجم يلبي احتياجاتك
   • تذكر أن الأحجام الكبيرة تستهلك موارد أكثر
   • أمثلة:
     - لتخزين أرقام من 0 إلى 255، استخدم عرض 8 بت
     - لـ 4 مدخلات في المضاعف، تحتاج 2 بت للاختيار

3. حل المشاكل الشائعة:
   • إذا ظهرت رسالة خطأ عن الأسماء:
     - تأكد أن الاسم يبدأ بحرف
     - تأكد من عدم وجود مسافات
     - تأكد من عدم استخدام رموز خاصة
   
   • إذا لم يتم توليد الكود:
     - تأكد من إدخال جميع المعلمات المطلوبة
     - تأكد أن القيم ضمن النطاق المسموح
     - تأكد أن عدد المدخلات/المخارج من قوى الرقم 2

4. أفضل الممارسات:
   • احفظ الكود المولد في ملف فور إنشائه
   • اختبر الكود مع قيم صغيرة أولاً
   • استخدم التعليقات لتوثيق التغييرات

5. اختصارات مفيدة:
   • Ctrl+C: نسخ الكود المحدد
   • Ctrl+V: لصق النص
   • Ctrl+A: تحديد كل الكود
""")

        # Make all text widgets read-only
        start_text.configure(state='disabled')
        comp_text.configure(state='disabled')
        tips_text.configure(state='disabled')
        
        # Close button
        close_button = ttk.Button(help_frame, text="Close", command=help_window.destroy)
        close_button.pack(pady=10)

    def create_header(self):
        header_frame = ttk.Frame(self.main_container, style='Header.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = ttk.Label(header_frame,
                               text="VHDL Code Generator",
                               style='Header.TLabel')
        title_label.pack(side='left', padx=20)
        
        help_button = ttk.Button(header_frame,
                                text="Help",
                                command=self.show_help,
                                style='Help.TButton')
        help_button.pack(side='right', padx=20)

    def configure_styles(self):
        # Configure modern style theme
        style = ttk.Style()
        style.theme_use('clam')

        # Define color scheme - Beige and Brown theme
        primary_color = '#FFF0DC'      # Light Beige
        secondary_color = '#E8B88C'    # Warm Sand
        accent_color = '#5C3C24'       # Dark Brown
        text_color = '#000000'         # Black
        button_text_color = '#FFFFFF'  # White
        input_bg = '#FFF0DC'          # Light Beige
        header_color = '#5C3C24'       # Dark Brown for header
        container_bg = '#F5E6D3'       # Slightly darker beige for container background

        # Configure the main container style
        style.configure('Main.TFrame', 
                       background=container_bg)

        # Configure help button style
        style.configure('Help.TButton',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=button_text_color,
                       background='#5C3C24',  # Dark Brown
                       relief='flat',
                       borderwidth=0,
                       padding=(15, 8))
        style.map('Help.TButton',
                 background=[('active', '#3D2817')],  # Darker Brown when active
                 foreground=[('active', button_text_color)])

        # Configure frame styles
        style.configure('Content.TFrame', 
                       background=container_bg)
        style.configure('Header.TFrame', 
                       background=header_color)
        
        # Configure label frame style
        style.configure('TLabelframe', 
                       background=primary_color,
                       relief='solid',
                       borderwidth=1,
                       bordercolor=accent_color)
        style.configure('TLabelframe.Label', 
                       font=('Segoe UI', 11, 'bold'),
                       foreground=text_color,
                       background=primary_color)

        # Configure label styles
        style.configure('Header.TLabel', 
                       font=('Segoe UI', 28, 'bold'),
                       foreground='#FFF0DC',  # Light Beige
                       background=header_color)
        style.configure('TLabel',
                       font=('Segoe UI', 11),
                       foreground=text_color,
                       background=primary_color)

        # Configure button styles
        style.configure('TButton',
                       font=('Segoe UI', 11, 'bold'),
                       foreground=button_text_color,
                       background='#5C3C24',  # Dark Brown
                       relief='flat',
                       borderwidth=0,
                       padding=(20, 10))
        style.map('TButton',
                 background=[('active', '#3D2817')],  # Darker Brown when active
                 foreground=[('active', button_text_color)])

        # Configure entry and combobox styles
        style.configure('TEntry',
                       font=('Segoe UI', 11),
                       fieldbackground=secondary_color,
                       foreground=text_color,
                       borderwidth=1,
                       relief='solid')
        style.configure('TCombobox',
                       font=('Segoe UI', 11),
                       fieldbackground=secondary_color,
                       foreground=text_color,
                       borderwidth=1,
                       relief='solid',
                       arrowsize=15)
        style.map('TCombobox',
                 fieldbackground=[('readonly', secondary_color)],
                 selectbackground=[('readonly', accent_color)],
                 selectforeground=[('readonly', button_text_color)])

        # Configure scrolled text style
        style.configure('Code.TFrame',
                       background=secondary_color,
                       relief='solid',
                       borderwidth=1,
                       bordercolor=accent_color)

    def create_content_area(self):
        content_frame = ttk.Frame(self.main_container)
        content_frame.pack(fill='x', pady=10)

        # Left column - Make draggable
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side='left', fill='both', expand=True, padx=10)
        self.make_draggable(left_frame)

        # Component selection
        comp_frame = ttk.LabelFrame(left_frame, text="Component Configuration", padding=10)
        comp_frame.pack(fill='x')
        self.make_draggable(comp_frame)

        ttk.Label(comp_frame, text="Select Component:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.component_var = tk.StringVar(value="MUX")
        components = ["MUX", "DeMUX", "Decoder", "Encoder", "Shift Register", "SRAM", "Clock Divider"]
        self.component_menu = ttk.Combobox(comp_frame, textvariable=self.component_var, values=components, state='readonly', width=35)
        self.component_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.component_menu.bind('<<ComboboxSelected>>', self.update_params)

        ttk.Label(comp_frame, text="Code Type:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.code_type_var = tk.StringVar(value="Function")
        self.code_type_menu = ttk.Combobox(comp_frame, textvariable=self.code_type_var, values=["None", "Function", "Procedure"], state='readonly', width=35)
        self.code_type_menu.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Right column - Make draggable
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side='right', fill='both', expand=True, padx=10)
        self.make_draggable(right_frame)

        # Names configuration - Make draggable
        names_frame = ttk.LabelFrame(right_frame, text="Name Configuration", padding=10)
        names_frame.pack(fill='x')
        self.make_draggable(names_frame)

        vcmd = (self.root.register(self.validate_length), '%P')
        
        ttk.Label(names_frame, text="Entity Name:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entity_var = tk.StringVar(value="Entity_1")
        self.entity_entry = ttk.Entry(names_frame, textvariable=self.entity_var, validate='key', validatecommand=vcmd, width=35)
        self.entity_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(names_frame, text="Architecture Name:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.arch_var = tk.StringVar(value="Arch_1")
        self.arch_entry = ttk.Entry(names_frame, textvariable=self.arch_var, validate='key', validatecommand=vcmd, width=35)
        self.arch_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(names_frame, text="Function/Procedure Name:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.fun_var = tk.StringVar(value="Fun_1")
        self.func_proc_entry = ttk.Entry(names_frame, textvariable=self.fun_var, validate='key', validatecommand=vcmd, width=35)
        self.func_proc_entry.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    def make_draggable(self, widget):
        """Make a widget draggable by mouse"""
        widget.bind('<Button-1>', self.start_drag)
        widget.bind('<B1-Motion>', self.drag)
        widget.bind('<ButtonRelease-1>', self.stop_drag)
        widget._drag_data = {'x': 0, 'y': 0, 'dragging': False}

    def start_drag(self, event):
        """Begin drag of a widget"""
        widget = event.widget
        widget._drag_data = {
            'x': event.x,
            'y': event.y,
            'dragging': True,
            'start_x': widget.winfo_x(),
            'start_y': widget.winfo_y()
        }
        # Raise the widget to the top
        widget.lift()

    def drag(self, event):
        """Handle dragging of the widget"""
        widget = event.widget
        if widget._drag_data['dragging']:
            # Calculate the new position
            dx = event.x - widget._drag_data['x']
            dy = event.y - widget._drag_data['y']
            new_x = widget._drag_data['start_x'] + dx
            new_y = widget._drag_data['start_y'] + dy
            
            # Move the widget using place
            widget.place(x=new_x, y=new_y)

    def stop_drag(self, event):
        """End drag of a widget"""
        widget = event.widget
        widget._drag_data['dragging'] = False

    def create_buttons(self):
        button_frame = ttk.Frame(self.main_container)
        button_frame.pack(fill='x', pady=10)

        # Center align buttons
        buttons_center = ttk.Frame(button_frame)
        buttons_center.pack(anchor='center')

        ttk.Button(buttons_center, text="Generate Code", command=self.generate_code, style='TButton').pack(side='left', padx=5)
        ttk.Button(buttons_center, text="Clear Code", command=self.clear_code, style='TButton').pack(side='left', padx=5)
        ttk.Button(buttons_center, text="Save to File", command=self.save_code, style='TButton').pack(side='left', padx=5)
        ttk.Button(buttons_center, text="Copy to Clipboard", command=self.copy_code, style='TButton').pack(side='left', padx=5)

    def create_code_display(self):
        # Create a frame for the code display with a title
        code_frame = ttk.LabelFrame(self.main_container, text="Generated VHDL Code", padding=15)
        code_frame.pack(fill='both', expand=True, pady=10)

        # Create a container frame for the code text area
        code_container = ttk.Frame(code_frame, style='Code.TFrame')
        code_container.pack(fill='both', expand=True, padx=5, pady=5)

        # Create line numbers text widget
        self.line_numbers = tk.Text(
            code_container,
            width=8,
            padx=5,
            pady=5,
            takefocus=0,
            border=0,
            background='#E8E8E8',
            foreground='#2F4F4F',
            font=('Consolas', 16),
            state='disabled'
        )
        self.line_numbers.pack(side='left', fill='y')

        # Create the main code text widget
        self.code_text = scrolledtext.ScrolledText(
            code_container,
            wrap=tk.NONE,
            width=180,
            height=60,
            font=('Consolas', 16),
            bg='white',
            fg='#2F4F4F',
            insertbackground='#008080',
            selectbackground='#20B2AA',
            selectforeground='white',
            relief='flat',
            padx=20,
            pady=15
        )
        self.code_text.pack(fill='both', expand=True)

        # Add horizontal scrollbar
        h_scroll = ttk.Scrollbar(code_container, orient='horizontal', command=self.code_text.xview)
        h_scroll.pack(side='bottom', fill='x')
        self.code_text.configure(xscrollcommand=h_scroll.set)

        # Bind events for line numbers
        self.code_text.bind('<KeyRelease>', self.update_line_numbers)
        self.code_text.bind('<MouseWheel>', self.update_line_numbers)
        self.code_text.bind('<ButtonRelease-1>', self.update_line_numbers)

    def update_line_numbers(self, event=None):
        """Update the line numbers in the text widget."""
        # Enable editing of line numbers
        self.line_numbers.configure(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        
        # Get the total number of lines
        total_lines = str(self.code_text.get('1.0', tk.END)).count('\n')
        
        # Generate line numbers
        line_numbers = '\n'.join(str(i).rjust(3) for i in range(1, total_lines + 1))
        self.line_numbers.insert('1.0', line_numbers)
        
        # Disable editing of line numbers
        self.line_numbers.configure(state='disabled')
        
        # Sync scrolling
        self.line_numbers.yview_moveto(self.code_text.yview()[0])

    def validate_length(self, new_value):
        """Validate that the input length does not exceed 15 characters and follows VHDL naming rules."""
        if not new_value:  # Allow empty string for initial state
            return True
            
        # Check for invalid characters
        valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
        if not all(c in valid_chars for c in new_value):
            return False
            
        # Check length
        return len(new_value) <= 15

    def validate_vhdl_name(self, name, field_name):
        """Validate VHDL naming conventions."""
        if not name:
            messagebox.showerror("Error", f"{field_name} name cannot be empty")
            return False

        # VHDL reserved words
        reserved_words = {
            'abs', 'access', 'after', 'alias', 'all', 'and', 'architecture', 'array', 'assert', 'attribute',
            'begin', 'block', 'body', 'buffer', 'bus', 'case', 'component', 'configuration', 'constant',
            'disconnect', 'downto', 'else', 'elsif', 'end', 'entity', 'exit', 'file', 'for', 'function',
            'generate', 'generic', 'group', 'guarded', 'if', 'impure', 'in', 'inertial', 'inout', 'is',
            'label', 'library', 'linkage', 'literal', 'loop', 'map', 'mod', 'nand', 'new', 'next', 'nor',
            'not', 'null', 'of', 'on', 'open', 'or', 'others', 'out', 'package', 'port', 'postponed',
            'procedure', 'process', 'pure', 'range', 'record', 'register', 'reject', 'rem', 'report',
            'return', 'rol', 'ror', 'select', 'severity', 'signal', 'shared', 'sla', 'sll', 'sra', 'srl',
            'subtype', 'then', 'to', 'transport', 'type', 'unaffected', 'units', 'until', 'use', 'variable',
            'wait', 'when', 'while', 'with', 'xnor', 'xor'
        }

        # Check if name is a reserved word
        if name.lower() in reserved_words:
            messagebox.showerror("Error", f"{field_name} name '{name}' is a VHDL reserved word")
            return False

        # Check for spaces
        if ' ' in name:
            messagebox.showerror("Error", f"{field_name} name cannot contain spaces")
            return False

        # Must start with a letter
        if not name[0].isalpha():
            messagebox.showerror("Error", f"{field_name} name must start with a letter")
            return False

        # Can only contain letters, numbers, and underscores
        if not all(c.isalnum() or c == '_' for c in name):
            messagebox.showerror("Error", f"{field_name} name can only contain letters, numbers, and underscores")
            return False

        # Cannot end with an underscore
        if name.endswith('_'):
            messagebox.showerror("Error", f"{field_name} name cannot end with an underscore")
            return False

        # Cannot have consecutive underscores
        if '__' in name:
            messagebox.showerror("Error", f"{field_name} name cannot contain consecutive underscores")
            return False

        return True

    def update_params(self, *args):
        # Clear previous parameters
        for widget in self.param_frame.winfo_children():
            widget.destroy()
        self.params.clear()

        component = self.component_var.get()
        if component == "MUX":
            self.params["Number of inputs"] = tk.StringVar()
            tk.Label(self.param_frame, text="Number of inputs:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Number of inputs"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')
            self.params["Width of channels"] = tk.StringVar()
            tk.Label(self.param_frame, text="Width of channels:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=2, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Width of channels"], width=15).grid(row=0, column=3, padx=10, pady=5, sticky='w')
        elif component == "DeMUX":
            self.params["Number of outputs"] = tk.StringVar()
            tk.Label(self.param_frame, text="Number of outputs:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Number of outputs"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')
            self.params["Width of channels"] = tk.StringVar()
            tk.Label(self.param_frame, text="Width of channels:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=2, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Width of channels"], width=15).grid(row=0, column=3, padx=10, pady=5, sticky='w')
        elif component == "Decoder":
            self.params["Width"] = tk.StringVar()
            tk.Label(self.param_frame, text="Width of input:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Width"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')
        elif component == "Encoder":
            self.params["Width"] = tk.StringVar()
            tk.Label(self.param_frame, text="Width of output:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Width"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')
        elif component == "Shift Register":
            self.params["Width"] = tk.StringVar()
            tk.Label(self.param_frame, text="Width of register:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Width"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')
            self.params["Type"] = tk.StringVar(value="Serial-In Parallel-Out")
            tk.Label(self.param_frame, text="Type:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=2, padx=10, pady=5, sticky='e')
            ttk.Combobox(self.param_frame, textvariable=self.params["Type"], values=["Serial-In Parallel-Out", "Parallel-In Serial-Out"], state='readonly', width=20).grid(row=0, column=3, padx=10, pady=5, sticky='w')
        elif component == "SRAM":
            self.params["addr_width"] = tk.StringVar()
            tk.Label(self.param_frame, text="Address Width:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["addr_width"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')
            self.params["data_width"] = tk.StringVar()
            tk.Label(self.param_frame, text="Data Width:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=2, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["data_width"], width=15).grid(row=0, column=3, padx=10, pady=5, sticky='w')
        elif component == "Clock Divider":
            self.params["Division Factor"] = tk.StringVar()
            tk.Label(self.param_frame, text="Division Factor:", bg='#E8B88C', fg='#5C3C24', font=('Segoe UI', 11)).grid(row=0, column=0, padx=10, pady=5, sticky='e')
            ttk.Entry(self.param_frame, textvariable=self.params["Division Factor"], width=15).grid(row=0, column=1, padx=10, pady=5, sticky='w')

    def clear_code(self):
        """Clear the generated VHDL code display."""
        self.code_text.delete(1.0, tk.END)

    def save_code(self):
        """Save the generated VHDL code to a .vhdl file."""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "No code to save. Please generate code first.")
            return

        entity_name = self.entity_entry.get().strip() or "vhdl_code"
        file_path = filedialog.asksaveasfilename(
            defaultextension=".vhdl",
            filetypes=[("VHDL files", "*.vhdl"), ("All files", "*.*")],
            initialfile=f"{entity_name}.vhdl"
        )
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(code)
                messagebox.showinfo("Success", f"Code saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def copy_code(self):
        """Copy the generated VHDL code to the clipboard."""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code:
            messagebox.showwarning("Warning", "No code to copy. Please generate code first.")
            return
        try:
            pyperclip.copy(code)
            messagebox.showinfo("Success", "Code copied to clipboard")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy code: {str(e)}")

    def is_power_of_two(self, n):
        return n > 0 and (n & (n - 1)) == 0

    def validate_inputs(self):
        component = self.component_var.get()
        
        # Validate entity name
        entity_name = self.entity_entry.get()
        if not self.validate_vhdl_name(entity_name, "Entity"):
            return False

        # Validate architecture name
        arch_name = self.arch_entry.get()
        if not self.validate_vhdl_name(arch_name, "Architecture"):
            return False

        # Validate function/procedure name
        func_proc_name = self.func_proc_entry.get()
        if not self.validate_vhdl_name(func_proc_name, "Function/Procedure"):
            return False

        # Check for duplicate names
        names = [entity_name.lower(), arch_name.lower(), func_proc_name.lower()]
        if len(set(names)) != len(names):
            messagebox.showerror("Error", "Entity, Architecture, and Function/Procedure names must be unique")
            return False

        try:
            if component == "MUX":
                required = ["Number of inputs", "Width of channels"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                inputs = int(self.params["Number of inputs"].get())
                width = int(self.params["Width of channels"].get())
                if inputs <= 0 or width <= 0:
                    raise ValueError("Inputs and width must be positive")
                if not self.is_power_of_two(inputs):
                    messagebox.showerror("Error", "Number of inputs must be a power of 2")
                    return False
            elif component == "DeMUX":
                required = ["Number of outputs", "Width of channels"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                outputs = int(self.params["Number of outputs"].get())
                width = int(self.params["Width of channels"].get())
                if outputs <= 0 or width <= 0:
                    raise ValueError("Outputs and width must be positive")
                if not self.is_power_of_two(outputs):
                    messagebox.showerror("Error", "Number of outputs must be a power of 2")
                    return False
            elif component == "Decoder":
                required = ["Width"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                width = int(self.params["Width"].get())
                if width <= 0:
                    raise ValueError("Width must be positive")
                if width > 8:
                    messagebox.showerror("Error", "Width cannot exceed 8 (would generate too many outputs)")
                    return False
            elif component == "Encoder":
                required = ["Width"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                width = int(self.params["Width"].get())
                if width <= 0:
                    raise ValueError("Width must be positive")
                if width > 8:
                    messagebox.showerror("Error", "Width cannot exceed 8 (would require too many inputs)")
                    return False
            elif component == "Shift Register":
                required = ["Width"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                width = int(self.params["Width"].get())
                if width <= 0:
                    raise ValueError("Width must be positive")
                if width > 128:
                    messagebox.showerror("Error", "Width cannot exceed 128 bits")
                    return False
                if not self.params["Type"].get():
                    messagebox.showerror("Error", "Shift Register type must be selected")
                    return False
            elif component == "SRAM":
                required = ["addr_width", "data_width"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                addr_width = int(self.params["addr_width"].get())
                data_width = int(self.params["data_width"].get())
                
                # Basic validation
                if addr_width <= 0 or data_width <= 0:
                    raise ValueError("Address and data width must be positive")
                
                # Show warnings for large values but allow them
                if addr_width > 16:  # 65,536 addresses
                    result = messagebox.askquestion("Warning", 
                        f"Large address width ({addr_width} bits) will generate {2**addr_width:,} memory locations.\n" +
                        "This might require significant hardware resources.\n" +
                        "Do you want to continue?")
                    if result != 'yes':
                        return False
                
                if data_width > 128:  # 128-bit data
                    result = messagebox.askquestion("Warning",
                        f"Large data width ({data_width} bits) might require significant hardware resources.\n" +
                        "Do you want to continue?")
                    if result != 'yes':
                        return False
                        
            elif component == "Clock Divider":
                required = ["Division Factor"]
                for req in required:
                    if not self.params[req].get():
                        messagebox.showerror("Error", f"Missing {req}")
                        return False
                div_factor = int(self.params["Division Factor"].get())
                if div_factor <= 0:
                    raise ValueError("Division Factor must be positive")
                if div_factor > 1048576:  # 2^20
                    messagebox.showerror("Error", "Division Factor cannot exceed 1048576")
                    return False
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return False
        return True

    def generate_code(self):
        try:
            if not self.validate_inputs():
                return

            component = self.component_var.get()
            code_type = self.code_type_var.get()
            entity_name = self.entity_entry.get()
            arch_name = self.arch_entry.get()
            func_proc_name = self.func_proc_entry.get()

            params = {}
            if component == "MUX":
                params = {
                    "inputs": int(self.params["Number of inputs"].get()),
                    "width": int(self.params["Width of channels"].get())
                }
            elif component == "DeMUX":
                params = {
                    "outputs": int(self.params["Number of outputs"].get()),
                    "width": int(self.params["Width of channels"].get())
                }
            elif component == "Decoder":
                params = {"width": int(self.params["Width"].get())}
            elif component == "Encoder":
                params = {"width": int(self.params["Width"].get())}
            elif component == "Shift Register":
                params = {
                    "width": int(self.params["Width"].get()),
                    "type": self.params["Type"].get()
                }
            elif component == "SRAM":
                params = {
                    "addr_width": int(self.params["addr_width"].get()),
                    "data_width": int(self.params["data_width"].get())
                }
            elif component == "Clock Divider":
                params = {"div_factor": int(self.params["Division Factor"].get())}

            if code_type == "None":
                vhdl_code = self.get_basic_vhdl_code(component, entity_name, arch_name, params)
            else:
                vhdl_code = self.get_vhdl_code(component, code_type, entity_name, arch_name, func_proc_name, params)

            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(tk.END, vhdl_code)
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

    def get_basic_vhdl_code(self, component, entity_name, arch_name, params):
        """Generate basic VHDL code without function/procedure"""
        from string import Template
        
        if component == "MUX":
            inputs = params["inputs"]
            width = params["width"]
            
            template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
$mux_inputs
        sel : in std_logic_vector($sel_width downto 0);
        Bitout : out std_logic_vector($data_width downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
begin
    process(sel, $input_list)
    begin
        case to_integer(unsigned(sel)) is
$case_statements
            when others => Bitout <= (others => '0');
        end case;
    end process;
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                mux_inputs=self.generate_mux_inputs(inputs, width),
                sel_width=int(math.log2(inputs))-1,
                data_width=width-1,
                input_list=', '.join([f'inp{i}' for i in range(inputs)]),
                case_statements=self.generate_mux_case_statements(inputs)
            )
            
        elif component == "DeMUX":
            outputs = params["outputs"]
            width = params["width"]
            
            template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        input : in std_logic_vector($data_width downto 0);
        sel : in std_logic_vector($sel_width downto 0);
$demux_outputs
    );
end $entity_name;

architecture $arch_name of $entity_name is
begin
    process(input, sel)
    begin
        $output_init;
        case to_integer(unsigned(sel)) is
$case_statements
            when others => null;
        end case;
    end process;
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                data_width=width-1,
                sel_width=int(math.log2(outputs))-1,
                demux_outputs=self.generate_demux_outputs(outputs, width),
                output_init='; '.join([f"out{i} <= (others => '0')" for i in range(outputs)]),
                case_statements=self.generate_demux_case_statements(outputs)
            )
            
        elif component == "Decoder":
            width = params["width"]
            num_outputs = 2**width
            
            template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        input : in std_logic_vector($width_minus_1 downto 0);
$outputs
    );
end $entity_name;

architecture $arch_name of $entity_name is
begin
    process(input)
    begin
        $output_init;
        case to_integer(unsigned(input)) is
$case_statements
            when others => null;
        end case;
    end process;
end $arch_name;""")
            
            outputs = '\n'.join([f"        out{i} : out std_logic;" for i in range(num_outputs)])
            output_init = '; '.join([f"out{i} <= '0'" for i in range(num_outputs)])
            case_statements = '\n'.join([f"            when {i} => out{i} <= '1';" for i in range(num_outputs)])
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                width_minus_1=width-1,
                outputs=outputs,
                output_init=output_init,
                case_statements=case_statements
            )
            
        elif component == "Encoder":
            width = params["width"]
            num_inputs = 2**width
            
            template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
$inputs
        output : out std_logic_vector($width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
begin
    process($input_list)
    begin
        output <= (others => '0');
$case_statements
    end process;
end $arch_name;""")
            
            inputs = '\n'.join([f"        in{i} : in std_logic;" for i in range(num_inputs)])
            input_list = ', '.join([f"in{i}" for i in range(num_inputs)])
            case_statements = '\n'.join([
                f"        if in{i} = '1' then\n            output <= std_logic_vector(to_unsigned({i}, {width}));\n        end if;"
                for i in range(num_inputs)
            ])
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                width_minus_1=width-1,
                inputs=inputs,
                input_list=input_list,
                case_statements=case_statements
            )
            
        elif component == "Shift Register":
            width = params["width"]
            shift_type = params["type"]
            
            if shift_type == "Serial-In Parallel-Out":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity $entity_name is
    port (
        clk, reset : in std_logic;
        serial_in : in std_logic;
        parallel_out : out std_logic_vector($width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal shift_reg : std_logic_vector($width_minus_1 downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            shift_reg <= (others => '0');
        elsif rising_edge(clk) then
            shift_reg <= shift_reg($width_minus_2 downto 0) & serial_in;
        end if;
    end process;
    
    parallel_out <= shift_reg;
end $arch_name;""")
            else:  # Parallel-In Serial-Out
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity $entity_name is
    port (
        clk, reset, load : in std_logic;
        parallel_in : in std_logic_vector($width_minus_1 downto 0);
        serial_out : out std_logic
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal shift_reg : std_logic_vector($width_minus_1 downto 0);
begin
    process(clk, reset)
    begin
        if reset = '1' then
            shift_reg <= (others => '0');
        elsif rising_edge(clk) then
            if load = '1' then
                shift_reg <= parallel_in;
            else
                shift_reg <= shift_reg($width_minus_2 downto 0) & '0';
            end if;
        end if;
    end process;
    
    serial_out <= shift_reg($width_minus_1);
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                width_minus_1=width-1,
                width_minus_2=width-2
            )
            
        elif component == "SRAM":
            addr_width = params["addr_width"]
            data_width = params["data_width"]
            
            template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        clk : in std_logic;
        we : in std_logic;  -- Write enable
        addr : in std_logic_vector($addr_width_minus_1 downto 0);
        data_in : in std_logic_vector($data_width_minus_1 downto 0);
        data_out : out std_logic_vector($data_width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    type ram_type is array (0 to $max_addr) of std_logic_vector($data_width_minus_1 downto 0);
    signal ram : ram_type := (others => (others => '0'));
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                ram(to_integer(unsigned(addr))) <= data_in;
            end if;
        end if;
    end process;
    
    data_out <= ram(to_integer(unsigned(addr)));
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                addr_width_minus_1=addr_width-1,
                data_width_minus_1=data_width-1,
                max_addr=2**addr_width-1
            )
            
        elif component == "Clock Divider":
            div_factor = params["div_factor"]
            
            template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        clk_in : in std_logic;
        reset : in std_logic;
        clk_out : out std_logic
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal counter : integer range 0 to $div_minus_1;
    signal temp_clk : std_logic;
begin
    process(clk_in, reset)
    begin
        if reset = '1' then
            counter <= 0;
            temp_clk <= '0';
        elsif rising_edge(clk_in) then
            if counter = $div_minus_1 then
                temp_clk <= not temp_clk;
                counter <= 0;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;
    
    clk_out <= temp_clk;
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                div_minus_1=div_factor-1
            )
            
        else:
            return "-- Component type not supported"

    def get_vhdl_code(self, component, code_type, entity_name, arch_name, func_proc_name, params):
        """Generate VHDL code with function/procedure"""
        from string import Template
        
        if component == "MUX":
            inputs = params["inputs"]
            width = params["width"]
            sel_width = int(math.log2(inputs))-1
            
            if code_type == "Function":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
$mux_inputs
        sel : in std_logic_vector($sel_width downto 0);
        Bitout : out std_logic_vector($data_width downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    function $func_name(
$func_inputs
        sel : std_logic_vector($sel_width downto 0))
        return std_logic_vector is
        variable result : std_logic_vector($data_width downto 0);
    begin
        case to_integer(unsigned(sel)) is
$case_statements
            when others => result := (others => '0');
        end case;
        return result;
    end function;
begin
    Bitout <= $func_name($input_list, sel);
end $arch_name;""")
            else:  # Procedure
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
$mux_inputs
        sel : in std_logic_vector($sel_width downto 0);
        Bitout : out std_logic_vector($data_width downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    procedure $proc_name(
$proc_inputs
        sel : in std_logic_vector($sel_width downto 0);
        signal output : out std_logic_vector($data_width downto 0)) is
    begin
        case to_integer(unsigned(sel)) is
$case_statements
            when others => output <= (others => '0');
        end case;
    end procedure;
begin
    process($input_list, sel)
    begin
        $proc_name($input_list, sel, Bitout);
    end process;
end $arch_name;""")

            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                func_name=func_proc_name,
                proc_name=func_proc_name,
                mux_inputs=self.generate_mux_inputs(inputs, width),
                sel_width=sel_width,
                data_width=width-1,
                func_inputs=self.generate_mux_func_inputs(inputs, width),
                proc_inputs=self.generate_mux_proc_inputs(inputs, width),
                input_list=', '.join([f'inp{i}' for i in range(inputs)]),
                case_statements=self.generate_mux_case_statements(inputs, code_type)
            )
            
        elif component == "DeMUX":
            outputs = params["outputs"]
            width = params["width"]
            sel_width = int(math.log2(outputs))-1
            
            if code_type == "Function":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        input : in std_logic_vector($data_width downto 0);
        sel : in std_logic_vector($sel_width downto 0);
$demux_outputs
    );
end $entity_name;

architecture $arch_name of $entity_name is
    type output_array is array (0 to $max_outputs) of std_logic_vector($data_width downto 0);
    
    function $func_name(
        input : std_logic_vector($data_width downto 0);
        sel : std_logic_vector($sel_width downto 0))
        return output_array is
        variable result : output_array;
    begin
        result := (others => (others => '0'));
        case to_integer(unsigned(sel)) is
$case_statements
            when others => null;
        end case;
        return result;
    end function;

    signal output_signals : output_array;
begin
    output_signals <= $func_name(input, sel);
$output_assignments
end $arch_name;""")
            else:  # Procedure
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        input : in std_logic_vector($data_width downto 0);
        sel : in std_logic_vector($sel_width downto 0);
$demux_outputs
    );
end $entity_name;

architecture $arch_name of $entity_name is
    procedure $proc_name(
        input : in std_logic_vector($data_width downto 0);
        sel : in std_logic_vector($sel_width downto 0);
$proc_outputs) is
    begin
$output_init
        case to_integer(unsigned(sel)) is
$case_statements
            when others => null;
        end case;
    end procedure;
begin
    process(input, sel)
    begin
        $proc_name(input, sel, $output_list);
    end process;
end $arch_name;""")

            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                func_name=func_proc_name,
                proc_name=func_proc_name,
                data_width=width-1,
                sel_width=sel_width,
                max_outputs=outputs-1,
                demux_outputs=self.generate_demux_outputs(outputs, width),
                proc_outputs=self.generate_demux_proc_outputs(outputs, width),
                output_init='; '.join([f"out{i} <= (others => '0')" for i in range(outputs)]),
                case_statements=self.generate_demux_case_statements(outputs, code_type),
                output_assignments='\n'.join([f"    out{i} <= output_signals({i});" for i in range(outputs)]),
                output_list=', '.join([f'out{i}' for i in range(outputs)])
            )
            
        elif component == "Decoder":
            width = params["width"]
            num_outputs = 2**width
            
            if code_type == "Function":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        input : in std_logic_vector($width_minus_1 downto 0);
$outputs
    );
end $entity_name;

architecture $arch_name of $entity_name is
    type output_array is array (0 to $max_outputs) of std_logic;
    
    function $func_name(input : std_logic_vector($width_minus_1 downto 0))
        return output_array is
        variable result : output_array := (others => '0');
    begin
        result(to_integer(unsigned(input))) := '1';
        return result;
    end function;

    signal output_signals : output_array;
begin
    output_signals <= $func_name(input);
$output_assignments
end $arch_name;""")
            else:  # Procedure
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        input : in std_logic_vector($width_minus_1 downto 0);
$outputs
    );
end $entity_name;

architecture $arch_name of $entity_name is
    procedure $proc_name(
        input : in std_logic_vector($width_minus_1 downto 0);
$proc_outputs) is
    begin
$output_init
        case to_integer(unsigned(input)) is
$case_statements
            when others => null;
        end case;
    end procedure;
begin
    process(input)
    begin
        $proc_name(input, $output_list);
    end process;
end $arch_name;""")

            outputs = '\n'.join([f"        out{i} : out std_logic;" for i in range(num_outputs)])
            output_assignments = '\n'.join([f"    out{i} <= output_signals({i});" for i in range(num_outputs)])
            proc_outputs = '\n'.join([f"        signal out{i} : out std_logic;" for i in range(num_outputs)])
            output_init = '; '.join([f"out{i} <= '0'" for i in range(num_outputs)])
            case_statements = '\n'.join([f"            when {i} => out{i} <= '1';" for i in range(num_outputs)])
            output_list = ', '.join([f'out{i}' for i in range(num_outputs)])
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                func_name=func_proc_name,
                proc_name=func_proc_name,
                width_minus_1=width-1,
                max_outputs=num_outputs-1,
                outputs=outputs,
                output_assignments=output_assignments,
                proc_outputs=proc_outputs,
                output_init=output_init,
                case_statements=case_statements,
                output_list=output_list
            )
            
        elif component == "Encoder":
            width = params["width"]
            num_inputs = 2**width
            
            if code_type == "Function":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
$inputs
        output : out std_logic_vector($width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    function $func_name($func_inputs)
        return std_logic_vector is
        variable result : std_logic_vector($width_minus_1 downto 0);
    begin
        result := (others => '0');
$case_statements
        return result;
    end function;
begin
    output <= $func_name($input_list);
end $arch_name;""")
            else:  # Procedure
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
$inputs
        output : out std_logic_vector($width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    procedure $proc_name(
$proc_inputs
        signal output : out std_logic_vector($width_minus_1 downto 0)) is
    begin
        output <= (others => '0');
$case_statements
    end procedure;
begin
    process($input_list)
    begin
        $proc_name($input_list, output);
    end process;
end $arch_name;""")

            inputs = '\n'.join([f"        in{i} : in std_logic;" for i in range(num_inputs)])
            func_inputs = '\n'.join([f"        in{i} : std_logic;" for i in range(num_inputs)])
            proc_inputs = '\n'.join([f"        signal in{i} : in std_logic;" for i in range(num_inputs)])
            input_list = ', '.join([f"in{i}" for i in range(num_inputs)])
            case_statements = '\n'.join([
                f"        if in{i} = '1' then\n            {'result' if code_type == 'Function' else 'output'} := std_logic_vector(to_unsigned({i}, {width}));\n        end if;"
                for i in range(num_inputs)
            ])
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                func_name=func_proc_name,
                proc_name=func_proc_name,
                width_minus_1=width-1,
                inputs=inputs,
                func_inputs=func_inputs,
                proc_inputs=proc_inputs,
                input_list=input_list,
                case_statements=case_statements
            )
            
        elif component == "Shift Register":
            width = params["width"]
            shift_type = params["type"]
            
            if shift_type == "Serial-In Parallel-Out":
                if code_type == "Function":
                    template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity $entity_name is
    port (
        clk, reset : in std_logic;
        serial_in : in std_logic;
        parallel_out : out std_logic_vector($width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal shift_reg : std_logic_vector($width_minus_1 downto 0);
    
    function $func_name(
        current_reg : std_logic_vector($width_minus_1 downto 0);
        serial_in : std_logic)
        return std_logic_vector is
    begin
        return current_reg($width_minus_2 downto 0) & serial_in;
    end function;
begin
    process(clk, reset)
    begin
        if reset = '1' then
            shift_reg <= (others => '0');
        elsif rising_edge(clk) then
            shift_reg <= $func_name(shift_reg, serial_in);
        end if;
    end process;
    
    parallel_out <= shift_reg;
end $arch_name;""")
                else:  # Procedure
                    template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity $entity_name is
    port (
        clk, reset : in std_logic;
        serial_in : in std_logic;
        parallel_out : out std_logic_vector($width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal shift_reg : std_logic_vector($width_minus_1 downto 0);
    
    procedure $proc_name(
        signal current_reg : in std_logic_vector($width_minus_1 downto 0);
        signal serial_in : in std_logic;
        signal next_reg : out std_logic_vector($width_minus_1 downto 0)) is
    begin
        next_reg <= current_reg($width_minus_2 downto 0) & serial_in;
    end procedure;
begin
    process(clk, reset)
    begin
        if reset = '1' then
            shift_reg <= (others => '0');
        elsif rising_edge(clk) then
            $proc_name(shift_reg, serial_in, shift_reg);
        end if;
    end process;
    
    parallel_out <= shift_reg;
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                width_minus_1=width-1,
                width_minus_2=width-2
            )
            
        elif component == "SRAM":
            addr_width = params["addr_width"]
            data_width = params["data_width"]
            
            if code_type == "Function":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        clk : in std_logic;
        we : in std_logic;
        addr : in std_logic_vector($addr_width_minus_1 downto 0);
        data_in : in std_logic_vector($data_width_minus_1 downto 0);
        data_out : out std_logic_vector($data_width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    type ram_type is array (0 to $max_addr) of std_logic_vector($data_width_minus_1 downto 0);
    signal ram : ram_type := (others => (others => '0'));
    
    function $func_name(
        memory : ram_type;
        addr : std_logic_vector($addr_width_minus_1 downto 0))
        return std_logic_vector is
    begin
        return memory(to_integer(unsigned(addr)));
    end function;
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                ram(to_integer(unsigned(addr))) <= data_in;
            end if;
        end if;
    end process;
    
    data_out <= $func_name(ram, addr);
end $arch_name;""")
            else:  # Procedure
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        clk : in std_logic;
        we : in std_logic;
        addr : in std_logic_vector($addr_width_minus_1 downto 0);
        data_in : in std_logic_vector($data_width_minus_1 downto 0);
        data_out : out std_logic_vector($data_width_minus_1 downto 0)
    );
end $entity_name;

architecture $arch_name of $entity_name is
    type ram_type is array (0 to $max_addr) of std_logic_vector($data_width_minus_1 downto 0);
    signal ram : ram_type := (others => (others => '0'));
    
    procedure $proc_name(
        signal memory : in ram_type;
        signal addr : in std_logic_vector($addr_width_minus_1 downto 0);
        signal data : out std_logic_vector($data_width_minus_1 downto 0)) is
    begin
        data <= memory(to_integer(unsigned(addr)));
    end procedure;
begin
    process(clk)
    begin
        if rising_edge(clk) then
            if we = '1' then
                ram(to_integer(unsigned(addr))) <= data_in;
            end if;
        end if;
    end process;
    
    process(ram, addr)
    begin
        $proc_name(ram, addr, data_out);
    end process;
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                func_name=func_proc_name,
                proc_name=func_proc_name,
                addr_width_minus_1=addr_width-1,
                data_width_minus_1=data_width-1,
                max_addr=2**addr_width-1
            )
            
        elif component == "Clock Divider":
            div_factor = params["div_factor"]
            
            if code_type == "Function":
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        clk_in : in std_logic;
        reset : in std_logic;
        clk_out : out std_logic
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal counter : integer range 0 to $div_minus_1;
    signal temp_clk : std_logic;
    
    function $func_name(
        current_count : integer;
        current_clk : std_logic)
        return std_logic is
    begin
        if current_count = $div_minus_1 then
            return not current_clk;
        else
            return current_clk;
        end if;
    end function;
begin
    process(clk_in, reset)
    begin
        if reset = '1' then
            counter <= 0;
            temp_clk <= '0';
        elsif rising_edge(clk_in) then
            if counter = $div_minus_1 then
                temp_clk <= $func_name(counter, temp_clk);
                counter <= 0;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;
    
    clk_out <= temp_clk;
end $arch_name;""")
            else:  # Procedure
                template = Template("""library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity $entity_name is
    port (
        clk_in : in std_logic;
        reset : in std_logic;
        clk_out : out std_logic
    );
end $entity_name;

architecture $arch_name of $entity_name is
    signal counter : integer range 0 to $div_minus_1;
    signal temp_clk : std_logic;
    
    procedure $proc_name(
        signal current_count : in integer;
        signal current_clk : in std_logic;
        signal next_clk : out std_logic) is
    begin
        if current_count = $div_minus_1 then
            next_clk <= not current_clk;
        else
            next_clk <= current_clk;
        end if;
    end procedure;
begin
    process(clk_in, reset)
    begin
        if reset = '1' then
            counter <= 0;
            temp_clk <= '0';
        elsif rising_edge(clk_in) then
            if counter = $div_minus_1 then
                $proc_name(counter, temp_clk, temp_clk);
                counter <= 0;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;
    
    clk_out <= temp_clk;
end $arch_name;""")
            
            return template.substitute(
                entity_name=entity_name,
                arch_name=arch_name,
                func_name=func_proc_name,
                proc_name=func_proc_name,
                div_minus_1=div_factor-1
            )
            
        else:
            return "-- Component type not supported"

    def generate_mux_inputs(self, inputs, width):
        return '\n'.join([f"        inp{i} : in std_logic_vector({width-1} downto 0);" for i in range(inputs)])

    def generate_mux_func_inputs(self, inputs, width):
        return '\n'.join([f"        inp{i} : std_logic_vector({width-1} downto 0);" for i in range(inputs)])

    def generate_mux_proc_inputs(self, inputs, width):
        return '\n'.join([f"        signal inp{i} : in std_logic_vector({width-1} downto 0);" for i in range(inputs)])

    def generate_mux_case_statements(self, inputs, code_type=None):
        if code_type == "Function":
            return '\n'.join([f"            when {i} => result := inp{i};" for i in range(inputs)])
        elif code_type == "Procedure":
            return '\n'.join([f"            when {i} => output <= inp{i};" for i in range(inputs)])
        else:
            return '\n'.join([f"            when {i} => Bitout <= inp{i};" for i in range(inputs)])

    def generate_demux_outputs(self, outputs, width):
        return '\n'.join([f"        out{i} : out std_logic_vector({width-1} downto 0);" for i in range(outputs)])

    def generate_demux_proc_outputs(self, outputs, width):
        return '\n'.join([f"        signal out{i} : out std_logic_vector({width-1} downto 0);" for i in range(outputs)])

    def generate_demux_case_statements(self, outputs, code_type=None):
        if code_type == "Function":
            return '\n'.join([f"            when {i} => result({i}) := input;" for i in range(outputs)])
        elif code_type == "Procedure":
            return '\n'.join([f"            when {i} => out{i} <= input;" for i in range(outputs)])
        else:
            return '\n'.join([f"            when {i} => out{i} <= input;" for i in range(outputs)])

    def create_context_menu(self, event):
        """Create right-click context menu"""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Reset Layout", command=self.reset_layout)
        context_menu.add_separator()
        context_menu.add_command(label="Save Layout", command=self.save_layout)
        context_menu.add_command(label="Load Layout", command=self.load_layout)
        context_menu.post(event.x_root, event.y_root)

    def reset_layout(self):
        """Reset all widgets to their original positions"""
        for widget in self.main_container.winfo_children():
            widget.pack_forget()
            widget.place_forget()
        self.create_content_area()
        self.create_buttons()
        self.create_code_display()
        self.update_params()

    def save_layout(self):
        """Save current layout to a file"""
        try:
            layout = {}
            for widget in self.main_container.winfo_children():
                if hasattr(widget, '_drag_data'):
                    layout[str(widget)] = {
                        'x': widget.winfo_x(),
                        'y': widget.winfo_y()
                    }
            with open('layout.json', 'w') as f:
                json.dump(layout, f)
            messagebox.showinfo("Success", "Layout saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save layout: {str(e)}")

    def load_layout(self):
        """Load layout from a file"""
        try:
            with open('layout.json', 'r') as f:
                layout = json.load(f)
            for widget in self.main_container.winfo_children():
                if str(widget) in layout:
                    pos = layout[str(widget)]
                    widget.place(x=pos['x'], y=pos['y'])
            messagebox.showinfo("Success", "Layout loaded successfully!")
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No saved layout found.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load layout: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernVHDLCodeGenerator(root)
    root.mainloop()
