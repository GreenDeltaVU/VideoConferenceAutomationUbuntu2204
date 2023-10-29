import subprocess
import time
import pyautogui
import sys
import shlex
import pandas as pd
import psutil

import threading


def get_element_pid_with_highest_resource_usage():
    element_processes = []

    # Iterate through all running processes
    for process in psutil.process_iter(attrs=["pid", "name", "memory_percent"]):
        if (
            "element-desktop" in process.info["name"].lower()
        ):  # Check if process name contains "element"
            element_processes.append(process)

    if not element_processes:
        return None
    # Find the element process with the highest CPU usage
    highest_cpu_usage_process = max(
        element_processes, key=lambda process: process.info["memory_percent"]
    )

    return highest_cpu_usage_process.info["pid"]


def send_a_message_element(message):
    global measurement_running
    time.sleep(5)
    print("going to click chat")
    # Click on contact to talk
    pyautogui.click(x=303, y=225)  # Replace with the actual coordinates
    print("chat-clicked")

    time.sleep(2)
    # Click here to write the message
    pyautogui.click(x=606, y=1055)  # Replace with the actual coordinates

    time.sleep(2)
    # Type your message (optional)
    pyautogui.typewrite(message)

    time.sleep(3)
    # #click here to send message
    # pyautogui.click(x=200, y=200)  # Replace with the actual coordinates

    # # Attach the file (click the "Attach" button and choose a file)
    # pyautogui.click(x=300, y=300)  # Replace with the actual coordinates for the "Attach" button
    # time.sleep(2)  # Wait for the file dialog to open
    # pyautogui.write('/path/to/your/file')  # Replace with the actual file path
    # pyautogui.press('enter')

    # Send the message
    pyautogui.press("enter")

    time.sleep(2)
    measurement_running = False

def send_an_image_element():
    global measurement_running
    time.sleep(5)
    print("going to click chat")
    # Click on the chat PERSON
    pyautogui.click(x=303, y=225)  # Replace with the actual coordinates
    print("chat-clicked")

    time.sleep(2)
    # Click here to attach
    pyautogui.click(x=1506, y=1046)  # Replace with the actual coordinates

    time.sleep(2)
    # Click here to select pictures folder
    pyautogui.click(x=614, y=657)  # Replace with the actual coordinates

    time.sleep(3)
    # select image
    pyautogui.click(x=805, y=496)  # Replace with the actual coordinates

    time.sleep(3)
    #
    pyautogui.press("enter")

    time.sleep(2)
    pyautogui.press("enter")

    time.sleep(8)

    # Signal the measurement thread to stop
    measurement_running = False


def send_a_pdf_element():
    global measurement_running
    time.sleep(5)
    print("going to click chat")
    # Click on the chat PERSON
    pyautogui.click(x=303, y=225)  # Replace with the actual coordinates
    print("chat-clicked")

    time.sleep(2)
    # Click here to attach
    pyautogui.click(x=1506, y=1046) # Replace with the actual coordinates

    time.sleep(2)
    # Click here to select pictures folder
    pyautogui.click(x=614, y=657)  # Replace with the actual coordinates

    time.sleep(3)
    # select pdf
    pyautogui.click(x=805, y=517)  # Replace with the actual coordinates

    time.sleep(3)
    #
    pyautogui.press("enter")

    time.sleep(2)
    pyautogui.press("enter")

    time.sleep(8)

    # Signal the measurement thread to stop
    measurement_running = False


def send_a_zip_element():
    global measurement_running
    time.sleep(5)
    print("going to click chat")
    # Click on the chat PERSON
    pyautogui.click(x=303, y=225)  # Replace with the actual coordinates
    print("chat-clicked")

    time.sleep(2)
    # Click here to attach
    pyautogui.click(x=1506, y=1046) # Replace with the actual coordinates

    time.sleep(2)
    # Click here to select pictures folder
    pyautogui.click(x=614, y=657)  # Replace with the actual coordinates

    time.sleep(3)
    # select zip
    pyautogui.click(x=805, y=541)  # Replace with the actual coordinates

    time.sleep(3)
    # S
    pyautogui.press("enter")

    time.sleep(2)
    pyautogui.press("enter")

    time.sleep(8)

    # Signal the measurement thread to stop
    measurement_running = False


def video_conference():
    global measurement_running
    time.sleep(5)
    print("going to click chat")
    # Click on conference call
    pyautogui.click(x=1197, y=337)  # Replace with the actual coordinates
    print("chat-clicked")
    time.sleep(3)
    #TURN OFF CAMERA
    pyautogui.click(x=658, y=382)

    time.sleep(2)
    # Click here to join meeting
    pyautogui.click(x=688, y=318) # Replace with the actual coordinates

    # Signal the measurement thread to stop
    measurement_running = False

def powerjoular_measurement_function(p_id):
    global measurement_running
    powerjoular_command = (
        f'echo " " | sudo -S -k powerjoular -l -p {p_id} -f element_image_energy.csv'
    )
    powerjoular_process = subprocess.Popen(
        powerjoular_command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print("Measurement started")

    # Monitor the shared variable to stop the measurement
    while measurement_running:
        time.sleep(1)

    # Terminate the powerjoular process
    powerjoular_process.terminate()




if __name__ == '__main__':
    lorum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit"

    for i in range(2):

        # Shared variable to signal the measurement thread to stop
        measurement_running = True

        # open element
        subprocess.Popen(["element-desktop"])
        time.sleep(3)
        # Get the element PID and start powerjoular measurement
        p_id = get_element_pid_with_highest_resource_usage()

        if p_id is not None:
            print(
                f"element meeting with the highest resource consumption is running with PID: {p_id}"
            )
            powerjoular_thread = threading.Thread(
                target=powerjoular_measurement_function, args=(p_id,)
            )
            powerjoular_thread.start()
        else:
            print("No element meeting is running.")

        # time.sleep(2)
        print(f"element process started with PID: {p_id}")
        video_conference()
        # Start sending the file
        #send_a_message_element(lorum)
        send_an_image_element()
        # send_a_zip_element()
        # send_a_pdf_element()
        # Wait for the measurement thread to finish
        #time.sleep(300)
        powerjoular_thread.join()
        
        
        pyautogui.click(x=1749, y=8)
        time.sleep(2)
        pyautogui.click(x=1707, y=99)
        #subprocess.Popen(["pkill","-f", "element-desktop"])
        time.sleep(4)