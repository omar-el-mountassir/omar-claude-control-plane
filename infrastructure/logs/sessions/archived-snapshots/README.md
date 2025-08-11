# Archived Shell Snapshots

**Archive Date**: 2025-08-10  
**Purpose**: Archive old shell snapshot files to reduce directory clutter  

## Archive Policy

**Retention**: Keep recent 30 days of snapshots in active directory  
**Archive Location**: `temp/archived-snapshots/`  
**Cleanup Frequency**: Monthly  

## Snapshot File Format

Files follow pattern: `snapshot-bash-[timestamp]-[id].sh`  

- Timestamp: Unix timestamp in milliseconds
- ID: Random alphanumeric identifier

## Usage

These files contain bash command history and can be reviewed for:

- Command pattern analysis
- Historical workflow reconstruction  
- Debugging past session activities

Archive files can be safely deleted if storage space is needed.
