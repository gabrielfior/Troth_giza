from dotenv import load_dotenv
from giza_actions.action import action, Action
from giza_actions.task import task

from verifiable_tg_bot.actions.async_bot import run

load_dotenv()

@task(name="pre process")
async def preprocess():
    print(f"Preprocessing...")
    yield "preprocess"

@action(name="Action: dummy action", log_prints=True)
async def execution():
    print("Starting bot run")
    await run()
    print("Finishing bot run")
    
if __name__ == "__main__":
    action_deploy = Action(entrypoint=execution, name="hello-world-async-action")
    action_deploy.serve(name="hello-world-async-action")
    #asyncio.run(execution())