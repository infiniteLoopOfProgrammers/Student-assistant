from datetime import datetime
import json
from PIL import Image, ImageDraw, ImageFont
import os


class week_planner:
    def __init__(self, fontPath, fontSize, width, height, lineColor,textColor, lineWidth, bgColor, outPath, nameImage, days):
        self.font = ImageFont.truetype(fontPath, fontSize)
        self.fontSize = fontSize
        self.width = width
        self.height = height
        self.lineColor = lineColor
        self.textColor = textColor
        self.lineWidth = lineWidth
        self.bgColor = bgColor
        self.outPath = outPath
        self.nameImage = nameImage
        self.days = days

    def create_week_planner2(self, course_list):
        self.image = Image.new("RGB", (self.width, self.height), self.bgColor)
        draw = ImageDraw.Draw(self.image)
        height = self.height // len(course_list)
        height_move = height
        for course in course_list:
            text = str(course["Units"]) + " : " + " تعداد واحد ("+course["Course_teacher"]+") " + course["Course_name"]
            text = course["Course_name"] + " ("+course["Course_teacher"]+") " + " تعداد واحد " + " : " + str(course["Units"]) 
            draw.text((self.width//2, height_move - (height//2)),
                      text, fill=self.textColor, font=self.font, anchor="mm",direction="rtl")
            height_move += height
        
        
    
    def create_week_planner(self, course_list):
        self.image = Image.new("RGB", (self.width, self.height), self.bgColor)
        draw = ImageDraw.Draw(self.image)
        
        start_time_main = 8
        end_time_main = 20
        num_terms =(end_time_main-start_time_main)//2
        
        cell_width = self.width // (num_terms + 1)
        cell_height = self.height // (len(self.days) + 1)
        
        
        start_time = start_time_main
        for i in range(num_terms):
            x = (num_terms - i) * cell_width
            time_label = f"{start_time + 2:02d}:00 - {start_time:02d}:00"
            draw.text((x - cell_width // 2, cell_height // 2),
                      time_label, fill=self.textColor, font=self.font, anchor="mm")
            draw.line([(x, 0), (x, self.height)],
                      fill=self.lineColor, width=self.lineWidth)
            start_time += 2
            
        for i, day in enumerate(days):
            y = (i + 1) * cell_height
            draw.line([(0, y), (self.width, y)], fill=self.lineColor, width=3)
            draw.text((self.width - cell_width // 2, y + cell_height // 2),
                      day, fill=self.textColor, font=self.font, anchor="mm")
            
        count_utils = sum(course["Units"] for course in course_list)    
        draw.text(
                    (self.width - cell_width // 2, cell_height // 2),
                    f"تعداد واحد : {count_utils}",
                    fill=self.textColor,
                    font=self.font,
                    anchor="mm",
                )
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
                y = (course_day + 1) * cell_height
                x = (num_terms - (start_time - 8)//2) * cell_width

                printloc_x = x - cell_width // 2
                printloc_y = y + cell_height // 2
                printText = f"{course_name}"
                if week == "زوج":
                    draw.line(
                        [(x-cell_width, printloc_y), (x, printloc_y)], fill=self.lineColor, width=3)
                    printloc_y = y + cell_height // 4
                    printText += f" ({week})"
                elif week == "فرد":
                    draw.line(
                        [(x-cell_width, printloc_y), (x, printloc_y)], fill=self.lineColor, width=3)
                    printloc_y = y + (cell_height // 4)*3
                    printText += f" ({week})"

                draw.text(
                    (printloc_x, printloc_y),
                    printText,
                    fill=self.textColor,
                    font=self.font,
                    anchor="mm",
                )

        


    def saveImage(self, counter = 0):
        self.image.save(self.outPath + "/" + self.nameImage + f"{counter}.png")


if __name__ == "__main__":
    with open('out/best_individuals.json', 'r', encoding='utf-8') as f:
        courses = json.load(f)

    days = ["شنبه", "يك شنبه", "دوشنبه", "سه شنبه", "چهارشنبه", "پنج شنبه"]
    font = "font\B NAZANIN BOLD_YASDL.COM.TTF"
    week_planner_obj = week_planner(
        font, 24, 1920, 800, "black","black", 3, (242, 243, 245), "./pic", "week_planner", days)
    
    week_planner_obj2 = week_planner(
        font, 24, 1000, 800, "black",(77,88,108), 3, (237, 245, 248), "./pic", "week_ditaile", days)
    
    if "Course_name" in courses[0]:
        week_planner_obj.create_week_planner(courses)
        week_planner_obj.saveImage()
        week_planner_obj2.create_week_planner2(courses)
        week_planner_obj2.saveImage()
    else:
        for i in range(len(courses)):
            week_planner_obj.create_week_planner(courses[i])
            week_planner_obj.saveImage(i)
            week_planner_obj2.create_week_planner2(courses[i])
            week_planner_obj2.saveImage(i)
# end main
