import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

def main():
    root = tb.Window(themename="superhero")
    root.title("Microsip CSV Filter")
    root.geometry("600x400")

    text_log = tk.Text(root, wrap=tk.WORD, font=("Consolas", 10), height=10)
    text_log.pack(expand=True, fill='both', padx=10, pady=10)

    progress = ttk.Progressbar(root, mode="indeterminate", length=400)
    progress.pack(pady=10)

    convert_time_var = tk.BooleanVar(value=False)
    ttk.Checkbutton(
        root,
        text="Convert 'Time' to readable format",
        variable=convert_time_var,
        bootstyle="info"
    ).pack(pady=5)

    filter_type_var = tk.StringVar(value="in")
    ttk.Label(root, text="Select filter type:", bootstyle="info").pack(pady=5)
    filter_type_combobox = ttk.Combobox(
        root,
        textvariable=filter_type_var,
        values=["in", "miss", "both"],
        state="readonly",
        bootstyle="info"
    )
    filter_type_combobox.pack(pady=5)
    filter_type_combobox.current(0)

    def log(msg):
        text_log.insert(tk.END, msg + '\n')
        text_log.see(tk.END)
        root.update()

    def filtrar_csv():
        log("Opening file selector...")
        arquivo_csv = filedialog.askopenfilename(
            title="Select the CSV file",
            filetypes=[("CSV Files", "*.csv")]
        )

        if not arquivo_csv:
            log("No file selected.")
            return

        log(f"Selected file: {arquivo_csv}")

        try:
            progress.start()
            df = pd.read_csv(arquivo_csv)
            log("CSV file loaded successfully.")
        except Exception as e:
            progress.stop()
            log(f"Error loading file: {e}")
            return

        try:
            time_as_datetime = pd.to_datetime(df['Time'], unit='s')
            filter_type = filter_type_var.get()

            if filter_type == "in":
                df_filtered = df[(df['Type'] == 'in') & (time_as_datetime.dt.year == 2024)]
                suffix = "in"
            elif filter_type == "miss":
                df_filtered = df[(df['Type'] == 'miss') & (time_as_datetime.dt.year == 2024)]
                suffix = "miss"
            else:
                df_filtered = df[(df['Type'].isin(['in', 'miss'])) & (time_as_datetime.dt.year == 2024)]
                suffix = "both"

            log(f"Total filtered calls ({filter_type}): {len(df_filtered)}")

            if convert_time_var.get():
                df_filtered['Time'] = time_as_datetime.dt.strftime('%Y-%m-%d %H:%M:%S')
                log("Field 'Time' converted to readable format.")

            base, ext = os.path.splitext(arquivo_csv)
            new_file = f"{base}_FILTERED_{suffix}.csv"
            df_filtered.to_csv(new_file, index=False)
            log(f"Filtered file saved as: {new_file}")
            messagebox.showinfo("Success", f"File saved as:\n{new_file}")
        except Exception as e:
            log(f"Error processing: {e}")
        finally:
            progress.stop()

    ttk.Button(root, text="Select and Filter CSV", command=filtrar_csv, bootstyle=SUCCESS).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
