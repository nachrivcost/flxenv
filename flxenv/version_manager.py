import platform
import requests
import tarfile
import os
import shutil

FLUX_TAR_DIR = '/tmp/flux_releases'
FLUX_BIN_DIR = '~/flux/bin'
GITHUB_USER = 'fluxcd'
GITHUB_REPO = 'flux2'
github_repo_releases = f'https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases'
so = ""
arch = ""
release = ""
github_download_url = 'https://github.com/fluxcd/flux2/releases/download/v{release}/flux_{release}_{so}_{arch}.tar.gz'

# Returns the operating system
def get_operating_system():
    return platform.system().lower()

# Returns the architecture
def get_architecture():
    return platform.machine().lower()

# Constructs the download URL for the release
def get_github_download_url(release: str, so: str, arch: str):
    return github_download_url.format(release=release, so=so, arch=arch)

def get_flux_releases():
    # Make a Get request to the Github API
    response = requests.get(github_repo_releases)
    # If the request was successful
    if response.status_code == 200:
        # Return the content of the request
        json_data = response.json()
        releases = []
        for release in json_data:
            releases.append(release['tag_name'])
        return releases
    else:    
        # If the request was not successful, return an error message
        return f'Error: {response.status_code}'
    
# Check if the release is valid
def is_valid(releases, release):
    if f"v{release}" in releases:
        return True
    else:
        return False

def download_flux(release, so, arch, tmp_dir=FLUX_TAR_DIR):
    url = get_github_download_url(release, so, arch)
    mkdir_cmd = f'{os.path.expanduser(tmp_dir)}/{release}'
    print(f'Creating directory {mkdir_cmd}')
    # Check if the directory exists before creating it
    if not os.path.exists(mkdir_cmd):
        # Create the directory
        try:
            os.makedirs(mkdir_cmd)
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    # If the directory already exists, inform that the directory already exists

    print(f'Downloading {url} to {os.path.expanduser(tmp_dir)}/{release}/flux-v{release}.tar.gz')
    # Download the file from `url` and save it locally under `file_name`:
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        try:
            print(f'Opening {os.path.expanduser(tmp_dir)}/{release}/flux.tar.gz')
            with open(f'{os.path.expanduser(tmp_dir)}/{release}/flux.tar.gz', 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        except Exception as e: 
            print(f'Error: {e}')

def untar_flux(release, tmp_dir=FLUX_TAR_DIR, bin_dir=FLUX_BIN_DIR):
    # Check if the directory exists before creating it
    if not os.path.exists(os.path.expanduser(bin_dir)):
        # Create the directory
        try:
            os.makedirs(os.path.expanduser(bin_dir))
        except Exception as e:
            print(f'Error: {e}')
            exit(1)
    # Untar the file
    tar = tarfile.open(f'{os.path.expanduser(tmp_dir)}/{release}/flux.tar.gz', "r:gz")
    tar.extractall(path=f'{os.path.expanduser(tmp_dir)}/{release}')
    tar.close()
    print(f'Copying {os.path.expanduser(tmp_dir)}/{release}/flux to {os.path.expanduser(bin_dir)}/flux-v{release}')
    try:
        shutil.copy(f'{os.path.expanduser(tmp_dir)}/{release}/flux', f'{os.path.expanduser(bin_dir)}/flux-v{release}')
    except Exception as e:
        print(f'Error: {e}')
    
# Set version of flux to use in the PATH
def set_version(release, bin_dir=FLUX_BIN_DIR):
    # Try to remove the symlink if it exists
    print(f'Removing symlink {os.path.expanduser(bin_dir)}/flux')
    try:
        os.remove(f'{os.path.expanduser(bin_dir)}/flux')
    except Exception as e:
        print(f'Error: {e}')
    
    # Create the symlink
    print(f'Creating symlink {os.path.expanduser(bin_dir)}/flux-v{release} to {os.path.expanduser(bin_dir)}/flux')
    try:
        os.symlink(f'{os.path.expanduser(bin_dir)}/flux-v{release}', f'{os.path.expanduser(bin_dir)}/flux')
    except Exception as e:
        print(f'Error: {e}')

# Check if the release is installed
def is_installed(release, bin_dir=FLUX_BIN_DIR):
    bin_dir = os.path.expanduser(bin_dir)
    if os.path.exists(f'{bin_dir}/flux-v{release}'):
        return True
    else:
        return False

# List installed releases
def list_installed_releases(bin_dir=FLUX_BIN_DIR):
    # Expand the tilde manually
    bin_dir = os.path.expanduser(bin_dir)
    releases = []
    for file in os.listdir(bin_dir):
        if file.startswith('flux-v'):
            releases.append(file.split('-v')[1])
    return releases

#remove a release
def remove_release(release, bin_dir=FLUX_BIN_DIR):
    # Expand the tilde manually
    bin_dir = os.path.expanduser(bin_dir)
    release_path = os.path.join(bin_dir, f'flux-v{release}')
    if os.path.exists(release_path):
        try:
            if os.path.isdir(release_path):
                shutil.rmtree(release_path)
            else:
                os.remove(release_path)
            print(f'Release {release} removed')
        except Exception as e:
            print(f'Error: {e}')
    else:
        print(f'Error: {release} is not installed')

#remove all releases
def remove_all_releases(bin_dir=FLUX_BIN_DIR):
    # Expand the tilde manually
    bin_dir = os.path.expanduser(bin_dir)
    for file in os.listdir(bin_dir):
        if file.startswith('flux-v'):
            release = file.split('-v')[1]
            release_path = os.path.join(bin_dir, file)
            try:
                if os.path.isdir(release_path):
                    shutil.rmtree(release_path)
                else:
                    os.remove(release_path)
                print(f'Release {release} removed')
            except Exception as e:
                print(f'Error: {e}')
    print('All releases removed')

# Check if the version contains the letter 'v', if not, add it
def remove_v(release):
    if release[0] == 'v':
        release = release[1:]
    return release
