# Standard
from enum import Enum
import os
import pickle
# Internal
from _paths import boxes_dir


class Hypervisor(Enum):
    SOFTWARE = 'software'
    MAC_HVF = 'hvf'
    LINUX_KVM = 'kvm'


class Architecture(Enum):
    ARM = 'arm'
    I386 = 'i386'
    X86_64 = 'x86_64'


class Box:
    def __init__(self, name, arch=Architecture.X86_64, cdrom=None,
            drives=None, hypervisor=Hypervisor.SOFTWARE, ram='512M'):
        self.name = name
        self.arch = arch
        self.cdrom = cdrom
        if drives is None:
            drives = {}
        self.drives = drives
        self.hypervisor = hypervisor
        self.ram = ram

    def get_command(self):
        # Use the appropriate QEMU command for the architecture
        command = 'qemu-system-' + str(self.arch.value)

        # Add CDROM
        cdrom = self.cdrom
        if cdrom:
            command += ' -cdrom ' + str(cdrom)

        # Add drives
        drives = self.drives
        for letter, path in drives:
            command += ' -hd' + letter + ' ' + path

        # Add hypervisor
        hypervisor = self.hypervisor
        hypervisor_is_hardware = hypervisor != Hypervisor.SOFTWARE
        if hypervisor and hypervisor_is_hardware:
            command += ' -accel ' + str(hypervisor.value)

        # Add RAM
        ram = self.ram
        if ram:
            command += ' -m ' + ram

        return command

    def get_path(self):
        return os.path.join(boxes_dir, self.name + '.qarl')

    def delete(self):
        box_path = self.get_path()
        os.remove(box_path)

    def load(self):
        # Load the pickled box from its file
        box_path = self.get_path()
        self.load_from(box_path)

    def load_from(self, path):
        # Load the pickled box from its file
        f = open(path, 'rb')
        pickled_box = pickle.load(f)
        f.close()

        # Update the box's values
        self.__dict__.update(pickled_box)

    def save(self):
        box_path = self.get_path()
        self.save_to(box_path)

    def save_to(self, path):
        # Save this box to its file
        f = open(path, 'wb')
        pickle.dump(self.__dict__, f, 2)
        f.close()

    def run(self):
        # Generate the startup command
        command = self.get_command()
        # Start the process and return its error code
        return os.system(command)


def box_exists(name):
    box = Box(name)
    box_path = box.get_path()
    return os.path.exists(box_path)


def create_box(name):
    box = Box(name)
    box.save()
    return box


def delete_box(name):
    box = Box(name)
    box.delete()


def load_box(name):
    box = Box(name)
    box.load()
    return box

def load_box_from(path):
    box = Box(None)
    box.load_from(path)
    return box
