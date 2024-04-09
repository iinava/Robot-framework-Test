import json
import subprocess
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def execute_tests(request):
    if request.method == 'POST':
        try:
            
            #retriving data from json request body
            
            data = json.loads(request.body)
            tests = data.get('tests', [])
            
            # generating .robots file for tests from recived data
            
            Robot_File = Generate_Robot_Test(tests)
            
            #executing robot file using subprocess
            
            Test_Results = Execute_Robot_Test(Robot_File)
            
            print(Test_Results,"this are the results")
            
            #returning  test results and status
            
            if 'error' in Test_Results:
                return JsonResponse(Test_Results, status=500)
            else:
                return JsonResponse({'status': 'success', 'results': Test_Results})
            
        except json.JSONDecodeError as e:
            logger.error("Error decoding JSON: %s", e)
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            logger.error("Error executing tests: %s", e)
            return JsonResponse({'error': 'Failed to execute tests'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are supported'}, status=405)


def Generate_Robot_Test(tests):
    
    #configure path for saving file with robot commands
    
    OutputDir = 'robot_suits'
    os.makedirs(OutputDir, exist_ok=True)
    Robot_File_path = os.path.join(OutputDir, 'generated_tests.robot')
    
    
    #template for generating test commands

    Testcase_Template = """
*** Settings ***
Library    SeleniumLibrary

*** Test Cases ***
{title}
{commands}
"""
  #writng the file 
  
    with open(Robot_File_path, 'w') as file:
        for test in tests:
            title = test.get('title', 'Untitled Test')
            commands = "\n".join(["    "+step for step in test.get('steps', [])])
            Testcase_content = Testcase_Template.format(title=title, commands=commands)
            file.write(Testcase_content)

    return Robot_File_path


def Execute_Robot_Test(Robot_File):
    try:
        #Executing the robot test commands using subprocess,return result
        
        result = subprocess.run(['robot', Robot_File], capture_output=True, text=True, check=True)
        Test_Results = result.stdout
        return Test_Results
    except subprocess.CalledProcessError as e:
        logger.error("Robot Framework execution failed with exit code %s: %s", e.returncode, e.output)
        return {'error': f'Robot Framework execution failed with exit code {e.returncode}: {e.output}'}
    except Exception as e:
        logger.error("Error executing test suite: %s", e)
        return {'error': 'Failed to execute test suite'}

