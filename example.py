# import my_python_module.crusty as rust_lib
from crusty import sum_as_string


def main():
    result = sum_as_string(5, 9)
    print(result)


if __name__ == '__main__':
    main()
