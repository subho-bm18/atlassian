class FileSystem:
    def __init__(self):
        self.paths = {'': -1}  # Root directory is represented with empty string
    
    def createPath(self, path: str, value: int) -> bool:
        if not path or path == '/' or path in self.paths:
            return False

        parent = path[:path.rfind('/')]
        if parent not in self.paths:
            return False
        
        self.paths[path] = value
        return True

    def get(self, path: str) -> int:
        return self.paths.get(path, -1)

fs = FileSystem()
print(fs.createPath("/a", 1))     # True
print(fs.createPath("/a/b", 2))   # True
print(fs.createPath("/c/d", 3))   # False ("/c" does not exist)
print(fs.get("/a"))               # 1
print(fs.get("/a/b"))             # 2
print(fs.get("/c"))               # -1
