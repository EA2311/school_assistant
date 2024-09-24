# School Assistant

This Django project is designed to provide a platform for distance 
learning. At the moment, it is adapted specifically for the education 
of the younger grades of the school, where the distance learning process
involves students completing homework and sending photos of the 
completed work to the teacher for evaluation. It provides opportunities 
to create classes, subjects, tasks and homework for participants of the 
educational process.

---

## Technology stack

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![image](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)
![image](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
![image](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![image](https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white)

---

## Usage

### To try this project on your local machine follow the next steps:

1. Clone this repository on your local machine:

```bash
git clone https://github.com/EA2311/school_assistant.git
```

2. Navigate to the project directory:

```bash
cd school_assistant
```

3. Create and activate the virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create .env file with your own SECRET_KEY variable.


6. Start database migrations:

```bash
python manage.py migrate
```

7. Start the Django development server:

```bash
python manage.py runserver
```

8. Open your web browser and visit [http://localhost:8000](http://localhost:8000) to see the app in action.

---

## Main features

This project can have two types of users: **teacher** and **student**. Registration and authorization are available for each type of user.

The **teacher** has the following opportunities:

- **Creating classes**: Teachers can create a class by specifying a title and cover.
- **Creation of disciplines**: Teachers can create educational disciplines individually for each class.
- **Assignments**: Teachers can create assignments for subjects and attach study materials to them.
- **View**: Teachers can view the list of students in their class and their completed work.
- **Assessment**: Teachers can assess assignments submitted by students and set grades.

The **student** has the following opportunities:

- **Joining a class**: Students can join a certain class at the beginning of their studies with a special unique key that the teacher has.
- **View subjects**: Students can view the list of studied subjects.
- **Assignments and Grades**: Students can view homework assignments and see grades for completed work.
- **Completion of tasks**: Students can mark completed homework in the form of text and images.

---

### Thank you for your interest in my project!
