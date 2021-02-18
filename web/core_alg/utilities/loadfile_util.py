
from core_alg.base import Bone
from core_alg.base import Device


def get_device_dir_by_folder_name(device):
    if device == Device.Type.SENSOR_I:
        device_dir = 'structure_sensor'
    elif device == Device.Type.IPHONE_TEN:
        device_dir = 'iphone_ten'
    elif device == Device.Type.CR1:
        device_dir = 'CR-1-l-fem'
    elif device == Device.Type.CR2:
        device_dir = 'CR-2-r-tib'
    elif device == Device.Type.CR3:
        device_dir = 'CR-3-r-hum'
    elif device == Device.Type.CR4:
        device_dir = 'CR-4-r-rad'
    elif device == Device.Type.UIC4:
        device_dir = 'UIC4'
    elif device == Device.Type.UIC6_L:
        device_dir = 'UIC-6-l'
    elif device == Device.Type.UIC6_R:
        device_dir = 'UIC-6-r'
    elif device == Device.Type.UIC7_L:
        device_dir = 'UIC-7-l'
    elif device == Device.Type.UIC7_R:
        device_dir = 'UIC-7-r'
    elif device == Device.Type.UIC9_L:
        device_dir = 'UIC-9-l'
    elif device == Device.Type.UIC9_R:
        device_dir = 'UIC-9-r'
    elif device == Device.Type.UIC10_L:
        device_dir = 'UIC-10-l'
    elif device == Device.Type.UIC10_R:
        device_dir = 'UIC-10-r'
    else:
        device_dir = 'New-UIC-4-r'

    return device_dir