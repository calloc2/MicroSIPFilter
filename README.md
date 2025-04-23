# Microsip Call Filter

A Python application to filter call records from a CSV file based on type (`in`, `miss`, or `both`) and optionally convert timestamps to a readable format.

## Features
- Filter calls by type (`in`, `miss`, or `both`).
- Specify a date range for filtering.
- Convert Unix timestamps to a human-readable format.
- Save filtered results to a new CSV file.

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

2. Running:
   ```bash
   python main.py
   ```