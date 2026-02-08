import click
from rich.console import Console
from cli.commands import upload, chat, search, manage

console = Console()

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """
    Local RAG System - CLI Version
    
    A privacy-friendly document search and chat system.
    """
    pass

# Register commands
cli.add_command(upload.upload)
cli.add_command(chat.chat)
cli.add_command(search.search)
cli.add_command(manage.manage)

if __name__ == '__main__':
    cli()