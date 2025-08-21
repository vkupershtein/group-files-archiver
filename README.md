# Group Files Archiver

**Group Files Archiver** is a Python-based command-line utility for archiving files that belong to all members of a given Linux user group.
It can either **move** or **copy** files to an archive folder and then compress them into an archive.
The program is designed to be robust against multiple invocations and logs its operations.

---

## Installation

### From Debian source package

1. Clone git repository:

   ```bash
   git clone https://github.com/vkupershtein/group-files-archiver.git
   ```

2. Build the `.deb` package from source with script:

   ```bash
   cd group-files-archive
   ./build_deb.sh
   ```

   This will produce a `.deb` file in the parent directory.

3. Install the package:

   ```bash
   cd ..
   sudo apt install ./group-files-archiver_0.1.0-1_all.deb
   ```

---

## Files and Directories

After installation, the package provides:

* **Executable**: `/usr/bin/group-files-archiver`
* **Logs**: `/var/log/group-files-archiver/group-files-archiver.log`
* **Archives**: `/var/lib/group-files-archiver/archives`
* **Locks**: `/var/lib/group-files-archiver/locks`

> In development (when running directly with `python3 main.py`), the program defaults to relative paths:
>
> * `log/group-files-archiver.log`
> * `archive/`
> * `locks/`

---

## Usage

Run the tool with the name of a Linux group:

```bash
sudo group-files-archiver <groupname> [options]
```

### Options

* `-c`, `--copy-files`
  Copy files instead of moving them.

* `--archive-location PATH`
  Override the default archive directory.

* `--input-paths PATH [PATH ...]`
  Directories to scan for files (default: `/home`).

### Example

Move all files belonging to group **developers** into the archive:

```bash
sudo group-files-archiver developers
```

Copy files from `/srv/data` into a custom archive location:

```bash
sudo group-files-archiver developers -c \
  --archive-location /mnt/backup/dev-team \
  --input-paths /srv/data
```

---

## Logging

All actions and errors are logged to:

```
/var/log/group-files-archiver/group-files-archiver.log
```

---

## Notes

* Requires Python **≥3.8**.
* Root privileges are necessary
* Locking ensures that only **one archive process per group and per user** can run at a time. Different groups can be archived in parallel.
