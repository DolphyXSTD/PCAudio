import psutil

def command(app):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app:
            try:
                proc.terminate()  # Sends a SIGTERM signal (graceful termination)
                print(f"Terminated process: {proc.info['name']} (PID: {proc.info['pid']})")
            except psutil.NoSuchProcess:
                print(f"Process {proc.info['name']} (PID: {proc.info['pid']}) no longer exists.")
            except psutil.AccessDenied:
                print(f"Access denied to terminate process {proc.info['name']} (PID: {proc.info['pid']}).")
