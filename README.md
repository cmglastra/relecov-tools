# relecov-tools
[![python_lint](https://github.com/BU-ISCIII/relecov-tools/actions/workflows/python_lint.yml/badge.svg)](https://github.com/BU-ISCIII/relecov-tools/actions/workflows/python_lint.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> THIS REPO IS UNDER ACTIVE DEVELOPMENT.

relecov-tools is a set of helper tools for the assembly of the different elements in the RELECOV platform (Spanish Network for genomic surveillance of SARS-Cov-2) as data download, processing, validation and upload to public databases, as well as analysis runs and database storage.

## Table of contents

* [Installation](#installation)
* [Usage](#usage)
    * [download](#download)
    * [read-lab-metadata](#read-lab-metadata)
    * [read-bioinfo-metadata](#read-bioinfo-metadata)
    * [validate](#validate)
    * [map](#map)
    * [upload-to-ena](#upload-to-ena)
    * [upload-to-gisaid](#upload-to-gisaid)
    * [launch](#launch)
    * [update-db](#update-db)
* [Aknowledgements](#aknowledgements)

## Installation

### Bioconda
Soon

### Pip
Soon

### Development version
If you want to install the latest code in the repository:

```
conda create -n relecov_dev pip
pip install --force-reinstall --upgrade git+https://github.com/bu-isciii/relecov-tools.git@develop
```

## Usage

### Command-line
relecov-tools provides a command-line version with help descriptions and params prompt if needed.

```
$ relecov-tools --help
             ___   ___       ___  ___  ___
\    |--|   |   \ |    |    |    |    |   | \      /
\    \  /   |__ / |__  |    |___ |    |   |  \    /
/    /  \   |  \  |    |    |    |    |   |   \  /
/    |--|   |   \ |___ |___ |___ |___ |___|    \/
RELECOV-tools version 0.0.1
Usage: relecov-tools [OPTIONS] COMMAND [ARGS]...

Options:
--version                  Show the version and exit.
-v, --verbose              Print verbose output to the console.
-l, --log-file <filename>  Save a verbose log to a file.
--help                     Show this message and exit.

Commands:
    download                Download files located in sftp server.
    read-lab-metadata       Create the json compliant to the relecov schema from...
    read-bioinfo-metadata   Create the json compliant to the relecov schema with Bioinfo Metadata.
    validate                Validate json file against schema.
    map                     Convert data between phage plus schema to ENA,...
    upload-to-ena           parsed data to create xml files to upload to ena
    upload-to-gisaid        parsed data to create files to upload to gisaid
    update-db               feed database with metadata jsons
    launch                  launch viralrecon in hpc
```
#### download
The command `download` connects to a transfer protocol (currently sftp) and downloads all files in the different available folders in the passed credentials. In addition, it checks if the files in the current folder match the files in the metadata file and also checks if there are md5sum for each file. Else, it creates one before storing in the final repository.

```
$ relecov-tools download --help
Usage: relecov-tools download [OPTIONS]

  Download files located in sftp server.

  Options:
    -u, --user            User name for login to sftp server
    -p, --password        Password for the user to login
    -d, --download_option Select the download option: [download_only, download_clean, delete_only].
        download_only will only download the files
        download_clean will remove files from sftp after download
        delete_only will only delete the files
    -o, --output_location Flag: Select location for downloaded files, overrides config file location
    -t, --target_folders  Flag: Select which sftp folders will be targeted giving [paths] or via prompt
    -f, --conf_file       Configuration file in yaml format (no params file)
    --help                Show this message and exit.
```

Configuration can be passed in several formats:
- if no config_file is passed, default values are fetched from conf/configuration.json, and user and password are asked in prompt.
- Default values can be overwritten using a yml config file, so you can input user, password, sftp_server, etc.

Config file example with all available options:
```
sftp_server: "sftprelecov.isciii.es"
sftp_port: "22"
sftp_user : "user"
sftp_passwd : "pass"
storage_local_folder: "/tmp/relecov"
tmp_folder_for_metadata: "/tmp/relecov/tmp"
allowed_sample_extensions:
    - .fastq.gz
    - .fasta
```

#### read-lab-metadata
`read-lab-metadata` command reads the excel file with laboratory metadata and processes it adding additional needed fields.

```
$ relecov-tools read-lab-metadata --help
Usage: relecov-tools read-metadata [OPTIONS]

  Create the json compliant to the relecov schema from the Metadata file.

  Options:
    -m, --metadata_file PATH     file containing metadata in xlsx format.
    -s, --sample_list_file PATH  Json with the additional metadata to add to the
    received user metadata.
    -o, --metadata-out PATH      Path to save output  metadata file in json format.
    --help                       Show this message and exit.
```


An example for the metadata excel file can be found [here](./relecov_tools/example_data/METADATA_LAB_TEST.xlsx)

#### read-bioinfo-metadata
`read-bioinfo-metadata` Include the results from the Bioinformatics analysis into the Json previously created with read-lab-metadata module.

```
$ relecov-tools read-bioinfo-metadata --help
Usage: relecov-tools read-bioinfo-metadata [OPTIONS]

   Create the json compliant to the relecov schema with Bioinfo Metadata.

   Options:
      -j, --json_file       Json file containing lab metadata
      -i, --input_folder    Path to folder containing analysis results
      -s, --software_name   Name of the software employed in the bioinformatics analysis (default: viralrecon).
      -o, --out_dir         Path to save output file"
```
- Note: Software-specific configurations are available in [bioinfo_config.json](./relecov_tools/conf/bioinfo_config.json).

#### validate
`validate` commands validate the data in json format outputted by `read-metadata` command against a json schema, in this case the relecov [schema specification](./relecov_tools/schema/relecov_schema.json).

```
$ relecov-tools validate --help
Usage: relecov-tools validate [OPTIONS]

  Validate json file against schema.

  Options:
    -j, --json_file TEXT    Json file to validate
    -s, --json_schema TEXT  Json schema
    -m, --metadata PATH     Origin file containing metadata
    -o, --out_folder TEXT   Path to save validate json file
    --help                  Show this message and exit.

```

#### map
The command `map` converts a data in json format from relecov data model to ena or gisaid data model using their own schemas acording to their annotated ontology terms.

```
$ relecov-tools map --help
Usage: relecov-tools map [OPTIONS]

  Convert data between phage plus schema to ENA, GISAID, or any other schema

  Options:
    -p, --origin_schema TEXT        File with the origin (relecov) schema
    -j, --json_data TEXT            File with the json data to convert
    -d, --destination_schema [ENA|GSAID|other]
    schema to be mapped
    -f, --schema_file TEXT          file with the custom schema
    -o, --output TEXT               File name and path to store the mapped json
    --help                          Show this message and exit.
```

#### upload-to-ena
`upload-to-ena` command uses json data mapped to ena schema to use the [ena_upload_cli](https://github.com/usegalaxy-eu/ena-upload-cli) package to upload raw data and metadata to ENA db.

```
Usage: relecov-tools upload-to-ena [OPTIONS]

  parsed data to create xml files to upload to ena

  Options:
    -u, --user                               user name for login to ena
    -p, --password                           password for the user to login
    -c, --center                             center name
    -e, --ena_json                           where the validated json is
    -t, --template_path                      path to folder containing ENA xml templates
    -a, --action                             select one of the available options: [add|modify|cancel|release]
    --dev                                    Flag: Test submission
    --upload_fastq                           Flag: Upload fastq files. Mandatory for "add" action
    -m", --metadata_types                    List of metadata xml types to submit [study,experiment,run,sample]
    -o, --output_path TEXT                   output folder for the xml generated files
    --help                                   Show this message and exit.

```

#### upload-to-gisaid
`upload-to-gisaid` uses the json mapped to gisaid schema to upload raw data and metadata to GISAID db

```
Usage: relecov-tools upload-to-gisaid [OPTIONS]

  parsed data to create xml files to upload to ena

  Options:
    -u, --user            user name for login
    -p, --password        password for the user to login
    -c, --client_id       client-ID provided by clisupport@gisaid.org
    -t, --token           path to athentication token
    -e, --gisaid_json     path to validated json mapped to GISAID
    -i, --input_path      path to fastas folder or multifasta file
    -f, --frameshift      frameshift notification: ["catch_all", "catch_none", "catch_novel"]
    -x, --proxy_config    introduce your proxy credentials as: username:password@proxy:port
    --single              Flag: input is a folder with several fasta files.
    --gzip                Flag: input fasta is gziped.
```

#### update-db
    -u, --user                         user name for login
    -p, --password                     password for the user to login
    -t, --type                         Select the type of information to upload to database [sample,bioinfodata,variantdata]
    -d, --databaseServer               Name of the database server receiving the data [iskylims,relecov]

#### launch
SOON

### Python package mode
relecov-tools is designed in a way that you can use import the different modules and use them in your own scripts, for example:

```
import relecov_tools.sftp_handle
user="admin"
passwd="1234"
conf_file="/path/to/conf"

sftp_connection = relecov_tools.sftp_handle.SftpHandle(
    user, password, conf_file
)
sftp_connection.download()
```

DOCs soon!!


## Acknowledgements
Python package idea and design is really inspired in [nf-core/tools](https://github.com/nf-core/tools).
