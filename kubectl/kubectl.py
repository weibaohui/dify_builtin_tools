from typing import Any

from core.tools.errors import ToolProviderCredentialValidationError
from core.tools.provider.builtin.kubectl.tools.kubectl_exec import KubectlExecTool
from core.tools.provider.builtin_tool_provider import BuiltinToolProviderController


class KubectlProvider(BuiltinToolProviderController):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            KubectlExecTool().invoke()
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
