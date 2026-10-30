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
| `repository` | URL for the APT repository (packages.sury.org on all Debian-based systems, including Ubuntu) | str | yes |  |
| `migrate_from_ppa` | Switch PHP packages that are still installed from the ondrej/php PPA (used on Ubuntu up to version 4.x of this role) to the configured repository, in one apt transaction followed by a PHP-FPM restart Without it, the role stops before changing the repository when it finds such packages. See "Migrating from the ondrej/php PPA" below. | bool | no | `False` |

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

## Migrating from the ondrej/php PPA

Up to version 4.x, this role used the [ondrej/php PPA](https://launchpad.net/~ondrej/+archive/ubuntu/php) on Ubuntu.
The PPA publishes no packages for Ubuntu 26.04 and later, so from version 5.0.0 on the role uses
[packages.sury.org](https://packages.sury.org/php/) on all Debian-based systems, including Ubuntu.

This only matters for existing Ubuntu hosts with `php.repository.apt.enabled: true`. The PPA builds carry a higher
version than the packages.sury.org builds of the same PHP release (e.g. `8.1.34-9+ubuntu24.04.1+deb.sury.org+1`
vs. `8.1.34-9+0~20261021.82+ubuntu24.04~1.gbp4e430a`). After the repository switch, apt therefore keeps the
installed PPA builds, and installing a new extension fails because it requires the exact packages.sury.org
build of `php<version>-common`. Downgrading single packages by hand is not an option: apt would remove
`php<version>-fpm` and `php<version>-cli` to resolve the dependencies.

On every run, before it touches the repository configuration, the role looks for installed `php*` packages
whose installed version comes from the PPA, or from no repository at all (a PPA that was already removed).
Without further configuration, the role stops at that point and lists those packages: the host keeps its PPA and
nothing is changed. This also works in check mode.

To migrate a host (once per host, repeatable):

1. Plan a short PHP-FPM restart, the migration restarts the service.
2. Run the playbook with `--check` to see whether the host is affected: the role stops and lists the PHP
   packages from the PPA.
3. Set `php.repository.apt.migrate_from_ppa: true` for the host (e.g. in its `host_vars`).
4. Run the playbook. The role replaces the PPA with packages.sury.org and switches all affected PHP packages to
   their current packages.sury.org build in a single apt transaction (no package is removed). PHP-FPM is
   restarted afterwards.
5. Run the playbook again: once nothing is left from the PPA, the migration steps do nothing. The option can
   stay enabled, or be removed again.

If the PPA is also configured outside of this role (e.g. via `add-apt-repository`, as
`/etc/apt/sources.list.d/ondrej-ubuntu-php-*.sources`), remove that file before migrating. Otherwise apt keeps
offering the higher PPA builds, and the next `apt upgrade` installs them again.

### Unattended upgrades

Unattended upgrades only install packages from origins that are explicitly allowed. To have PHP updated
automatically, packages.sury.org has to be allowed as an origin, e.g. with
`system.unattended_upgrades.config.origins_pattern` of the
[ansible-proserver-system](https://github.com/punktDe/ansible-proserver-system) role:

```yaml
system:
  unattended_upgrades:
    config:
      origins_pattern:
        php: "origin=deb.sury.org,codename=${distro_codename}"
```

An entry for the PPA (`origin=LP-PPA-ondrej-php`) matches nothing after the switch, replace it. On a host that
was switched without migrating, unattended upgrades never downgrade: they leave the PPA builds in place and
only replace them, PHP-FPM restart included, once packages.sury.org publishes a newer PHP release.

### Without this role

The manual equivalent is to replace the PPA with packages.sury.org in the apt sources, then switch every
installed PHP package at once, e.g. for PHP 8.1 on Ubuntu 24.04:

```sh
apt-get update
apt-get install --allow-downgrades $(dpkg-query -W -f='${db:Status-Abbrev} ${Package}
' 'php*' \
  | awk '$1 == "ii" {print $2}' \
  | while read -r p; do v=$(apt-cache madison "$p" | awk -F' [|] ' '/packages.sury.org/ {print $2; exit}'); \
    [ -n "$v" ] && echo "$p=$v"; done)
systemctl restart php8.1-fpm
```

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
