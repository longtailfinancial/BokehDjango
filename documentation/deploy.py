"""
For deploying panel-django.
"""


def edit_sshd_config():
    """
    Edit SSHD Config.
    """
    file_location = "/etc/ssh/sshd_config"
    with open(file_location, "w") as config_file:
        content = config_file.read()
        content.replace("PermitRootLogin yes", "PermitRootLogin no")
        content.replace("PasswordAuthentication yes", "PasswordAuthentication no")
        content.replace("UsePAM yes", "UsePAM no")
        config_file.write(content)
