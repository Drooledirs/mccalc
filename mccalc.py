import tkinter as tk
import tkinter.font as tkFont
import os
import sys

# --- Minecraft Theme Colors ---
LIGHT_BG = "#d7c89a"
LIGHT_FG = "#3f3f3f"
LIGHT_BOX_BG = "#e0dbb8"
LIGHT_OVERFLOW_BG = "#b3aa88"

DARK_BG = "#2e2e2e"
DARK_FG = "#fefefe"
DARK_BOX_BG = "#555555"
DARK_OVERFLOW_BG = "#888888"

dark_mode = False

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load Minecraftia font if available
FONT_PATH = resource_path("Minecraftia-Regular.ttf")
if os.path.exists(FONT_PATH):
    minecraft_font = ("Minecraftia", 10)
else:
    minecraft_font = ("Courier", 10)

def clear_visuals():
    for widget in visual_frame.winfo_children():
        widget.destroy()

def create_visualizer(stacks, extras, stack_size=64):
    clear_visuals()
    total_slots = stacks + (1 if extras > 0 else 0)
    cols = 9
    max_rows = 6
    max_visible = cols * max_rows
    visible_slots = min(total_slots, max_visible)
    hidden_slots = total_slots - visible_slots

    box_bg = DARK_BOX_BG if dark_mode else LIGHT_BOX_BG
    overflow_bg = DARK_OVERFLOW_BG if dark_mode else LIGHT_OVERFLOW_BG
    fg = DARK_FG if dark_mode else LIGHT_FG

    for i in range(visible_slots):
        frame = tk.Frame(visual_frame, width=40, height=40, bg=box_bg, relief="ridge", borderwidth=3)
        frame.grid_propagate(False)
        frame.grid(row=i // cols, column=i % cols, padx=2, pady=2)
        label = tk.Label(frame, font=minecraft_font, bg=box_bg, fg=fg)
        label.pack(expand=True, fill="both")
        label.config(text=str(stack_size) if i < stacks else str(extras))

    if hidden_slots > 0:
        frame = tk.Frame(visual_frame, width=40, height=40, bg=overflow_bg, relief="ridge", borderwidth=3)
        frame.grid_propagate(False)
        frame.grid(row=visible_slots // cols, column=visible_slots % cols, padx=2, pady=2)
        label = tk.Label(frame, font=minecraft_font, bg=overflow_bg, fg=fg, text=f"{hidden_slots}+")
        label.pack(expand=True, fill="both")

def parse(entry):
    try:
        return int(entry.get())
    except:
        return 0

def clear_inputs():
    for widget in input_frame.winfo_children():
        widget.destroy()
    result_var.set("")
    clear_visuals()

def setup_stack_to_items():
    clear_inputs()
    tk.Label(input_frame, text="Stacks:", font=minecraft_font).grid(row=0, column=0, sticky='w')
    stack_entry = tk.Entry(input_frame)
    stack_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Extra Items:", font=minecraft_font).grid(row=1, column=0, sticky='w')
    extra_entry = tk.Entry(input_frame)
    extra_entry.grid(row=1, column=1)

    def calculate():
        stacks = parse(stack_entry)
        extras = parse(extra_entry)
        total = stacks * 64 + extras
        result_var.set(f"{stacks} stacks + {extras} items = {total} items")
        create_visualizer(stacks, extras)

    stack_entry.bind("<KeyRelease>", lambda e: calculate())
    extra_entry.bind("<KeyRelease>", lambda e: calculate())
    calculate()

def setup_items_to_stack():
    clear_inputs()
    tk.Label(input_frame, text="Total Items:", font=minecraft_font).grid(row=0, column=0, sticky='w')
    items_entry = tk.Entry(input_frame)
    items_entry.grid(row=0, column=1)

    def calculate():
        total = parse(items_entry)
        stacks = total // 64
        extras = total % 64
        result_var.set(f"{total} items = {stacks} stacks + {extras} items")
        create_visualizer(stacks, extras)

    items_entry.bind("<KeyRelease>", lambda e: calculate())
    calculate()

def setup_16_stack():
    clear_inputs()
    tk.Label(input_frame, text="16-Stacks:", font=minecraft_font).grid(row=0, column=0, sticky='w')
    stack_entry = tk.Entry(input_frame)
    stack_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Extra Items:", font=minecraft_font).grid(row=1, column=0, sticky='w')
    extra_entry = tk.Entry(input_frame)
    extra_entry.grid(row=1, column=1)

    def calculate():
        stacks = parse(stack_entry)
        extras = parse(extra_entry)
        total = stacks * 16 + extras
        result_var.set(f"{stacks} 16-stacks + {extras} = {total} items")
        create_visualizer(stacks, extras, stack_size=16)

    stack_entry.bind("<KeyRelease>", lambda e: calculate())
    extra_entry.bind("<KeyRelease>", lambda e: calculate())
    calculate()

def setup_shulkers():
    clear_inputs()
    tk.Label(input_frame, text="Shulkers:", font=minecraft_font).grid(row=0, column=0, sticky='w')
    shulker_entry = tk.Entry(input_frame)
    shulker_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Filled Slots:", font=minecraft_font).grid(row=1, column=0, sticky='w')
    slots_entry = tk.Entry(input_frame)
    slots_entry.grid(row=1, column=1)

    tk.Label(input_frame, text="Extra Items:", font=minecraft_font).grid(row=2, column=0, sticky='w')
    extra_entry = tk.Entry(input_frame)
    extra_entry.grid(row=2, column=1)

    tk.Label(input_frame, text="Stack Size (16/64):", font=minecraft_font).grid(row=3, column=0, sticky='w')
    stack_type_entry = tk.Entry(input_frame)
    stack_type_entry.grid(row=3, column=1)

    def calculate():
        shulkers = parse(shulker_entry)
        slots = parse(slots_entry)
        extras = parse(extra_entry)
        stack_size = parse(stack_type_entry) or 64
        total_stacks = shulkers * 27 + slots
        total_items = total_stacks * stack_size + extras
        result_var.set(f"{total_items} items ({total_stacks} stacks + {extras})")
        create_visualizer(total_stacks, extras, stack_size=stack_size)

    for entry in [shulker_entry, slots_entry, extra_entry, stack_type_entry]:
        entry.bind("<KeyRelease>", lambda e: calculate())
    calculate()

def setup_gui_calculator():
    clear_inputs()
    expression = tk.StringVar()

    def press(char):
        expression.set(expression.get() + char)

    def clear():
        expression.set("")
        result_var.set("")
        clear_visuals()

    def evaluate():
        try:
            # safe eval with limited globals
            result = eval(expression.get(), {"__builtins__": None}, {"abs": abs, "round": round})
            result_var.set(f"{expression.get()} = {result}")
            update_display(result)
        except:
            result_var.set("Invalid expression")
            clear_visuals()

    def update_display(result):
        clear_visuals()
        box_bg = DARK_BOX_BG if dark_mode else LIGHT_BOX_BG
        fg = DARK_FG if dark_mode else LIGHT_FG
        frame = tk.Frame(visual_frame, width=100, height=40, bg=box_bg, relief="ridge", borderwidth=3)
        frame.grid_propagate(False)
        frame.grid(row=0, column=0, padx=2, pady=2)
        label = tk.Label(frame, font=minecraft_font, bg=box_bg, fg=fg, text=str(result))
        label.pack(expand=True, fill="both")

    tk.Entry(input_frame, textvariable=expression, font=("Courier", 14), width=28).grid(row=0, column=0, columnspan=4, pady=10)

    buttons = [
        ("7", "8", "9", "/"),
        ("4", "5", "6", "*"),
        ("1", "2", "3", "-"),
        ("0", "(", ")", "+"),
        ("C", "=", "", "")
    ]

    for r, row in enumerate(buttons, 1):
        for c, char in enumerate(row):
            if char:
                action = clear if char == "C" else (evaluate if char == "=" else lambda ch=char: press(ch))
                btn = tk.Button(input_frame, text=char, width=6, height=2, font=minecraft_font, command=action)
                btn.grid(row=r, column=c, padx=2, pady=2)

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    apply_colors()

def apply_colors():
    bg = DARK_BG if dark_mode else LIGHT_BG
    fg = DARK_FG if dark_mode else LIGHT_FG

    root.config(bg=bg)
    top_button_frame.config(bg=bg)
    input_frame.config(bg=bg)
    visual_frame.config(bg=bg)
    result_label.config(bg=bg, fg=fg)
    bottom_frame.config(bg=bg)
    version_label.config(bg=bg, fg="#888")
    dark_mode_button.config(bg=bg, fg=fg)

    for frame in [top_button_frame, input_frame]:
        for widget in frame.winfo_children():
            try:
                widget.config(bg=bg, fg=fg)
            except:
                pass

def on_calc_button_click(setup_func):
    setup_func()
    apply_colors()

# Main GUI
root = tk.Tk()
root.title("Minecraft Stack Calculator")
root.geometry("750x620")

top_button_frame = tk.Frame(root)
top_button_frame.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack()

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=minecraft_font)
result_label.pack(pady=10)

visual_frame = tk.Frame(root)
visual_frame.pack(pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)

version_label = tk.Label(bottom_frame, text="MC Calc v1.5.3", font=minecraft_font, fg="#888")
version_label.pack(side="left")

dark_mode_button = tk.Button(bottom_frame, text="Toggle Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(side="left", padx=10)

# Top Buttons
tk.Button(top_button_frame, text="Stacks → Items", command=lambda: on_calc_button_click(setup_stack_to_items)).grid(row=0, column=0, padx=5)
tk.Button(top_button_frame, text="Items → Stacks", command=lambda: on_calc_button_click(setup_items_to_stack)).grid(row=0, column=1, padx=5)
tk.Button(top_button_frame, text="16 Stacks", command=lambda: on_calc_button_click(setup_16_stack)).grid(row=0, column=2, padx=5)
tk.Button(top_button_frame, text="Shulkers", command=lambda: on_calc_button_click(setup_shulkers)).grid(row=0, column=3, padx=5)
tk.Button(top_button_frame, text="GUI Calculator", command=lambda: on_calc_button_click(setup_gui_calculator)).grid(row=0, column=4, padx=5)

setup_stack_to_items()
apply_colors()
root.mainloop()


