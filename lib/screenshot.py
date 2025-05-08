import subprocess
import platform
import os


def x11Screenshot(path):
    resp = subprocess.run(["scrot",path])
    return resp.returncode == 0

def windowsScreenshot(path):
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
    resp = subprocess.run(["powershell","-c",screenShotScript])
    return resp.returncode == 0

def macScreenshot(path):
    resp = subprocess.run(["screencapture",path])
    return resp.returncode == 0

def screenshot(path):
    system = platform.system().lower()

    if system == "windows":
        return windowsScreenshot(path)
    if system == "linux":
        if os.getenv('XDG_SESSION_TYPE') == "wayland":
            print("Doesn't have wayland support")
            return False
        return x11Screenshot(path)
    if system == "darwin":
        macScreenshot(path)
    else:
        raise Exception(f'Undefined Platform {system}')
