from dotenv import load_dotenv
from giza_actions.action import action, Action
from giza_actions.task import task
load_dotenv()

@task(name="pre process")
def preprocess():
    print(f"Preprocessing...")

@action(name="Action: dummy action", log_prints=True)
def execution():
    print("Starting dummy action")
    preprocess()
    print("Finishing dummy action")
    
if __name__ == "__main__":
    #action_deploy = Action(entrypoint=execution, name="pytorch-mnist-action")
    action_deploy = Action(entrypoint=execution, name="hello-world-action")
    action_deploy.serve(name="hello-world-action-deployment")
    #execution()