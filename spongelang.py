"""
SpongeLang: a simple programming language AI can use
scroll down to the end for docs though idk why you'd wanna use this in anything i only made this because it's cool
"""

import re
from typing import Callable  # I LOVE TYPE HINTING I LOVE TYPE HINTING YES YES


def extract_spongelang(input_string):
    pattern = r"```(?:spongelang|slang)\n(.*?)```"
    matches = re.findall(pattern, input_string, re.DOTALL)
    return matches


def remove_spongelang(input_string):
    pattern = r"```(?:spongelang|slang)\n(.*?)```"
    output_string = re.sub(pattern, "", input_string, flags=re.DOTALL)
    return output_string


# ! GODDAMNIT IT WORKS REMOVE THESE TESTS
# !############################################
# !############################################
test = """
hello world

```spongelang
spongelang yipeeeee
```

hello world

```py
not spongelang :(
```

`hello world`
"""

for code in extract_spongelang(test):
    print(code)

print(remove_spongelang(test))
print(type(extract_spongelang))
# !############################################
# !############################################
# ! GODDAMNIT IT WORKS REMOVE THESE TESTS


def process_function_calls(code: str, functions: list[tuple[str, Callable]]):
    function_names = [function[0] for function in functions]
    for line in code.splitlines():
        process_single_line(line, function_names, functions)


def process_single_line(
    line: str, function_names: list[str], functions: list[tuple[str, Callable]]
):
    print("reading line")
    for i, function_name in enumerate(function_names):
        print("checking line for functions")
        if line.startswith(function_name):
            print("function found!", function_name)
            args = [
                group[0] if group[0] else group[1] if group[1] else group[2]
                for group in re.findall(
                    r'"([^"]*)"|\'([^\']*)\'|(\S+)',
                    line.replace(f"{function_name} ", ""),
                )
            ]  # TODO HEL;P WHAT IS THIS
            function = functions[i][1]
            print("converting args to correct types")
            for i, annotate in enumerate(function.__annotations__.values()):
                args[i] = annotate(args[i])
                print(f"converted to {type(args[i])} successfully!")
            print(function(*args))  # ! debug make it not print when finished


def add(x: float, y: float):
    return x + y


def multiply(x: float, y: float):
    return x * y


def spongelang_print(prints: str):
    # why do i have to do this
    print(prints)


functions = [("add", add), ("multiply", multiply), ("print", spongelang_print)]

code = """
add 3 4
multiply 64.0 64.1
print "Hello, world!"
"""

processed_code = process_function_calls(code, functions)
# //print(processed_code)
