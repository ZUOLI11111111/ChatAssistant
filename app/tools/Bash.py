import asyncio
import os
from typing import Optional
from app.tools.Exceptions import ToolError
from app.tools.Base import BaseTool, CLIResult

class BashSession:
    _started: bool
    _process: asyncio.subprocess.Process
    command: str = "/bin/bash"
    _output_delay: float = 0.2
    _timeout: float = 120.0
    _sentinel: str = "<<exit>>"

    def __init__(self):
        self._started = False
        self._time_out = False

    async def Start(self):
        if self._started:
            return 

        self._process = await asyncio.create_subprocess_shell(self.command, preexec_fn = os.setsid, shell=True,bufsize=0, stdin=asyncio.subprocess.PIPE, stdout = asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,)
        self._started = True

    def Stop(self):
        if not self._started:
            raise ToolError("Session has not started.")
        if self._process.returncode is not None:
            return 
        self._process.terminate()

    async def Run(self, command: str):
        if not self._started:
            raise ToolError("Session has srarted.")
        if self._process.returncode is not None:
            return CLIResult(system="tool must be restarted",error=f"bash has exited with returncode {self._process.returncode}",)
        if self._time_out:       
            raise ToolError(f"timed out: bash has not returned in {self._timeout} seconds and must be restarted.",)
        assert self._process.stdin
        assert self._process.stdout
        assert self._process.stderr
        self._process.stdin.write(command.encode()+f"; echo '{self._sentinel}'\n".encode())
        await self._process.stdin.drain()
        try:
            async with asyncio.timeout(self._timeout):
                while True:
                    await asyncio.sleep(self._output_delay)
                    output = (self._process.stdout._buffer.decode())
                    if self._sentinel in output:
                        output = output[: output.index(self._sentinel)]
                        break
        except asyncio.TimeoutError:
            self._time_out = True
            raise ToolError(f"timed out: bash has not returned in {self._timeout} seconds and must be restarted",) from None
        if output.endswith("\n"):
            output = output[:-1]

        error = (self._process.stderr._buffer.decode())
        if error.endswith("\n"):
            error = error[:-1]
        self._process.stdout._buffer.clear()
        self._process.stderr._buffer.clear()
        return CLIResult(output=output, error=error)

class Bash(BaseTool):
    name: str = "bash"
    description: str = """Execute a bash command in the terminal.
* Long running commands: For commands that may run indefinitely, it should be run in the background and the output should be redirected to a file, e.g. command = `python3 app.py > server.log 2>&1 &`.
* Interactive: If a bash command returns exit code `-1`, this means the process is not yet finished. The assistant must then send a second call to terminal with an empty `command` (which will retrieve any additional logs), or it can send additional text (set `command` to the text) to STDIN of the running process, or it can send command=`ctrl+c` to interrupt the process.
* Timeout: If a command execution result says "Command timed out. Sending SIGINT to the process", the assistant should retry running the command in the background.
"""
    parameters: dict = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The bash command to execute. Can be empty to view additional logs when previous exit code is `-1`. Can be `ctrl+c` to interrupt the currently running process.",
            },
        },
        "required": ["command"],
    }
    _session: Optional[BashSession] = None

    async def Execute(self, command: str | None = None, restart: bool = False, **kwargs) -> CLIResult:
        if restart:
            if self._session:
                self._session.Stop()
            self._session = BashSession()
            await self._session.Start()
            return CLIResult(system="tool has been restarted.")
        if self._session is None:
            self._session = BashSession()
            await self._session.Start()
        if command is not None:
            return await self._session.Run(command)
        raise ToolError("no command provided.")

if __name__=="__main__":
    bash=Bash()
    t = asyncio.run(bash.Execute("ls -l"))
    print(t)
