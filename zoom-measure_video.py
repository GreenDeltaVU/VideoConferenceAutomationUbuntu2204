import subprocess
import time
import sys
import shlex
import pandas as pd
import psutil
import pyautogui

def get_zoom_pid_with_highest_resource_usage():
	zoom_processes = []
	
	# Iterate through all running processes
	for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
		if "zoom" in process.info['name'].lower():  # Check if process name contains "zoom"
			zoom_processes.append(process)
	
	if not zoom_processes:
		return None
	# Find the Zoom process with the highest CPU usage
	highest_cpu_usage_process = max(zoom_processes, key=lambda process: process.info['memory_percent'])
	
	return highest_cpu_usage_process.info['pid']


def start_zoom_meeting(meeting_id, passcode):
	# Construct the Zoom meeting URL
	zoom_cmd = f"zoommtg://zoom.us/join?action=join&confno={meeting_id}"

	# Use Popen to start Zoom and capture the process information
	zoom_process = subprocess.Popen(["xdg-open", zoom_cmd])

	# Sleep for a short duration to ensure Zoom has started
	time.sleep(5)  # Wait for the Zoom window to open

	
	# Simulate keyboard input to enter the passcode
	subprocess.run(["xdotool", "type", passcode])
	print('passcode')
	subprocess.run(["xdotool", "key", "Return"])
	print('returnkey')
	


	try:
		zoom_process.wait()
		#print('test')
		time.sleep(20)  # Wait for the Zoom window to open

		
		# Get the PID of the Zoom process
		#zoom_pid = zoom_process.pid
		zoom_pid = get_zoom_pid_with_highest_resource_usage()

		if zoom_pid is not None:
			print(f"Zoom meeting with the highest resource consumption is running with PID: {zoom_pid}")
		else:
			print("No Zoom meeting is running.")
		time.sleep(2)
		pyautogui.click(x=534, y=922) 
		time.sleep(2)
		print(f"Zoom process started with PID: {zoom_pid}")
	
        #number of experiment iterations 
		for i in range(2):
			try:
				#powerjoular_command = f'echo " " | sudo -S -k powerjoular -l -p {zoom_pid} -f zoom_energy.csv'
				powerjoular_command = f'echo " " | sudo -S -k timeout 10 powerjoular -l -p {zoom_pid} -f zoom_energy.csv'
				powerjoular_process = subprocess.run(powerjoular_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
			except subprocess.CalledProcessError as e:
				# PowerJoular is force kill due to timeout - Calculation finish
				print("Finish measurement")
			except e:
				print(f"Subprocess returned a non-zero exit status: {e.returncode}")

			print("------")
			print(zoom_pid)
			
			time.sleep(2)
			#if its in the last iteration
			if i == 1:
				print("last zoom")
				subprocess.Popen(["pkill", "zoom"])
				time.sleep(2)
			
	except KeyboardInterrupt:
		print("Measurement interrupted.")

if __name__ == "__main__":
    
	if len(sys.argv) != 3:
		print("Usage: python zoom_meeting.py MEETING_ID PASSCODE")
	else:
		meeting_id = sys.argv[1]
		passcode = sys.argv[2]
		start_zoom_meeting(meeting_id, passcode)



