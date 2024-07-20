from smb.SMBConnection import SMBConnection

# With the current credentials we don't have access to dynamically upload data - so keeping this for future
class SMBClient:
    def __init__(self, server_name, username, password, domain, is_direct_tcp=True):
        self.server_name = server_name
        self.username = username
        self.password = password
        self.domain = domain
        self.is_direct_tcp = is_direct_tcp
        self.conn = SMBConnection(username, password, 'client', server_name, domain=domain, is_direct_tcp=is_direct_tcp)

    def connect(self):
        try:
            self.conn.connect(self.server_name, 139 if self.is_direct_tcp else 445)
            print(f"Connected to {self.server_name} successfully.")
        except Exception as e:
            print(f"Connection failed: {e}")

    def disconnect(self):
        self.conn.close()
        print("Disconnected.")

    def upload(self, local_path, remote_path):
        try:
            with open(local_path, 'rb') as local_file:
                self.conn.storeFile('service', remote_path, local_file)
            print(f"File {local_path} uploaded to {remote_path} successfully.")
        except Exception as e:
            print(f"Upload failed: {e}")

    def delete(self, remote_path):
        try:
            self.conn.deleteFiles('share', remote_path)
            print(f"File {remote_path} deleted successfully.")
        except Exception as e:
            print(f"Deletion failed: {e}")

    def delete_folder(self, remote_folder):
        try:
            items = self.conn.listPath('share', remote_folder)

            for item in items:
                if item.filename not in ['.', '..']:
                    self.conn.deleteFiles('share', f"{remote_folder}/{item.filename}")
                    print(f"Deleted: {remote_folder}/{item.filename}")

            print(f"Folder {remote_folder} deleted successfully.")
        except Exception as e:
            print(f"Deletion failed: {e}")
