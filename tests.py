from functions.get_files_info import get_files_info

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

if __name__ == "__main__":
    test_get_files_info_1()
    test_get_files_info_2()
    test_get_files_info_3()
    test_get_files_info_4()