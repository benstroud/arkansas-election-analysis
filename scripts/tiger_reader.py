"""Minimal standard-library reader for TIGER/Line polygon shapefiles stored as zip files.

Reads .shp (polygon records) and .dbf (attribute table) straight from the zip, so the
downloaded archives are never extracted. Only what the map needs is supported:
polygon and null shapes, string/numeric attributes.
"""

import struct
import zipfile


def _shapefile_members(z):
    shp = next(n for n in z.namelist() if n.endswith(".shp"))
    base = shp[:-4]
    return z.read(base + ".shp"), z.read(base + ".dbf")


def parse_shp(data):
    """Return a list of shapes; each shape is a list of rings, each ring a list of (lon, lat)."""
    shapes = []
    offset = 100
    while offset + 8 <= len(data):
        _rec_no, clen_words = struct.unpack(">ii", data[offset:offset + 8])
        content = data[offset + 8: offset + 8 + clen_words * 2]
        stype = struct.unpack("<i", content[:4])[0]
        if stype == 0:
            shapes.append([])
        elif stype in (5, 15, 25):  # polygon (incl. Z/M variants: coordinates are the first 2 doubles)
            nparts, npts = struct.unpack("<ii", content[36:44])
            parts = struct.unpack(f"<{nparts}i", content[44:44 + 4 * nparts])
            pts_off = 44 + 4 * nparts
            flat = struct.unpack(f"<{2 * npts}d", content[pts_off:pts_off + 16 * npts])
            pts = list(zip(flat[0::2], flat[1::2]))
            bounds = list(parts) + [npts]
            rings = [pts[bounds[i]:bounds[i + 1]] for i in range(nparts)]
            shapes.append(rings)
        else:
            raise ValueError(f"unsupported shape type {stype}")
        offset += 8 + clen_words * 2
    return shapes


def parse_dbf(data):
    """Return a list of dict records keyed by field name."""
    nrec = struct.unpack("<I", data[4:8])[0]
    hlen = struct.unpack("<H", data[8:10])[0]
    rlen = struct.unpack("<H", data[10:12])[0]
    fields = []
    pos = 32
    while data[pos] != 0x0D:
        name = data[pos:pos + 11].split(b"\x00")[0].decode("latin-1")
        length = data[pos + 16]
        fields.append((name, length))
        pos += 32
    records = []
    for i in range(nrec):
        rec = data[hlen + i * rlen: hlen + (i + 1) * rlen]
        if rec[:1] == b"*":  # deleted record
            continue
        p = 1
        row = {}
        for name, length in fields:
            row[name] = rec[p:p + length].decode("latin-1").strip()
            p += length
        records.append(row)
    return records


def read_zip_shapefile(zip_path):
    """Return (shapes, records) for the single shapefile inside a TIGER zip."""
    with zipfile.ZipFile(zip_path) as z:
        shp, dbf = _shapefile_members(z)
    shapes = parse_shp(shp)
    records = parse_dbf(dbf)
    if len(shapes) != len(records):
        raise ValueError(f"{zip_path}: {len(shapes)} shapes but {len(records)} records")
    return shapes, records
