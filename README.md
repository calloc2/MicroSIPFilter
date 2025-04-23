# Microsip Call Filter

A Python application to filter call records from a CSV file based on type (`in`, `miss`, or `both`) and optionally convert timestamps to a readable format.

## Features
- Filter calls by type (`in`, `miss`, or `both`).
- Specify a date range for filtering.
- Convert Unix timestamps to a human-readable format.
- Save filtered results to a new CSV file.
- Multi-language support.

## Supported Languages
The application supports the following languages:
- Afrikaans (`af`)
- Arabic (`ar`)
- Belarusian (`be`)
- Bulgarian (`bg`)
- Bosnian (`bs`)
- Catalan (`ca`)
- Corsican (`co`)
- Czech (`cs`)
- Welsh (`cy`)
- Danish (`da`)
- German (`de`)
- German (Switzerland) (`de_ch`)
- Greek (`el`)
- English (`en`)
- Esperanto (`eo`)
- Spanish (`es`)
- Spanish (International) (`es_int`)
- Estonian (`et`)
- Basque (`eu`)
- Persian (`fa`)
- Finnish (`fi`)
- French (`fr`)
- Irish (`ga`)
- Scottish Gaelic (`gd`)
- Galician (`gl`)
- Hebrew (`he`)
- Hindi (`hi`)
- Croatian (`hr`)
- Hungarian (`hu`)
- Armenian (`hy`)
- Indonesian (`id`)
- Icelandic (`is`)
- Italian (`it`)
- Japanese (`ja`)
- Georgian (`ka`)
- Korean (`ko`)
- Kurdish (`ku`)
- Luxembourgish (`lb`)
- Lithuanian (`lt`)
- Latvian (`lv`)
- Macedonian (`mk`)
- Mongolian (`mn`)
- Malay (`ms`)
- Norwegian Bokmål (`nb`)
- Dutch (`nl`)
- Norwegian Nynorsk (`nn`)
- Polish (`pl`)
- Pashto (`ps`)
- Portuguese (`pt`)
- Portuguese (Brazil) (`pt_br`)
- Romanian (`ro`)
- Russian (`ru`)
- Slovak (`sk`)
- Slovenian (`sl`)
- Albanian (`sq`)
- Serbian (`sr`)
- Serbian (Latin) (`sr_latn`)
- Swedish (`sv`)
- Tamil (`ta`)
- Thai (`th`)
- Turkish (`tr`)
- Tatar (`tt`)
- Ukrainian (`uk`)
- Uzbek (`uz`)
- Vietnamese (`vi`)
- Simplified Chinese (`zh_cn`)
- Traditional Chinese (`zh_tw`)

## Requirements
- Python 3.8+
- Required libraries:
  - `pandas`
  - `ttkbootstrap`
  - `tkcalendar`

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd microsipFilter
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python main.py
   ```