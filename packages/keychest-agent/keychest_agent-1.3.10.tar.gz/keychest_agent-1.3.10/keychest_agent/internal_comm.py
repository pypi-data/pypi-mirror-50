#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@keychest.net>, 2019
"""
import socket
import sys
import time
from threading import Thread

from keychest_agent.logger import logger
from keychest_agent.config import KCConfig

__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@keychest.net'
__status__ = 'Development'


def is_service_running():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the port where the server is listening
    server_address = ('localhost', KCConfig.config.internal_socket_2)

    # noinspection PyBroadException
    try:
        sock.connect(server_address)
        return True
    except:
        return False
    finally:
        sock.close()

def get_registration(force=False, staging=False, testing=False):
    """
    Connect to InternalComm server and get a registration ID
    :return:
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    server_address = ('localhost', KCConfig.config.internal_socket_2)

    try:
        sock.connect(server_address)

        command = "register"
        if force:
            command += " force"
        if staging:
            command += " staging"
        elif testing:
            command += " testing"

        # Send data
        sock.sendall(command.encode())

        data = sock.recv(4096)
        data_str = data.decode("utf-8")
        if len(data) < 8:
            return None
        else:
            return data_str
    except Exception as ex:
        sys.stderr.write("Error requesting registration, cause: %s" % str(ex))
        return None
    finally:
        sock.close()

class InternalComm(Thread):
    """
    A simple socket server that will listen to requests while running as service
    """
    def __init__(self, agent_object):

        super().__init__()
        self.agent_object = agent_object
        self._stopping = False

    def stop_now(self):
        self._stopping = True

    def run(self):
        logger.debug('KeyChest agent - internal TCP server')
        downstream_port = KCConfig.config.internal_socket_2

        bound = False
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while (not bound) and (not self._stopping):
            tries = 20
            while tries > 0 and not bound:
                try:
                    soc.bind(('localhost', downstream_port))
                    logger.debug('Internal socket bound. host:{0}, port:{1}'.
                                 format("localhost", downstream_port))
                    bound = True
                except socket.error:
                    soc.close()
                    tries -= 1
                    time.sleep(5)
                    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if not bound:
                logger.error("The port %d is used by another process" % downstream_port)
                # and we will keep trying

        # Start listening on socket
        soc.listen(16)  # default somaxconn

        while not self._stopping:
            try:
                soc.settimeout(0.5)  # we need to interrupt waiting
                conn, addr = soc.accept()

                # noinspection PyBroadException
                try:
                    data_raw = conn.recv(4096)

                    if len(data_raw) == 0:  # connection was closed
                        break
                    buffer_list = None
                    try:
                        # buffer_list.append(data_raw)
                        if buffer_list is None:
                            buffer_list = data_raw
                        else:
                            buffer_list += data_raw
                    except TypeError:
                        logger.info("Received data can't be converted to text - internal socket")
                        pass

                    # noinspection PyBroadException
                    try:
                        data = buffer_list.decode('utf-8')
                    except Exception:
                        data = ""

                    requests = data.split()
                    register = False
                    force = False
                    testing_env = False
                    staging_env = False
                    for _request in requests:
                        if _request.lower() == "register":
                            register = True
                        elif _request.lower() == "force":
                            force = True
                        elif _request.lower() == "testing":
                            testing_env = True
                        elif _request.lower() == 'staging':
                            staging_env = True

                    if register:
                        if KCConfig.config.agent_email.startswith("dummy") or force:
                            # preserve the logging option
                            local_log = KCConfig.config.do_local_log
                            default_cfg = KCConfig.default_config()
                            KCConfig.write_configuration(default_cfg)
                            KCConfig.config.do_local_log = local_log

                            # update environment
                            if staging_env:
                                default_cfg = KCConfig.default_config()
                                KCConfig.config.logging_server \
                                    = default_cfg.logging_server.replace("keychest.net", "a3.keychest.net")
                                if "a3.keychest.net" not in KCConfig.config.control_server:
                                    KCConfig.config.control_server \
                                        = default_cfg.control_server.replace("keychest.net", "a3.keychest.net")
                                KCConfig.write_configuration(KCConfig.config)
                            elif testing_env:
                                default_cfg = KCConfig.default_config()
                                KCConfig.config.logging_server \
                                    = default_cfg.logging_server.replace("https://keychest.net", "http://127.0.0.1")
                                KCConfig.config.control_server \
                                    = default_cfg.control_server.replace("http://keychest.net", "http://127.0.0.1")
                                KCConfig.write_configuration(KCConfig.config)

                            self.agent_object.do_registration()
                            pass

                        # let's send back the ID and the location of the config file
                        _response = KCConfig.config.agent_email + " " + KCConfig.get_config_file_path()
                        conn.sendall(_response.encode())
                except BaseException as ex:
                    logger.error("Base exception in internal socket server", cause=str(ex))
                    break
                except IOError:
                    break
                finally:
                    conn.close()

            # here we get on accept timeout
            except socket.timeout:
                pass
            except Exception as ex:
                logger.error("Unexpected exception in internal socket", cause=str(ex))
