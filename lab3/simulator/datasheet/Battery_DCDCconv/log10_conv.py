#THis file will converte x axis values from db scale to linear scale

# ...existing code...
#THis file will converte x axis values from db scale to linear scale

import argparse
import math
from pathlib import Path

def convert_file(in_path: Path, out_path: Path) -> None:
    with in_path.open('r') as fin, out_path.open('w') as fout:
        header_written = False
        for raw in fin:
            line = raw.strip()
            if not line:
                continue
            # preserve header if present
            if line.lower().startswith('x') and ('y' in line or ',' in line):
                fout.write(line + '\n')
                header_written = True
                continue
            # skip comment-like lines
            if line.startswith('//') or line.startswith('#'):
                fout.write(line + '\n')
                continue
            parts = [p.strip() for p in line.split(',')]
            if len(parts) < 2:
                # write unchanged if unexpected format
                fout.write(line + '\n')
                continue
            try:
                x_log = float(parts[0])
                x_lin = 10 ** x_log
                # keep the y part(s) unchanged
                rest = ', '.join(parts[1:])
                fout.write(f"{x_lin}, {rest}\n")
            except ValueError:
                fout.write(line + '\n')

def main():
    p = argparse.ArgumentParser(description="Convert x values from log10 scale to linear.")
    p.add_argument('input', nargs='?', default="trace_2.4V_log10",
                   help="input file (default: trace_2.4V_log10)")
    p.add_argument('-o', '--output', default=None,
                   help="output file (default: input_linear)")
    args = p.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        return

    out_path = Path(args.output) if args.output else in_path.with_name(in_path.stem + "_linear" + in_path.suffix)
    convert_file(in_path, out_path)
    print(f"Converted file written to: {out_path}")

if __name__ == "__main__":
    main()
# ...existing code...