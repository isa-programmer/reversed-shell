import subprocess
import platform
import os


class Screenshot:
    def __init__(self):
        self.system = platform.system().lower()

    def X11Screenshot(self,path):
        resp = subprocess.run(["scrot",path],text=True,capture_output=True)
        return resp.returncode == 0

    def WindowsScreenshot(self,path):
        screenShotScript = f'''
        Add-Type -AssemblyName System.Windows.Forms
        Add-Type -AssemblyName System.Drawing
        
        $bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
        $bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
        $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
        $graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
        $bitmap.Save("{path}", [System.Drawing.Imaging.ImageFormat]::Png)
        $graphics.Dispose()
        $bitmap.Dispose() '''
        resp = subprocess.run(["powershell","-c",screenShotScript],text=True,capture_output=True)
        return resp.returncode == 0

    def MacScreenshot(self,path):
        resp = subprocess.run(["screencapture",path],text=True,capture_output=True)
        return resp.returncode == 0


    def WaylandScreenshot(self,path):
        for scshot in ["gnome-screenshot","spectacle","grim"]:
            if subprocess.run(["which",scshot]).returncode == 0:
                if scshot == "gnome-screenshot":
                    resp = subprocess.run(["gnome-screenshot","-f",path],text=True,capture_output=True)
                    return resp.returncode == 0
                elif scshot == "spectacle":
                    resp = subprocess.run(["spectacle","-n","-f",path],text=True,capture_output=True)
                    return resp.returncode == 0
                elif scshot == "grim":
                    resp = subprocess.run(["grim",path],text=True,capture_output=True)
                    return resp.returncode == 0
                else:
                    return False
        return False

    def screenshot(self,path):
        if self.system == "windows":
            return self.WindowsScreenshot(path)
        
        elif self.system == "linux":
            if os.getenv('XDG_SESSION_TYPE') == "wayland":
                return self.WaylandScreenshot(path)
            return self.X11Screenshot(path)
        
        elif self.system == "darwin":
            return self.MacScreenshot(path)
        
        else:
            raise Exception(f'Undefined Platform {self.system}')
