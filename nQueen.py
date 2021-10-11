import json


def set_none(value):
    if value == "":
        return None
    else:
        return value


def convert_to_int(value):
    if value == "":
        return None
    else:
        return int(value)


def create_list(value):
    if value == "":
        return []
    else:
        return value.split(",")


class Employee:
    def __init__(self, emp_name=None, emp_experience=None,
                 date_of_joining=None,
                 date_of_birth=None,
                 emp_age=None,
                 project_name=None,
                 emp_skills=None,
                 user_type="Employee",
                 emp_id=None
                 ):
        self.emp_id = emp_id
        self.name = emp_name
        self.experience = emp_experience
        self.date_of_joining = date_of_joining
        self.date_of_birth = date_of_birth
        self.age = emp_age
        self.project_name = project_name
        self.skills = emp_skills
        self.__user_type = user_type
        self.info_dict = {}

    def get_details(self):
        return (f'\n Employee Details '
                f'\n Employee ID :{self.emp_id} '
                f'\n Employee Name : {self.name}'
                f'\n Experiance : {self.experience}'
                f'\n Date of joining : {self.date_of_joining}'
                f'\n Date of Birth : {self.date_of_birth}'
                f'\n Age : {self.age}'
                f'\n Projects : {self.project_name}'
                f'\n Skills : {self.skills}\n')

    def set_by_emp_id(self, db, emp_id):
        temp_dict = db.read_one(emp_id)
        if not temp_dict:
            return False
        self.emp_id = emp_id
        self.name = temp_dict['name']
        self.experience = temp_dict['years_of_experience']
        self.date_of_joining = temp_dict['joining_date']
        self.date_of_birth = temp_dict['dob']
        self.age = temp_dict['age']
        self.project_name = temp_dict['project_name']
        self.skills = temp_dict['skill_set']
        self.__user_type = temp_dict['user_type']
        return True

    def get_info_dict(self):
        self.info_dict['emp_id'] = self.emp_id
        self.info_dict['user_type'] = self.__user_type
        self.info_dict['name'] = self.name
        self.info_dict['years_of_experience'] = self.experience
        self.info_dict['joining_date'] = self.date_of_joining
        self.info_dict['dob'] = self.date_of_birth
        self.info_dict['age'] = self.age
        self.info_dict['project_name'] = self.project_name
        self.info_dict['skill_set'] = self.skills
        return self.info_dict


class Database:
    def __init__(self, filename):
        self.filename = filename

    def add_emp(self, employee):
        with open(self.filename, 'r') as f:
            data = json.load(f)
        dict_len = data['employees'][-1]['emp_id']
        if dict_len is None:
            dict_len = 1
        else:
            dict_len += 1
        tempdict = {
            'emp_id': dict_len,
            'name': employee.name,
            'user_type': "Employee",
            'years_of_experience': employee.experience,
            'joining_date': employee.date_of_joining,
            'dob': employee.date_of_birth,
            'age': employee.age,
            'project_name': employee.project_name,
            'skill_set': employee.skills
        }
        data['employees'].append(tempdict)
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=3)

    def update(self, update_emp_info_dict):
        with open(self.filename, 'r') as fr:
            data = json.load(fr)
        temp_list = []
        for emp in data['employees']:
            if emp['emp_id'] == update_emp_info_dict['emp_id']:
                temp_list.append(update_emp_info_dict)
            else:
                temp_list.append(emp)
        temp_dict = {'employees': temp_list}
        with open(self.filename, 'w') as fw:
            json.dump(temp_dict, fw, indent=3)

    def read_one(self, emp_id):
        with open(self.filename, 'r') as fr:
            data = json.load(fr)
        flag = 0
        for emp in data['employees']:
            if emp['emp_id'] == emp_id:
                flag += 1
                break
        if flag == 0:
            return False
        else:
            return data['employees'][emp_id]

    def delete_emp(self, delete_emp_id):
        with open(self.filename, 'r') as fr:
            data = json.load(fr)
        temp_list = []
        for emp in data['employees']:
            if emp['emp_id'] == delete_emp_id:
                pass
            else:
                temp_list.append(emp)
        temp_dict = {'employees': temp_list}
        with open(self.filename, 'w') as fw:
            json.dump(temp_dict, fw, indent=3)

    def show_all(self):
        with open(self.filename, 'r') as fr:
            data = json.load(fr)
        all_employees = []
        for emp in data['employees']:
            if emp['user_type'] == 'admin':
                continue
            else:
                all_employees.append([emp['emp_id'], emp['name']])
        return all_employees


