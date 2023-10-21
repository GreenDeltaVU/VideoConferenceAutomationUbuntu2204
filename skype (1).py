import subprocess
import time
import sys
import shlex
import pandas as pd
import psutil

def get_skype_pid_with_highest_resource_usage(app_name):
	skype_processes = []
	
	# Iterate through all running processes
	for process in psutil.process_iter(attrs=['pid', 'name', 'memory_percent']):
		if app_name in process.info['name'].lower():  # Check if process name contains "skype"
			skype_processes.append(process)
	
	if not skype_processes:
		return None
	# Find the skype process with the highest CPU usage
	highest_cpu_usage_process = max(skype_processes, key=lambda process: process.info['memory_percent'])
	
	return highest_cpu_usage_process.info['pid']
	
def open_skype_meeting(meeting_url):
	subprocess.Popen(["skype"])
	subprocess.Popen(["xdg-open", meeting_url])
	time.sleep(10)
	subprocess.run(["xdotool", "key", "Return"])
	print("return clicked")
	
	try:
		time.sleep(20)  # Wait for the skype window to open

		skype_pid = get_skype_pid_with_highest_resource_usage("skype")

		if skype_pid is not None:
			print(f"skype meeting with the highest resource consumption is running with PID: {skype_pid}")
		else:
			print("No skype meeting is running.")
			
		time.sleep(2)
		print(f"skype process started with PID: {skype_pid}")
		
		for i in range(10):
			try :
				#powerjoular_command = f'echo " " | sudo -S -k timeout 10 powerjoular -l -p {skype_pid} -f skype_energy.csv'
				powerjoular_command = f'echo " " | sudo -S -k timeout 10 powerjoular -l -p {skype_pid} -f skype_energy.csv'
				powerjoular_process = subprocess.run(powerjoular_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
			except subprocess.CalledProcessError as e:
				# PowerJoular is force kill due to timeout - Calculation finish
				print("Finish measurement")
			except e:
				print(f"Subprocess returned a non-zero exit status: {e.returncode}")

			print("------")
			print(skype_pid)
			
			time.sleep(2)
			# Create the CSV file
			#with open("skype_energy.csv", "a") as f:
			#	f.write(powerjoular_process.stdout)
			#	# Add a new line for separation
			#	f.write("\n")
	except KeyboardInterrupt:
		print("Measurement interrupted.")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Usage: python open_skype_meeting.py <meeting_url>")
	else:
		meeting_url = sys.argv[1]
		open_skype_meeting(meeting_url)

