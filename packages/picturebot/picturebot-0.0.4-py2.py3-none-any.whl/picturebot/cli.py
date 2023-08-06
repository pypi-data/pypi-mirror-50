"""Console script for picturebot."""

import sys
import os
import json
import click
import picturebot as pb
import picturebot.helper as helper
import generalutils.guard as grd

def Location(path):
    '''Config file location method
    
    Args:
        path (string): Path to the config file
    '''

    click.echo(f'Config file location: {path}')

def Create(config):
    '''Setup the workspace method
    
    Args:
        config (Config): Config data object
    '''

    # Get the current working directory of where the script is executed
    cwd = os.getcwd()

    #Check whether the current working directory exists
    grd.Filesystem.PathExist(cwd)

    #Check whether the workplace folder exists    
    grd.Filesystem.PathExist(config.Workplace)

    # Only create the flow when the script is executed from the workspace directory
    if cwd == config.Workplace:
        #Loop-over the workflows
        for flow in config.Workflow:
            pathToFlow = helper.FullFilePath(config.Workplace, flow)
            helper.CreateFolder(pathToFlow)
            grd.Filesystem.PathExist(pathToFlow)
            click.echo(f'Flow created: {pathToFlow}')
    else:
        click.echo(f'Script command should be called from the workspace directory: {config.Workplace}')

def Rename(config):
    '''Method to rename files within the baseflow directory
    
    Args:
        config (Config): Config data object
    '''

    # Get the current working directory of where the script is executed
    cwd = os.getcwd()

    # Check whether the current working directory exists
    grd.Filesystem.PathExist(cwd)

    # Obtain the name of the base directory of the current working directory
    basename = os.path.basename(cwd)
    
    # Obtain the path to the base flow project
    pathToBaseflowProject = helper.FullFilePath(config.Workplace, config.Baseflow, basename)
    # Check whether the the path to the base flow project exists
    grd.Filesystem.PathExist(pathToBaseflowProject)

    # Only rename filenames within a baseflow project directory
    if cwd == pathToBaseflowProject:
        # Loop-ver the workflows and add an project directory to each flow
        for flow in config.Workflow:
            # Obtain the path to the project flow
            pathToFlowProject = helper.FullFilePath(config.Workplace,flow,basename)

            # Check if folder exists ...
            if not grd.Filesystem.IsPath(pathToFlowProject):
                helper.CreateFolder(pathToFlowProject)

                grd.Filesystem.PathExist(pathToFlowProject)

                click.echo(f'Project created: {pathToFlowProject}')

        print('\r\n')
    else:
        click.echo(f'Script command should be called from the baseflow directory: {pathToBaseflowProject}')

    flow = ''
    counter = 0

    # Loop over every word of the flow name directory
    for i in basename.split(' '):
        # Append the individual words to an '_'
        flow += f'{i}_'

    # Obtain the original picture name within a flow directory
    pictures = os.listdir(cwd)
    # sort by date
    pictures.sort(key=os.path.getmtime)

    # Loop over every picture withing the flow directory
    for index, picture in enumerate(pictures, 1):
        # Get the extension of the original picture
        extension = picture.split('.')[1]

        # Get absolute path to the picture
        pathToPicture = os.path.join(cwd,picture)

        # Check whether the absolute path to the picture is existing
        grd.Filesystem.PathExist(pathToPicture)

        # Get the new name for the picture
        newName = f"{flow}{index}.{extension}"

        # Obtain the absolute path to the new picture name
        pathToNewPicture = os.path.join(cwd, newName)

        # Only rename the changed files
        if not pathToNewPicture == pathToPicture:
            # Rename the picture file
            os.rename(pathToPicture, pathToNewPicture)

            click.echo(f"Renaming: {picture} -> {newName}")

            # Check whether the new picture file exists after renaming
            grd.Filesystem.PathExist(pathToNewPicture)

            counter += 1

    click.echo(f"Renamed files: {counter}")

def Version():
    '''Method which prints the current script version'''

    click.echo(f'Script version: {pb.__version__}')
   
@click.command()
@click.option('--create', '-c', is_flag=True, help='Create workspace directory')
@click.option('--rename', '-r', is_flag=True, help='Rename the files in the main flow directory')
@click.option('--location', '-l', is_flag=True, help='Config file location')
@click.option('--version', '-v', is_flag=True, help='Script version')
def main(create,rename, location, version):
    """Console script for picturebot."""
    
    pathToConfig = helper.FullFilePath("config.json")
    
    # Check whether the path to the confile exists
    grd.Filesystem.PathExist(pathToConfig)

    with open(pathToConfig) as f:
         # Load data from file
        data = json.load(f)
        config = helper.Config(data['workplace'], data['workflow'], data['baseflow'])

    if create:
        Create(config)
    elif rename:
        Rename(config)
    elif location:
        Location(pathToConfig)
    elif version:
        Version()
    else:
        click.echo('No arguments were passed, please enter --help for more information')

if __name__ == "__main__":
    main() # pragma: no cover
