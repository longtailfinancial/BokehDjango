"""
For deploying bokeh-django.
"""

import os
from subprocess import STDOUT, check_call
import logging
logger = logging.getLogger(__name__)
import fire

class ConfigDict(dict):
    """
    A typed dict used for configuration.
    """

class BokehDjangoInstaller:
    """
    Used to install BokehDjango project on Linode.
    """
    def __init__(self: object, dry_run: bool = True):
        """
        Pass dry_run True if you do not want to modify the server. 
        """
        self.dry_run = dry_run

    def _edit_file(self: object, file_location: str, replacements: dict):
        """
        Edit a file on the deploy machine.
        MODIFIES SYSTEM
        USE `--dry_run = True` TO TEST WITHOUT EFFECTING SYSTEM
        """
        logger.info(f"Replacing content in {file_location}")
        with open(file_location, "w") as f:
            content = f.read()

            for key, value in replacements.items():
                content = content.replace(key, value)

            logger.debug(f"New Content: \n\n{content}\n\n")
            if not self.dry_run:
                f.write(content)
                logger.info(f"File Sucessfully Written")
            else:
                logger.info(f"Skipping overwrite file. Run with --dry-run = False to perform a deploy.")


    def _add_lines_to_file(self: object, file_location: str, additional_lines: list):
        """
        Append lines to a file on the deploy machine.
        MODIFIES SYSTEM
        USE `--dry_run = True` TO TEST WITHOUT EFFECTING SYSTEM
        """
        logger.info(f"Appending {additional_lines} to {file_location}")
        with open(file_location, "w") as f:
            content = f.read()

            for line in additional_lines:
                content = content + f"\n{line}"

            logger.debug(f"New Content: \n\n{content}\n\n")
            if not self.dry_run:
                f.write(content)
                logger.info(f"File Sucessfully Written")
            else:
                logger.info(f"Skipping overwrite file. Run with --dry-run = False to perform a deploy.")


    def _call_instruction(self: object, instruction: list):
        """
        Use check_call to run commands with arguments. 
        If the command is successful (returns 0) then the process continues.
        Otherwise, check_call will raise CalledProcessError.
        """
        if not self.dry_run:
            check_call(instruction, stdout=open(os.devnull,'wb'), stderr=STDOUT)
        else:
            logger.info(f"Skipping {instruction}. Run with --dry-run = False to perform a deploy.")


    def install_bokeh_django(self: object, group='ltfdev', user='shawn', full_name='Shawn Anderson'):
        """
        Default install for the BokehDjango project.
        Implemented in python by Shawn Anderson July 3 2020.
        """

        ssh_config = {
            "PermitRootLogin yes": "PermitRootLogin no",
            "PasswordAuthentication yes": "PasswordAuthentication no",
            "UsePAM yes": "UsePAM no",
            }

        self._edit_file("/etc/ssh/ssh_config", ssh_config)

        machine_updates = [
            ['apt-get', 'update'],
            ['apt-get', 'upgrade'],
            ['apt-get', 'install', '-y', 'gcc'],
            ['apt-get', 'install', '-y', 'python3.8-dev'],
            ['apt-get', 'install', '-y', 'fail2ban'],
            ['apt-get', 'install', '-y', 'git-core'],
            ['apt-get', 'install', '-y', 'virtualenv'],
            ['apt-get', 'install', '-y', 'gunicorn'],
            ['apt-get', 'install', '-y', 'nginx'],
                ]
        for update in machine_updates:
            self._call_instruction(update)

        # Append to sudoers file
        self._add_lines_to_file('/etc/sudoers', f"%{group} ALL=(ALL) ALL")

        # Update Permissions
        permission_updates = [
            ['/usr/sbin/groupadd', group],
            ['chmod', '0440', '/etc/sudoers'],
            ['/usr/sbin/useradd', '-c', full_name, '-m', '-g', group, user],
            ['/usr/bin/passwd', user],
            ['/usr/sbin/usermod', '-a', '-G', group, user],
            ['mkdir ', f'/home/{user}/.ssh'],
                ]
        for update in permission_updates:
            self._call_instruction(update)

if __name__ == "__main__":
    fire.Fire(BokehDjangoInstaller)

