from core_alg.base import Filefolder


def get_folder_dir_by_folder_name(folder_name):
    if folder_name == Filefolder.Type.SENSOR_I:
        files_dir = 'structure_sensor'
    elif folder_name == Filefolder.Type.IPHONE_TEN:
        files_dir = 'iphone_ten'
    elif folder_name == Filefolder.Type.UIC4:
        files_dir = 'UIC-4'
    elif folder_name == Filefolder.Type.NEW_UIC4:
        files_dir = 'New-UIC-4-r'
    elif folder_name == Filefolder.Type.UIC5_L:
        files_dir = 'UIC-5-l'
    elif folder_name == Filefolder.Type.UIC5_R:
        files_dir = 'UIC-5-r'
    elif folder_name == Filefolder.Type.UIC6_L:
        files_dir = 'UIC-6-l'
    elif folder_name == Filefolder.Type.UIC6_R:
        files_dir = 'UIC-6-r'
    elif folder_name == Filefolder.Type.NEW_UIC6_L:
        files_dir = 'New-UIC-6-l'
    elif folder_name == Filefolder.Type.NEW_UIC6_R:
        files_dir = 'New-UIC-6-r'
    elif folder_name == Filefolder.Type.UIC7_L:
        files_dir = 'UIC-7-l'
    elif folder_name == Filefolder.Type.UIC7_R:
        files_dir = 'UIC-7-r'
    elif folder_name == Filefolder.Type.UIC8_L:
        files_dir = 'UIC-8-l'
    elif folder_name == Filefolder.Type.UIC8_R:
        files_dir = 'UIC-8-r'
    elif folder_name == Filefolder.Type.UIC9_L:
        files_dir = 'UIC-9-l'
    elif folder_name == Filefolder.Type.UIC9_R:
        files_dir = 'UIC-9-r'
    elif folder_name == Filefolder.Type.UIC10_L:
        files_dir = 'UIC-10-l'
    elif folder_name == Filefolder.Type.UIC10_R:
        files_dir = 'UIC-10-r'
    else:
        files_dir = ''

    return files_dir
