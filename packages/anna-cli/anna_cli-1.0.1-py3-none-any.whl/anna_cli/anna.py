import click
import requests

remote = ''
token = ''


@click.group()
def cli():
	"""
	Simple CLI for querying books on Google Books by Oyetoke Toby
	"""
	pass


@cli.command()
@cli.argument('action')
@cli.argument('value')
def remote(action, value):
	global remote
	if action is 'set':
		remote = value
	elif action is 'get':
		click.echo(remote)
#[
#  {
#    "container": "799692e7f6",
#    "created_at": "Wed, 20 Feb 2019 22:03:00 GMT",
#    "driver": "chrome",
#    "id": 0,
#    "log": "",
#    "site": "lillynails",
#    "status": "running",
#    "tag": "chrome-lillynails-799692e7f6",
#    "updated_at": "Wed, 20 Feb 2019 22:03:01 GMT"
#  }
#]


@cli.command()
@cli.option('--id', '-i')
@cli.option('--container', '-c')
@cli.option('--driver', '-d')
@cli.option('--log', '-l')
@cli.option('--site', '-s')
@cli.option('--status', '-S')
@cli.option('--tag', '-t')
def get(id, container, driver, log, site, status, tag):
	pass




if __name__ == '__main__':
	cli()
