""" Evaluate Dockerfile Generator """

import os

from auto import generate
from auto import images

from evaluator import data


def evaluate_generate():
    """ Evaluate the correctness of Generated Dockerfiles """
    incorrect = 0
    correct = 0
    # Directories to test with
    directories = (
        "gentest1", "gentest2", "gentest3", "gentest4", "gentest5", "gentest6",
        "gentest7", "gentest8", "gentest9", "gentest10", "gentest11",
        "gentest12"
    )
    # Run evaluation for each directory
    for file in directories:
        data.GENERATE_DATA["output"].append("Evaluating " + file)
        # Generate Dockerfile
        generate.generate_dockerfile(
            "Docker-Automation/samples/" + file,
            add="&& chmod +x test.sh && ./test.sh"
        )
        # Build image
        images.build_image(
            "Docker-Automation/samples/" + file, file, threaded=False
        )
        # Run image
        if images.run_image(file + ":latest", args="--rm", sep=False) == 1:
            data.GENERATE_DATA["output"].append(
                "\tImage: " + file + " is incorrect"
            )
            incorrect = incorrect + 1
        else:
            data.GENERATE_DATA["output"].append(
                "\tImage: " + file + " is correct"
            )
            correct = correct + 1
        # Delete generated image
        os.system("docker rmi " + file + ":latest")
        data.GENERATE_DATA["output"].append("\n")
    # Add test information to data file
    data.GENERATE_DATA["num_tests"] = len(directories)
    data.GENERATE_DATA["num_correct"] = correct
    data.GENERATE_DATA["num_incorrect"] = incorrect
