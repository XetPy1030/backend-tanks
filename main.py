import click
import pytest
import uvicorn

from tanks.server import create_server


@click.group()
def cli():
    pass


@click.command(help='Start the server')
@click.option('--release', is_flag=True, help='Run in release mode')
@click.option('--log-level', default='info', help='Log level')
def server(release: bool, log_level: str):
    click.echo('Starting server...')

    app = create_server(debug=not release)
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=8080,
        log_level=log_level,
    )


@click.command(help='Run the tests')
@click.option('--enable-warnings', is_flag=True, help='Enable warnings')
def tests(enable_warnings: bool):
    click.echo('Running tests...')

    args = ['-v', 'tests']
    if not enable_warnings:
        args.append('--disable-warnings')
    pytest.main(args)


cli.add_command(server)
cli.add_command(tests)

if __name__ == '__main__':
    cli()
