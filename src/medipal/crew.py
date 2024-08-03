from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# Uncomment the following line to use an example of a custom tool
# from medipal.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

from crewai_tools import tool 
from langchain_groq import ChatGroq
# from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyMuPDFLoader
import os
# llm = ChatGroq(
# 	model='mixtral-8x7b-32768',
# 	temperature=0,
# 	api_key='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'
# )
@tool('PDF search Tool')
def pdf_search_tool():
	"""useful for searching PDFs"""
	return PyMuPDFLoader("./medicalbill.pdf").load()

@CrewBase
class MedipalCrew():
	"""Medipal crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	#pdf_search_tool:any



	def __init__(self) -> None:
		filename = os.path.basename("./medicalbill.pdf")
		# file_path = os.path.basename(filename)
		# self.pdf_search_tool = PDFSearchTool(pdf="https://github.com/invoice-x/invoice2data/blob/master/tests/compare/NetpresseInvoice.pdf")
		# loader =  PyPDFLoader("./medicalbill.pdf")
		# loader = PyPDFLoader("https://arxiv.org/pdf/1706.03762")
		# self.pdf_search_tool = PyMuPDFLoader("https://arxiv.org/pdf/1706.03762").load()
		# pages = loader.load_and_split()
		# data = loader.load()
		# data[0]
		# docs = loader.load()
		# console.log({ docs });
	
	@agent
	def Bill_Agent(self) -> Agent:
		return Agent(
			config=self.agents_config['Bill_Agent'],
			verbose=True,
			tools=[pdf_search_tool],
			# tools = [self.get_text()]
			# llm=llm
		)

	@agent
	def Call_Agent(self) -> Agent:
		return Agent(
			config=self.agents_config['Call_Agent'],
			verbose=True,
			tools=[pdf_search_tool],
			# tools = [self.get_text()]
			# llm=llm
		)

	@task
	def bill_task(self) -> Task:
		return Task(
			config=self.tasks_config['bill_task'],
			agent=self.Bill_Agent()
		)

	@task
	def call_task(self) -> Task:
		return Task(
			config=self.tasks_config['call_task'],
			agent=self.Call_Agent(),
			output_file='report.md'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Medipal crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)