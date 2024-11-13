import os

def remove_null_bytes_in_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    # Open the file in binary mode, read contents, and remove null bytes
                    with open(file_path, 'rb') as f:
                        content = f.read().replace(b'\x00', b'')
                    
                    # Write the cleaned content back to the file
                    with open(file_path, 'wb') as f:
                        f.write(content)
                    
                    print(f"Cleaned null bytes from: {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

# Replace 'your_directory_path' with the path to the directory containing your Python files
remove_null_bytes_in_files('D:\Documents\Django-Projects\InvoiceManager\InvoiceManager_v5')
