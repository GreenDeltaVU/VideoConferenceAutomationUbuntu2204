import subprocess
import time
import sys
import shlex
import pandas as pd
import psutil
import pyautogui
def get_rocketchat_pid_with_highest_resource_usage(app_name):
	rocketchat_processes = []
	
	# Iterate through all running processes
	for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
		if app_name in process.info['name'].lower():  # Check if process name contains "rocketchat"
			rocketchat_processes.append(process)
	
	if not rocketchat_processes:
		return None
	# Find the rocketchat process with the highest CPU usage
	highest_cpu_usage_process = max(rocketchat_processes, key=lambda process: process.info['memory_percent'])
	
	return highest_cpu_usage_process.info['pid']
	
def open_rocketchat_meeting(meeting_url):
	subprocess.Popen(["rocketchat-desktop"])
	time.sleep(3)
	subprocess.Popen(["xdg-open", meeting_url])
	time.sleep(5)
	pyautogui.click(x=246, y=667) 
	time.sleep(3)
	pyautogui.click(x=306, y=593) 
	time.sleep(3)
	# subprocess.run(["xdotool", "key", "Return"])
	print("return clicked")
	
	try:
		time.sleep(15)  # Wait for the rocketchat window to open

		rocketchat_pid = get_rocketchat_pid_with_highest_resource_usage("firefox")

		if rocketchat_pid is not None:
			print(f"rocketchat meeting with the highest resource consumption is running with PID: {rocketchat_pid}")
		else:
			print("No rocketchat meeting is running.")
			
		time.sleep(2)
		print(f"rocketchat process started with PID: {rocketchat_pid}")
		
		for i in range(2):
			try :
				#powerjoular_command = f'echo " " | sudo -S -k timeout 10 powerjoular -l -p {rocketchat_pid} -f rocketchat_energy.csv'
				powerjoular_command = f'echo " " | sudo -S -k timeout 5 powerjoular -l -p {rocketchat_pid} -f rocketchat_camera_off_energy.csv'
				powerjoular_process = subprocess.run(powerjoular_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
			except subprocess.CalledProcessError as e:
				# PowerJoular is force kill due to timeout - Calculation finish
				print("Finish measurement")
			except e:
				print(f"Subprocess returned a non-zero exit status: {e.returncode}")

			print("------")
			print(rocketchat_pid)
			
			time.sleep(2)
			if i == 1:
				print('final iteration')
				subprocess.Popen(["pkill", "firefox"])
				time.sleep(3)
				subprocess.Popen(["pkill", "rocketchat-desk"])
			# Create the CSV file
			#with open("rocketchat_energy.csv", "a") as f:
			#	f.write(powerjoular_process.stdout)
			#	# Add a new line for separation
			#	f.write("\n")
	except KeyboardInterrupt:
		print("Measurement interrupted.")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python open_rocketchat_meeting.py <meeting_url>")
	else:
		meeting_url = sys.argv[1]
		open_rocketchat_meeting(meeting_url)

