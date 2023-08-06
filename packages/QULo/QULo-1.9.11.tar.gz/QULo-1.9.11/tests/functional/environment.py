#!/bin/env python3

#######################################################################
# Copyright (C) 2018, 2019 David Palao
#
# This file is part of QULo.
#
#  QULo is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  QULo is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with QULo.  If not, see <http://www.gnu.org/licenses/>.
#
#######################################################################


import tempfile
import os
import shutil
import socket

from tests.common.docker import FTDocker
from tests.functional.graphite import Graphite


DOCKER_FT_ENVIRONMENT = "docker"
LOCALHOST_FT_ENVIRONMENT = "localhost"

DEFAULT_QULO_FT_ENVIRONMENT = DOCKER_FT_ENVIRONMENT
#DEFAULT_QULO_FT_ENVIRONMENT = LOCALHOST_FT_ENVIRONMENT

QULO_FT_ENVIRONMENT_VAR = "QULO_FT_ENVIRONMENT"

DOCKER_COMPOSE_COMMON = """version: '3.5'

x-qulo-src:
  &qulo-src
  type: bind
  source: /home/palao/HPCkz/QULo
  target: /QULo
    
services:"""

DOCKER_COMPOSE_SERVICE = """
  {service_name}:
    container_name: {container_name}
    image: qulo
    hostname: {hostname}
    command: bash -c "pip install {pip_user_flag} -e /QULo && {user_path}{command} && tail -F {logfile}"
    volumes:
      - *qulo-src
      {logs_volume}
      {pid_dir_volume}
      {conf_volume}
"""

PIP_USER_FLAG = "--user"
USER_PATH = "~/.local/bin/"

DOCKER_COMPOSE_GRAPHITE_SERVICE = """
  graphite:
    container_name: graphite
    image: graphiteapp/graphite-statsd
    restart: always
    ports:
      - 80:80
      - 2003-2004:2003-2004
      - 2023-2024:2023-2024
      - 8125:8125/udp
      - 8126:8126
    environment:
      AUTO_REFRESH_INTERVAL: 1
"""

DOCKER_COMPOSE_SERVICE_USER = "    user: {user}\n"
DOCKER_COMPOSE_VOLUME = "- {local_path}:{container_path}"


