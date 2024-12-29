# Employee Feedback Analysis Portal

## About the Code

* sentiment.py : Load the feedback, acquire and save responses from ChatGPT.
* analyse_results.py : Process response from ChatGPT, create graphs and output final results files.
* var.py: Holds system prompt for GPT.
* get_jsons.py: Flask backend to return json results for interface to consume.
* make_interface.py: Create the web interface.

## Other files/folders
* /data: Holds the data sources.
* /graphs: Holds output graphs.
* /summaries: Holds text summaries of results.
* /templates: Holds the html templates.

## Notes to run
* pip install requirements.txt
* For AI analysis: Create a .env file with the parameter OPEN_AI_API_KEY .
* For website: TBD.

## About the Site

* Landing Page: Navigate to either mental health or special belief graphs for all employees.\
Select a specific employee to view a comprehensive summary for.
![alt text](image.png)

* View a two sentence summary of the employee's feedback, focusing on mental health and specific beliefs. Also includes mental health graphs and word cloud of specific beliefs. ![](image-1.png)

## Things that would have been nice to include
* More attractive formatting of website.
* Page that highlights employees that may be at severe mental health risk.