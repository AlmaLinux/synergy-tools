# synergy-tools

Tools for managing and validating the [AlmaLinux Synergy](https://wiki.almalinux.org/repos/Synergy.html) repository.

## check_epel_synergy.py

Detects RPM packages that exist in both **EPEL** (Extra Packages for Enterprise Linux) and **AlmaLinux Synergy** repositories. This helps maintainers identify overlapping packages that could cause conflicts when both repos are enabled.

### Supported versions

- AlmaLinux / RHEL 8
- AlmaLinux / RHEL 9

### How it works

1. Fetches `repodata/repomd.xml` from EPEL and Synergy repos (x86_64 and aarch64)
2. Downloads and decompresses primary metadata (gzip or zstd)
3. Parses the XML to extract package names
4. Reports packages present in both repositories

### Usage

```bash
pip install -r requirements.txt
python3 check_epel_synergy.py
```

#### Example output

```
Package exists in both EPEL and Synergy for version 8: xapps-devel
Package exists in both EPEL and Synergy for version 9: some-package
```

If no overlaps are found:

```
No overlapping packages found in EPEL and Synergy repositories
```

### Adding a new version

Add the version number to `supported_versions` and the corresponding repo URLs to `epel_repos` and `synergy_repos` dictionaries in `check_epel_synergy.py`.

## Contributing

Please report issues or submit pull requests via the [GitHub issue tracker](https://github.com/AlmaLinux/synergy-tools/issues).

For questions, reach out to the [AlmaLinux Development](https://chat.almalinux.org/almalinux/channels/development) team.

## License

This project is licensed under the GNU General Public License v3.0. See [LICENSE](LICENSE) for details.
