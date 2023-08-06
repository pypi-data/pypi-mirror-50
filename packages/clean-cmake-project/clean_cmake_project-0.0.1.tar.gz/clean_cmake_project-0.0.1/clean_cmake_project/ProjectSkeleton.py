#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import datetime
import stringcase

src = "src"
tests = "tests"
libs = "libs"
cmake = "CMakeLists.txt"
host = os.getlogin()
now = datetime.today().strftime('%Y-%m-%d')


class ProjectBuilder:
    def __init__(self, project_name, path_input):

        if os.path.exists(path_input):
            print("Path exists !!")
        else:
            path_input = os.getcwd()
            print("Path does not exist ! -> default to current directory", path_input)

        self.path = path_input
        self.base_const = stringcase.constcase(os.path.basename(self.path))
        self.base_snake = stringcase.constcase(os.path.basename(self.path))
        print("Current working directory %s" % self.path)

        self.snake = stringcase.snakecase(project_name)
        self.const = stringcase.constcase(project_name)
        self.pascal = stringcase.pascalcase(project_name)

        self.create_base()
        self.create_project()

        # print current projects
        print("Current source projects: ")
        for d in next(os.walk(os.path.join(self.path, src)))[1]:
            print("\t", d)

        # print current projects
        print("Current source projects - tests: ")
        for d in next(os.walk(os.path.join(self.path, tests)))[1]:
            print("\t", d)

    def download_gtest(self):
        if not os.path.exists(os.path.join(self.path, libs)):
            os.mkdir(os.path.join(self.path, libs))
            if not os.path.exists(os.path.join(self.path, libs, "googletest")):
                os.chdir(os.path.join(self.path, libs))
                gtest_path = "https://github.com/google/googletest.git"
                os.system("git clone " + gtest_path)
                os.chdir("..")

    def create_cmake(self):
        if not os.path.exists(os.path.join(self.path, cmake)):
            cmake_string = ("cmake_minimum_required(VERSION 3.10)\n"
                            "project({})\n"
                            "\n"
                            "set(CMAKE_CXX_STANDARD 17)\n"
                            "\n"
                            "include_directories(src)\n"
                            "\n"
                            "add_subdirectory(libs/googletest)\n"
                            ).format(self.base_snake)
            with open(os.path.join(self.path, cmake), "w+") as cmake_file:
                cmake_file.write(cmake_string)

    def create_base(self):
        self.create_cmake()
        self.download_gtest()
        if not os.path.exists(os.path.join(self.path, tests)):
            os.mkdir(os.path.join(self.path, tests))
        if not os.path.exists(os.path.join(self.path, src)):
            os.mkdir(os.path.join(self.path, src))

    def append_to_cmake(self):
        # add_subdirectory to CMakeFile
        cmake_string = ("\n"
                        "add_subdirectory({1}/{0})\n"
                        "add_subdirectory({2}/{0}_test)\n"
                        ).format(self.snake, src, tests)
        with open(os.path.join(self.path, cmake), "a") as cmake_file:
            cmake_file.write(cmake_string)

    def create_src(self):
        src_path = os.path.join(self.path, src, self.snake)
        os.mkdir(src_path)
        cmake_string = ("cmake_minimum_required(VERSION 3.10)\n"
                        "project({0})\n"
                        "\n"
                        "set(CMAKE_CXX_STANDARD 17)\n"
                        "\n"
                        "set({1}_SOURCE_FILES\n"
                        "        {2}.cpp {2}.h\n"
                        "    )\n"
                        "\n"
                        "add_library({0} ${{{1}_SOURCE_FILES}})\n").format(self.snake, self.const, self.pascal)
        with open(os.path.join(src_path, cmake), 'w+') as f:
            f.write(cmake_string)

        h_string = ("//\n"
                    "// Created by {0} on {1}.\n"
                    "//\n"
                    "\n"
                    "#ifndef {4}_{2}_H\n"
                    "#define {4}_{2}_H  \n"
                    "\n"
                    "class {3} {{\n"
                    "\n"
                    "}}; \n"
                    "\n"
                    "#endif //{4}_{2}_H\n"
                    ).format(host, now, self.const, self.pascal, self.base_const)
        with open(os.path.join(src_path, self.pascal + ".h"), 'w+') as f:
            f.write(h_string)

        cpp_string = ("//\n"
                      "// Created by {0} on {1}.\n"
                      "//\n"
                      "#include \"{2}.h\"\n"
                      ).format(host, now, self.pascal)
        with open(os.path.join(src_path, self.pascal + ".cpp"), 'w+') as f:
            f.write(cpp_string)

    def create_test(self):
        tests_path = os.path.join(self.path, tests, self.snake + "_test")
        os.mkdir(tests_path)

        cmake_string = ("cmake_minimum_required(VERSION 3.10)\n"
                        "project({0})\n"
                        "\n"
                        "enable_testing()\n"   
                        "include_directories(${{gtest_SOURCE_DIR}}/include ${{gtest_SOURCE_DIR}})\n"
                        "set({1}_TEST_FILES\n"
                        "        {2}_tests.cpp\n"
                        "    )\n"
                        "add_executable(run{3}Tests ${{{1}_TEST_FILES}})\n"
                        "target_link_libraries(run{3}Tests gtest gtest_main)\n"
                        "target_link_libraries(run{3}Tests {2})\n"
                        ).format(tests, self.const, self.snake, self.pascal)
        with open(os.path.join(tests_path, cmake), 'w+') as f:
            f.write(cmake_string)

        cpp_string = ("//\n"
                      "// Created by {0} on {1}.\n"
                      "//\n"
                      "#include \"{3}/{2}.h\"\n"
                      "#include \"gtest/gtest.h\"\n"
                      "\n"
                      "\n"
                      "TEST(basic_{3}_check, test_eq){{\n"
                      "\tEXPECT_EQ(1, 1);\n"
                      "}}\n"
                      "\n"
                      "TEST(basic_{3}_check, test_neq){{\n"
                      "\tEXPECT_NE(1, 0);\n"
                      "}}\n"
                      "\n"
                      ).format(host, now, self.pascal, self.snake)
        with open(os.path.join(tests_path, self.snake + "_tests.cpp"), 'w+') as f:
            f.write(cpp_string)

    def create_project(self):
        if os.path.exists(os.path.join(self.path, src, self.snake)):
            print("Folder already exists")
        else:
            self.append_to_cmake()
            self.create_src()
            self.create_test()


def build(b_name, b_path):
    ProjectBuilder(b_name, b_path)


def main():
    name = input("Enter New Project Name: ")
    print("Project name from input", name)
    path = input("Enter Folder Path: ")
    print("Path from input", path)
    build(name, path)
