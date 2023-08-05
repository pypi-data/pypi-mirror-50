import click
import os

@click.command()
def install():
    project_name = click.prompt('Enter a project name')
    auth = click.prompt('Do you want user auth? (y/n)').lower()

    path = os.getcwd()
    install_path = f"{path}/{project_name}"

    if auth == 'y':
        url = 'https://github.com/XzavierDunn/restPlus.git'
    else:
        url = 'https://github.com/XzavierDunn/Flask-Template.git'

    print('\nGit cloning template')
    print('--------------------\n')

    os.system(f'git clone {url} {install_path}')

    print(f'\nInstall completed, Read the readme at {url}\n')

    remote = click.prompt('Would you like to change the git remote url (y/n)').lower()

    if remote == 'y':
        url = click.prompt("Enter your repo's url")
        os.chdir(project_name)
        os.system(f'git remote set-url origin {url}')
        print('Completed')
    else:
        pass

