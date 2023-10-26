"""Console script for meta_eukaryome_detect."""

import click


@click.command()
def main():
    """Main entrypoint."""
    click.echo("meta-eukaryome-detect")
    click.echo("=" * len("meta-eukaryome-detect"))
    click.echo("Pathogen, Parasite, Eukaryote and Virus detection in metagenomes.")


if __name__ == "__main__":
    main()  # pragma: no cover
