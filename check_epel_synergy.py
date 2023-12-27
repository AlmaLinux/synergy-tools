# This script checks if a package exists in both EPEL and Synergy repos for a given version
# Usage: python3 check_epel_synergy.py
# Example of output "Package exists in both EPEL and Synergy for version 8: xapps-devel"

# To add a new version, add the version number to supported_versions list
# and add the repo links to epel_repos and synergy_repos dictionaries

import logging
import urllib.request
import requests
import xml.etree.ElementTree as ET
import gzip

supported_versions = [8, 9]

epel_repos = {
    8: [
        "https://dl.fedoraproject.org/pub/epel/8/Everything/x86_64/",
        "https://dl.fedoraproject.org/pub/epel/8/Everything/aarch64/"
    ],
    9: [
        "https://dl.fedoraproject.org/pub/epel/9/Everything/x86_64/",
        "https://dl.fedoraproject.org/pub/epel/9/Everything/aarch64/"

    ]
}

synergy_repos = {
    8: [
        "https://repo.almalinux.org/almalinux/8.9/synergy/x86_64/os/",
        "https://repo.almalinux.org/almalinux/8.9/synergy/aarch64/os/",
    ],
    9: [
        "https://repo.almalinux.org/almalinux/9.3/synergy/x86_64/os/",
        "https://repo.almalinux.org/almalinux/9.3/synergy/aarch64/os/",
    ]
}

logging.basicConfig(level=logging.INFO)

def get_primary_file_location(repo_link):
    try:
        repomd = requests.get(urllib.parse.urljoin(repo_link, 'repodata/repomd.xml'))
        repomd.raise_for_status()
        root = ET.fromstring(repomd.text)
        for child in root:
            if child.attrib and 'primary' == child.attrib['type']:
                for child1 in child:
                    if 'location' in child1.tag:
                        return child1.attrib['href']
    except requests.RequestException as e:
        logging.error(f"Error fetching repomd.xml: {e}")
    return None

def download_and_extract_primary(repo_link, primary_filename):
    try:
        primary = requests.get(urllib.parse.urljoin(repo_link, primary_filename))
        primary.raise_for_status()
        return gzip.decompress(primary.content)
    except requests.RequestException as e:
        logging.error(f"Error downloading primary file: {e}")
    return None

def parse_primary_xml(primary_data):
    file_list = []
    root = ET.fromstring(primary_data)
    for rpm in root:
        if 'package' in rpm.tag and rpm.attrib['type'] == 'rpm':
            for rpm_data in rpm:
                tag = rpm_data.tag.replace('{http://linux.duke.edu/metadata/common}', '')
                if 'name' == tag:
                    file_list.append(rpm_data.text)
                    break
    return file_list

def get_file_list(repo_list):
    file_list = []
    for repo_link in repo_list:
        # logging.info(f'Getting metadata from {repo_link}')
        primary_location = get_primary_file_location(repo_link)
        if primary_location:
            primary_data = download_and_extract_primary(repo_link, primary_location)
            if primary_data:
                file_list.extend(parse_primary_xml(primary_data))
    return file_list

def main():
    interserctions_found = False
    for version in supported_versions:
        epel_rpms = get_file_list(epel_repos[version])
        synergy_rpms = get_file_list(synergy_repos[version])
        common_packages = set(epel_rpms).intersection(synergy_rpms)
        for package in common_packages:
            interserctions_found = True
            print(f"Package exists in both EPEL and Synergy for version {version}: {package}")
    if not interserctions_found:
        print("No packages found in both EPEL and Synergy repos")

if __name__ == '__main__':
    main()
