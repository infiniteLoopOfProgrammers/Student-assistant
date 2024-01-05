from datetime import datetime
import json
from PIL import Image, ImageDraw, ImageFont
import os


def create_week_planner(course_list, namePic):
    width, height = 1920, 800
    image = Image.new("RGB", (width, height),(242,243,245))
    draw = ImageDraw.Draw(image)
    font_size = 24
    font = ImageFont.truetype("font\B NAZANIN BOLD_YASDL.COM.TTF", font_size)
    days = ["شنبه", "يك شنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه"]
    num_terms = 6
    cell_width = width // (num_terms + 1)
    cell_height = height // (len(days) + 1)
    draw.line([(0, 0), (0, height)], fill="black", width=3)
    for i in range(num_terms + 1):
        x = i * cell_width
        draw.line([(x, 0), (x, height)], fill="black", width=3)

    start_time = 8
    for i in range(num_terms):
        x = (num_terms - i) * cell_width
        time_label = f"{start_time + 2:02d}:00 - {start_time:02d}:00"
        draw.text((x - cell_width // 2, cell_height // 2),
                  time_label, fill="black", font=font, anchor="mm")
        draw.line([(x, cell_height), (x - cell_width, cell_height)],
                  fill="black", width=2)
        start_time += 2

    for i, day in enumerate(days):
        y = (i + 1) * cell_height
        draw.line([(0, y), (width, y)], fill="black", width=3)
        draw.text((width - cell_width // 2, y + cell_height // 2),
                  day, fill="black", font=font, anchor="mm")
        for j in range(num_terms):
            for course in course_list:
                course_name = course["Course_name"]
                if "Time" not in course:
                    continue
                for item in course["Time"]:

                    start_time = datetime.strptime(
                        item["Start_Time"], "%H:%M").hour
                    end_time = datetime.strptime(
                        item["End_Time"], "%H:%M").hour
                    course_day = days.index(item["Course_day"])
                    week = item["Week"]
                    x = (num_terms - j) * cell_width
                    term_start_time = 8 + 2 * j
                    term_end_time = term_start_time + 2
                    if (
                        i == course_day
                        and start_time >= term_start_time
                        and end_time <= term_end_time
                        and term_start_time >= 8
                        and term_end_time <= 20
                    ):
                        printloc_x = x - cell_width // 2
                        printloc_y = y + cell_height // 2
                        printText = f"{course_name}"
                        if week == "زوج":
                            draw.line([(x-cell_width, printloc_y), (x,
                                    printloc_y)], fill="black", width=3)
                            printloc_y = y + cell_height // 4
                            printText += f" ({week})"
                        elif week == "فرد":
                            draw.line([(x-cell_width, printloc_y), (x,
                                    printloc_y)], fill="black", width=3)
                            printloc_y = y + (cell_height // 4)*3
                            printText += f" ({week})"
                        
                        draw.text(
                            (printloc_x, printloc_y),
                            printText,
                            fill="black",
                            font=font,
                            anchor="mm",
                        )

    count_utils = sum(course["Units"] for course in course_list)
    image.save(namePic+f"_{count_utils}.png")


with open('out/best_individuals.json', 'r', encoding='utf-8') as f:
    courses = json.load(f)

name = "pic/week_planner"
# create_week_planner(courses,name)
for i in range(len(courses)):
    create_week_planner(courses[i], name+f"{i}")
