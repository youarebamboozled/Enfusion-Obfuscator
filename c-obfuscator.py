"""
Enfusion Obfuscator. This Program is used to obfuscate Enfusion style code.
Copyright (C) 2022  YouAreBamboozled

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import os
import re
import math
import random
import string
import base64


def variable_renamer(given_string):
    """
    renames all vars to random names if it works
    """

    variable_dictionary = {}
    special_cases = {"typedef", "unsigned"}
    index = 0
    new_string = ""

    split_code = re.split('\"', given_string)

    filtered_code = re.findall("(?:\w+\s+)(?!main)^(?!override).*$(?:\*)*([a-zA-Z_][a-zA-Z0-9_]*)", given_string)

    for found_example in filtered_code:
        if found_example not in special_cases:
            if found_example not in variable_dictionary:
                variable_dictionary[found_example] = random_string(12)

    for section in split_code:
        if index % 2 == 0:
            for entry in variable_dictionary:
                re_string = r"\W{}\W".format(entry)
                while True:
                    first_found_entry = re.search(re_string, section)
                    if not first_found_entry:
                        break
                    start = first_found_entry.start(0)
                    end = first_found_entry.end(0)
                    section = section[:start + 1] + variable_dictionary[entry] + section[end - 1:]
        if index >= 1:
            new_string = new_string + "\"" + section
        else:
            new_string = new_string + section
        index += 1
    return new_string


def random_c_code():
    c_code = """
        int {} = {};
        string {} = "{}";
    """.format(random_string(12), random_int(0, 100), random_string(12), random_string(12))

    return c_code


def whitespace_remover(a):
    """
    Function to remove all whitespace, except for after functions, variables, and imports
    """
    splits = re.split('\"', a)
    code_string = "((\w+\s+)[a-zA-Z_*][|a-zA-Z0-9_]*|#.*|return [a-zA-Z0-9_]*| [[.].]|else)"
    index = 0
    a = ""
    for s in splits:
        # If it's not the contents of a string, remove spaces of everything but code
        if index % 2 == 0:
            s_spaceless = re.sub("[\s]", "", s)  # Create a spaceless version of s
            s_code = re.findall(code_string, s)  # find all spaced code blocks in s
            for code in s_code:
                old = re.sub("[\s]", "", code[0])
                new = code[0]
                if code[0][0] == '#':
                    new = code[0] + "\n"  # Adding a newline for preprocessor commands
                elif "unsigned" in code[0] or "else" in code[0]:
                    new = code[0] + " "
                s_spaceless = s_spaceless.replace(old,
                                                  new)  # Replace the spaceless code blocks in s with their spaced
                # equivalents
        else:
            s_spaceless = s
        if index >= 1:
            a = a + "\"" + s_spaceless
        else:
            a = a + s_spaceless
        index += 1
    return a


def random_string(stringLength=8):
    """
    Function to generate a random string with given length.
    """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def random_comment(stringLength=100):
    """
    Function to generate a random comment.
    Can pass it an integer string length to make it that size else it will be 100
    """
    letters = string.ascii_lowercase
    return "/*" + ''.join(random.choice(letters) for i in range(stringLength)) + "*/"


def random_int(mini, maxi):
    """
    Function to generate a random integer between min and max
    """
    return random.randint(mini, maxi)


def create_typedefs(given_string):
    """
    Function to rename all types like int, string, etc. to random names
    """
    # add random typedefs for all c types at the start
    typedef_string = ""

    for entry in ["int ", "void ", "float ", "bool ", "SCR_CharacterControllerComponent",
                  "SCR_InventoryStorageManagerComponent", "Replication", "IEntity", "EL_GameModeRoleplay"]:
        rs = random_string(100)
        rs1 = random_string(100)
        rs2 = random_string(100)
        rs3 = random_string(100)
        ri = random_int(1, 1000)
        ri1 = random_int(1, 1000)
        ri2 = random_int(1, 1000)
        ri3 = random_int(1, 1000)
        typedef_string = typedef_string + "{}typedef{}{}{}{}{};\n".format(random_comment(ri), random_comment(ri1),
                                                                          entry, random_comment(ri2), rs,
                                                                          random_comment(ri3))
        typedef_string = typedef_string + "{}typedef{}{}{}{}{};\n".format(random_comment(ri1), random_comment(ri3),
                                                                          entry, random_comment(ri2), rs1,
                                                                          random_comment(ri3))
        typedef_string = typedef_string + "{}typedef{}{}{}{}{};\n".format(random_comment(ri3), random_comment(ri),
                                                                          entry, random_comment(ri2), rs2,
                                                                          random_comment(ri1))
        typedef_string = typedef_string + "{}typedef{}{}{}{}{};\n".format(random_comment(ri), random_comment(ri1),
                                                                          entry, random_comment(ri2), rs3,
                                                                          random_comment(ri3))
        # Replace all instances of the type with the random name
        given_string = given_string.replace(entry, random_comment(random_int(100, 1000)) + rs3 + " " +
                                            random_comment(random_int(100, 1000)))
    return typedef_string + given_string


def comment_remover(given_string):
    """
    Function to remove C style comments
    """
    # Remove all C++ style comments
    cpp_filtered_code = re.findall(r"\/\/.*", given_string)
    for entry in cpp_filtered_code:
        given_string = given_string.replace(entry, "")

    c_filtered_code = re.findall(
        r"\/\*.*\*\/", given_string)
    for entry in c_filtered_code:
        given_string = given_string.replace(entry, "")

    return given_string


def main():
    cwd = os.getcwd()
    msg = "5257356d64584e706232346754324a6d64584e6a595852766369424462334235636d6c6e614851674b454d70494449774d6a49674" \
          "9466c76645546795a554a6862574a76623370735a57514b494341674946526f61584d6763484a765a334a686253426a6232316c63" \
          "7942336158526f494546435530394d5656524654466b67546b386756304653556b464f56466b75436941674943425561476c7a494" \
          "76c7a49475a795a5755676332396d64486468636d5573494746755a4342356233556759584a6c4948646c62474e76625755676447" \
          "3867636d566b61584e30636d6c696458526c49476c304369416749434231626d526c6369426a5a584a3059576c7549474e76626d5" \
          "27064476c76626e4d7549413d3d"
    if r"C-Code-Obfuscator" in cwd:
        offset = cwd.find("C-Code-Obfuscator") + 17
        cwd = cwd[:offset]
        cwd = cwd + cwd[-18] + "tests"
    else:
        dmsg = str(base64.b64decode(bytes.fromhex(msg).decode("utf-8")))
        dmsg = dmsg[2:207]
        dmsg = dmsg.replace("\\n", "\n")

        print(dmsg)

        cwd = input('Path to C Source Files Directory: ')

    print("Looking for C Source Files in {}...".format(cwd))

    print("Log: ")
    for filename in os.listdir(cwd):
        print("\n {} : \r".format(filename))
        if ".c" in filename or ".h" in filename:
            with open(os.path.join(cwd, filename)) as file_data:
                file_string = file_data.read()
                print("PASS\n")
                file_string = comment_remover(file_string)
                file_string = variable_renamer(file_string)
                file_string = create_typedefs(file_string)
                f = open("obfuscated_" + filename, "w+")
                f.write(file_string)
                print(file_string)

        else:
            print("FAIL")


if __name__ == "__main__":
    main()

