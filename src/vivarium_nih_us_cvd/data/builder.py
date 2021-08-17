"""Modularized functions for building project data artifacts.

This module is an abstraction around the load portion of our artifact building ETL pipeline.
The intent is to be declarative so it's easy to see what is put into the artifact and how.
Some degree of verbosity/boilerplate is fine in the interest of transparancy.

.. admonition::

   Logging in this module should be done at the ``debug`` level.

"""
from pathlib import Path
from typing import Union

from loguru import logger
import pandas as pd
from vivarium.framework.artifact import Artifact, EntityKey

from vivarium_nih_us_cvd.constants import data_keys
from vivarium_nih_us_cvd.data import loader


def open_artifact(output_path: Path, location: str) -> Artifact:
    """Creates or opens an artifact at the output path.

    Parameters
    ----------
    output_path
        Fully resolved path to the artifact file.
    location
        Proper GBD location name represented by the artifact.

    Returns
    -------
        A new artifact.

    """
    if not output_path.exists():
        logger.debug(f"Creating artifact at {str(output_path)}.")
    else:
        logger.debug(f"Opening artifact at {str(output_path)} for appending.")

    artifact = Artifact(output_path)

    key = data_keys.METADATA_LOCATIONS
    if key not in artifact:
        artifact.write(key, [location])

    return artifact


def load_and_write_data(artifact: Artifact, key: Union[str, data_keys.SourceSink], location: str):
    """Loads data and writes it to the artifact if not already present.

    Parameters
    ----------
    artifact
        The artifact to write to.
    key
        The entity key associated with the data to write.
    location
        The location associated with the data to load and the artifact to
        write to.

    """
    if isinstance(key, data_keys.SourceSink):
        source = key.source
        sink = key.sink
    else:
        source = sink = key

    if sink in artifact:
        logger.debug(f'Data for {sink} already in artifact.  Skipping...')
    else:
        logger.debug(f'Loading data for {source} for location {location}.')
        data = loader.get_data(key, location)
        logger.debug(f'Writing data for {source} to artifact at location {sink}.')
        artifact.write(sink, data)
    return artifact.load(sink)


def handle_special_cases(artifact: Artifact, location: str):
    loader.handle_special_cases(artifact, location)