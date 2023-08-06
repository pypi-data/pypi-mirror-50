#!/usr/local/bin/python3

import click
import json

from group import Anna
import persist
from anna_client.client import Client

client = Client(endpoint=persist.get('endpoint'))
client.inject_token(persist.get('token'))


@click.group(Anna)
def cli():
	"""
	CLI for the anna API   github.com/patrikpihlstrom/anna-api.git
	"""
	pass


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('action')
@click.argument('endpoint', required=False)
def endpoint(action, endpoint=None):
	"""
	get or set the endpoint
	:param action:
	:param endpoint:
	:return:
	"""
	if action == 'set':
		persist.set('endpoint', endpoint)
	elif action == 'get':
		click.echo(persist.get('endpoint'))


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('action')
@click.argument('token', required=False)
def token(action, token=None):
	"""
	get or set the token
	:param action:
	:param token:
	:return:
	"""
	if action == 'set':
		persist.set('token', token)
	elif action == 'get':
		click.echo(persist.get('token'))


def is_json(string):
	try:
		json.loads(string)
	except ValueError:
		return False
	except TypeError:
		return False
	return True


def echo(response):
	if hasattr(response, 'content'):
		if is_json(response.content):
			click.echo(json.dumps(response.json(), indent=4, sort_keys=True))
		else:
			click.echo(response.content)
	else:
		click.echo(json.dumps(response, indent=4, sort_keys=True))


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--drivers', '-d', default=[])
@click.option('--sites', '-s', default=[])
def push(drivers, sites):
	"""
	push a new job to the queue
	:param drivers:
	:param sites:
	:return:
	"""
	jobs = []
	drivers = drivers.split(',')
	sites = sites.split(',')
	if isinstance(drivers, str):
		drivers = [drivers]
	if isinstance(sites, str):
		sites = [sites]

	for driver in drivers:
		for site in sites:
			jobs.append({'site': site, 'driver': driver})
	response = client.create_jobs(data=jobs)
	echo(response)


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--id', '-i', default=[])
@click.option('--container', '-c', default=[])
@click.option('--driver', '-d', default=[])
@click.option('--site', '-s', default=[])
@click.option('--status', '-S', default=[])
def get(id, container, driver, site, status):
	"""
	get jobs based on the provided filter
	:param id:
	:param container:
	:param driver:
	:param site:
	:param status:
	:return:
	"""
	where = {}
	if len(id) > 0:
		where['id_in'] = id
	if len(container) > 0:
		where['container_in'] = container
	if len(driver) > 0:
		where['driver_in'] = driver
	if len(site) > 0:
		where['site_in'] = site
	if len(status) > 0:
		where['status_in'] = status
	response = client.get_jobs(
		where=where, fields=('id', 'site', 'driver', 'status', 'updatedAt', 'container', 'log'))
	echo(response)


@cli.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--id', '-i', default=[])
@click.option('--container', '-c', default=[])
@click.option('--driver', '-d', default=[])
@click.option('--site', '-s', default=[])
@click.option('--status', '-S', default=[])
def rm(id, container, driver, site, status):
	"""
	get jobs based on the provided filter
	:param id:
	:param container:
	:param driver:
	:param site:
	:param status:
	:param tag:
	:return:
	"""
	where = {}
	if len(id) > 0:
		where['id_in'] = id
	if len(container) > 0:
		where['container_in'] = container
	if len(driver) > 0:
		where['driver_in'] = driver
	if len(site) > 0:
		where['site_in'] = site
	if len(status) > 0:
		where['status_in'] = status
	response = client.delete_jobs(
		where=where)
	echo(response)


if __name__ == '__main__':
	cli()
