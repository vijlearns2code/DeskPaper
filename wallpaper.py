from pathlib import Path
from pywal import wallpaper
from wallpaperChanger import settings


def set_wallpaper(file: Path):
    """Change wallpaperChanger to the provided file.

    :raises FileNotFoundError: if the provided file does not exist.
    """
    if not file.exists() or not file.is_file():
        raise FileNotFoundError(f"'{file}' was not found.")

    if settings.ISWINDOWS:
        import ctypes
        ctypes.windll.user32.SystemParametersInfoW(20, 0, str(file), 3)
    else:
        wallpaper.change(str(file))