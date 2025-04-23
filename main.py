import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import yaml
import webbrowser
import json
from ttkbootstrap.widgets import DateEntry 

CONFIG_FILE = "config.json"

def load_translation(language):
    with open(f"translations/{language}.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)

def load_config():
    if not os.path.exists(CONFIG_FILE) or os.stat(CONFIG_FILE).st_size == 0:
        default_config = {
            "language": "en",
            "theme": "superhero"
        }
        save_config(default_config)
        return default_config
    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            default_config = {
                "language": "en",
                "theme": "superhero"
            }
            save_config(default_config)
            return default_config

def save_config(config):
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, indent=4)

current_language = "en"
translations = load_translation(current_language)

def translate(key, **kwargs):
    return translations.get(key, key).format(**kwargs)

def load_available_languages():
    translations_dir = "translations"
    languages = []
    for file in os.listdir(translations_dir):
        if file.endswith(".yaml"):
            lang_code = os.path.splitext(file)[0]
            languages.append(lang_code)
    return languages

def main():
    global current_language, translations

    config = load_config()
    current_language = config.get("language", "en")
    current_theme = config.get("theme", "superhero")
    translations = load_translation(current_language)

    available_languages = load_available_languages()

    def update_language(lang):
        global translations
        current_language = lang
        translations = load_translation(lang)
        config["language"] = lang
        save_config(config)
        root.title(translate("title"))
        filter_label.config(text=translate("select_filter_type"))
        convert_time_check.config(text=translate("convert_time"))
        filter_button.config(text=translate("filter_button"))
        menubar.entryconfig(0, label=translate("language_menu"))
        menubar.entryconfig(1, label=translate("theme_menu"))
        menubar.entryconfig(2, label=translate("about_menu"))

    def update_theme(theme):
        root.style.theme_use(theme)
        config["theme"] = theme
        save_config(config)

    def open_about():
        webbrowser.open("https://github.com/calloc2/MicroSIPFilter")

    root = tb.Window(themename=current_theme)
    root.title(translate("title"))
    root.geometry("600x400")

    menubar = tk.Menu(root)

    language_menu = tk.Menu(menubar, tearoff=0)
    for lang_code in available_languages:
        lang_name = load_translation(lang_code)["language_name"]
        language_menu.add_command(label=lang_name, command=lambda l=lang_code: update_language(l))
    menubar.add_cascade(label=translate("language_menu"), menu=language_menu)

    theme_menu = tk.Menu(menubar, tearoff=0)
    for theme in root.style.theme_names():
        theme_menu.add_command(label=theme, command=lambda t=theme: update_theme(t))
    menubar.add_cascade(label=translate("theme_menu"), menu=theme_menu)

    about_menu = tk.Menu(menubar, tearoff=0)
    about_menu.add_command(label="GitHub", command=open_about)
    menubar.add_cascade(label=translate("about_menu"), menu=about_menu)

    root.config(menu=menubar)

    text_log = tk.Text(root, wrap=tk.WORD, font=("Consolas", 10), height=10)
    text_log.pack(expand=True, fill='both', padx=10, pady=10)

    progress = ttk.Progressbar(root, mode="indeterminate", length=400)
    progress.pack(pady=10)

    convert_time_var = tk.BooleanVar(value=config.get("convert_time", False))
    convert_time_check = ttk.Checkbutton(
        root,
        text=translate("convert_time"),
        variable=convert_time_var,
        bootstyle="info"
    )
    convert_time_check.pack(pady=5)

    filter_type_var = tk.StringVar(value=config.get("filter_type", "in"))
    filter_label = ttk.Label(root, text=translate("select_filter_type"), bootstyle="info")
    filter_label.pack(pady=5)
    filter_type_combobox = ttk.Combobox(
        root,
        textvariable=filter_type_var,
        values=["in", "miss", "both"],
        state="readonly",
        bootstyle="info"
    )
    filter_type_combobox.pack(pady=5)
    filter_type_combobox.current(["in", "miss", "both"].index(config.get("filter_type", "in")))

    date_frame = ttk.Frame(root)
    date_frame.pack(pady=10)

    start_date_label = ttk.Label(date_frame, text="Start Date:", bootstyle="info")
    start_date_label.grid(row=0, column=0, padx=5)
    start_date_entry = DateEntry(
        date_frame,
        dateformat="%Y-%m-%d",
        bootstyle="info"
    )
    start_date_entry.grid(row=0, column=1, padx=5)

    end_date_label = ttk.Label(date_frame, text="End Date:", bootstyle="info")
    end_date_label.grid(row=0, column=2, padx=5)
    end_date_entry = DateEntry(
        date_frame,
        dateformat="%Y-%m-%d",
        bootstyle="info"
    )
    end_date_entry.grid(row=0, column=3, padx=5)

    def log(msg):
        text_log.insert(tk.END, msg + '\n')
        text_log.see(tk.END)
        root.update()

    def filtrar_csv():
        log(translate("select_file"))
        arquivo_csv = filedialog.askopenfilename(
            title=translate("select_file"),
            filetypes=[("CSV Files", "*.csv")]
        )

        if not arquivo_csv:
            log(translate("no_file_selected"))
            return

        log(f"{translate('file_selected')} {arquivo_csv}")

        try:
            progress.start()
            df = pd.read_csv(arquivo_csv)
            log(translate("csv_loaded"))
        except Exception as e:
            progress.stop()
            log(f"{translate('error_loading')} {e}")
            return

        try:
            time_as_datetime = pd.to_datetime(df['Time'], unit='s')
            filter_type = filter_type_var.get()

            start_date = pd.to_datetime(start_date_entry.entry.get())
            end_date = pd.to_datetime(end_date_entry.entry.get())
            df = df[(time_as_datetime >= start_date) & (time_as_datetime <= end_date)]

            if filter_type == "in":
                df_filtered = df[df['Type'] == 'in']
                suffix = "in"
            elif filter_type == "miss":
                df_filtered = df[df['Type'] == 'miss']
                suffix = "miss"
            else:
                df_filtered = df[df['Type'].isin(['in', 'miss'])]
                suffix = "both"

            log(translate("total_filtered", filter_type=filter_type))

            if convert_time_var.get():
                df_filtered['Time'] = time_as_datetime.dt.strftime('%Y-%m-%d %H:%M:%S')
                log(translate("time_converted"))

            base, ext = os.path.splitext(arquivo_csv)
            new_file = f"{base}_FILTERED_{suffix}.csv"
            df_filtered.to_csv(new_file, index=False)
            log(f"{translate('file_saved')} {new_file}")
            messagebox.showinfo(translate("success"), f"{translate('file_saved')}:\n{new_file}")
        except Exception as e:
            log(f"{translate('error_processing')} {e}")
        finally:
            progress.stop()

    filter_button = ttk.Button(root, text=translate("filter_button"), command=filtrar_csv, bootstyle=SUCCESS)
    filter_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
