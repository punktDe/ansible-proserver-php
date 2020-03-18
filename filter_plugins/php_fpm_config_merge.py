def php_fpm_config_merge(input: dict):
    output = []

    for pool, pool_config in input.items():
        if not pool_config:
            continue

        for option, value in pool_config.items():
            if value is None:
                state = 'absent'
            else:
                state = 'present'

            output += [{
                'pool': pool,
                'option': option,
                'value': value,
                'state': state,
            }]

    return output


class FilterModule(object):
    def filters(self):
        return {
            'php_fpm_config_merge': php_fpm_config_merge,
        }
