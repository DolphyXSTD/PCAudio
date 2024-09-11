import psutil

def command(app):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == app:
            try:
                print(proc.info)
                proc.terminate()
                print(f"Terminated process: {proc.info['name']} (PID: {proc.info['pid']})")
            except:
                pass
