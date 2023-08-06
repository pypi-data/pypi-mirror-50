# Standard
from argparse import ArgumentParser
import os
# Internal
from boxes import box_exists, create_box, delete_box, load_box, load_box_from
import _paths


# Create an argument parser
parser = ArgumentParser(
    prog='qarl',
    # usage='qarl <command> [options]',
    description='QARL - Qemu Automation that is Really Light-weight.',
    epilog='Copyright (c) 2019 Joseph (Jacy) Caruso'
)

# Add subparsers for sub-commands
subparsers = parser.add_subparsers(title='commands', metavar='Command', help='Description', dest='command')

# Subparser for `qarl add <box> <path>`
add_parser = subparsers.add_parser('add', help='add an box from a .qarl file')
add_parser.add_argument('path', help='path to the .qarl file')

# Subparser for `qarl command <box>`
command_parser = subparsers.add_parser('command', help='get the command used to start a box')
command_parser.add_argument('box', help='name of the box to create')

# Subparser for `qarl create <box>`
create_parser = subparsers.add_parser('create', help='create a new box')
create_parser.add_argument('box', help='name of the box to create')

# Subparser for `qarl eject-cd <box> <path>`
eject_cd_parser = subparsers.add_parser('eject-cd', help='eject a CDROM (.iso) into a box')
eject_cd_parser.add_argument('box', help='name of the box')

# Subparser for `qarl get <box>`
get_parser = subparsers.add_parser('get', help='get an attribute of a box')
get_parser.add_argument('box', help='name of the box')
get_parser.add_argument('attribute', help='the attribute to get')

# Subparser for `qarl insert-cd <box> <path>`
insert_cd_parser = subparsers.add_parser('insert-cd', help='insert a CDROM (.iso) into a box')
insert_cd_parser.add_argument('box', help='name of the box')
insert_cd_parser.add_argument('path', help='path to the CDROM file')

# Subparser for `qarl remove <box>`
remove_parser = subparsers.add_parser('remove', help='remove an existing box')
remove_parser.add_argument('box', help='name of the box to remove')

# DEPRECATED: Subparser for `qarl set <box>`
set_parser = subparsers.add_parser('set', help='set an attribute of a box')
set_parser.add_argument('box', help='name of the box')
set_parser.add_argument('attribute', help='the attribute to set')
set_parser.add_argument('value', help='the value to set the attribute to')

# Subparser for `qarl set-ram <box> <path>`
set_ram_parser = subparsers.add_parser('set-ram', help='change the amount of ram to allocate')
set_ram_parser.add_argument('box', help='name of the box')
set_ram_parser.add_argument('ram', help='the amount of ram to allocate')

# Subparser for `qarl start <box>`
start_parser = subparsers.add_parser('start', help='startup a box')
start_parser.add_argument('box', help='name of the box to start')

# Parse the arguments
args = parser.parse_args()

# Disect them into a more readable form
# command, box_name = args.command, args.box
command = args.command

if ('box' in args):
    box_name = args.box

# qarl add <path>
if command == 'add':
    # Load the box at the given path
    box = load_box_from(args.path)
    box.save()

elif command == 'command':
    # If the box already exists, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exist.")
        exit(1)

    # Load the box and print its startup command
    box = load_box(box_name)
    command = box.get_command()
    print(command)

# qarl <box> create
elif command == 'create':
    # If the box already exists, tell the user and exit with error code
    if box_exists(box_name):
        print("Box '" + box_name + "' already exists.")
        exit(1)

    # Create a box with the given name
    create_box(box_name)

# qarl eject-cd <box> <path>
elif command == 'eject-cd':
    # If the box already exists, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exist.")
        exit(1)

    # Load the box and set the CDROM
    box = load_box(box_name)
    box.cdrom = None
    box.save()

# qarl get <box> <attribute>
elif command == 'get':
    # If the box already exists, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exist.")
        exit(1)

    # Load the box
    box = load_box(box_name)

    # If it has the attribute, print it
    attribute = args.attribute
    try:
        value = getattr(box, attribute)
        print(value)
    except:
        print("Invalid attribute '" + attribute + "'")

# qarl insert-cd <box> <path>
elif command == 'insert-cd':
    # If the box already exists, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exist.")
        exit(1)

    # Load the box and set the CDROM
    box = load_box(box_name)
    box.cdrom = args.path
    box.save()

# qarl remove <box>
elif command == 'remove':
    # If the box doesn't exist, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exists.")
        exit(1)

    # Delete the box with the given name
    delete_box(box_name)

# DEPRECATED: qarl set <box> <attribute> <value>
elif command == 'set':
    # If the box already exists, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exist.")
        exit(1)

    # Load the box
    box = load_box(box_name)

    # If it has the attribute, print it
    attribute = args.attribute
    value = None
    exec('import boxes\nvalue = ' + args.value)
    try:
        previous_value = getattr(box, attribute)
        setattr(box, attribute, value)
        print(previous_value, '->', value)
        box.save()
    except:
        print("Invalid attribute '" + attribute + "'")

# qarl insert-cd <box> <path>
elif command == 'set-ram':
    # If the box already exists, tell the user and exit with error code
    if not box_exists(box_name):
        print("Box '" + box_name + "' does not exist.")
        exit(1)

    # Load the box and set the CDROM
    box = load_box(box_name)
    box.ram = args.ram
    box.save()

# qarl start <box>
elif command == 'start':
    box = load_box(box_name)
    box.run()

# qarl
else:
    parser.print_help()
