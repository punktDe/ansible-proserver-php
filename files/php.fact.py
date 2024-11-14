#!/usr/bin/env python3
from pathlib import Path
import os
import re
import json
import subprocess

class PhpFacts:           
    def get_os_family(self) -> str:
        os_family = re.findall(r"debian|freebsd", os.uname().version.lower())
        if len(os_family) == 0:
            raise OSError(f"Unsupported OS family: {os.uname().version}")
        else:
            return os_family[0]

    def get_php_version(self) -> str:
        os_family = self.get_os_family()
        if os_family == "debian":
            command='apt-cache search --names-only "^php[0-9].[0-9]$" | grep -o "[0-9]\\.[0-9]"'
        else:
            command="php -r 'echo phpversion();' | grep -o '[0-9]\\.[0-9]' | head -n1"
        command_output = subprocess.run(command, shell=True, capture_output=True)
        if len(command_output.stdout) > 0:
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
                'prefix': {'config': "/etc/local/etc" if os_family == "freebsd" else f"/etc/php/{self.get_php_version()}/cli"},
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
