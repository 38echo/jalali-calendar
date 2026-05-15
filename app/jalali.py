#!/usr/bin/env python3
"""
A comprehensive Persian (Jalali) calendar web application server.

This module provides a real-time Jalali calendar that automatically updates every 60 seconds and
serves it as an interactive HTML page on port 8000. The application runs two concurrent processes:
one continuously generates and updates the calendar HTML, and the other serves the HTML file via
HTTP. The calendar displays all 12 months of the current Jalali year in a responsive 3-column grid
layout with modern styling, highlighting today's date prominently. The Jalali calendar is the
official calendar system used in Iran and Afghanistan.
"""

import http.server
import socketserver
import time
from multiprocessing import Process
import jdatetime


def jalali():
    """
    Continuously generates and writes updated Jalali calendar HTML to index.html.

    This function runs an infinite loop that regenerates the complete Jalali calendar HTML
    every 60 seconds and writes it to the index.html file. This ensures that the calendar
    always displays the current date when accessed via the web server. The function maintains
    persistence by keeping index.html in sync with the current date, so any viewer accessing
    the server will see today's date highlighted in red.

    The calendar generation respects the Persian calendar system where:
    - Months 1-6 have 31 days (Farvardin through Shahrivar)
    - Months 7-11 have 30 days (Mehr through Bahman)
    - Month 12 (Esfand) has 29 or 30 days depending on leap year
    """
    while True:
        calendar_string = generate_jalali_html_calendar()
        with open("index.html", "w", encoding="utf-8") as text_file:
            text_file.write(calendar_string)
        time.sleep(60)


def server():
    """
    Launches an HTTP server to serve the generated Jalali calendar HTML file.

    This function starts a simple HTTP server that listens on port 8000 and serves the
    index.html file (containing the Jalali calendar) to any client that connects. The server
    uses Python's built-in socketserver.TCPServer and http.server.SimpleHTTPRequestHandler to
    handle HTTP requests. This function runs indefinitely, continuously serving requests from
    web browsers and clients. When accessed via http://localhost:8000, clients receive the
    current Jalali calendar HTML with all styling and interactivity intact.
    """
    port = 8000

    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", port), Handler) as httpd:
        print("serving at port", port)
        httpd.serve_forever()


