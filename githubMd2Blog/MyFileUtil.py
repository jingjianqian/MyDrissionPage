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

    def file_if_exists(self):
        print(self._path)
        return True
