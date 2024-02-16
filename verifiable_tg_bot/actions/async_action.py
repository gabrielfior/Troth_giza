import asyncio

from dotenv import load_dotenv
from giza_actions.action import action, Action

from verifiable_tg_bot.actions.async_bot import run

load_dotenv()

@action(name="Action: dummy action", log_prints=True)
async def execution():
    print("Starting bot run")
    await run()
    print("Finishing bot run")
    
if __name__ == "__main__":
    action_deploy = Action(entrypoint=execution, name="verifiable-ml-bot")
    action_deploy.serve(name="verifiable-ml-local-execution")
    #asyncio.run(execution())