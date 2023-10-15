
import os
import shutil


def normalize(name):
    char_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k', 'л': 'l',
        'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh',
        'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ь': '',
        'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D',
        'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z', 'И': 'I',
        'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K', 'Л': 'L',
        'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
        'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh',
        'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ь': '',
        'Ю': 'Yu', 'Я': 'Ya'
    }
    
    result = ''
    for char in name:
        if char.isalnum():
            result += char
        elif char in char_map:
            result += char_map[char]
        else:
            result += '_'
    
    return result


def sort_files(directory):
   
    categories = ['images', 'videos', 'documents', 'music', 'archives', 'unknown']
    for category in categories:
        os.makedirs(os.path.join(directory, category), exist_ok=True)
    
    known_extensions = {
        'images': {'jpeg', 'png', 'jpg', 'svg'},
        'videos': {'avi', 'mp4', 'mov', 'mkv'},
        'documents': {'doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'},
        'music': {'mp3', 'ogg', 'wav', 'amr'},
        'archives': {'zip', 'gz', 'tar'}
    }
    
    
    for root, _, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            file_extension = filename.split('_')[-1].lower()
        
            normalized_name = normalize(filename)
            
            category = 'unknown'
            for cat, extensions in known_extensions.items():
                if file_extension in extensions:
                    category = cat
                    break
            
        
            if category == 'archives':
                archive_folder = os.path.join(directory, 'archives', normalized_name)
                os.makedirs(archive_folder, exist_ok=True)
                shutil.unpack_archive(file_path, archive_folder)
            else:
                
                new_file_path = os.path.join(directory, category, normalized_name)
                shutil.move(file_path, new_file_path)
    
  
    for root, dirs, _ in os.walk(directory, topdown=False):
        for directory in dirs:
            folder_path = os.path.join(root, directory)
            if not os.listdir(folder_path):
                os.rmdir(folder_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sort.py <directory>")
        sys.exit(1)

    target_directory = sys.argv[1]
    sort_files(target_directory)
