# Tome Tracker

A Python-based personal library management tool that fetches book metadata via ISBN lookup and tracks reading progress.

## Overview

This project allows users to build and manage a personal book database by entering ISBNs. The application calls the Google Books API for book information and stores it in a PostgreSQL database, with a simple terminal-based interface for interaction.

**N.B.** this project is currently under development. The core functionality is operational, with plans for enhanced search capabilities and a web-based frontend under consideration.

## Current Features

- ISBN-based book lookup using Google Books API
- PostgreSQL database storage for book metadata
- Terminal interface for CRUD operations
- Read/unread book status tracking


## Planned Enhancements

 - Advanced search and filtering options
 - Web interface (with FastAPI and Jinja2)
 - Barcode scanning integration (with OpenCV)