def generate_jalali_html_calendar() -> str:
    """
    Generates a complete HTML representation of the Jalali calendar for the current year.

    This function creates a fully-styled, responsive HTML calendar displaying all 12 months
    of the current Jalali (Persian) year. It retrieves the current date to highlight today's
    date with a red background, making it easily identifiable. The calendar uses modern web
    design principles including:
    - A responsive 3-column grid that adapts to 2 columns on medium screens and 1 column on mobile
    - CSS variables for consistent color theming with slate blue headers and red highlights
    - Proper Persian calendar structure with months named in English transliteration
    - Correct day-of-week calculations respecting the Persian calendar's Saturday-start week
    - Hover effects and box shadows for enhanced visual feedback
    - Proper handling of varying month lengths and leap year calculations

    Returns:
        str: A complete HTML5 document string containing the styled Jalali calendar that is ready
             to be written to a file and served via HTTP. The calendar automatically adapts to
             different screen sizes through CSS media queries.
    """
    # 1. Get today's real-time date components
    today = jdatetime.date.today()
    current_year = today.year
    current_month = today.month
    current_day = today.day

    months_names = [
        "Farvardin",
        "Ordibehesht",
        "Khordad",
        "Tir",
        "Mordad",
        "Shahrivar",
        "Mehr",
        "Aban",
        "Azar",
        "Dey",
        "Bahman",
        "Esfand",
    ]

    # Traditional calendar headers (jdatetime index: Sat=0, Sun=1, ..., Fr=6)
    week_headers = ["Sa", "Su", "Mo", "Tu", "We", "Th", "Fr"]

    # 2. Modern UI Web Design Styles
    html = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        "    <meta charset='utf-8'>",
        "    <style>",
        "        :root {",
        "            --primary-blue: #2C3E50; /* Slate Blue Header */",
        "            --accent-blue: #34495E;",
        "            --highlight-red: #E74C3C; /* Vibrant Red Highlight */",
        "            --bg-light: #F4F6F7;",
        "            --border-color: #E5E8E8;",
        "            --text-dark: #2C3E50;",
        "            --text-muted: #7F8C8D;",
        "        }",
        "        body { ",
        "            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; ",
        "            background-color: var(--bg-light); ",
        "            color: var(--text-dark);",
        "            padding: 40px 20px; ",
        "            margin: 0;",
        "        }",
        "        h1 { ",
        "            text-align: center; ",
        "            font-weight: 300;",
        "            font-size: 2.5rem;",
        "            margin-bottom: 40px;",
        "            color: var(--primary-blue);",
        "        }",
        "        .calendar-grid { ",
        "            display: grid; ",
        "            grid-template-columns: repeat(3, 1fr); ",
        "            gap: 25px; ",
        "            max-width: 1100px; ",
        "            margin: 0 auto; ",
        "        }",
        "        .month-table { ",
        "            background: white; ",
        "            border-collapse: separate; ",
        "            border-spacing: 0;",
        "            width: 100%; ",
        "            border-radius: 8px; ",
        "            overflow: hidden;",
        "            box-shadow: 0 4px 6px rgba(0,0,0,0.03), 0 1px 3px rgba(0,0,0,0.05); ",
        "            transition: transform 0.2s ease, box-shadow 0.2s ease;",
        "        }",
        "        .month-table:hover {",
        "            transform: translateY(-5px);",
        "            box-shadow: 0 10px 15px rgba(0,0,0,0.05);",
        "        }",
        "        .month-title { ",
        "            background-color: var(--primary-blue); ",
        "            color: white; ",
        "            font-weight: 600; ",
        "            font-size: 1.15rem;",
        "            text-align: center; ",
        "            padding: 15px; ",
        "            letter-spacing: 0.5px;",
        "        }",
        "        th { ",
        "            background-color: #FAFAFA; ",
        "            color: var(--text-muted); ",
        "            font-weight: 600;",
        "            font-size: 0.85rem; ",
        "            padding: 12px 8px; ",
        "            text-align: center; ",
        "            border-bottom: 1px solid var(--border-color);",
        "        }",
        "        /* Darken Friday column slightly */",
        "        th:last-child { color: var(--highlight-red); opacity: 0.8; }",
        "        td { ",
        "            padding: 12px 8px; ",
        "            text-align: center; ",
        "            font-size: 0.95rem;",
        "            color: #34495E;",
        "            border-bottom: 1px solid #F9F9F9;",
        "            width: 14.28%; ",
        "        }",
        "        .today { ",
        "            color: white !important; ",
        "            font-weight: bold; ",
        "            background-color: var(--highlight-red) !important; ",
        "            border-radius: 6px; ",
        "            box-shadow: 0 2px 4px rgba(231, 76, 60, 0.4);",
        "        }",
        "        .empty-cell { background-color: #FCFCFC; }",
        "        @media (max-width: 900px) { .calendar-grid { grid-template-columns: repeat(2, 1fr); } }",
        "        @media (max-width: 600px) { .calendar-grid { grid-template-columns: 1fr; } }",
        "    </style>",
        "</head>",
        "<body>",
        f"    <h1>Jalali Year Calendar &mdash; {current_year}</h1>",
        "    <div class='calendar-grid'>",
    ]

    # 3. Loop through all 12 months
    for m_idx in range(1, 13):
        html.append("        <table class='month-table'>")
        html.append(
            f"            <tr><th colspan='7' class='month-title'>{months_names[m_idx-1]} ({m_idx})</th></tr>"
        )

        # Add weekday row headers
        html.append(
            "            <tr>"
            + "".join(f"<th>{day}</th>" for day in week_headers)
            + "</tr>"
        )

        # Calculate days in the month
        if m_idx <= 6:
            days_in_month = 31
        elif m_idx <= 11:
            days_in_month = 30
        else:
            days_in_month = 30 if jdatetime.date(current_year, 1, 1).isleap() else 29

        # Get the first day of the month
        first_day_date = jdatetime.date(current_year, m_idx, 1)
        start_padding = first_day_date.weekday()

        html.append("            <tr>")

        # Insert initial empty cells for padding
        for _ in range(start_padding):
            html.append("                <td class='empty-cell'></td>")

        current_column = start_padding

        # Populate days
        for day in range(1, days_in_month + 1):
            if (
                current_year == today.year
                and m_idx == current_month
                and day == current_day
            ):
                cell_class = " class='today'"
            else:
                cell_class = ""

            html.append(f"                <td{cell_class}>{day}</td>")
            current_column += 1

            # Break row table if it hits the end of the week (Friday / 7th column)
            if current_column == 7:
                if day < days_in_month:
                    html.append("            </tr>\n            <tr>")
                current_column = 0

        # Pad trailing empty cells at the end of the month block
        if current_column < 7 and current_column > 0:
            for _ in range(7 - current_column):
                html.append("                <td class='empty-cell'></td>")

        html.append("            </tr>")
        html.append("        </table>")

    # Close structure
    html.extend(["    </div>", "</body>", "</html>"])

    return "\n".join(html)


if __name__ == "__main__":
    jalali_process = Process(target=jalali)
    jalali_process.start()
    server_process = Process(target=server)
    server_process.start()
