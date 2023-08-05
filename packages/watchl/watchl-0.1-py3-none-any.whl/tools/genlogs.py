import click
import time
from datetime import datetime
from watchl.models.logs import LogLine


@click.command()
@click.argument("source", type=click.Path())
@click.argument("target", type=click.Path())
def main(source: str, target: str):
    with open(source, "r", encoding="utf-8") as file_in:
        for line in file_in:
            log = LogLine.parse(line)._replace(time=datetime.now())
            with open(target, "a", encoding="utf-8") as file_out:
                file_out.write(f"{log}\n")
            time.sleep(0.01)


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
