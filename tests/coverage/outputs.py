import os
import shutil

TEST_OUTPUT_DIRECTORY = "./tests/outputs/"


def destroy_previous_outputs():
    if os.path.exists(TEST_OUTPUT_DIRECTORY):
        shutil.rmtree(TEST_OUTPUT_DIRECTORY)

    os.mkdir(TEST_OUTPUT_DIRECTORY)

    generate_git_keep_file()


def generate_git_keep_file():
    f = open(TEST_OUTPUT_DIRECTORY + ".gitkeep", "w+")
    f.close()

