from subprocess import Popen, PIPE
import subprocess
from logger_settings import logger
import os


"""Uploads the files to google drive via gdrive
Args:
    path: path of the directory or zipfile 
    
*If make_compression is False a folder will be created to contain all the files.
"""
def upload_drive(path):
    
    logger.info("Uploading to google drive")
    args = []
    if os.path.exists(path):
        if os.path.isdir(path):
            args = ['gdrive\\gdrive.exe', 'upload', '-r', path]
        else:
            args = ['gdrive\\gdrive.exe', 'upload', path]
            
    p = None
    try:
        p = Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        logger.error("Cant execute the upload process to Google Drive" + str(e))
        
    out, error = p.communicate()
    if out == 0:
        logger.error("An error occurred while uploading to google drive: " + error)
    else:
        logger.info("Your files have been uploaded successfully")


"""Saves the credentials provided by the user for the use of gdrive
*The file witch contains the credentials of gdrive will be placed in '../AppData/Roaming/.gdrive/'
"""
def get_credentials(token=None):

    args = ['gdrive\\gdrive.exe', 'about']
    p = None
    try:
        p = Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        logger.error("Cant execute the validation process of gdrive" + str(e))
    
    p.stdin.write(str(token))
    
    out, error = p.communicate()
    
    if error:
        logger.error("Not valid token")
    else:
        logger.info("Credentials saved")
       

"""Download the files from google drive to local
Args:
    file_id: id of the file / directory that we want to download
    
* If it is a directory it will be downloaded, if it is a zip file the unzip method will be called.
"""
def download_drive(file_id):
    
    args = ['gdrive\\gdrive.exe', 'download', file_id]

    p = None
    try:
        p = Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        logger.error("Cant execute the validation process of gdrive" + str(e))
    
    out, error = p.communicate()


"""Get the used space, free space and total size of the google drive account.
    
Returns: used space, free space and total size of the google drive account respectively
"""
def get_size():
    
    args = ['gdrive\\gdrive.exe', 'about']
    p = None
    try:
        p = Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    except Exception as e:
        logger.error("Cant execute the validation process of gdrive" + str(e))
    
    out, error = p.communicate()
    
    if error:
        logger.error("Cant retrive the size from Google Drive")
    else:
        logger.info("Size retrievered")
    
    # Get the relevant info from the output
    x = [item.split(': ') for item in out.split('\n')]  
    
    # Used space, free space, total space
    return x[1][1].split(' '), x[2][1].split(' '), x[3][1].split(' ')


"""This method takes care of deleting backups after a certain time or under a user-specified backup limit
Args:
    name: name of the file / directory that we want to delete
"""
def del_backup(name):
    pass