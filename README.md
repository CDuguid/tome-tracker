# Tome Tracker

A Python-based personal library management tool that fetches book metadata via ISBN lookup and tracks reading progress.

## Overview

This project allows users to build and manage a personal book database by scanning barcodes for ISBNs or by manually entering them. The application calls the Google Books API for book information and stores it in a PostgreSQL database, with a simple terminal-based interface for interaction.

**N.B.** this project is currently under development. The core functionality is operational, with plans for enhanced search capabilities and a web-based frontend under consideration. No testing has been performed on Windows.

## Current Features

- ISBN-based book lookup using Google Books API
- PostgreSQL database storage for book metadata
- Barcode scanning integration (with OpenCV for image recognition)
- Terminal interface for CRUD operations
- Read/unread book status tracking

## Installation Notes
This project uses the pyzbar library, which in turn depends on the zbar shared library. Non-Windows installations will need to ensure that the zbar library is installed: see the Installation section [here](https://pypi.org/project/pyzbar/).

The main database needs to be initialised:
```
psql -f db/init_db.sql
```

If running the tests, the testing database will also need initialising:
```
psql -f db/init_test_db.sql
```


## Planned Enhancements

 - Advanced search and filtering options
 - Web interface (with FastAPI and Jinja2)
 - More advanced image recognition to identify books by their front covers
