import os
import shutil
import sys
import unicodedata
from pathlib import Path
import zipfile
import tarfile
import gzip

IMAGE_EXTENSIONS = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO_EXTENSIONS = ('AVI', 'MP4', 'MOV', 'MKV')
DOCUMENT_EXTENSIONS = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO_EXTENSIONS = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE_EXTENSIONS = ('ZIP', 'GZ', 'TAR')

def normalize(text):
    normalized_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZабвгдеєжзиіїйклмнопрстуфхцчшщьюяАБВГДЕЄЖЗИІЇЙКЛМНОПРСТЮУФХЦЧШЩЬЮЯАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789.-_')
    normalized_text = ''.join(c if c in allowed_chars else '_' for c in normalized_text)
    return normalized_text

def extract_archive(archive_path, destination_folder):
    archive_path = Path(archive_path)
    destination_folder = Path(destination_folder)
    
    if archive_path.suffix == '.zip':
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination_folder)
    elif archive_path.suffix == '.tar':
        with tarfile.open(archive_path, 'r') as tar_ref:
            tar_ref.extractall(destination_folder)
    elif archive_path.suffix == '.gz':
        with gzip.open(archive_path, 'rb') as gz_ref:
            with tarfile.open(fileobj=gz_ref, mode='r') as tar_ref:
                tar_ref.extractall(destination_folder)
    else:
        print(f"Unsupported archive format: {archive_path.suffix}")

def process_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        
        if os.path.isfile(item_path):
            file_extension = item.split('.')[-1].upper()
            normalized_name = normalize(item.split('.')[0])
            new_name = f"{normalized_name}.{file_extension}"
            
            if file_extension in IMAGE_EXTENSIONS:
                destination_folder = 'images'
            elif file_extension in VIDEO_EXTENSIONS:
                destination_folder = 'video'
            elif file_extension in DOCUMENT_EXTENSIONS:
                destination_folder = 'documents'
            elif file_extension in AUDIO_EXTENSIONS:
                destination_folder = 'audio'
            elif file_extension in ARCHIVE_EXTENSIONS:
                destination_folder = 'archives'
                archive_folder = os.path.join(folder_path, 'archives', normalized_name)
                os.makedirs(archive_folder, exist_ok=True)
                extract_archive(item_path, archive_folder)
                continue
            else:
                destination_folder = 'unknown'
                new_name = item  
            
            destination_path = os.path.join(folder_path, destination_folder, new_name)
            os.makedirs(os.path.dirname(destination_path), exist_ok=True)
            shutil.move(item_path, destination_path)
        
        elif os.path.isdir(item_path) and item not in ('archives', 'video', 'audio', 'documents', 'images'):
            process_folder(item_path)
            if not os.listdir(item_path):
                os.rmdir(item_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sort.py folder_path")
    else:
        target_folder = sys.argv[1]
        process_folder(target_folder)

