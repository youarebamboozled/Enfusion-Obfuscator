import os
import re
import math
import random
import string
import base64


def variable_renamer(given_string):
    """
    Function to rename all variables and functions.
    given_string is a string of C/C++ code
    """
    # Variable declarations:
    variable_dictionary = {}
    special_cases = {"typedef", "unsigned"}
    index = 0
    new_string = ""

    # Split the code to indicate when it enters/exits a string
    split_code = re.split('\"', given_string)

    # REGEX to find all function and variable declarations ignoring main
    filtered_code = re.findall("(?:\w+\s+)(?!main)^(?!override).*$(?:\*)*([a-zA-Z_][a-zA-Z0-9_]*)", given_string)

    # For loop to add examples found from running a REGEX to a dictionary object
    # Ignores special cases and repeats
    # When a value is entered it is also assigned a random string of length 12
    for found_example in filtered_code:
        if found_example not in special_cases:
            if found_example not in variable_dictionary:
                variable_dictionary[found_example] = random_string(12)

    # For each even section in split code (odd indicates that it is in a string)
    # replace all the variable and function names with what is defined in the dictionary
    for section in split_code:
        if index % 2 == 0:
            for entry in variable_dictionary:
                # Used \W because we don't want to replace a variable if it is inside another word.
                re_string = r"\W{}\W".format(entry)
                # While loop to go through every entry and replace it
                # Breaks when it cannot find another instance
                while True:
                    first_found_entry = re.search(re_string, section)
                    if not first_found_entry:
                        break
                    # Gets the iterator start and endpoints of the searched re_string
                    # Then replaces the information inbetween with the dictionary value
                    start = first_found_entry.start(0)
                    end = first_found_entry.end(0)
                    section = section[:start + 1] + variable_dictionary[entry] + section[end - 1:]
        # Add the current section back to make the original string but with obfuscated names
        # Accounts for adding a quote everytime except for the first scenario
        if index >= 1:
            new_string = new_string + "\"" + section
        else:
            new_string = new_string + section
        index += 1
    # Return the obfuscated code
    return new_string


def random_string(stringLength=8):
    """
    Function to generate a random string.
    Can pass it an integer string length to make it that size else it will be 8
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


def random_c_code():
    c_code = """
        int {} = {};
        string {} = "{}";
    """.format(random_string(12), random_int(0, 100), random_string(12), random_string(12))

    return c_code


def random_int(min, max):
    """
    Function to generate a random integer between min and max
    """
    return random.randint(min, max)


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
    Function to (currently) remove C++ style comments
    given_string is a string of C/C++ code
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
    """
    The main function to begin the obfuscation of c code files
    """
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
                # file_string = whitespace_remover(file_string)
                file_string = create_typedefs(file_string)
                f = open("obfuscated_" + filename, "w+")
                f.write(file_string)
                print(file_string)

        else:
            print("FAIL")


if __name__ == "__main__":
    main()

