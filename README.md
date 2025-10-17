<!-- BEGIN_ANSIBLE_DOCS -->
# ansible-proserver-php

Ansible role for PHP

## Supported Operating Systems

- Debian 12
- Ubuntu 24.04, 22.04
- FreeBSD [Proserver](https://infrastructure.punkt.de/de/produkte/proserver.html)

## Role Arguments



Default variables that begin with `ansible_local` are populated using the PHP fact script (files/php.fact.py).

This scripts detects many PHP-related variables automatically depending on the system (e.g. PHP version, PHP-FPM service name, configuration, directories).

The fact script is copied to the target machine at the beginning of the role execution, even in `check_mode`.

Apart from `php.version` (on a Debian-based system), you probably shouldn't change the variables starting with `ansible_local`, unless you know what you're doing.

#### Options for `php`

| Option               |Description| Type                         |Required|Default|
|----------------------|---|------------------------------|---|---|
| `repository`         | Configuration for an optional 3rd party APT repository used to install alternative PHP versions (Debian-based only) | dict of 'repository' options | yes |  |
| `version`            | PHP version to install on the target machine. Only applies to Debian-based systems. On FreeBSD Proserver-based systems, PHP is pre-installed based on the system Blueprint and detected automatically; no manual setting needed. On Debian-based systems, this option defaults to the latest version available from your system's repositories However, if `php.repository.apt.enabled` is set to true, this can be set to any version of PHP available in the third-party repo. To check which versions of PHP are available on your system, run `apt search --names-only php` | str                          | no | {{ ansible_local.php.version | default('') }} |
| `prefix`             | Directories for PHP configuration files (e.g. php.ini). Defaults to `config: "/etc/php/{{ php.version }}/cli"` on Linux and `config: "/usr/local/etc"` on FreeBSD. Most of the time, you probably don't need to change this variable. | dict                         | no | "{{ ansible_local.php.prefix | default({}) }}" |
| `php.ini`            | Defines config options to be written into php.ini. The options are defined as key-value pairs in a YAML dictionary, e.g. `memory_limit: 2G` or `upload_max_filesize: 500M` | dict                         | no |  |
| `fpm`                | PHP-FPM configuration | dict of 'fpm' options        | yes |  |
| `phpfpmtop`          | Options for phpfpmtop, a performance monitor for PHP-FPM. | dict of 'phpfpmtop' options  | no |  |
| `install_extensions` | Defines PHP extensions to be installed on the target machine in the `{'extension_name': true}` format, e.g. `{'pdo-mysql': true, 'mbstring': true}`. Only applies to Debian-based targets. | dict                         | no |  |
| `install_composer`   | Whether to install [Composer](https://getcomposer.org) on the target machine. Only applies to Debian-based targets. | bool                         | no | False |
| `scandir`            | Defines PHP modules to be disabled in the default-context (FPM) and/or cli-context (CLI). | dict of 'scandir' options    | no |  |
#### Options for `php.repository`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `apt` |  | dict of 'apt' options | yes |  |

#### Options for `php.repository.apt`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `enabled` | Whether the 3rd party APT repository should be installed and used | bool | no | False |
| `key_url` | URL for the GPG key used to signed the APT repository | str | yes |  |
| `repository` | URL for the APT repository | str | yes |  |

#### Options for `php.fpm`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `service` | PHP-FPM service name | str | no | {{ ansible_local.php.fpm.service | default('') }} |
| `prefix` | Path to PHP-FPM configuration files. Contains "config" and "pool_config" parameters, which default to `/usr/local/etc and /usr/local/etc/php-fpm.d` on FreeBSD, and `/etc/php/{{ php.version }}/fpm` and `/etc/php/{{ php.version }}/fpm/pool.d` on Linux respectively. | str | no | {{ ansible_local.php.fpm.prefix | default({}) }} |
| `pools` | Defines PHP-FPM pools. By default, only `www` pool is defined which runs under user `proserver:proserver` | dict | no | {"www": {"user": "proserver", "group": "proserver", "listen.owner": "proserver", "listen.group": "{{ ansible_local.php.fpm.pools.www['listen.group'] | default('') }}", "listen": "{{ ansible_local.php.fpm.pools.www.listen | default({}) }}"}} |

#### Options for `php.phpfpmtop`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `release` |  | dict of 'release' options | no |  |

#### Options for `php.phpfpmtop.release`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `url` | URL to the phpfpmtop binary. | str | no |  |
| `checksum` | SHA256 checksum of the phpfpmtop binary. | str | no |  |

#### Options for `php.scandir`

|Option| Description                                                  | Type |Required|Default|
|---|--------------------------------------------------------------|------|---|---|
| `php_ini_scan_dir_default` | Default path for php-modules.                                | str  | no | "/usr/local/etc/php" |
| `php_ini_scan_dir_cli` | Path for php-modules used in cli.                            | str  | no | "/usr/local/etc/php-cli" |
| `php_modules_disable` | List of php-modules to disable in default path.              | str  | no |  |
| `php_cli_modules_disable` | List of php-modules to disable in cli path.                  | list  | no |  |
| `overwrite_scandir_for_cli_user` | List of users for whom to overwrite PHP_INI_SCAN_DIR for cli | list | no |  |

*Example to disable xsl,dom and xmlreader only for proserver user*
```yaml
php:
  scandir:
    php_cli_modules_disable:
      - ext-20-dom
      - ext-30-xmlreader
      - ext-30-xsl
    overwrite_scandir_for_cli_user:
      - proserver 
```


## Dependencies
None.

## Installation
Add this role to the requirements.yml of your playbook as follows:
```yaml
roles:
  - name: php
    src: https://github.com/punktDe/ansible-proserver-php
```

Afterwards, install the role by running `ansible-galaxy install -r requirements.yml`

## Example Playbook

```yaml
- hosts: all
  roles:
    - name: php
```


<!-- END_ANSIBLE_DOCS -->
