<p align="center"><img width="750" src="https://upload.wikimedia.org/wikipedia/commons/5/58/MyAnimeList_-_Full_Text_Logo.jpg" alt="MAL-Organizer logo"></p>

<p align="center">
    <a href="https://github.com/YisusChrist/MAL-Organizer/issues">
        <img src="https://img.shields.io/github/issues/YisusChrist/MAL-Organizer?color=171b20&label=Issues%20%20&logo=gnubash&labelColor=e05f65&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/MAL-Organizer/forks">
        <img src="https://img.shields.io/github/forks/YisusChrist/MAL-Organizer?color=171b20&label=Forks%20%20&logo=git&labelColor=f1cf8a&logoColor=ffffff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/MAL-Organizer/stargazers">
        <img src="https://img.shields.io/github/stars/YisusChrist/MAL-Organizer?color=171b20&label=Stargazers&logo=octicon-star&labelColor=70a5eb">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/MAL-Organizer/actions">
        <img alt="Tests Passing" src="https://github.com/YisusChrist/MAL-Organizer/actions/workflows/github-code-scanning/codeql/badge.svg">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://github.com/YisusChrist/MAL-Organizer/pulls">
        <img alt="GitHub pull requests" src="https://img.shields.io/github/issues-pr/YisusChrist/MAL-Organizer?color=0088ff">&nbsp;&nbsp;&nbsp;
    </a>
    <a href="https://opensource.org/license/gpl-2-0/">
        <img alt="License" src="https://img.shields.io/github/license/YisusChrist/MAL-Organizer?color=0088ff">
    </a>
</p>

<br>

<p align="center">
    <a href="https://github.com/YisusChrist/MAL-Organizer/issues/new?assignees=YisusChrist&labels=bug&projects=&template=bug_report.yml">Report Bug</a>
    ·
    <a href="https://github.com/YisusChrist/MAL-Organizer/issues/new?assignees=YisusChrist&labels=feature&projects=&template=feature_request.yml">Request Feature</a>
    ·
    <a href="https://github.com/YisusChrist/MAL-Organizer/issues/new?assignees=YisusChrist&labels=question&projects=&template=question.yml">Ask Question</a>
    ·
    <a href="https://github.com/YisusChrist/MAL-Organizer/security/policy#reporting-a-vulnerability">Report security bug</a>
</p>

<br>

![Alt](https://repobeats.axiom.co/api/embed/81174e1fee0494d3fb02bdf748155d57e701266b.svg "Repobeats analytics image")

<br>

`MAL-Organizer` is a project that helps you organize and manage your anime watchlist on MyAnimeList. It allows you to easily add, remove, and update your anime list from the command line.

<br>

<details>
<summary>Table of Contents</summary>

- [Requirements](#requirements)
- [Installation](#installation)
  - [From PyPI](#from-pypi)
  - [Manual installation](#manual-installation)
  - [Uninstall](#uninstall)
- [Usage](#usage)
- [Contributors](#contributors)
  - [How do I contribute to MAL-Organizer?](#how-do-i-contribute-to-mal-organizer)
- [License](#license)

</details>

## Requirements

Here's a breakdown of the packages needed and their versions:

- [malclient-upgraded](https://pypi.org/project/malclient-upgraded) (version 1.3.3)
- [platformdirs](https://pypi.org/project/platformdirs) (version 4.0.0)
- [python-dotenv](https://pypi.org/project/python-dotenv) (version 1.0.0)
- [rich-argparse-plus](https://pypi.org/project/rich-argparse-plus) (version 0.3.1.4)
- [rich](https://pypi.org/project/rich) (version 13.7.0)
- [tqdm](https://pypi.org/project/tqdm/) (version 4.66.1)

> [!NOTE]
> The software has been developed and tested using Python `3.12.1`. The minimum required version to run the software is Python 3.6. Although the software may work with previous versions, it is not guaranteed.

## Installation

### From PyPI

`MAL-Organizer` can be installed easily as a PyPI package. Just run the following command:

```bash
pip3 install mal_organizer
```

> [!IMPORTANT]
> For best practices and to avoid potential conflicts with your global Python environment, it is strongly recommended to install this program within a virtual environment. Avoid using the --user option for global installations. We highly recommend using [pipx](https://pypi.org/project/pipx) for a safe and isolated installation experience. Therefore, the appropriate command to install `mal_organizer` would be:
>
> ```bash
> pipx install mal_organizer
> ```

The program can now be ran from a terminal with the `mal_organizer` command.

### Manual installation

If you prefer to install the program manually, follow these steps:

> [!WARNING]
> This will install the version from the latest commit, not the latest release.

1. Download the latest version of [mal_organizer](https://github.com/YisusChrist/mal_organizer) from this repository:

   ```bash
   git clone https://github.com/YisusChrist/mal_organizer
   cd mal_organizer
   ```

2. Install the package:

   ```bash
   poetry install
   ```

3. Run the program:

   ```bash
   poetry run mal_organizer
   ```

### Uninstall

If you installed it from PyPI, you can use the following command:

```bash
pipx uninstall mal_organizer
```

## Usage

To run the `mal-organizer` script, you can use the following command:

```bash
mal_organizer [OPTIONS] ...
```

where `[OPTIONS]` are the command line options described below:

![CLI arguments](https://i.imgur.com/8M6OGED.png)

## Contributors

<a href="https://github.com/YisusChrist/MAL-Organizer/graphs/contributors"><img src="https://contrib.rocks/image?repo=YisusChrist/MAL-Organizer" /></a>

### How do I contribute to MAL-Organizer?

Before you participate in our delightful community, please read the [code of conduct](https://github.com/YisusChrist/.github/blob/main/CODE_OF_CONDUCT.md).

I'm far from being an expert and suspect there are many ways to improve – if you have ideas on how to make the configuration easier to maintain (and faster), don't hesitate to fork and send pull requests!

We also need people to test out pull requests. So take a look through [the open issues](https://github.com/YisusChrist/MAL-Organizer/issues) and help where you can.

See [Contributing Guidelines](https://github.com/YisusChrist/.github/blob/main/CONTRIBUTING.md) for more details.

## License

`MAL-Organizer` is released under the [GPL-3.0 license](https://opensource.org/licenses/GPL-3.0).
