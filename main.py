import click
import uvicorn

from tanks.server import create_server


@click.group()
def cli():
    pass


@click.command(help='Start the server')
@click.option('--release', is_flag=True, help='Run in release mode')
def server(release: bool):
    click.echo('Starting server...')

    app = create_server(debug=not release)
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8080,
        log_level='info',
    )


cli.add_command(server)

if __name__ == '__main__':
    cli()
