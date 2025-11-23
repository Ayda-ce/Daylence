# Imports
import os
import sys
import psutil
from PyQt5 import QtWidgets
from splash_screen import SplashScreen
from PyQt5.QtWidgets import QApplication

# Get the directory where the executable or script is located
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Running as script
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lock file path - next to the executable/script
LOCK_FILE = os.path.join(BASE_DIR, ".planner_app.lock")
# print("Saving/Loading last_info.dat from:", os.path.join(BASE_DIR, "Files", "last_info.dat"))
LAST_INFO_FILE = os.path.join(BASE_DIR, "Files", "last_info.dat")

def prevent_multiple_instances():
    if os.path.exists(LOCK_FILE):
        try:
            with open(LOCK_FILE, "r") as f:
                pid = int(f.read().strip())
            
            if psutil.pid_exists(pid):
                return False
            else:
                os.remove(LOCK_FILE)
                
        except (ValueError, Exception) as e:
            try:
                os.remove(LOCK_FILE)
            except:
                pass
    
    # Create new lock file
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
        return True
    except Exception as e:
        return True  # Continue anyway to avoid blocking

def remove_lock():
    # write_log("Attempting to remove lock file...")
    try:
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)

    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Error removing lock file: {e}")


# Main function
def main():
    app = QApplication(sys.argv)

    if not prevent_multiple_instances():
        QtWidgets.QMessageBox.warning(None, "warning", "Program is already running.")
        # sys.exit(app.exec_())
        sys.exit(1)  
    else:
        splash_screen = SplashScreen()
        splash_screen.show()
        app.aboutToQuit.connect(remove_lock)
        
    sys.exit(app.exec_())
    print("Exited cleanly.")
if __name__ == "__main__":
    main()