"""Console script for picturebot."""
import sys
import os
import json
import click
import picturebot.helper as helper
import generalutils.guard as grd


def Location(path):
    click.echo(f'Config file location: {path}')

def Create(config):
#     #Check whether the workplace folder exists    
    grd.Filesystem.PathExist(config.Workplace)

#     #Loop-over the workflows
    for flow in config.Workflow:
        pathToFlow = helper.FullFilePath(config.Workplace,flow)
        helper.CreateFolder(pathToFlow)
        grd.Filesystem.PathExist(pathToFlow)

def Rename(config):
    # Get the current working directory of where the script is executed
    cwd = os.getcwd()

    # Check whether the current working directory exists
    grd.Filesystem.PathExist(cwd)

    # Obtain the name of the base directory of the current working directory
    basename = os.path.basename(cwd)

#     # Loop-ver the workflows and add an project directory to each flow
    for flow in config.Workflow:
#         # Obtain the path to the project flow
        pathToFlowProject = helper.FullFilePath(config.Workplace,flow,basename)

        helper.CreateFolder(pathToFlowProject)

        grd.Filesystem.PathExist(pathToFlowProject)

        print(f"Added folder: {pathToFlowProject}")

    print('\r\n')

    flow = ''
    counter = 0

#     # Loop over every word of the flow name directory
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

        # Rename the picture file
        os.rename(pathToPicture, pathToNewPicture)

        print(f"Renaming: {picture} -> {newName}")

        # Check whether the new picture file exists after renaming
        grd.Filesystem.PathExist(pathToNewPicture)

        counter += 1
    
    print(f"Renamed files: {counter}")

@click.command()
@click.option('--create', '-c', is_flag=True, help='Create workspace directory')
@click.option('--rename', '-r', is_flag=True, help='Rename the files in the main flow directory')
@click.option('--location', '-l', is_flag=True, help='Config file location')
# @pass_config
def main(create,rename, location):
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
    else:
        click.echo('No arguments were passed, please enter --help for more information')

if __name__ == "__main__":
    main()  # pragma: no cover