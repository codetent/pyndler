![Python package](https://github.com/codetent/pyndler/workflows/Python%20package/badge.svg)
![License](https://img.shields.io/github/license/codetent/pyndler)

# pyndler

## Description

Pyndler is a lightweight tool for bundling a pyz file in an exe file. If an executable is deployed, it can also be useful
to set an executable icon or additional metadata (product name, company name, versions, ...).

Python projects must be bundled using [shiv](https://github.com/linkedin/shiv), [zipapp](https://docs.python.org/3/library/zipapp.html) or any other pyz-like packaging tool, before they can be bundled as .exe files using Pyndler.

## How does it work?

Pyndler uses the fantastic python [simple launcher](https://bitbucket.org/vinay.sajip/simple_launcher/src/master/) mentioned in [PEP 397](https://www.python.org/dev/peps/pep-0397/).

First, the pylauncher is copied to the target path. Then the pyz file is appended to the launcher. Afterwards, an additional icon or metadata is set using [rcedit](https://github.com/electron/rcedit) - a great project usually used for branding electron project.

## Usage

Install the latest pyndler release using pip:

```
pip install pyndler
```

Run pyndler:

```
pyndler <SOURCE>
    -c, --config VALUE:ExistingFile      Path to config file for setting additional metadata
    --gui                                Set to true, if source is a GUI application
    -i, --icon VALUE:ExistingFile        Path to exe icon
    --refresh                            Refresh Windows icon cache after building
    -t, --target VALUE:ExistingFile      Path to output file. If not set, the source path is taken
```

Example call:

```
pyndler example.pyz --icon icon.ico --config app.cfg
```

The metadata config file must be written using INI-like syntax with keys listed [here](https://docs.microsoft.com/de-de/windows/win32/menurc/versioninfo-resource?redirectedfrom=MSDN), grouped in a `VERSIONINFO` section like:

```
[VERSIONINFO]
<key>=<value>
```

For info about setting an explicit python interpreter, see [this](https://bitbucket.org/vinay.sajip/simple_launcher/wiki/Launching%20an%20interpreter%20in%20a%20location%20relative%20to%20the%20launcher%20executable) wiki page.
