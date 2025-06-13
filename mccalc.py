import tkinter as tk

# --- Dark mode colors ---
LIGHT_BG = "#f0f0f0"
LIGHT_FG = "#000000"
LIGHT_BOX_BG = "#ddd"
LIGHT_OVERFLOW_BG = "#ccc"

DARK_BG = "#222222"
DARK_FG = "#eeeeee"
DARK_BOX_BG = "#555555"
DARK_OVERFLOW_BG = "#888888"

dark_mode = True  # start in dark mode

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
        frame = tk.Frame(visual_frame, width=40, height=40, bg=box_bg, relief="ridge", borderwidth=2)
        frame.grid_propagate(False)
        frame.grid(row=i // cols, column=i % cols, padx=2, pady=2)
        label = tk.Label(frame, font=("Segoe UI", 9, "bold"), bg=box_bg, fg=fg)
        label.pack(expand=True, fill="both")

        if i < stacks:
            label.config(text=str(stack_size))
        else:
            label.config(text=str(extras))

    if hidden_slots > 0:
        frame = tk.Frame(visual_frame, width=40, height=40, bg=overflow_bg, relief="ridge", borderwidth=2)
        frame.grid_propagate(False)
        frame.grid(row=visible_slots // cols, column=visible_slots % cols, padx=2, pady=2)
        label = tk.Label(frame, font=("Segoe UI", 9, "bold"), bg=overflow_bg, fg=fg, text=f"{hidden_slots}+")
        label.pack(expand=True, fill="both")

def parse(entry):
    try:
        return int(entry.get())
    except:
        return 0

def auto_calculate(func):
    # wrapper to call calculate automatically on any input change
    def inner(*args):
        func()
    return inner

def setup_stack_to_items():
    clear_inputs()
    tk.Label(input_frame, text="Stacks:").grid(row=0, column=0, sticky='w')
    stack_entry = tk.Entry(input_frame)
    stack_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Extra Items:").grid(row=1, column=0, sticky='w')
    extra_entry = tk.Entry(input_frame)
    extra_entry.grid(row=1, column=1)

    def calculate():
        stacks = parse(stack_entry)
        extras = parse(extra_entry)
        total = stacks * 64 + extras
        result_var.set(f"{stacks} stacks + {extras} items = {total} items")
        create_visualizer(stacks, extras)

    # Bind entry changes to auto calculate
    stack_entry.bind("<KeyRelease>", lambda e: calculate())
    extra_entry.bind("<KeyRelease>", lambda e: calculate())

    calculate()  # initial calculate

def setup_items_to_stack():
    clear_inputs()
    tk.Label(input_frame, text="Total Items:").grid(row=0, column=0, sticky='w')
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
    tk.Label(input_frame, text="16-Stacks:").grid(row=0, column=0, sticky='w')
    stack_entry = tk.Entry(input_frame)
    stack_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Extra Items:").grid(row=1, column=0, sticky='w')
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
    tk.Label(input_frame, text="Shulkers:").grid(row=0, column=0, sticky='w')
    shulker_entry = tk.Entry(input_frame)
    shulker_entry.grid(row=0, column=1)

    tk.Label(input_frame, text="Filled Slots:").grid(row=1, column=0, sticky='w')
    slots_entry = tk.Entry(input_frame)
    slots_entry.grid(row=1, column=1)

    tk.Label(input_frame, text="Extra Items:").grid(row=2, column=0, sticky='w')
    extra_entry = tk.Entry(input_frame)
    extra_entry.grid(row=2, column=1)

    tk.Label(input_frame, text="Stack Size (16/64):").grid(row=3, column=0, sticky='w')
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

    shulker_entry.bind("<KeyRelease>", lambda e: calculate())
    slots_entry.bind("<KeyRelease>", lambda e: calculate())
    extra_entry.bind("<KeyRelease>", lambda e: calculate())
    stack_type_entry.bind("<KeyRelease>", lambda e: calculate())
    calculate()

def clear_inputs():
    for widget in input_frame.winfo_children():
        widget.destroy()
    result_var.set("")
    clear_visuals()

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
    version_label.config(bg=bg, fg="#888")  # fixed grey
    dark_mode_button.config(bg=bg, fg=fg)

    for widget in top_button_frame.winfo_children():
        widget.config(bg=bg, fg=fg)
    for widget in input_frame.winfo_children():
        try:
            widget.config(bg=bg, fg=fg)
        except:
            pass

def on_calc_button_click(setup_func):
    # When switching mode, keep dark mode on & just call setup_func
    setup_func()
    apply_colors()

# Main GUI setup
root = tk.Tk()
root.title("MC Calc")
root.geometry("700x600")

# Frames
top_button_frame = tk.Frame(root)
top_button_frame.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack()

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var, font=("Segoe UI", 12))
result_label.pack(pady=10)

visual_frame = tk.Frame(root)
visual_frame.pack(pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(side="bottom", fill="x", pady=5, padx=5)

# Version label on bottom-left
version_label = tk.Label(bottom_frame, text="version 1.5 RELEASE.", fg="#888", font=("Segoe UI", 9))
version_label.pack(side="left")

# Dark mode toggle button next to version
dark_mode_button = tk.Button(bottom_frame, text="Toggle Dark Mode", command=toggle_dark_mode)
dark_mode_button.pack(side="left", padx=10)

# Buttons
tk.Button(top_button_frame, text="Stacks → Items", command=lambda: on_calc_button_click(setup_stack_to_items)).grid(row=0, column=0, padx=5)
tk.Button(top_button_frame, text="Items → Stacks", command=lambda: on_calc_button_click(setup_items_to_stack)).grid(row=0, column=1, padx=5)
tk.Button(top_button_frame, text="16 Stacks", command=lambda: on_calc_button_click(setup_16_stack)).grid(row=0, column=2, padx=5)
tk.Button(top_button_frame, text="Shulkers", command=lambda: on_calc_button_click(setup_shulkers)).grid(row=0, column=3, padx=5)

setup_stack_to_items()
apply_colors()

root.mainloop()


