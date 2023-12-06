def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

start = 50
end = 100

print(f"Prime numbers between {start} and {end}:")
for num in range(start, end + 1):
    if is_prime(num):
        print(num)
        
"""
import datetime
import time

# Get the current time
start_time = datetime.datetime.now()

# Calculate the end time after 24 hours
end_time = start_time + datetime.timedelta(hours=4)

# Print continuously until the end time is reached
while datetime.datetime.now() < end_time:
    current_time = datetime.datetime.now()
    print(f"Current time: {current_time}")

    # Delay for 1 second before the next print
    time.sleep(1)
"""

"""
import os
import git
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep
from azureml.core import Workspace, Experiment, Environment, ScriptRunConfig
from azureml.core.compute import AmlCompute, ComputeTarget
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies

# Clone the GitHub repository to the Azure ML environment
repo_url = 'https://github.com/varun350/Sales-forecast-deployment-using-Flask-API.git'
target_directory = 'target_directory'
repo_path = os.path.join(target_directory, 'Sales-forecast-deployment-using-Flask-API')

# Check if the repository already exists; if not, clone it
if not os.path.exists(repo_path):
    git.Repo.clone_from(repo_url, repo_path)
    print(f"Repository cloned to: {repo_path}")
else:
    print(f"Repository already exists at: {repo_path}")

# Connect to the Azure ML workspace
ws = Workspace.from_config()
compute_target_name = 'test-forecast1'
# Get or create the compute target
try:
    compute_target = ComputeTarget(workspace=ws, name=compute_target_name)
    print(f'Using existing compute target: {compute_target_name}')
except:
    compute_config = AmlCompute.provisioning_configuration(vm_size='STANDARD_DS3_V2', max_nodes=1)
    compute_target = ComputeTarget.create(ws, compute_target_name, compute_config)
    compute_target.wait_for_completion(show_output=True)

env = Environment.get(workspace=ws, name="Environment_setup")
run_config = RunConfiguration()
run_config.target = compute_target
run_config.environment = env

# Create a PythonScriptStep using the specified environment
step = PythonScriptStep(
    script_name= 'Sales_Forecast.py',
    arguments=[],
    compute_target=compute_target,
    source_directory='target_directory/Sales-forecast-deployment-using-Flask-API',
    runconfig=run_config,
    allow_reuse=False
)

## Create a pipeline and run it
pipeline = Pipeline(workspace=ws, steps=[step])
experiment = Experiment(workspace=ws, name='default')
run = experiment.submit(pipeline)
run.wait_for_completion(show_output=True)
"""

