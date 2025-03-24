from pydantic import Field

from app.agent.browser import BrowserAgent
from app.config import config
from app.prompt.browser import NEXT_STEP_PROMPT as BROWSER_NEXT_STEP_PROMPT
from app.prompt.manus import NEXT_STEP_PROMPT, SYSTEM_PROMPT
from app.tool import Terminate, ToolCollection
from app.tool.browser_use_tool import BrowserUseTool
from app.tool.python_execute import PythonExecute
from app.tool.str_replace_editor import StrReplaceEditor


class Manus(BrowserAgent):
    """
    一个多功能的通用代理，使用规划来解决各种任务。

    该代理扩展了 BrowserAgent，包含了一组全面的工具和功能，
    包括 Python 执行、网页浏览、文件操作和信息检索，以处理各种用户请求。
    """

    name: str = "Manus"
    description: str = (
        "一个多功能的代理，可以使用多种工具解决各种任务"
    )

    system_prompt: str = SYSTEM_PROMPT.format(directory=config.workspace_root)
    next_step_prompt: str = NEXT_STEP_PROMPT

    max_observe: int = 10000
    max_steps: int = 20

    # 添加通用工具到工具集合
    available_tools: ToolCollection = Field(
        default_factory=lambda: ToolCollection(
            PythonExecute(), BrowserUseTool(), StrReplaceEditor(), Terminate()
        )
    )

    async def think(self) -> bool:
        """处理当前状态并根据适当上下文决定下一步操作。"""
        # 存储原始提示信息
        original_prompt = self.next_step_prompt

        # 仅检查最近的消息（最后3条）以检测浏览器活动
        recent_messages = self.memory.messages[-3:] if self.memory.messages else []
        browser_in_use = any(
            "browser_use" in msg.content.lower()
            for msg in recent_messages
            if hasattr(msg, "content") and isinstance(msg.content, str)
        )

        if browser_in_use:
            # 临时覆盖为浏览器特定提示以获取浏览器上下文
            self.next_step_prompt = BROWSER_NEXT_STEP_PROMPT

        # 调用父类的 think 方法
        result = await super().think()

        # 恢复原始提示信息
        self.next_step_prompt = original_prompt

        return result
