import sys
import json
import os
from json_reader.decoder import JSONDecoder, iter_loads
from json_reader.decoder_node_py import NodePyCompatibleScanner


def main():
    decoder = JSONDecoder(scanner_cls=NodePyCompatibleScanner)
    for data, _ in iter_loads(sys.stdin.read(), decoder=decoder):
        print(
            json.dumps(
                data, indent=int(os.getenv("INDENT", "0")) or None, ensure_ascii=False
            )
        )


if __name__ == '__main__':
    main()
