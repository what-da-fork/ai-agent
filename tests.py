from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

'''
def test_get_files_info_1():
    results = get_files_info("calculator", ".")
    print(f"Result for current directory:\n{results}")

def test_get_files_info_2():
    directory = "pkg"
    results = get_files_info("calculator", directory)
    print(f"Result for '{directory}' directory:\n{results}")

def test_get_files_info_3():
    directory = "/bin"
    results = get_files_info("calculator", directory)
    print(f"Result for '{directory}' directory:\n{results}")

def test_get_files_info_4():
    directory = "../"
    results = get_files_info("calculator", directory)
    print(f"Result for '{directory}' directory:\n{results}")

def test_get_file_content_1():
    file_path = "main.py"
    results = get_file_content("calculator", file_path)
    print(f"Result for file '{file_path}':\n{results}")

def test_get_file_content_2():
    file_path = "pkg/calculator.py"
    results = get_file_content("calculator", file_path)
    print(f"Result for file '{file_path}':\n{results}")

def test_get_file_content_3():
    file_path = "/bin/cat"
    results = get_file_content("calculator", file_path)
    print(f"Result for file '{file_path}':\n{results}")

def test_get_file_content_4():
    file_path = "pkg/does_not_exist.py"
    results = get_file_content("calculator", file_path)
    print(f"Result for file '{file_path}':\n{results}")
'''

def test_write_file_1():
    file_path = "lorem.txt"
    content = "wait, this isn't lorem ipsum"
    results = write_file("calculator", file_path, content)
    print(f"Result for writing to file '{file_path}':\n{results}")

def test_write_file_2():
    file_path = "pkg/morelorem.txt"
    content = "lorem ipsum dolor sit amet"
    results = write_file("calculator", file_path, content)
    print(f"Result for writing to file '{file_path}':\n{results}")

def test_write_file_3():
    file_path = "/tmp/temp.txt"
    content = "this should not be allowed"
    results = write_file("calculator", file_path, content)
    print(f"Result for writing to file '{file_path}':\n{results}")

if __name__ == "__main__":
    #test_get_files_info_1()
    #test_get_files_info_2()
    #test_get_files_info_3()
    #test_get_files_info_4()
    #test_get_file_content_1()
    #test_get_file_content_2()
    #test_get_file_content_3()
    #test_get_file_content_4()
    test_write_file_1()
    test_write_file_2()
    test_write_file_3()
    