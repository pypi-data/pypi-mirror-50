# jupyterlab-hdf5

Open and explore HDF5 files in Jupyterlab.

![hdf_preview](README.png)

Currently in late alpha. Basic functionality has been achieved!

## Installation

For a development install (currently the only option), do the following in the repository directory:

```bash
pip install .
jlpm build:dev
```

To watch for/rebuild on changes to this extension's source code, run:

```bash
jlpm run build:watch
```

## What's in this extension

This extension has two parts: an hdf5 filebrowser, and an hdf5 dataset file type.

### HDF5 Filebrowser

Allows you to navigate an `.hdf5` file's groups as though they were directories in a filesystem. Any `.hdf5` file on a user's system can be opened by entering its path (relative to the Jupyterlab home directory) in the box at the top of the browser.

### HDF5 dataset file type

When you open a dataset using the hdf5 filebrowser, a document will open that displays the contents of the dataset via a grid.

## Status of the latest version

- filebrowser

  - works well, and allows you to open datasets via a double click. Some minor UI issues remain (mostly with the breadcrumbs and the `.hdf5` path input box).

- dataset file type
  - currently, only the first 100x100 chunk of a dataset will load. The next goal of development is to enable dynamic loading of the rest of a dataset's chunks.
