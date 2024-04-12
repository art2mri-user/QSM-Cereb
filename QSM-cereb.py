'''
BSD 3-Clause License

Copyright (c) 2023, art2mri

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

import os
import subprocess
import tkfilebrowser
import csv
import math
import shutil
import getpass
import webbrowser
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import filedialog
from tkinter import simpledialog
from datetime import datetime
from tkinter import ttk


#############################

def get_pass():
	password = getpass.getpass('Enter the [sudo] password:')
	wrap = "sudo -S ls"
	try:
		subprocess.run(wrap, shell=True, check=True, input=password.encode(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError as e:
		print("\033[91m\033[1mIncorrect password. Please try again.\033[0m")
		password = getpass.getpass('Enter the [sudo] password:')
	try:
		subprocess.run(wrap, shell=True, check=True, input=password.encode(),stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	except subprocess.CalledProcessError as e:
		print("\033[91m\033[1mIncorrect password. Aborting Function.\033[0m")
		raise SystemExit(1)
	return password
	
#############################

def get_exit(command_a, command_b):
		exit2 = subprocess.run(command_a, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		if exit2 != 0:
			subprocess.run(command_b, shell=True, check=True)
		else:
			subprocess.run(command_a, shell=True, check=True)
			
#############################
def browse_folder_niigz():
	root = tk.Tk()
	root.withdraw()	
	
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mOUTPUT\033[0m \033[94m\033[1mFOLDER\033[0m')
	output = tkfilebrowser.askopendirnames()
	if not output:
		print('\033[91m\033[1mNo folder selected.\033[0m')
		return
	print ('\033[92m\033[1mSelected Folder:\033[0m')
	print(str(output[0]))	
	print('\033[94m\033[1mNOW SELECT THE WANTED\033[0m \033[92m\033[1m.nii.gz FILES\033[0m \033[94m\033[1mIN THE INPUT FOLDER:\033[0m')
	file_paths = filedialog.askopenfilenames(
		title="Select Files",
		filetypes=[("All Files","*.*")]
	)
	if not file_paths:
		print('\033[91m\033[1mNo dataset selected.\033[0m')
		return		
	print ('\033[92m\033[1mSelected Files:\033[0m')
	for i in file_paths:
		print(str(i))
		
	before = str(file_paths[0])	
	before = os.path.dirname(before)
	output = str(output[0])
	
	for i in file_paths:
		if '.nii.gz' not in i:
			os.system(os.path.basename(str(i))+'\033[91m\033[1m is not a .nii.gz file\033[0m')
		if '.nii.gz' in i:
			os.system('cd '+output+' && mkdir '+os.path.basename(str(i).replace(".nii.gz","")))
			os.system('cp '+before+'/'+os.path.basename(str(i))+' '+output+'/'+os.path.basename(str(i).replace(".nii.gz",""))+'/'+os.path.basename(str(i)))	
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')	
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder}.nii.gz EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING SEGMENTATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING SEGMENTATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mFOLDERS PREPARED!\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mFOLDERS PREPARED - CHECK THE WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mPREPARING FOLDERS FAILED\033[0m")
	else:	      			
		check_subfolders(str(output), str(output)+'/PrepareFoldersResults.txt')	   							
					
	
	
#############################

def browse_folder_BIDS():
	root = tk.Tk()
	root.withdraw()	
	
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mOUTPUT\033[0m \033[94m\033[1mFOLDER\033[0m')
	output = tkfilebrowser.askopendirnames()
	if not output:
		print('\033[91m\033[1mNo folder selected.\033[0m')
		return
	print ('\033[92m\033[1mSelected Folder:\033[0m')
	print(str(output[0]))	
	print('\033[94m\033[1mNOW SELECT THE BIDS\033[0m \033[92m\033[1mDATASET\033[0m \033[94m\033[1mFOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo dataset selected.\033[0m')
		return		
	print ('\033[92m\033[1mSelected Dataset:\033[0m')
	print(str(file_paths[0]))	
	before = str(file_paths[0])
	output = str(output[0])

	def process_folder(before, output):
		for root, dirs, files in os.walk(before): 
			if 'anat' in dirs:
				anat_folder = os.path.join(root, 'anat')
				for file in os.listdir(anat_folder): 				          			       
					if file.endswith('T1w.nii.gz'):
						file_name = file.replace('.nii.gz', '')
						subfolder_path = os.path.join(output, file_name)
						os.makedirs(subfolder_path, exist_ok=True)
						file_path = os.path.join(anat_folder, file)
						os.system('cp '+file_path+' '+os.path.join(subfolder_path, file))
						
  				
	process_folder(before, output)                    						
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')	
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder}.nii.gz EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING SEGMENTATION FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING SEGMENTATION FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mFOLDERS PREPARED!\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mFOLDERS PREPARED - CHECK THE WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mPREPARING FOLDERS FAILED\033[0m")
	else:	      			
		check_subfolders(str(output), str(output)+'/PrepareFoldersResults.txt')	   			
  
                         

#############################  

def docker():

	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)	
		
	progress_window = tk.Toplevel()
	progress_window.title("Automated Labeling Progress")

	progress_label = tk.Label(progress_window, text="Labeling...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()
		
	exit_code = os.system("docker --version")
	if exit_code != 0:
    		print('\033[91m\033[1mDOCKER NOT INSTALLED. Please install Docker before running this script.\033[0m')
    		raise SystemExit(1)
    		
	password = None		
		
	comando1='sudo -S docker stop qsm_cereb'
	comando2='sudo -S docker rm qsm_cereb'

	exit_code1 = subprocess.run('docker ps', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code1 != 0:
		if password == None:
			password = get_pass()	
		result = subprocess.check_output("sudo -S docker ps", shell=True, text=True, input=password)
		if 'qsm_cereb' in result:
			subprocess.run(comando1, shell=True, check=True, input=password.encode('utf-8'))
			subprocess.run(comando2, shell=True, check=True, input=password.encode('utf-8'))
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'qsm_cereb' in result:
			os.system('docker stop qsm_cereb')
			os.system('docker rm qsm_cereb')
		
	exit_code2 = subprocess.run('docker ps -a', stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit_code2 != 0:
		if password == None:
			password = get_pass()
		result = subprocess.check_output("sudo -S docker ps -a", shell=True, text=True, input=password)
		if 'qsm_cereb' in result:
			subprocess.run(comando2, shell=True, check=True, input=password.encode('utf-8'))
	else:
		result = subprocess.check_output("docker ps", shell=True, text=True)
		result = str(result)
		if 'qsm_cereb' in result:
			os.system('docker rm qsm_cereb')																	
	try:
    		subprocess.run('nvidia-smi', check=True)
    		docker_command = 'docker run -itd --gpus all --ipc=host --name qsm_cereb art2mri/qsm_cereb:1.0'
	except FileNotFoundError as gpu_error:
    		print(f"Error checking for GPU: {gpu_error}")
    		docker_command = 'docker run -itd --ipc=host --name qsm_cereb art2mri/qsm_cereb:1.0'
	except subprocess.CalledProcessError as gpu_error:
    		print(f"Error checking for GPU: {gpu_error}")
    		docker_command = 'docker run -itd --ipc=host --name qsm_cereb art2mri/qsm_cereb:1.0'	
	try:
    		subprocess.run(docker_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	except subprocess.CalledProcessError as docker_error:
		if password == None:
			password = get_pass()
		subprocess.run('sudo -S '+docker_command2, shell=True, check=True, input=password.encode('utf-8'))	
		print(f"Error running Docker command: {docker_error}")
    		   		    			
	loww1='docker run -itd --gpus all --ipc=host --name qsm_cereb art2mri/qsm_cereb:1.0'
	loww2='sudo -S docker run -itd --gpus all --ipc=host --name qsm_cereb art2mri/qsm_cereb:1.0'
	try:
		subprocess.run(loww1, shell=True, check=True, stderr=subprocess.DEVNULL)
	except subprocess.CalledProcessError as e:
			if password == None:
				password = get_pass()
			subprocess.run(loww2, shell=True, check=True, input=password.encode('utf-8'))
							
	for idx,i in enumerate(file_paths):
		update_progress_bar(idx + 1, len(file_paths))
		command53='docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz qsm_cereb:/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		command54='sudo -S docker cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz qsm_cereb:/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		try:
			subprocess.run(command53, shell=True, check=True, stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError as e:
			if password == None:
				password = get_pass()
			subprocess.run(command54, shell=True, check=True, input=password.encode('utf-8'))
		command55='docker start qsm_cereb'
		command56='sudo -S docker start qsm_cereb'
		try:
			subprocess.run(command55, shell=True, check=True, stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError as e:
			if password == None:
				password = get_pass()
			subprocess.run(command56, shell=True, check=True, input=password.encode('utf-8'))					
		comando_11 = 'docker exec -it qsm_cereb python3 /home/scripts/cuda.py'
		comando_12 = 'sudo -S docker exec -it qsm_cereb python3 /home/scripts/cuda.py'
		comando_2 = 'sudo docker exec -it qsm_cereb python3 /home/scripts/cpu.py'
		command_1 = 'sudo docker exec -it qsm_cereb python3 /home/scripts/cuda.py'
		file_to_check = '/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'
		command_21 = 'docker exec -it qsm_cereb python3 /home/scripts/cpu.py'
		command_22 = 'sudo -S docker exec -it qsm_cereb python3 /home/scripts/cpu.py'
		exit16 = subprocess.run(comando_11, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		if exit16 != 0:
			os.system('sudo docker exec -it qsm_cereb python3 /home/scripts/cuda.py')
		else:
			os.system('docker exec -it qsm_cereb python3 /home/scripts/cuda.py')	
				
		check_file_command1 = f'docker exec -it qsm_cereb test -f {file_to_check} && echo "found" || echo "not found"'	      				
		check_file_command2 = f'sudo -S docker exec -it qsm_cereb test -f {file_to_check} && echo "found" || echo "not found"'
		exit15 = subprocess.run(check_file_command1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
		if exit15 != 0:
			check_file_command = check_file_command2
		else:
			check_file_command = check_file_command1
			
		check_result = subprocess.run(check_file_command, shell=True, stdout=subprocess.PIPE, text=True)
		if "not found" in check_result.stdout:
			print("\033[93mTried to predict on GPU, but your GPU is not able to work on this task. Please check your CUDA settings\033[0m")
			print('\033[95m\033[1mNow trying to perform on CPU, this may take much more time to finish\033[0m')
			exit16 = subprocess.run(command_21, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
			if exit16 != 0:
				os.system('sudo docker exec -it qsm_cereb python3 /home/scripts/cpu.py')
			else:
				os.system('docker exec -it qsm_cereb python3 /home/scripts/cpu.py')
		command555='docker exec -it qsm_cereb chmod -R 777 /home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'
		command666='sudo docker exec -it qsm_cereb chmod -R 777 /home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'
		get_exit(command555, command666)
		command515='docker cp qsm_cereb:/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'+' '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		command616='sudo docker cp qsm_cereb:/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'+' '+str(i)+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz'
		get_exit(command515, command616)
		command575='docker exec -it qsm_cereb rm -f /home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		command676='sudo docker exec -it qsm_cereb rm -f /home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		get_exit(command575, command676)			
	command63='docker stop qsm_cereb'
	command64='sudo -S docker stop qsm_cereb'
	exit19 = subprocess.run(command63, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit19 != 0:
		if password == None:
			password = get_pass()
		subprocess.run(command64, shell=True, check=True, input=password.encode('utf-8'))
	else:
		os.system(command63)
	command65='docker rm qsm_cereb'
	command66='sudo -S docker rm qsm_cereb'
	exit20 = subprocess.run(command65, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
	if exit20 != 0:
		if password == None:
			password = get_pass()
		subprocess.run(command66, shell=True, check=True, input=password.encode('utf-8'))
	else:
		os.system(command65)
	progress_label.config(text="AUTOMATED LABELING FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_seg_labeled.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING LABELED FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING LABELED FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mAUTOMATED LABELING FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mAUTOMATED LABELING FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mSEGMENTATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/AutomatedLabelingResults.txt')
	#pass		
	
#############################

def singularity():
	print('\033[94m\033[1mPLEASE SELECT THE\033[0m \033[92m\033[1mQSM-Cereb\033[0m \033[94m\033[1mFOLDER\033[0m')
	enigma_folder = tkfilebrowser.askopendirname()
	print('The \033[92m\033[1mQSM-Cereb\033[0m folder selected is located at: '+enigma_folder)
	
	print('\033[94m\033[1mPLEASE SELECT THE DESIRED\033[0m \033[92m\033[1mSUBFOLDERS\033[0m \033[94m\033[1mFROM THE PREPARED FOLDER:\033[0m')
	file_paths = tkfilebrowser.askopendirnames()
	if not file_paths:
		print('\033[91m\033[1mNo folders selected.\033[0m')
		return
		
	print ('\033[92m\033[1mSelected folders:\033[0m')
	for file_path in file_paths:
		print(file_path)
		
	before = str(file_paths[0])
	before = os.path.dirname(before)
		
	progress_window = tk.Toplevel()
	progress_window.title("Automated Labeling Progress")

	progress_label = tk.Label(progress_window, text="Labeling...")
	progress_label.pack()

	progress_bar = ttk.Progressbar(progress_window, length=300, mode="determinate")
	progress_bar.pack()

	progress_text = tk.Label(progress_window, text="")
	progress_text.pack()
	
	def update_progress_bar(current, total):
		progress_percent = int((current / total) * 99)
		progress_bar["value"] = progress_percent
		progress_text["text"] = f"{progress_percent}% done"
		progress_window.update()

	exit_code = os.system("singularity --version")
	exity_code = os.system("apptainer --version")
	if exit_code and exity_code != 0:
    		print('\033[91m\033[1mSINGULARITY AND APPTAINER NOT INSTALLED. Please install one of them before running this script.\033[0m')
    		raise SystemExit(1)		
	password = None
	
	k = os.listdir(enigma_folder+'/qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/')
	for i in k:
		if os.path.isdir(enigma_folder+'/qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+str(i)):
			shutil.rmtree(enigma_folder+'/qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+str(i))
		else:
			os.remove(enigma_folder+'/qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+str(i))	
	path = enigma_folder+'/qsm_cereb.simg/home'
	dir_list = os.listdir(path)		
	for i in dir_list:
		if 'SCT' not in i:
			if 'datav2' not in i:
				if 'scripts' not in i:
					command21='rm -rf '+path+'/'+str(i)
					command22='sudo -S rm -rf '+path+'/'+str(i)
					exit2 = subprocess.run(command21, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
					if exit2 != 0:
						if password == None:
							password = get_pass()
						subprocess.run(command22, shell=True, check=True, input=password.encode('utf-8'))
					else:
						os.system(command21)
					
	for idx,i in enumerate(file_paths):
		if any(arq.endswith('.nii.gz') for arq in os.listdir('qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/')):
			command219='rm qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/*nii.gz'
			command222='sudo -S rm qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/*nii.gz'
			exit238 = subprocess.run(command219, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
			if exit238 != 0:
				if password == None:
					password = get_pass()
				subprocess.run(command222, shell=True, check=True, input=password.encode('utf-8'))
			else:
				os.system(command219)	
		update_progress_bar(idx + 1, len(file_paths))
		command67='cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder
		command68='sudo cp '+str(i)+'/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder
		get_exit(command67, command68)
		command69='chmod -R 777 '+enigma_folder+'/'+os.path.basename(str(i))+'.nii.gz'
		command70='sudo chmod -R 777 '+enigma_folder+'/'+os.path.basename(str(i))+'.nii.gz'
		get_exit(command69, command70)
		try:
			os.system('mv '+os.path.basename(str(i))+'.nii.gz '+'qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz')
		except subprocess.CalledProcessError as e:
			os.system('sudo mv '+os.path.basename(str(i))+'.nii.gz '+'qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz')	
		command73='chmod -R 777 qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		command74='sudo chmod -R 777 qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/'+os.path.basename(str(i))+'_0000.nii.gz'
		get_exit(command73, command74)
		try:
			subprocess.run(["singularity --version"], check=True, shell=True)
			command_1 = 'singularity exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cuda.py'
			command_12 = 'sudo singularity exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cuda.py'
			command_2 = 'singularity exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cpu.py'
			command_22= 'sudo singularity exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cpu.py'
			exit333 = subprocess.run(command_1, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
			if exit333 != 0:
				command111 = command_12
			else:
				command111 = command_1
			try:
        			subprocess.check_call(command111, shell=True, stderr=subprocess.DEVNULL)	
			except subprocess.CalledProcessError as e:
				pass  
			dire = 'qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'
			file1 = os.path.basename(str(i))+'.nii.gz'
			way = os.path.join(dire, file1)	     				
			if os.path.exists(way):
				print('OK')
			else:	
				print("\033[93mTried to predict on GPU, but your GPU is not able to work on this task. Please check your CUDA settings\033[0m")
				print('\033[95m\033[1mNow trying to perform on CPU, this may take much more time to finish\033[0m')
				exit339 = subprocess.run(command_2, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
				if exit339 != 0:
					command211 = command_22
				else:
					command211 = command_2
				subprocess.run(command211, shell=True)
		except subprocess.CalledProcessError:
			command_11 = 'apptainer exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cuda.py'
			command_11_1 = 'sudo apptainer exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cuda.py'
			command_22 = 'apptainer exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cpu.py'
			command_22_2 = 'sudo apptainer exec --writable --nv qsm_cereb.simg/ python3 /home/scripts/cpu.py'
			exit3333 = subprocess.run(command_11, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
			if exit3333 != 0:
				command1111 = command_11_1
			else:
				command1111 = command_11
			try:
        			subprocess.check_call(command1111, shell=True, stderr=subprocess.DEVNULL)	
			except subprocess.CalledProcessError as e:
				pass  
			dire = 'qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'
			file1 = os.path.basename(str(i))+'.nii.gz'
			way = os.path.join(dire, file1)	     				
			if os.path.exists(way):
				print('OK')
			else:	
				print("\033[93mTried to predict on GPU, but your GPU is not able to work on this task. Please check your CUDA settings\033[0m")
				print('\033[95m\033[1mNow trying to perform on CPU, this may take much more time to finish\033[0m')
				exit338 = subprocess.run(command_22, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
				if exit338 != 0:
					command221 = command_22_2
				else:
					command221 = command_22
				subprocess.run(command_221, shell=True)
		command75='chmod -R 777 qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'
		command76='sudo chmod -R 777 qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz'			
		get_exit(command75, command76)
		os.system('mv -v '+enigma_folder+'/qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'.nii.gz '+enigma_folder+'/qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'_seg_labeled.nii.gz')
		try:
			os.system('rm qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/*nii.gz')
		except subprocess.CalledProcessError as e:
			os.system('sudo rm qsm_cereb.simg/home/datav2/nnUNet_raw/Dataset530_QSM-DN_128-96-96/imagesTs/*nii.gz')
		try:
			os.system('mv '+enigma_folder+'/'+'qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+enigma_folder)
		except subprocess.CalledProcessError as e:
			os.system('sudo mv '+enigma_folder+'/'+'qsm_cereb.simg/home/datav2/inference/530_QSM/preds/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+enigma_folder)			
		try:
			os.system('mv '+enigma_folder+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+str(i))
		except subprocess.CalledProcessError as e:
			os.system('sudo mv '+enigma_folder+'/'+os.path.basename(str(i))+'_seg_labeled.nii.gz '+str(i))
	progress_label.config(text="AUTOMATED LABELING FINISHED!")
	progress_window.update()
	progress_window.after(4000, progress_window.destroy)
	print('\n')
	print('\033[92m\033[1mRESULTS:\033[0m')
	print('\n')
	def check_subfolders(directory, output_file_path):
		all_responses_are_one = True
		with open(output_file_path, 'w') as output_file:
			for subfolder in os.listdir(directory):
				subfolder_path = os.path.join(directory, subfolder)
				if os.path.isdir(subfolder_path):
					files = os.listdir(subfolder_path)
					if any('_seg_labeled.nii.gz' in file for file in files):
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[92m\033[1mOK\033[0m")
						output_file.write(f"{subfolder}.nii.gz OK" + '\n')						
					elif not os.listdir(subfolder_path):
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}\033[0m \033[93m\033[1mEMPTY FOLDER\033[0m")
						output_file.write(f"{subfolder} EMPTY FOLDER" + '\n')						
					else:
						all_responses_are_one = False
						print(f"\033[94m\033[1m{subfolder}.nii.gz\033[0m \033[91m\033[1mFAILED (MISSING LABELED FILE)\033[0m")
						output_file.write(f"{subfolder}.nii.gz FAILED (MISSING LABELED FILE)" + '\n')
                			
		if all_responses_are_one:
			print('\n')
			print("\033[92m\033[1mAUTOMATED LABELING FINISHED\033[0m")
		else:
			print('\n')
			print("\033[93m\033[1mAUTOMATED LABELING FINISHED WITH WARNINGS\033[0m")
	
	if not os.listdir(before):
		print('\n')
		print("\033[91m\033[1mSEGMENTATION FAILED\033[0m")
	else:	      			
		check_subfolders(str(before), str(before)+'/AutomatedLabelingResults.txt')	   

#############################

def open_checkbox_window():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Choose Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        automated(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated(choice):
    if choice:
        if choice == "Docker":
            docker()
        elif choice == "Singularity/Apptainer":
            singularity()
            
#############################

def open_SCT():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Choose Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        automated_SCT(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated_SCT(choice):
    if choice:
        if choice == "Docker":
            docker()
        elif choice == "Singularity/Apptainer":
            singularity() 
            
#############################

def open_browse():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Select File Format")

    def on_checkbox_click():
        choice = ".nii.gz" if container_choice.get() == ".nii.gz" else "BIDS"
        checkbox_window.destroy()
        automated_browse(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text=".nii.gz", variable=container_choice, value=".nii.gz")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="BIDS", variable=container_choice, value="BIDS")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated_browse(choice):
    if choice:
        if choice == ".nii.gz":
            browse_folder_niigz()
        elif choice == "BIDS":
            browse_folder_BIDS() 
            
#############################

def open_reg():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Select Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        automated_reg(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def automated_reg(choice):
    if choice:
        if choice == "Docker":
            reg_aut_docker()
        elif choice == "Singularity/Apptainer":
            reg_aut_singularity() 
            
#############################

def open_ext():
    checkbox_window = tk.Toplevel(root)
    checkbox_window.title("Select Platform")

    def on_checkbox_click():
        choice = "Docker" if container_choice.get() == "Docker" else "Singularity/Apptainer"
        checkbox_window.destroy()
        container_ext(choice)

    container_choice = tk.StringVar()

    checkbox_frame = tk.Frame(checkbox_window)
    checkbox_frame.pack(side="top", pady=(10, 0))

    docker_button = tk.Radiobutton(checkbox_frame, text="Docker", variable=container_choice, value="Docker")
    docker_button.pack(side="left", padx=(0, 10))

    singularity_button = tk.Radiobutton(checkbox_frame, text="Singularity/Apptainer", variable=container_choice, value="Singularity/Apptainer")
    singularity_button.pack(side="left")

    ok_button = tk.Button(checkbox_window, text="OK", command=on_checkbox_click)
    ok_button.pack(side="top", pady=(10, 0))

    button_x, button_y, _, _ = ok_button.bbox("insert")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x_position = root.winfo_x() + button_x
    y_position = root.winfo_y() + button_y

    checkbox_window.geometry(f"300x85+{x_position}+{y_position}")

def container_ext(choice):
    if choice:
        if choice == "Docker":
            ext_docker()
        elif choice == "Singularity/Apptainer":
            ext_singularity()                                               
            
#############################

def open_tutorial():
    url = "https://github.com/art2mri/Enigma-SC" 
    webbrowser.open_new(url)
    
#############################	

root = tk.Tk()
root.title("QSM-cereb")

window_width = 520
window_height = 450
root.geometry(f"{window_width}x{window_height}")
root.configure(bg='gray')

image_path = "files/brain.png"  
img = Image.open(image_path)

img = img.resize((200, 200))

img = ImageTk.PhotoImage(img)

title_label = tk.Label(root, text="QSM Cerebellum Segmentation", bg='gray', font=("Helvetica", 20, "bold"))
title_label.pack(pady=10)

subtitle_label = tk.Label(root, text="QSM Cereb", bg='gray', font=("Helvetica", 16))
subtitle_label.pack(pady=5)

image_label = tk.Label(root, image=img, bg='gray')
image_label.pack()

images_path_button = tk.Button(root, text="Prepare Folders", height=2, width=20, command=open_browse, highlightbackground="black", highlightthickness=2)
spinal_cord_segmentation_button = tk.Button(root, text="Segmentation", height=2, width=20, command=open_SCT, highlightbackground="black", highlightthickness=2)

images_path_button.pack(pady=10)
spinal_cord_segmentation_button.pack(pady=10)

button_frame = tk.Frame(root, bg='gray')
button_frame.pack(pady=10)

container_choice = tk.StringVar()
container_choice.set("")

version_label = tk.Label(root, text="Version 1.0", bg='gray', font=("Helvetica", 11, "bold"))
version_label.place(relx=1.0, rely=1.0, anchor='se', bordermode='outside', x=-10, y=-10)

tutorial_button = tk.Button(root, text="Tutorial", height=1, width=5, highlightbackground="black", highlightthickness=2, command=open_tutorial)
tutorial_button.place(relx=0.0, rely=1.0, anchor='sw', bordermode='outside', x=10, y=-10)

button_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
