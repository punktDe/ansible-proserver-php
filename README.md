<!-- BEGIN_ANSIBLE_DOCS -->
<!--
Do not edit README.md directly!

This file is generated automatically by aar-doc and will be overwritten.

Please edit meta/argument_specs.yml instead.
-->
# ansible-proserver-php

php role for Proserver

## Supported Operating Systems

- Debian 12, 13
- Ubuntu 26.04, 24.04, 22.04
- FreeBSD [Proserver](https://infrastructure.punkt.de/de/produkte/proserver.html)

## Role Arguments



Default variables that begin with `ansible_local` are populated using the PHP fact script (files/php.fact.py).

This scripts detects many PHP-related variables automatically depending on the system (e.g. PHP version, PHP-FPM service name, configuration, directories).

The fact script is copied to the target machine at the beginning of the role execution, even in `check_mode`.

Apart from `php.version` (on a Debian-based system), you probably shouldn't change the variables starting with `ansible_local`, unless you know what you're doing.

#### Options for `php`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `repository` | Configuration for an optional 3rd party APT repository used to install alternative PHP versions (Debian-based only) | dict of `repository` [options](#options-for-main--php--repository) | yes |  |
| `version` | PHP version to install on the target machine. Only applies to Debian-based systems. On FreeBSD Proserver-based systems, PHP is pre-installed based on the system Blueprint and detected automatically; no manual setting needed. On Debian-based systems, this option defaults to the latest version available from your system's repositories However, if `php.repository.apt.enabled` is set to true, this can be set to any version of PHP available in the third-party repo. To check which versions of PHP are available on your system, run `apt search --names-only php` | str | no | `{{ ansible_local.php.version | default('') }}` |
| `prefix` | Directories for PHP configuration files (e.g. php.ini). Defaults to `config: "/etc/php/{{ php.version }}/cli"` on Linux and `config: "/usr/local/etc"` on FreeBSD. Most of the time, you probably don't need to change this variable. | dict | no | `"{{ ansible_local.php.prefix | default({}) }}"` |
| `php.ini` | Defines config options to be written into php.ini. The options are defined as key-value pairs in a YAML dictionary, e.g. `memory_limit: 2G` or `upload_max_filesize: 500M` | dict | no |  |
| `fpm` | PHP-FPM configuration | dict of `fpm` [options](#options-for-main--php--fpm) | yes |  |
| `phpfpmtop` | Options for phpfpmtop, a performance monitor for PHP-FPM. | dict of `phpfpmtop` [options](#options-for-main--php--phpfpmtop) | no |  |
| `install_extensions` | Defines PHP extensions to be installed on the target machine in the `{'extension_name': true}` format, e.g. `{'pdo-mysql': true, 'mbstring': true}`. Only applies to Debian-based targets. | dict | no |  |
| `install_composer` | Whether to install [Composer](https://getcomposer.org) on the target machine. Only applies to Debian-based targets. | bool | no | `False` |
| `modules` | Options for managing PHP modules. | dict of `modules` [options](#options-for-main--php--modules) | no |  |
| `cli` | Options for the PHP CLI environment. | dict of `cli` [options](#options-for-main--php--cli) | no |  |

#### Options for `php.repository`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `apt` |  | dict of `apt` [options](#options-for-main--php--repository--apt) | yes |  |

#### Options for `php.repository.apt`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `enabled` | Whether the 3rd party APT repository should be installed and used | bool | no | `False` |
| `key_url` | URL for the GPG key used to signed the APT repository | str | yes |  |
| `repository` | URL for the APT repository | str | yes |  |

#### Options for `php.fpm`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `service` | PHP-FPM service name | str | no | `{{ ansible_local.php.fpm.service | default('') }}` |
| `prefix` | Path to PHP-FPM configuration files. Contains "config" and "pool_config" parameters, which default to `/usr/local/etc and /usr/local/etc/php-fpm.d` on FreeBSD, and `/etc/php/{{ php.version }}/fpm` and `/etc/php/{{ php.version }}/fpm/pool.d` on Linux respectively. | str | no | `{{ ansible_local.php.fpm.prefix | default({}) }}` |
| `pools` | Defines PHP-FPM pools. By default, only `www` pool is defined which runs under user `proserver:proserver` | dict | no | `{"www": {"user": "proserver", "group": "proserver", "listen.owner": "proserver", "listen.group": "{{ ansible_local.php.fpm.pools.www['listen.group'] | default('') }}", "listen": "{{ ansible_local.php.fpm.pools.www.listen | default({}) }}"}}` |

#### Options for `php.phpfpmtop`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `release` |  | dict of `release` [options](#options-for-main--php--phpfpmtop--release) | no |  |

#### Options for `php.phpfpmtop.release`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `url` | URL to the phpfpmtop binary. | str | no |  |
| `checksum` | SHA256 checksum of the phpfpmtop binary. | str | no |  |

#### Options for `php.modules`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `disable` | Defines which PHP modules should be disabled globally, for CLI, or on a per-user basis. | dict of `disable` [options](#options-for-main--php--modules--disable) | no | `{'cli': [], 'all': [], 'for_users': []}` |

#### Options for `php.modules.disable`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `all` | List of PHP modules to disable for all SAPIs. | list of `` | no | `[]` |
| `cli` | List of PHP modules to disable for CLI specifically. | list of `` | no | `[]` |
| `for_users` | List of users whose shell configuration should enforce `PHP_INI_SCAN_DIR` pointing to the CLI modules directory. | list of `` | no | `[]` |

#### Options for `php.cli`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `ld_bind_now` | Sets `LD_BIND_NOW=1` for the given users through a login class in `/etc/login.conf`, so the dynamic linker resolves all symbols when PHP starts instead of on first use. FreeBSD only. Enabling it on any other system fails the play. Works around PHP CLI processes that segfault on exit on FreeBSD when many extensions are loaded ([FreeBSD PR 295991](https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=295991)). Use it instead of disabling modules for that crash. The login class applies to every login of these users (SSH logins and commands, `su -`, `sudo -i`) and to their cron jobs, independent of their shell and its startup files. Not covered are `sudo -u <user>` without `-i`, which resets the environment, and services started by rc. They need `LD_BIND_NOW=1` in their own environment. Removing it is a manual step: setting `enabled: false` or dropping a user from `for_users` leaves the login class and the users' class as they are. To undo it on a host, as root: move each user back with `pw usermod <user> -L default`, delete the block between the `BEGIN`/`END ANSIBLE MANAGED BLOCK: LD_BIND_NOW workaround (FreeBSD PR 295991)` markers from `/etc/login.conf`, run `cap_mkdb /etc/login.conf`, and check with `ssh <user>@<host> printenv LD_BIND_NOW`, which should print nothing. | dict of `ld_bind_now` [options](#options-for-main--php--cli--ld_bind_now) | no | `{'enabled': False, 'for_users': [], 'login_class': 'php_cli'}` |

#### Options for `php.cli.ld_bind_now`

|Option|Description|Type|Required|Default|
|---|---|---|---|---|
| `enabled` | Whether the login class is set up and assigned. `false` does nothing; it doesn't undo an earlier run, see the manual steps above. | bool | no | `False` |
| `for_users` | List of users that get the login class. Removing a user from the list doesn't move it back to `default`. | list of `` | no | `[]` |
| `login_class` | Name of the login class. It inherits everything else from the `default` class. The users are moved to this class, so pick a dedicated name if they are in a custom class today. | str | no | `php_cli` |

## Dependencies
None.

## Installation
Add this role to the requirements.yml of your playbook as follows:
```yaml
roles:
  - name: ansible-proserver-php
    src: https://github.com/punktDe/ansible-proserver-php
```

Afterwards, install the role by running `ansible-galaxy install -r requirements.yml`

## Example Playbook

```yaml
- hosts: all
  roles:
    - name: ansible-proserver-php
```

<!-- END_ANSIBLE_DOCS -->
