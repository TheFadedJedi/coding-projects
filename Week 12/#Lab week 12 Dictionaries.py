#Lab week 12 Dictionaries
meet_time={'CS101':'8:00 AM', 'CS102':'9:00 AM', 'CS103':'10:00 AM', 'NT110':'11:00 AM', 'CM241':'1:00 PM'}
room_num={'CS101':'3004', 'CS102':'4501', 'CS103':'6755', 'NT110':'1244', 'CM241':'1411'}
instructor_name={'CS101':'Haynes', 'CS102':'Alvarado', 'CS103':'Rich', 'NT110':'Burke', 'CM241':'Lee'}
coursenumber=input('Type your course number here:')
result=coursenumber+': '+meet_time[coursenumber]+', '+room_num[coursenumber]+', ' +instructor_name[coursenumber]
print(result)