from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import json

# Custom User Model
class User(AbstractUser):
    EMPLOYEE = 'EMPLOYEE'
    HR = 'HR'
    ADMIN = 'ADMIN'
    
    ROLE_CHOICES = [
        (EMPLOYEE, 'Employee'),
        (HR, 'HR'),
        (ADMIN, 'Admin'),
    ]
    
    userRole = models.CharField(max_length=10, choices=ROLE_CHOICES, default=EMPLOYEE)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)

    def __str__(self):
        return self.username

# Employee Model
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    address = models.TextField()  # Store JSON as string
    contact = models.CharField(max_length=15)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100)
    yearsOfExperience = models.IntegerField(default=0)
    isFresher = models.BooleanField(default=True)
    skills = models.TextField()  # Store JSON as string
    monthlySalary = models.DecimalField(max_digits=10, decimal_places=2)
    employmentDate = models.DateField(auto_now_add=True)
    
    paymentDetails = models.TextField()  # Store JSON as string
    leaveBalance = models.IntegerField(default=2)

    @property
    def yearlySalary(self):
        return self.monthlySalary * 12

    def set_address(self, address_dict):
        self.address = json.dumps(address_dict)  # Convert dict to string

    def get_address(self):
        return json.loads(self.address) if self.address else {}

    def set_skills(self, skills_list):
        self.skills = json.dumps(skills_list)

    def get_skills(self):
        return json.loads(self.skills) if self.skills else []

    def set_paymentDetails(self, payment_dict):
        self.paymentDetails = json.dumps(payment_dict)

    def get_paymentDetails(self):
        return json.loads(self.paymentDetails) if self.paymentDetails else {}

    def __str__(self):
        return self.user.username

# Attendance Model
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    inTime = models.TimeField(null=True, blank=True)
    outTime = models.TimeField(null=True, blank=True)
    isPresent = models.BooleanField(default=False)
    isAbsent = models.BooleanField(default=False)
    onLeave = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

# Leave Model
class Leave(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leaveType = models.CharField(max_length=100)
    reason = models.TextField()
    isAccepted = models.BooleanField(default=False)
    isRejected = models.BooleanField(default=False)
    reasonForRejecting = models.TextField(blank=True, null=True)

# Payroll Model
class Payroll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_salary(self):
        employee = Employee.objects.get(user=self.user)
        total_working_days = Attendance.objects.filter(user=self.user, isPresent=True).count()
        total_leave_days = Attendance.objects.filter(user=self.user, onLeave=True).count()
        return (employee.monthlySalary / 30) * (total_working_days + total_leave_days)
    
    def save(self, *args, **kwargs):
        self.salary = self.calculate_salary()
        super().save(*args, **kwargs)

# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    departmentHead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='department_head')
    
    @property
    def numberOfEmployees(self):
        return Employee.objects.filter(department=self).count()

    def __str__(self):
        return self.name

# Document Model
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    documentType = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents/')

# Attendance Report
class AttendanceReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    totalPresent = models.IntegerField()
    totalAbsent = models.IntegerField()
    totalLeave = models.IntegerField()

# Leave Report
class LeaveReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    totalLeaves = models.IntegerField()

# Payroll Report
class PayrollReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    totalSalary = models.DecimalField(max_digits=10, decimal_places=2)

# Company Holiday Calendar
class HolidayCalendar(models.Model):
    date = models.DateField()
    occasion = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.occasion} ({self.date})"
