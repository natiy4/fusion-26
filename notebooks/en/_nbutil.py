"""Shared helpers for building the FUSION Boot Camp 2026 notebook series."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def md(*lines):
    """Markdown cell from a list of source lines."""
    text = "\n".join(lines)
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(keepends=True)}


def code(*lines):
    """Code cell from a list of source lines."""
    text = "\n".join(lines)
    return {
        "cell_type": "code",
        "metadata": {},
        "execution_count": None,
        "outputs": [],
        "source": text.splitlines(keepends=True),
    }


def write_notebook(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    path = os.path.join(HERE, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=1)
    print("wrote", path, "(%d cells)" % len(cells))
