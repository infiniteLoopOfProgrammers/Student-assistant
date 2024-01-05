import pyodbc
from datetime import datetime
import json
from GetData import DataAdapter
from GetInputs import inputs
import pickle
import hashlib
# define the class of time of courses


class Time_of_course:
    def __init__(self, day,  Start_hour, End_hour, Week):
        self.day = day
        self.Start_hour = Start_hour
        self.End_hour = End_hour
        self.Week = Week

    def __dict__(self):
        week_str = "ثابت"
        if self.Week==1:
            week_str = "فرد"
        elif self.Week==2:
            week_str = "زوج"

        obj = {
            "Start_Time": self.Start_hour.strftime("%H:%M"),
            "End_Time": self.End_hour.strftime("%H:%M"),
            "Course_day": self.day,
            "Week": week_str
        }
        return obj

    def __getitem__(self, key):
        # با استفاده از این متد، اشیاء از این کلاس می‌توانند مانند یک دیکشنری ایندکس‌ پذیر باشند
        return getattr(self, key, None)

    def check_interception(self, another_course):
        if self.day != another_course.day:
            return False  # تداخل ندارد
        start_1= self.Start_hour
        end_1 = self.End_hour
        start_2 = another_course.Start_hour
        end_2 = another_course.End_hour
        # بررسی شرایط تداخل
        if end_1 <= start_2 or start_1 >= end_2:
            return False  # تداخل ندارد
        else:
            if self.Week == 3 or another_course.Week == 3 or another_course.Week == self.Week:
                return True  # تداخل دارد
            else:
                return False  # تداخل ندارد


class Course:
    def __init__(self, Id, College_code, College_name, Group_code, Group_name, Course_id,  Course_name, Units, Practica_unit, Capacity, Registered_number, Waiting_list, Gender, Course_teacher, Course_time_1, Course_exam, Limitation, For_entry, Compulsory_courses, Present, Type_of_course, Description):
        self.Id = Id
        self.College_code = College_code
        self.College_name = College_name
        self.Group_code = Group_code
        self.Group_name = Group_name
        self.Course_id = Course_id
        self.Course_name = Course_name
        self.Units = Units
        self.Practica_unit = Practica_unit
        self.Capacity = Capacity
        self.Registered_number = Registered_number
        self.Waiting_list = Waiting_list
        self.Gender = Gender
        self.Course_teacher = Course_teacher.replace("\r", "").replace("\n", "").strip()
        self.Course_time_1 = Course_time_1
        self.Course_exam = Course_exam
        self.CourseExamSplited = self.Course_exam_splited()
        self.Limitation = Limitation
        self.For_entry = For_entry
        self.Compulsory_courses = Compulsory_courses
        self.Present = Present
        self.Type_of_course = Type_of_course
        self.Description = Description
        self.TimesOfCourse = self.spliteTimeCourse()

    @staticmethod
    def text_to_time(text_time):
        start_time, end_time = text_time.split('-')
        start_datetime = datetime.strptime(start_time, "%H:%M")
        end_datetime = datetime.strptime(end_time, "%H:%M")
        start_hour = start_datetime.time()
        end_hour = end_datetime.time()
        return start_hour, end_hour

    @staticmethod
    def find_week(text):
        if text[0] == 'ز':
            return 2
        if text[0] == 'ف':
            return 1
        return 3

    def spliteTimeCourse(self):
        time = self.Course_time_1
        timeList = []
        if time is not None:  # checking that the course is not be null
            time_info = time.split("،")
            for item in time_info:
                item = item.lstrip()
                info = item.split(" ")
                temp = info[2]
                if temp[0] == '0' or temp[0] == '1':
                    day = info[1]
                    start_time, end_time = Course.text_to_time(temp)
                    if len(info) > 3:
                        week = Course.find_week(info[3])
                    else:
                        week = 3
                else:
                    day = info[1] + " " + info[2]
                    temp = info[3]
                    start_time, end_time = Course.text_to_time(temp)
                    if len(info) > 4:
                        week = Course.find_week(info[4])
                    else:
                        week = 3
                timeList.append(Time_of_course(
                    day, start_time, end_time, week))
            return timeList
        return None

    def Course_exam_splited(self):
        if self.Course_exam is None:
            return None
        if len(self.Course_exam) < 1:
            return None
        Course_exam_splite_temp = self.Course_exam.split()
        Course_exam_splite_temp_hour = Course_exam_splite_temp[3].split("-")
        return {"Data": Course_exam_splite_temp[1], "Start": datetime.strptime(Course_exam_splite_temp_hour[0], "%H:%M").time(), "End": datetime.strptime(Course_exam_splite_temp_hour[1], "%H:%M").time()}

    def check_interception_courses_exam(self, otherCourses):
        if self.CourseExamSplited is not None and otherCourses.CourseExamSplited is not None:
            if self.CourseExamSplited["Date"] != otherCourses.CourseExamSplited["Date"]:
                return False
            if self.CourseExamSplited["Start"] >= otherCourses.CourseExamSplited["End"] or self.CourseExamSplited["End"] <= otherCourses.CourseExamSplited["Start"]:
                return False

            return True
        else:
            return False

    def check_interception_courses(self, otherCourses):
        if self.TimesOfCourse is None or otherCourses.TimesOfCourse is None:
            return False
        if self.Course_id.split("_")[0] == otherCourses.Course_id.split("_")[0]:
            return True
        if self.Course_id == "3031010_07" and otherCourses.Course_id == "3031025_01":
            pass
        if self.Course_id == "3031025_01" and otherCourses.Course_id == "3031010_07":
            pass
        for itemTime1 in self.TimesOfCourse:
            for itemTime2 in otherCourses.TimesOfCourse:
                if itemTime1.check_interception(itemTime2):
                    return True

        return False

    def __dict__(self):
        obje = []
        if self.TimesOfCourse != None:
            for item in self.TimesOfCourse:
                obje.append(item.__dict__())

        one_course = {
            "Course_id": self.Course_id,
            "Course_id_main": self.Course_id.split("_")[0],
            "Course_name": self.Course_name,
            "Units": self.Units,
            "Course_teacher": self.Course_teacher,
        }
        if obje.__len__() > 0:
            one_course["Time"] = obje
        
        if self.CourseExamSplited is not None:
           one_course["ExamTime"] = {"Data": self.CourseExamSplited["Data"],
                                     "Start": self.CourseExamSplited["Start"].strftime("%H:%M"),
                                     "End": self.CourseExamSplited["End"].strftime("%H:%M")}
        return one_course

