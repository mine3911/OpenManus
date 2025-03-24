import asyncio

from app.agent.manus import Manus
from app.logger import logger


# 定义主异步函数
async def main():
    # 创建Manus实例
    agent = Manus()
    try:
        # 提示用户输入提示信息
        prompt = input("请输入您的提示信息: ")
        # 检查输入是否为空
        if not prompt.strip():
            logger.warning("提供的提示信息为空。")
            return

        # 记录正在处理请求的日志
        logger.warning("正在处理您的请求...")
        # 调用agent的run方法处理请求
        await agent.run(prompt)
        # 记录请求处理完成的日志
        logger.info("请求处理完成。")
    except KeyboardInterrupt:
        # 记录操作被中断的日志
        logger.warning("操作被中断。")

# 检查是否作为主程序运行
if __name__ == "__main__":
    # 运行主异步函数
    asyncio.run(main())
