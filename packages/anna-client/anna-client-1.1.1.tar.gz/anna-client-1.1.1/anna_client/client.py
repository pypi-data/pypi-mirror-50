from graphqlclient import GraphQLClient, json
import requests

from anna_client import graphql


class Client(GraphQLClient):
	"""
	Wrapper around GraphQLClient
	"""

	def __init__(self, endpoint):
		super().__init__(endpoint)

	def query(self, query: str, variables: str) -> list:
		return json.loads(super().execute(query=query, variables=variables))

	def get_jobs(self, where: dict = None, fields: tuple = ('id',)) -> list:
		if where is None:
			where = {}
		query = graphql.get_jobs_query(where=where, fields=fields)
		response = super().execute(query=query)
		response = json.loads(response)
		if 'jobs' in response:
			return response['jobs']
		return response

	def create_jobs(self, data: list) -> tuple:
		ids = []
		for mutation in graphql.get_create_mutations(data):
			response = json.loads(super().execute(mutation))
			if 'createJob' in response and 'id' in response['createJob']:
				ids.append(response['createJob']['id'])
		return tuple(ids)

	def delete_jobs(self, where: dict = None) -> tuple:
		if where is None:
			where = {}
		mutation = graphql.get_delete_mutation(where=where)
		response = json.loads(super().execute(mutation))
		return response

	def update_jobs(self, where: dict = None, data: dict = None) -> tuple:
		mutation = graphql.get_update_mutation(where=where, data=data)
		response = json.loads(super().execute(mutation))
		return response

	def reserve_jobs(self, worker: str, job_ids: tuple):
		mutation = graphql.get_reserve_jobs_mutation(worker=worker, job_ids=job_ids)
		response = json.loads(super().execute(mutation))
		return response

	def get_tasks(self, namespace: str) -> tuple:
		response = requests.get(str(self.endpoint).replace('graphql', 'task/' + namespace))
		if response.status_code is not 200:
			raise ValueError(response.text)
		response = json.loads(json.loads(response.text))
		if len(response) is not 2:
			raise ValueError
		return response[0], response[1]
