from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Leave)
admin.site.register(Payroll)
admin.site.register(Department)
admin.site.register(Document)
admin.site.register(HolidayCalendar)
admin.site.register(AttendanceReport)
admin.site.register(LeaveReport)
admin.site.register(PayrollReport)
