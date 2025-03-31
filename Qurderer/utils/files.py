import json
import os

class JsonFile:
    def __init__(self, filepath) -> None:
        self.filepath: str = filepath
        self.readType: str = 'r'
        self.encoding: str = 'utf-8'
        self.writeType: str = 'w'
        self.indent: int = 4

    def readJson(self) -> dict | None:
        try:
            with open(file=self.filepath, mode=self.readType, encoding=self.encoding) as jsonFile:
                return json.load(jsonFile)
        except FileNotFoundError:
            raise Exception(f"Error: File '{self.filepath}' does not exist.")
        except json.JSONDecodeError:
            raise Exception('Error: File contains malformed JSON.')
        except Exception as e:
            raise Exception(f'Unexpected error reading file: {e}')

    def writeJson(self, data: dict) -> bool:
        try:
            with open(file=self.filepath, mode=self.writeType, encoding=self.encoding) as jsonFile:
                json.dump(data, jsonFile, indent=self.indent)

            return True
        except PermissionError:
            raise Exception(f"Error: You do not have permissions to write to '{self.filepath}'.")
        except Exception as e:
            raise Exception(f'Unexpected error writing to file: {e}')

    def updateJson(self, newData: dict) -> bool:
        try:
            data = self.readJson()
            
            if data is None:
                return False

            for key, value in newData.items():
                data[key] = value

            success = self.writeJson(data=data)
            return success
        except TypeError:
            raise Exception('Error: The data provided is not a valid dictionary.')
        except Exception as e:
            raise Exception(f'Unexpected error updating JSON file: {e}')

    def deleteFile(self) -> bool:
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
            return True
        
        return False

class GenericFile:
    def __init__(self, filepath) -> None:
        self.filepath: str = filepath
        self.readType: str = 'r'
        self.encoding: str = 'utf-8'
        self.writeType: str = 'w'

    def readFile(self, lines: bool=False) -> str | list | None:
        try:
            with open(file=self.filepath, mode=self.readType, encoding=self.encoding) as file:
                return file.read() if not lines else file.readlines()
        except FileNotFoundError:
            raise Exception(f"Error: File '{self.filepath}' does not exist.")
        except Exception as e:
            raise Exception(f'Unexpected error reading file: {e}')

    def writeFile(self, data: str) -> bool:
        try:
            with open(file=self.filepath, mode=self.writeType, encoding=self.encoding) as file:
                file.write(data)

            return True
        except PermissionError:
            raise Exception(f"Error: You do not have permissions to write to '{self.filepath}'.")
        except Exception as e:
            raise Exception(f'Unexpected error writing to file: {e}')

    def deleteFile(self) -> bool:
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
            return True
        
        return False