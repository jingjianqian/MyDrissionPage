import os
import shutil
from datetime import datetime
from pathlib import Path


class MyFileUtil:
    def __init__(self, path):
        self._path = Path(path)

    def create_folder(self):
        try:
            self._path.mkdir(parents=True, exist_ok=True)
            print(f"成功创建文件夹 '{self._path}'")
            return True
        except FileExistsError:
            print(f"文件夹 '{self._path}' 已存在")
            return True
        except Exception as e:
            print("error:")
            print(f"创建文件夹 '{self._path}' 出错：{e}")
            return False

    def delete_folder(self):
        try:
            self._path.rmdir()
            print(f"成功删除文件夹 '{self._path}'")
        except FileNotFoundError:
            print(f"文件夹 '{self._path}' 不存在")
        except OSError as e:
            print(f"删除文件夹 '{self._path}' 出错：{e}")

    def create_file(self, filename):
        try:
            filepath = self._path / filename
            filepath.touch()
            print(f"成功创建文件 '{filepath}'")
        except Exception as e:
            print(f"创建文件 '{filename}' 出错：{e}")

    def delete_file(self, filename):
        try:
            filepath = self._path / filename
            filepath.unlink()
            print(f"成功删除文件 '{filepath}'")
        except FileNotFoundError:
            print(f"文件 '{filename}' 不存在")
        except Exception as e:
            print(f"删除文件 '{filename}' 出错：{e}")

    def file_if_exists(self, file_path):
        print(file_path)
        return True

    def list_folder_files(self):
        files = ""
        for filename in os.listdir(self._path):
            file_path = os.path.join(self._path, filename)
            if os.path.isfile(file_path):
                temp_str = '"/video/douyin/' + str(filename) + '",'
                files = files + temp_str
        return files

    def change_file_name(self, not_default_path: str):
        # 目标文件夹路径
        if self.file_if_exists(not_default_path) and not_default_path.rfind('/') != -1:
            target_folder = not_default_path[:not_default_path.rfind('/')]
            source_file_name = not_default_path[not_default_path.rfind('/'):]
            # 生成时间戳
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            # # 获取目标文件夹的父目录路径
            # parent_folder = os.path.dirname(target_folder)
            # # 构建目标文件夹路径
            # target_folder_with_timestamp = os.path.join(target_folder, f"{os.path.basename(target_folder)}_{timestamp}")
            # 构建目标文件路径
            file_name = os.path.basename(source_file_name)
            target_file = os.path.join(target_folder, timestamp+file_name)
            # 创建带时间戳的目标文件夹
            # os.makedirs(target_folder_with_timestamp, exist_ok=True)
            # 复制文件
            shutil.copy2(not_default_path, target_file)
            print(f"成功复制文件到 {target_file}")
            return target_file
        else:
            print(f"复制文件失败，请联系小经！！！")
            return False

