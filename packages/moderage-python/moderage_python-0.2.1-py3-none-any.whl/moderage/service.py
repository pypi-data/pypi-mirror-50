import yaml
import magic
from pathlib import Path
import logging

from moderage.clients import LocalClient, ServerClient
from moderage.experiment import Experiment


class ModeRage():

    def __init__(self, config_data=None):

        self._server_config_defaults = {
            'host': 'localhost',
            'port': '8118',
        }

        self._local_config_defaults = {

        }

        self._logger = logging.getLogger("Mode Rage client")

        self._logger.info('Attempting to load Mode Rage config from  ./.mrconfig')

        if isinstance(config_data, dict):
            self._mode, self._config = self._load_config(config_dict=config_data)
        else:
            self._mode, self._config = self._load_config(config_filename=config_data)

        cache_location = self._config['cache_location']
        if not cache_location.exists():
            cache_location.mkdir()

        self._logger.debug(f'Cache location: [{str(cache_location)}]')

        if self._mode == 'server':
            host = self._config['host']
            port = self._config['port']
            self._client = ServerClient(host, port, cache_location, self)

            if not self._client.check():
                self._logger.warning(f'Server not found, defaulting to local cache. host: [{host}:{port}]')
                self._mode = 'local'

        # Will save and load from local cache and use tinydb for file lookup
        if self._mode == 'local':
            self._client = LocalClient(cache_location, self)

    def get_config(self):
        return self._full_config

    def _load_config(self, config_dict=None, config_filename=None):
        """
        Looks for .mrconfig in local directory and loads settings if present
        """

        local_defaults = {
            'cache_location': Path.home().joinpath('.moderage')
        }

        # Use default config location if none is available
        if not config_filename and not config_dict:
            config_filename = './.mrconfig'

        if config_dict is not None:
            full_config = config_dict
        else:
            try:
                with open(config_filename, 'r') as config_file:
                    full_config = yaml.safe_load(config_file)
            except IOError as e:
                self._logger.info('Cannot load .mrconfig file. Using defaults.', e)
                return 'local', local_defaults

        mode = full_config['mode']

        self._full_config = full_config

        cache_location = Path(full_config['cache_location'] if 'cache_location' in full_config \
                                  else local_defaults['cache_location'])

        # expand any tilde '~' characters to full directory
        cache_location = cache_location.expanduser()

        if mode == 'server':
            server_config = full_config['server'] if 'server' in full_config else self._server_config_defaults
            return 'server', {**server_config, 'cache_location': cache_location}
        elif mode == 'local':
            local_config = full_config['local'] if 'local' in full_config else self._local_config_defaults
            return 'local', {**local_config, 'cache_location': cache_location}




    def save(self, meta_category, meta, parents=None, files=None, keep_originals=False):
        """
        :param parents: list of objects containing the id and category of experiments that this experiment relies on

        for example:

        {
            "id": "05c0581c-7ece-4cad-a26f-0e415ea1b01d",
            "metaCategory": "grid_world"
        }

        :param meta_category: A category name for this experiment, or this dataset
        :param meta: meta information for this experiment or dataset
        :param files: A list of files and metadata associated with this experiment or dataset

        Files must be in the following format:

        [
            "filename": "./path/to/my/file.xyz",
            "caption": "This is a description of my file"
        ]

        :return:
        """

        self._logger.info(f'Saving data to category [{meta_category}]')

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        return self._client.save(meta_category, meta, parents=parents, files=files, keep_originals=keep_originals)

    def add_parents(self, id, meta_category, parents):
        """

        :param id:
        :param meta_category:
        :param parents:
        :return:
        """

        self._logger.info(f'Adding parents to data experiment [{id}] in category [{meta_category}]')

        return self._client.add_parents(id, meta_category, parents)


    def add_files(self, id, meta_category, files, keep_originals=False):
        """

        :param id:
        :param meta_category:
        :param files:
        :return:
        """

        self._logger.info(f'Adding files to data experiment [{id}] in category [{meta_category}]')

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        return self._client.add_files(id, meta_category, files, keep_originals=keep_originals)

    def load(self, id, meta_category, ignore_files=False):
        """
        Load an experiment
        :param id: the id of the experiment
        :param meta_category: the category of the experiment
        :param ignore_files: If this is set to true, the files will not be downloaded and cached
        """

        self._logger.info(f'Loading data with id [{id}] in category [{meta_category}]')

        return self._client.load(id, meta_category, ignore_files)

    def _process_file_info(self, file):
        """
        Get the mime type of the file
        :param file:
        :return:
        """

        local_filename = file['file'] if 'file' in file else file['filename']

        file['contentType'] = magic.from_file(local_filename, True)

        return file
