#!/usr/bin/env python3
from pathlib import Path
import os
import re
import json
import subprocess

class PhpFacts:           
    def get_os_family(self) -> str:
        if os.path.exists("/etc/os-release"):
            os_vars = {}
            with open("/etc/os-release", "r", encoding="utf-8") as os_release:
                for line in os_release.readlines():
                    key, value = line.split("=")
                    os_vars.update({key: value})
            if os_vars.get("ID_LIKE"):
                os_family = str(os_vars.get("ID_LIKE")).lower().strip()
            else:
                os_family = str(os_vars.get("ID")).lower().strip()
        else:
            os_family = re.findall(r"debian|freebsd", os.uname().version.lower())
            if len(os_family) == 0:
                raise OSError(f"Unsupported OS family: {os.uname().version}")
            else:
                os_family = os_family[0]
        if os_family == "debian" or os_family == "freebsd":
            return os_family
        else:
            raise OSError(f"Unsupported OS family: {os_family}")

    def get_php_version(self) -> str:
        command="php -r 'echo PHP_MAJOR_VERSION.\".\".PHP_MINOR_VERSION;' | grep -o '[0-9]\\.[0-9]' | head -n1"
        command_output = subprocess.run(command, shell=True, capture_output=True)
        clean_output = command_output.stdout.decode().strip()
        if re.match(r"[0-9]+\.[0-9]", clean_output):
            return command_output.stdout.decode().strip()
        else:
            raise OSError(f"Error detecting the PHP version: command_output.stderr.decode()")

    def get_php_fpm_service(self):
        os_family = self.get_os_family()
        php_version = self.get_php_version()
        if os_family == "debian":
            service_name = f"php{php_version}-fpm"
            return service_name
        else:
            service_paths = Path("/usr/local/etc/rc.d").rglob("php*fpm")
            service_names = [str(path.stem) for path in service_paths]
            if len(service_names) > 1:
                raise OSError("Ambiguous PHP-FPM server names: found {', '.join(service_names}")
            else:
                return service_names[0]

    def generate_php_facts(self) -> dict:
        os_family = self.get_os_family()
        return {
                'version': self.get_php_version(),
                'prefix': {'config': "/usr/local/etc" if os_family == "freebsd" else f"/etc/php/{self.get_php_version()}/cli"},
                'fpm': {
                    'service': self.get_php_fpm_service(),
                    'prefix': {
                        'config': "/usr/local/etc" if os_family == "freebsd" else f"/etc/php/{self.get_php_version()}/fpm",
                        'pool_config': "/usr/local/etc/php-fpm.d" if os_family == "freebsd" else f"/etc/php/{self.get_php_version()}/fpm/pool.d",
                        },
                    'pools': {
                        'www': {
                            'listen.group': 'www' if os_family == "freebsd" else "www-data",
                            'listen': '/var/run/php-fpm/php-fpm.socket' if os_family == "freebsd" else f'/run/php/php{self.get_php_version()}-fpm.sock',
                }}}}



class Facts:
    def __str__(self):
        return json.dumps(PhpFacts().generate_php_facts())

if __name__ == '__main__':
    print(Facts())
