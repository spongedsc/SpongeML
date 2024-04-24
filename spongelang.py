# catches
"""
SpongeLang: a simple programming language AI can use
(original code written by butterroach 2024/4/20 omg funny number i just realized woah)
"""

import math
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


def process_function_calls(code: str, functions: list[tuple[str, Callable]]):
    function_names = [function[0] for function in functions]
    out = ""
    for line in code.splitlines():
        lout = process_single_line(line, function_names, functions)
        out += lout + "\n" if lout is not None else ""
    return out


def process_single_line(
    line: str, function_names: list[str], functions: list[tuple[str, Callable]]
):
    # print("reading line")
    for i, function_name in enumerate(function_names):
        # print("checking line for functions")
        if line.startswith(function_name):
            # print("function found!", function_name)
            args: list[str] = [
                group[0] if group[0] else group[1] if group[1] else group[2]
                for group in re.findall(
                    r'"([^"]*)"|\'([^\']*)\'|(\S+)',
                    line.replace(f"{function_name} ", ""),
                )
            ]  # TODO HEL;P WHAT IS THIS
            internalfunction = functions[i][1]
            # print("converting args to correct types")
            for i, annotate in enumerate(internalfunction.__annotations__.values()):
                if args[i].startswith("$"):
                    args[i] = spongelang_vars.get(args[i].replace("$", ""))
                args[i] = annotate(args[i])
                # print(f"converted to {type(args[i])} successfully!")
            out = internalfunction(*args)
            # print(out) # ! debug make it not print when finished
            return out


def add(x: float, y: float):
    return x + y


def subtract(x: float, y: float):
    return x - y


def multiply(x: float, y: float):
    return x * y


def divide(x: float, y: float):
    return x / y


def spongelang_print(prints: str):
    return prints


def spongelang_sin(x: float):
    # why do i have to do this
    return math.sin(x)


def spongelang_cos(x: float):
    return math.cos(x)


def spongelang_asin(x: float):
    return math.asin(x)


def spongelang_acos(x: float):
    return math.acos(x)


def con(*strs: str):
    return "".join(strs)


def define_var_str(var_name: str, var_value: str):
    spongelang_vars[var_name] = var_value


def define_var_int(var_name: str, var_value: int):
    spongelang_vars[var_name] = var_value


def define_var_float(var_name: str, var_value: float):
    spongelang_vars[var_name] = var_value


def define_var_fun(var_name: str, *var_value: str):
    spongelang_vars[var_name] = process_single_line(
        " ".join(var_value), [function[0] for function in functions], functions
    )


spongelang_vars = {}
functions = [
    ("add", add, "Adds two numbers."),
    ("sub", subtract, "Subtracts two numbers."),
    ("mul", multiply, "Multiplies two numbers."),
    ("div", divide, "Divides two numbers."),
    ("print", spongelang_print, "Prints output."),
    ("var str", define_var_str),
    ("var int", define_var_int),
    ("var float", define_var_float),
    ("var fun", define_var_fun),
    ("sin", spongelang_sin, "Calculates sine of x radians."),
    ("cos", spongelang_cos, "Calculates cosine of x radians."),
    (
        "con",
        con,
        "Concatenates strings together (can take an infinite number of arguments).",
    ),
    ("asin", spongelang_asin, "Calculates the arc sine."),
    ("acos", spongelang_acos, "Calculates the arc cosine."),
]

if __name__ == "__main__":
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

    code = """
var int x 3
var int y 5
var float v 64
var float w 64.1
var str a "Hello"
var str b ", "
var str c "World!"
var fun outhw con $a $c
var fun out1 add $x $y
var fun out2 mul $v $w
print $outhw
print $out1
print $out2
var int x 19
var float y .73
var fun out1 sin $x
var fun out2 cos $x
var fun out3 asin $y
var fun out4 acos $y
print $out1
print $out2
print $out3
print $out4
    """

    print("\n\n === START OF CODE === \n\n")
    output = process_function_calls(code, functions)
    print(output)
# catches
