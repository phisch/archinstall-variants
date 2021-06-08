# archinstall-variants

An [archinstall](https://github.com/archlinux/archinstall) plugin that lets you define and select variations of your
configuration.

## EXPERIMENTAL

Plugin support is currently only available in archinstalls master branch. It is not part of the official release yet,
and the plugin API is experimental, which means this plugin could break at any time. Please wait until archinstall
Plugin support is official, and this plugin ships a stable release before you use it.

Other than that, have fun experimenting with this!

## Usage
When loading this plugin in your `config.json`, you can define a `variants` key, which is a dict with variant names as keys, and a variant configuration dicts as values.
Running archinstall with a configuration like this, will ask you to select one of your configured variants to install.

After you made your selection, it merges the configuration of the selected variant into the root configuration.

When the value is a **list**, it **extends the base** list with the variant list, which allows you to create a variant
that for example adds additional packages to the base.

Every **other** variant **value will overwrite** or set its base value.

### Example
Imagine the following archinstall `config.json`:

```json
{
  "harddrive": {
    "path": "/dev/sda"
  },
  "packages": [
    "base",
    "base2"
  ],
  "plugin": "https://github.com/phisch/archinstall-variant/raw/master/archinstall-variant.py",
  "variants": {
    "desktop": {
      "hostname": "desktop",
      "packages": [
        "desktop-package"
      ]
    },
    "laptop": {
      "commands": [
        "echo 'i run on the laptop variant'"
      ],
      "harddrive": {
        "path": "/dev/nvme0n1"
      },
      "hostname": "laptop"
    }
  }
}
```

Running this configuration with archinstall will ask you to select one of the configured variants.

```shell
archinstall --config https://path/or/url/to/your/config.json
0: desktop
1: laptop
Select which variant you want to install (default: desktop):
```

Selecting the `desktop` variant, will change the configuration into:

```json
{
  "harddrive": {
    "path": "/dev/sda"
  },
  "hostname": "desktop",
  "packages": [
    "base",
    "base2",
    "desktop-package"
  ],
  "plugin": "https://github.com/phisch/archinstall-variant/raw/master/archinstall-variant.py"
}
```

Selecting `laptop` on the other hand, would result in:

```json
{
  "commands": [
    "echo 'i run on the laptop variant'"
  ],
  "harddrive": {
    "path": "/dev/nvme0n1"
  },
  "hostname": "laptop",
  "packages": [
    "base",
    "base2"
  ],
  "plugin": "https://github.com/phisch/archinstall-variant/raw/master/archinstall-variant.py"
}
```