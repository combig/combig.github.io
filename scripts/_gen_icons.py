import zlib, struct, math

SIZE = 180
S = 2.5
OFF = (SIZE - 64 * S) / 2

BG = (0x25, 0x63, 0xEB)
FG = (255, 255, 255)

segs = [
    ((16, 44), (16, 20)),
    ((16, 20), (23, 20)),
    ((23, 20), (29, 34)),
    ((29, 34), (35, 20)),
    ((35, 20), (42, 20)),
    ((42, 20), (42, 44)),
]
segs = [((OFF + a[0] * S, OFF + a[1] * S), (OFF + b[0] * S, OFF + b[1] * S)) for a, b in segs]
THICK = 5.5 * S / 2
RADIUS = 40.0


def dist_to_seg(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def in_rounded_rect(x, y):
    cx = min(max(x, RADIUS), SIZE - RADIUS)
    cy = min(max(y, RADIUS), SIZE - RADIUS)
    return math.hypot(x - cx, y - cy) <= RADIUS


rows = bytearray()
for y in range(SIZE):
    rows.append(0)
    for x in range(SIZE):
        if not in_rounded_rect(x + 0.5, y + 0.5):
            rows += bytes((0, 0, 0, 0))
            continue
        if any(dist_to_seg((x + 0.5, y + 0.5), a, b) <= THICK for a, b in segs):
            rows += bytes((*FG, 255))
        else:
            rows += bytes((*BG, 255))


def chunk(tag, data):
    body = tag + data
    return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xFFFFFFFF)


png = b'\x89PNG\r\n\x1a\n'
png += chunk(b'IHDR', struct.pack('>IIBBBBB', SIZE, SIZE, 8, 6, 0, 0, 0))
png += chunk(b'IDAT', zlib.compress(bytes(rows), 9))
png += chunk(b'IEND', b'')

with open('static/apple-touch-icon.png', 'wb') as f:
    f.write(png)
print('apple-touch-icon.png', len(png), 'bytes')
