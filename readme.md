to run the app follow this command in FORESIGHT_PROJECT FOLDER:
 streamlit run app.py 

makesure u have python 3.11.
If not then follow this:
on your current venv, >>deactivate  
>>Remove-Item -Recurse -Force .venv
>>uv venv --python 3.11 .venv
 .\.venv\Scripts\Activate.ps1                                                                    
>> `                                                                                                     
>> uv pip install --link-mode=copy -r requirements.txt     
