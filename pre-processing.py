import argparse
import sys
from typing import Tuple, Optional

import pandas as pd
from pyproj import Transformer


def parse_coord_pair(value: object) -> Tuple[Optional[float], Optional[float]]:
    """
    Parse a single string containing both coordinates into (lon, lat).

    Supported forms (examples):
    - "7.1234,47.5678"
    - "7.1234 47.5678"
    - "POINT(7.1234 47.5678)"
    - "7.1234;47.5678"

    Assumes order: lon, lat.
    Returns (None, None) if parsing fails.
    """
    if value is None:
        return None, None

    s = str(value).strip()
    if not s:
        return None, None

    # Handle WKT POINT syntax
    if s.upper().startswith("POINT"):
        s = s[s.find("(") + 1 : s.rfind(")")].strip()

    # Try common separators: comma, semicolon, space
    for sep in [",", ";", " "]:
        if sep in s:
            parts = [p for p in s.split(sep) if p.strip() != ""]
            if len(parts) == 2:
                try:
                    lon = float(parts[0])
                    lat = float(parts[1])
                    return lon, lat
                except ValueError:
                    return None, None

    # Fallback: if nothing matched
    return None, None


def transform_coords(
    df: pd.DataFrame,
    epsg_in: int,
    coord_cols: list,
) -> pd.DataFrame:
    """
    Transform coordinates from epsg_in to EPSG:4326.

    coord_cols:
        - length == 1: one column with both coordinates -> create 'longitude', 'latitude'
        - length == 2: two separate columns -> overwrite them with lon/lat in EPSG:4326
    """
    transformer = Transformer.from_crs(epsg_in, 4326, always_xy=True)

    if len(coord_cols) == 1:
        col = coord_cols[0]
        if col not in df.columns:
            raise ValueError(f"Coordinate column '{col}' not found in CSV.")

        # Parse the single column into lon/lat
        lon_lat = df[col].apply(parse_coord_pair)
        df["longitude"] = lon_lat.apply(lambda t: t[0])
        df["latitude"] = lon_lat.apply(lambda t: t[1])

        # Transform from epsg_in to 4326
        # (If epsg_in == 4326, this is effectively an identity, but still safe.)
        lon_vals, lat_vals = transformer.transform(
            df["longitude"].values,
            df["latitude"].values,
        )
        df["longitude"] = lon_vals
        df["latitude"] = lat_vals

    elif len(coord_cols) == 2:
        x_col, y_col = coord_cols
        if x_col not in df.columns:
            raise ValueError(f"Coordinate column '{x_col}' not found in CSV.")
        if y_col not in df.columns:
            raise ValueError(f"Coordinate column '{y_col}' not found in CSV.")

        # Transform and overwrite same columns
        lon_vals, lat_vals = transformer.transform(
            df[x_col].values,
            df[y_col].values,
        )
        df[x_col] = lon_vals
        df[y_col] = lat_vals
    else:
        raise ValueError("coord-cols must be either 1 or 2 column names.")

    return df


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Pre-process a CSV with coordinates: split/transform to EPSG:4326 "
            "and save as comma-separated file."
        )
    )

    parser.add_argument(
        "csv_path",
        help="Path to the input CSV file.",
    )

    parser.add_argument(
        "--sep",
        default=",",
        help=(
            "Field separator used in the input CSV "
            "(default: ','). For example: ';' or '\\t'."
        ),
    )

    parser.add_argument(
        "--coord-cols",
        nargs="+",
        required=True,
        help=(
            "Name(s) of coordinate column(s). "
            "Provide ONE column if both coordinates are in a single column, "
            "or TWO columns for separate X/Y (or lon/lat) columns."
        ),
    )

    parser.add_argument(
        "--epsg-in",
        type=int,
        required=True,
        help="EPSG code of the input coordinates (e.g. 2056, 3857, 4326).",
    )

    parser.add_argument(
        "--output",
        default=None,
        help=(
            "Path to the output CSV file (comma-separated). "
            "If not provided, the input file will be overwritten."
        ),
    )

    args = parser.parse_args()

    input_path = args.csv_path
    sep = args.sep
    coord_cols = args.coord_cols
    epsg_in = args.epsg_in
    output_path = args.output or input_path

    try:
        df = pd.read_csv(input_path, sep=sep)
    except Exception as e:
        print(f"Error reading CSV '{input_path}': {e}", file=sys.stderr)
        sys.exit(1)

    try:
        df = transform_coords(df, epsg_in, coord_cols)
    except Exception as e:
        print(f"Error transforming coordinates: {e}", file=sys.stderr)
        sys.exit(1)

    # Always save as comma-separated CSV
    try:
        df.to_csv(output_path, index=False)
    except Exception as e:
        print(f"Error writing CSV '{output_path}': {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
