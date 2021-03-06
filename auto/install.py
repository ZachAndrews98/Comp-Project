""" Checks OS and installs Docker following a specific instruction set """

import os
import platform

import docker


PLATFORM = platform.system()


def install():
    """ Main installation function """
    # If docker does not appear to be installed
    if not confirm_installation():
        # Linux based platform
        if PLATFORM == "Linux":
            # pylint: disable=W1505
            distro = platform.linux_distribution()
        # MacOS based platform (not confirmed to work)
        elif PLATFORM == "MacOS":
            distro = ("MacOS", "", "")
            print("Mac OS currently experimental")
        # Windows based platform (Not currently operational)
        elif PLATFORM == "windows":
            return "Windows currently not supported"
            # TODO: figure out method to determine home vs pro
        file = get_instructions(distro)
        if file != "No Instruction Set":
            execute_instructions(file)
        else:
            print("No Instruction Set Found")
        if confirm_installation():
            return "Docker successfully installed, \
                    please restart to complete installation."
        return "Issues installing Docker."
    return "Docker already installed."


def get_instructions(distro):
    """ Determines what instruction set is required to install Docker """
    file = ""
    if distro[0] == "Ubuntu":
        file = os.getenv('HOME') + "/Docker-Automation/instructions/ubuntu"
    elif distro[0] == "CentOS":
        file = os.getenv('HOME') + "/Docker-Automation/instructions/centos"
    elif distro[0] == "Debian":
        file = os.getenv('HOME') + "/Docker-Automation/instructions/debian"
    elif distro[0] == "Fedora":
        file = os.getenv('HOME') + "/Docker-Automation/instructions/fedora"
    elif distro[0] == "MacOS":
        file = os.getenv('HOME') + "/Docker-Automation/instructions/macos"
    else:
        file = "No Instruction Set"
    return file


def execute_instructions(file):
    """ Executes the installation instructions """
    print("Warning: A restart will occur once installation is finished.")
    print("\tThis allows for the installation of Docker to finish properly.")
    input("\tPress Enter to continue. Hit 'ctrl + c' to cancel.")
    commands = open(file, 'r')
    for command in commands:
        command = command.replace("\n", "")
        try:
            os.system(command)
        except BaseException:
            return False
    return True


def confirm_installation():
    """ Confirms if Docker was properly installed """
    installed = False
    try:
        # Try to get docker version
        version = os.system("docker --version")
        # If version exists
        if version != 32512:
            # Try to run hello-world image
            client = docker.from_env()
            if client.containers.run("hello-world:latest", remove=True):
                installed = True
            client.images.remove("hello-wold:latest")
            print("Installed:", installed)
    except BaseException:
        pass
    return installed
