"""Right-click context menu for the desktop pet."""
import threading
import tkinter as tk
from tkinter import simpledialog


def show_context_menu(pet, screen_pos):
    """Show a right-click context menu at the given screen position.

    Runs in a separate thread since tkinter needs its own event loop.
    """
    def _show():
        root = tk.Tk()
        root.withdraw()  # Hide the main tkinter window
        root.attributes("-topmost", True)

        menu = tk.Menu(root, tearoff=0)

        def feed():
            from states.eating import EatingState
            pet.change_state(EatingState(pet))
            root.destroy()

        def play():
            from states.playing import PlayingState
            pet.change_state(PlayingState(pet))
            root.destroy()

        def sleep():
            from states.sleeping import SleepingState
            pet.change_state(SleepingState(pet))
            root.destroy()

        def set_reminder():
            root.destroy()
            _show_reminder_dialog(pet)

        def quit_pet():
            pet.running = False
            root.destroy()

        def show_status():
            text = (
                f"饥饿度: {pet.status.hunger:.0f}/100\n"
                f"心情:   {pet.status.mood:.0f}/100\n"
                f"体力:   {pet.status.energy:.0f}/100"
            )
            from tkinter import messagebox
            messagebox.showinfo("宠物状态", text)
            root.destroy()

        menu.add_command(label="🍖 喂食", command=feed)
        menu.add_command(label="🎾 玩耍", command=play)
        menu.add_command(label="😴 睡觉", command=sleep)
        menu.add_separator()
        menu.add_command(label="📊 查看状态", command=show_status)
        menu.add_command(label="⏰ 设置提醒", command=set_reminder)
        menu.add_separator()
        menu.add_command(label="❌ 退出", command=quit_pet)

        # Position menu at mouse click
        menu.post(screen_pos[0], screen_pos[1])

        root.mainloop()

    thread = threading.Thread(target=_show, daemon=True)
    thread.start()


def _show_reminder_dialog(pet):
    """Show a dialog to set a reminder."""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    message = simpledialog.askstring(
        "设置提醒", "请输入提醒内容:", parent=root
    )
    if not message:
        root.destroy()
        return

    minutes_str = simpledialog.askstring(
        "设置提醒", "多少分钟后提醒?", parent=root
    )
    root.destroy()

    if not minutes_str:
        return

    try:
        minutes = float(minutes_str)
        pet.reminder_system.add_reminder(message, minutes * 60)
    except ValueError:
        pass