if __name__ == "__main__":
    localdb = Database("database.json")
    password = input("Enter Password - ")
    while password != "password":
        password = input("Enter Valid Password - ")
    print("\t\t\t Employee management system \t\t\t")
    operations = """
    Enter 1 to Add Employee 
    Enter 2 to Update Employee Information
    Enter 3 to Find an Employee Information
    Enter 4 to remove an Employee
    Enter 5 to Show all Employees
    Enter 0 to Exit
    """

    while True:
        try:
            n = int(input(operations))
        except ValueError as error:
            continue
        if n == 0:
            exit()
        elif n == 1:
            name = set_none(input("Enter Name : "))
            experience = convert_to_int(input("Enter year of Experience : "))
            doj = set_none(input("Date of Joining : "))
            dob = set_none(input("Date of birth : "))
            age = convert_to_int(input("Enter age : "))
            projects = create_list(input("Enter project names seperated by , : "))
            skills = create_list(input("Enter skills Seperated by , : "))
            emp1 = Employee(name, experience, doj, dob, age, projects, skills)
            localdb.add_emp(emp1)
            print("\n Employee Added Successfully !")
        elif n == 2:
            update_empid = int(input("Enter Employess ID which has to be updated"))
            update_emp = Employee()
            status = update_emp.set_by_emp_id(localdb, update_empid)
            if not status:
                print(f"Invalid Employee ID . Employee with {update_empid} does not exists")
                continue
            print(update_emp.get_details())
            update_emp_info_dict = update_emp.get_info_dict()
            for ele in update_emp_info_dict.keys():
                if ele in ['emp_id', 'user_type']:
                    continue
                try:
                    choice = int(input(f"Enter 1 to update {ele} OR 0 to Skip"))
                except ValueError as error:
                    choice = 0
                if choice == 1:
                    if ele in ['name', 'joining_date', 'dob']:
                        update_emp_info_dict[ele] = set_none(input(f'Enter {ele} : '))
                    elif ele in ['years_of_experience', 'age']:
                        update_emp_info_dict[ele] = convert_to_int(input(f'Enter {ele} in Numbers: '))
                    elif ele in ['project_name', 'skill_set']:
                        update_emp_info_dict[ele] = create_list(input(f'Enter {ele} seperated by , :  '))

                else:
                    continue
            localdb.update(update_emp_info_dict)
            print("\n Updated successfully \n")
        elif n == 3:
            find_empid = int(input("Enter Employess ID to get Details : "))
            find_emp = Employee()
            status1 = find_emp.set_by_emp_id(localdb, find_empid)
            if not status1:
                print(f"Invalid Employee ID . Employee with {find_empid} does not exists")
                continue
            print(find_emp.get_details())
        elif n == 4:
            delete_empid = int(input("Enter Employess ID to delete  : "))
            delete_emp = Employee()
            status2 = delete_emp.set_by_emp_id(localdb, delete_empid)
            if not status2:
                print(f"Invalid Employee ID . Employee with {delete_empid} does not exists")
                continue
            print(delete_emp.get_details())
            if int(input("Are you sure to delete , press 1 :")) == 1:
                localdb.delete_emp(delete_empid)
                print("\n Deleted Successfully !")
        elif n == 5:
            all_employees = localdb.show_all()
            print("\t\t\tAll Employees \t\t\t")
            print("\n \t\t\t Emp ID \t\t\t Name ")
            for emp in all_employees:
                print(f"\t\t\t\t {emp[0]} \t\t\t\t\t {emp[1]}")