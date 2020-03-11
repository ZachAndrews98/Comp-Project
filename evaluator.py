""" Evaluator """

import time, os

import docker

from auto import arguments, command_line

CLIENT = docker.from_env()
TOOL_AVERAGES = {
    'build_image': 0
}
TERM_AVERAGES = {
    'build_image': 0
}


def evaluate_build_image(num_tests):
    """ Evaluate runtimes of building images via tool and command line """
    os.system("docker rmi test-1:latest test:latest")
    args = ['--build', '--image', '--path',
            './gentest2', '--name', 'test', '--threaded']
    average_tool_time = 0
    average_terminal_time = 0
    for x in range(num_tests):
        print("Test Number:", str(x+1))
        print("\n\n")
        start_time = time.time()
        parsed_args = arguments.parse_args(args)
        command_line.command_line(parsed_args)
        average_tool_time = average_tool_time + \
                (time.gmtime(time.time() - start_time).tm_sec)
        print("Building directly using terminal")
        start_time = time.time()
        os.system(
            "docker build " + str(parsed_args.path) + " -t " + \
            str(parsed_args.name) + "-1"
        )
        average_terminal_time = average_terminal_time + \
                (time.gmtime(time.time() - start_time).tm_sec)
        os.system("docker rmi test-1:latest test:latest")

    TOOL_AVERAGES['build_image'] = average_tool_time / num_tests
    TERM_AVERAGES['build_image'] = average_terminal_time / num_tests


evaluate_build_image(5)
print("Average Tool: " + str(TOOL_AVERAGES['build_image']))
print("Average Terminal: " + str(TERM_AVERAGES['build_image']))
