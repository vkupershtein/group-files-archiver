#!/usr/bin/env python3

"""
Group files archiver entry point
"""
from group_files_archiver.config import create_config
from group_files_archiver.utils import activate_logging, ensure_paths
from group_files_archiver.cli import run as cli_run

def main():
    """Main program function to archive files that belong to the same group"""
    config = create_config()
    ensure_paths(config)
    activate_logging(config)
    cli_run(config)
    

if __name__ == '__main__':
    main()