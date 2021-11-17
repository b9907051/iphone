import platform

def get_directory(sub_path):
    if platform.system() == "Windows":
        # Local 端
        path = f'static/data/{sub_path}'
    else:
        # AWS 端
        path = f'/home/cathaylife04/smartphone/iphone11/static/data/{sub_path}'

    return path