import argparse
from . import version_manager

def main():
    parser = argparse.ArgumentParser(description='Flux Environment Manager')
    
    # Add arguments to your CLI
    parser.add_argument('--list', action='store_true', help='List available Flux versions')
    parser.add_argument('--list-installed', action='store_true', help='List installed Flux versions')
    parser.add_argument('--install', type=str, metavar='VERSION', help='Install a Flux version')
    parser.add_argument('--set-version', type=str, metavar='VERSION', help='Set the Flux version')
    parser.add_argument('--remove', type=str, metavar='VERSION', help='Remove a Flux version')
    parser.add_argument('--remove-all', action='store_true', help='Remove all Flux versions')

    
    args = parser.parse_args()
    
    # List available Flux versions
    if args.list:
        for release in version_manager.get_flux_releases():
            print(release)
    
    if args.install:
        print(f'Installing version {args.install}')
        release = args.install
        # Check if the version passed as an argument starts with the letter 'v'
        if release[0] == 'v':
            release = release[1:]
        
        # Check if the version is already installed
        if version_manager.is_installed(release):
            print(f'Version {release} is already installed')
            exit(0)
        
        # Get the operating system and architecture
        so = version_manager.get_operating_system()
        arch = version_manager.get_architecture()
       
        if version_manager.is_valid(version_manager.get_flux_releases(), release):
            version_manager.download_flux(release, so, arch)
            version_manager.untar_flux(release)
            version_manager.set_version(release)
        else:
            print(f'Error: {release} is not a valid release')
    
    if args.set_version:
        print(f'Setting version {args.set_version}')
        release = args.set_version
        # Remove the letter 'v' from the release
        release = version_manager.remove_v(release)
        # Check if the release is valid
        if version_manager.is_valid(releases=version_manager.get_flux_releases(), release=release):
            # Check if the release is installed
            if version_manager.is_installed(release):
                version_manager.set_version(release)
            else:
                print(f'Error: {release} is not installed')
        else:
            print(f'Error: {release} is not a valid release')
    
    if args.list_installed:
        print('Installed Flux versions:')
        for release in version_manager.list_installed_releases():
            print(release)
    
    if args.remove:
        print(f'Removing version {args.remove}')
        release = args.remove
        # Remove the letter 'v' from the release
        release = version_manager.remove_v(release)
        # Check if the release is installed
        if version_manager.is_installed(release):
            version_manager.remove_release(release)
        else:
            print(f'Error: {release} is not installed')

    if args.remove_all:
        print('Removing all versions')
        version_manager.remove_all_releases()
    

    if not any(vars(args).values()):
        parser.print_help()

if __name__ == "__main__":
    main()
