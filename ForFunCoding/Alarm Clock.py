#Alarm Clock
import time
from playsound import playsound

def set_alarm(alarm_time):
    print(f"Alarm set for {alarm_time}.")
    while True:
        current_time = time.strftime("%H:%M:%S")
        print(f"Current time: {current_time}", end="\r")
        if current_time == alarm_time:
            print("\nTime to wake up!")
            playsound('alarm_sound.mp3')  # Replace with your alarm sound file
            break
        time.sleep(1)

if __name__ == "__main__":
    alarm_time = input("Enter the alarm time in HH:MM:SS format: ")
    set_alarm(alarm_time)
