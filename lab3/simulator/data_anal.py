import sys
import pandas as pd
from io import StringIO

COLUMNS = [
    'time', 'soc', 'i_tot', 'i_mcu', 'i_rf', 'i_pv',
    'v_pv', 'real_i_pv', 'i_batt', 'v_batt',
    'i_air_quality_sensor', 'i_methane_sensor',
    'i_temperature_sensor', 'i_mic_click_sensor',
]

def load_sensor_data(filepath: str) -> pd.DataFrame:
    with open(filepath, 'r') as f:
        lines = f.read().strip().splitlines()
    lines[0] = lines[0].lstrip('%').strip()
    df = pd.read_csv(StringIO('\n'.join(lines)), sep=r'\s+')
    return df[COLUMNS]

def to_ascii_table(df: pd.DataFrame) -> str:
    col_widths = [max(len(str(col)), df[col].apply(lambda x: len(str(x))).max()) for col in df.columns]

    def row_str(values):
        return '| ' + ' | '.join(str(v).ljust(w) for v, w in zip(values, col_widths)) + ' |'

    separator = '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'

    lines = [
        separator,
        row_str(df.columns),
        separator,
        *[row_str(row) for _, row in df.iterrows()],
        separator,
    ]
    return '\n'.join(lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse_sensor_data.py <input_file> [output_file]")
        sys.exit(1)

    df = load_sensor_data(sys.argv[1])
    table = to_ascii_table(df)

    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
        with open(output_path, 'w') as f:
            f.write(table + '\n')
        print(f"Table written to {output_path}")
    else:
        print(table)