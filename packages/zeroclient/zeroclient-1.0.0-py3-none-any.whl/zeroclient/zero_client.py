# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""JSON RPC interface to Mobly Snippet Lib."""

from __future__ import print_function

from zeroclient import jsonrpc_client_base


class SnippetClient(jsonrpc_client_base.JsonRpcClientBase):
    """A client for interacting with snippet APKs using Mobly Snippet Lib.

    See superclass documentation for a list of public attributes.

    For a description of the launch protocols, see the documentation in
    mobly-snippet-lib, SnippetRunner.java.
    """

    def __init__(self):
        """Initializes a SnippetClient.

        Args:
            package: (str) The package name of the apk where the snippets are
                defined.
            ad: (AndroidDevice) the device object associated with this client.
        """
        super(SnippetClient, self).__init__()
        self._proc = None
        self.device_port = 8888

    @property
    def is_alive(self):
        """Is the client alive.

        The client is considered alive if there is a connection object held for
        it. This is an approximation due to the following scenario:

        In the USB disconnect case, the host subprocess that kicked off the
        snippet  apk would die, but the snippet apk itself would continue
        running on the device.

        The best approximation we can make is, the connection object has not
        been explicitly torn down, so the client should be considered alive.

        Returns:
            True if the client is considered alive, False otherwise.
        """
        return self._conn is not None

    def start_app_and_connect(self):
        """Starts snippet apk on the device and connects to it.

        This wraps the main logic with safe handling

        Raises:
            AppStartPreCheckError, when pre-launch checks fail.
        """
        try:
            self._start_app_and_connect()
        except Exception:
            # Precheck errors don't need cleanup, directly raise.
            raise
        except Exception as e:
            # Log the stacktrace of `e` as re-raising doesn't preserve trace.
            print('Failed to start app and connect.')
            # If errors happen, make sure we clean up before raising.
            try:
                self.stop_app()
            except Exception:
                print('Failed to stop app after failure to start and connect.')
            # Explicitly raise the original error from starting app.
            raise e

    def _start_app_and_connect(self):
        """Starts snippet apk on the device and connects to it.

        After prechecks, this launches the snippet apk with an adb cmd in a
        standing subprocess, checks the cmd response from the apk for protocol
        version, then sets up the socket connection over adb port-forwarding.

        Args:
            ProtocolVersionError, if protocol info or port info cannot be
                retrieved from the snippet apk.
        """
        # self.disable_hidden_api_blacklist()

        # persists_shell_cmd = self._get_persist_command()
        # Use info here so people can follow along with the snippet startup
        # process. Starting snippets can be slow, especially if there are
        # multiple, and this avoids the perception that the framework is hanging
        # for a long time doing nothing.
        self.log.info('_start_app_and_connect...')

        self.device_port = 8888

        self.connect()

        # Yaaay! We're done!
        print('...')

    def restore_app_connection(self, port=8888):
        """Restores the app after device got reconnected.

        Instead of creating new instance of the client:
          - Uses the given port (or find a new available host_port if none is
            given).
          - Tries to connect to remote server with selected port.

        Args:
          port: If given, this is the host port from which to connect to remote
              device port. If not provided, find a new available port as host
              port.

        Raises:
            AppRestoreConnectionError: When the app was not able to be started.
        """
        self.host_port = 8888
        # self._adb.forward(
        #     ['tcp:%d' % self.host_port,
        #      'tcp:%d' % self.device_port])
        try:
            self.connect()
        except Exception:
            # Log the original error and raise AppRestoreConnectionError.
            print('Failed to re-connect to app.')
            raise Exception("AA")

        # Because the previous connection was lost, update self._proc
        self._proc = None
        self._restore_event_client()

    def _start_event_client(self):
        """Overrides superclass."""
        event_client = SnippetClient()
        event_client.host_port = self.host_port
        event_client.device_port = self.device_port
        event_client.connect(self.uid,
                             jsonrpc_client_base.JsonRpcCommand.CONTINUE)
        return event_client

    def _restore_event_client(self):
        """Restores previously created event client."""
        if not self._event_client:
            self._event_client = self._start_event_client()
            return
        self._event_client.host_port = self.host_port
        self._event_client.device_port = self.device_port
        self._event_client.connect()
