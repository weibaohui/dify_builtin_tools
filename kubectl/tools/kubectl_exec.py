import json
from typing import Any, Union, ClassVar
import subprocess

from pydantic import ConfigDict

from core.tools.entities.tool_entities import ToolInvokeMessage
from core.tools.tool.builtin_tool import BuiltinTool


class KubectlExecTool(BuiltinTool):
    model_config = ConfigDict(ignored_types=(type(subprocess), type(json)))

    def _invoke(self,
                user_id: str,
                tool_parameters: dict[str, Any],
                ) -> Union[ToolInvokeMessage, list[ToolInvokeMessage]]:
        """
            invoke tools
        """
        # get text content
        command = tool_parameters.get('command', '')
        json_key = tool_parameters.get('json_key', '')
        if not command:
            return self.create_text_message('Invalid parameter command')
        # command = {\"result\": \"kubectl get pods -n default\\n```\"}
        # json_key = 'result'
        final_result = json.loads(command)[json_key]
        final_result = final_result.strip().replace("```", "").replace("\n", "").replace("\r", "")
        output = self.execute_command(final_result)
        return self.create_text_message(output)

    import subprocess

    @staticmethod
    def execute_command(command: str) -> str:
        """
        Execute a given binary command with arguments and return the output as a string.

        Parameters:
            command (str): The command to be executed.

        Returns:
            str: The output from the command execution.
        """

        try:
            # Using subprocess.run to execute the command
            result = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            # Returning the output
            return result.stdout
        except subprocess.CalledProcessError as e:
            # If an error occurs, returning the error message
            return f"An error occurred: {e.stderr}"