class FTEnvironment:
    """Environment for functional tests. The qmaster and qagent programs
    may require system wide privileges, hence a proper environment should
    be used in general, to be able to modify files in privileged places
    within containers, for instance."""

    def __init__(
            self, env_type, original_log_file_name,
            original_pid_dir, pid_dir_mode=0o755,
            root_workdir="/tmp", log_file_name="qulo.log",
            with_graphite=False):
        self._commands = ()
        self.env_type = env_type
        #self._programs = {program.name: program for program in programs}
        self.make_workdir(root_workdir)
        self.prepare_logging(log_file_name, original_log_file_name)
        self.setup_pid_dir(original_pid_dir, pid_dir_mode)
        self._running_commands = set()
        self.with_graphite = with_graphite
        self.docker_user = None

    def make_workdir(self, root_workdir):
        self._workdir = tempfile.TemporaryDirectory(
            dir=root_workdir, prefix="QULo-", suffix="-{}".format(self.name)
        )
        
    def prepare_logging(self, log_file_name, original_log_file_name):
        self.log_file_name = os.path.join(self._workdir.name, log_file_name)
        self.original_log_file_name = original_log_file_name
        self.link_logfiles()

    def setup_pid_dir(self, original_pid_dir, mode):
        self.original_pid_dir = original_pid_dir
        # I need basename here to be able to join absolute paths
        self.pid_dir = os.path.join(
            self._workdir.name, os.path.basename(self.original_pid_dir)
        )
        try:
            os.makedirs(self.pid_dir, mode=mode)
        except FileExistsError:
            pass
        
    @property
    def name(self):
        return self._env_type.name
    
    @property
    def env_type(self):
        return self._env_type

    @env_type.setter
    def env_type(self, env_type):
        self._env_type = _FT_ENVIRONMENT_DICT[env_type]

    @property
    def commands(self):
        """Every time that the commands property is read, it is deleted assuming that
        the read value is used to run something"""
        value = self._commands
        self._commands = ()
        return value

    @commands.setter
    def commands(self, new_commands):
        self._commands = self._commands + tuple(new_commands)

    def __enter__(self):
        return self.env_type.__enter__(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.env_type.__exit__(self, exc_type, exc_val, exc_tb)

    def link_logfiles(self):
        return self.env_type.link_logfiles(self)
    
    def __call__(self, *commands):
        self.commands = commands
        return self

    @property
    def output(self):
        return self.env_type.output(self)
    
    @property
    def stderr(self):
        return self.env_type.stderr(self)

    def run_in_container(self, command, container_name):
        command(pre_exe=("docker", "exec", container_name))

        
class FTEnvironmentType:
    @staticmethod
    def __enter__(env):
        # this method should create the  
        raise NotImplementedError()

    @staticmethod
    def __exit__(env, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @staticmethod
    def link_logfiles(env):
        raise NotImplementedError()

    @staticmethod
    def output(self):
        raise NotImplementedError()
    
        
class LocalhostFTEnvironmentType(FTEnvironmentType):
    name = LOCALHOST_FT_ENVIRONMENT
    
    @staticmethod
    def __enter__(env):
        if env.with_graphite:
            env.graphite = Graphite()
            env.graphite.down()
            env.graphite.up()
            env.graphite.wait_until_running()
            time.sleep(5)
        # WARNING: as it is now, this methond works with many commands,
        #          BUT only one output is kept!
        env._results = []
        commands = env.commands
        for command in commands:
            try:
                shutil.copyfile(command.test_conf, command.standard_conf)
            except TypeError:
                pass
            result = command()
            env._results.append(result)
            env._running_commands.add(command)
            command.hostname = socket.gethostname()
        return env

    @staticmethod
    def __exit__(env, exc_type, exc_val, exc_tb):
        while env._running_commands:
            cmd = env._running_commands.pop()
            cmd("stop")
        env.graphite.down()
            
    @staticmethod
    def link_logfiles(env):
        open(env.original_log_file_name, "a").close()
        os.link(env.original_log_file_name, env.log_file_name)

    @staticmethod
    def output(env):
        return "\n".join([_["stdout"].decode() for _ in env._results])

    stdout = output
    
    @staticmethod
    def stderr(env):
        return "\n".join([_["stderr"].decode() for _ in env._results])
    

class DockerFTEnvironmentType(FTEnvironmentType):
    name = DOCKER_FT_ENVIRONMENT
    
    @staticmethod
    def __enter__(env):
        # create docker-compose.yml
        commands = env.commands
        blocks = [DOCKER_COMPOSE_COMMON]
        if env.with_graphite:
            blocks.append(DOCKER_COMPOSE_GRAPHITE_SERVICE)
        for command in commands:
            command._piddir = env.pid_dir
            if command.test_conf and command.standard_conf:
                conf_volume = DOCKER_COMPOSE_VOLUME.format(
                    local_path=command.test_conf, container_path=command.standard_conf
                )
            else:
                conf_volume = ""
            logs_volume = DOCKER_COMPOSE_VOLUME.format(
                local_path=env.log_file_name, container_path=env.original_log_file_name
            )
            pid_dir_volume = DOCKER_COMPOSE_VOLUME.format(
                local_path=env.pid_dir,
                container_path=env.original_pid_dir,
            )
            name = command.name
            container = name
            service = name
            hostname = name
            command.container = {"name": container, "service": service, "hostname": hostname}
            pip_user_flag = ""
            user_path = ""
            if env.docker_user:
                pip_user_flag = PIP_USER_FLAG
                user_path = USER_PATH
            service = DOCKER_COMPOSE_SERVICE.format(
                service_name=service, container_name=container, hostname=hostname,
                command=" ".join(command.full_command_line()),
                logfile=env.original_log_file_name,
                conf_volume=conf_volume,
                logs_volume=logs_volume,
                pid_dir_volume=pid_dir_volume,
                pip_user_flag=pip_user_flag, user_path=user_path,
            )
            if env.docker_user:
                service += DOCKER_COMPOSE_SERVICE_USER.format(user=env.docker_user)
            blocks.append(service)
            env._running_commands.add(command)
            command.hostname = hostname
        docker_compose_contents = "".join(blocks)
        docker_compose_file = os.path.join(env._workdir.name, "docker-compose.yml")
        with open(docker_compose_file, "w") as f:
            f.write(docker_compose_contents)
        env._manager = FTDocker(env._workdir.name)
        env._manager.up()
        # for command in env._running_commands:
        #     command.host = env._manager.ids(command.container["service"])[0]
        return env
        
    @staticmethod
    def __exit__(env, exc_type, exc_val, exc_tb):
        services = env._manager.ps()
        for command in env._running_commands:
            if command.container["service"] in services:
                command.exit_code = env._manager.exit_code(command.name)
                command.args = ("stop",)
                command(pre_exe=("docker", "exec", command.container["name"]))
        env._manager.down()

    @staticmethod
    def link_logfiles(env):
        # In the DockerFTEnvironment case I only need to create the logfile:
        open(env.log_file_name, "w").close()

    @staticmethod
    def output(env):
        env._manager.get_logs()
        output = env._manager.output
        all_lines = [_ for _ in output.split("\n")]
        output_lines = [_.split("|\x1b[0m ")[-1] for _ in all_lines]
        exit_code_lines = [_ for _ in all_lines if "exited with code" in _]
        output = "\n".join(output_lines+exit_code_lines)
        return output

    stderr = output

    
_FT_ENVIRONMENT_DICT = {
    DOCKER_FT_ENVIRONMENT: DockerFTEnvironmentType,
    LOCALHOST_FT_ENVIRONMENT: LocalhostFTEnvironmentType,
}