def create_checksum(objects):
    sorted_objects = sorted(objects, key=lambda obj: obj.Id)
    # Serialize the list of objects to a bytes object
    serialized = pickle.dumps(sorted_objects)

    # Create a hash object
    hash_obj = hashlib.sha256()

    # Update the hash object with the serialized bytes object
    hash_obj.update(serialized)

    # Return the hexadecimal checksum
    return hash_obj.hexdigest()

courseCode, groupCode = inputs()
rows = DataAdapter(f"""SELECT Top 20 courses.*, courses.groupCode
                        FROM courses
                        WHERE (((courses.courseCode)=?) AND ((courses.groupCode)=?));
                        """,(courseCode,groupCode))


information_of_Courses = []
# information_of_time = []

# انتقال اطلاعات دیتابیس به یک آرایه
for row in rows:
    # new_Course = Course(rows[12])
    information_of_Courses.append(Course(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15],
                                         row[16], row[17], row[18], row[19], row[20], row[21]))

all_course = []
# نوشتن اطلاعات هر تایم از یک کلاس در یک خط جدید
for coursess in information_of_Courses:
    all_course.append(coursess.__dict__())

        
group_all_course = [[]]
group_all_course_checksum = [0]
for courses in information_of_Courses:
    group_all_course_temp = []
    index = 0
    for group in group_all_course:
        group_courses = [courses]
        flag = False
        for course_ in group:
            if courses.check_interception_courses(course_):
                flag = True
            else:
                group_courses.append(course_)
                
        if flag:
            group_all_course_temp.append(group_courses)
        else:
            group.append(courses) 
            group_all_course_checksum[index] = create_checksum(group)
            
        index += 1  
        
    for group in group_all_course_temp:
        checksum = create_checksum(group)  
        if checksum not in group_all_course_checksum :            
            group_all_course.append(group)
            group_all_course_checksum.append(checksum)
        else:
            pass  
                
group_all_course_json = []   
for group in group_all_course:
    group_course_json = []
    for course_ in group:
        group_course_json.append(course_.__dict__())
    group_all_course_json.append(group_course_json) 
       
with open("json/data.json", mode='w', encoding='utf-8') as file:
    json.dump(all_course, file, ensure_ascii=False)

with open("json/dataGroup.json", mode='w', encoding='utf-8') as file:
    json.dump(group_all_course_json, file, ensure_ascii=False)
