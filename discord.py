import argparse
from field_gen import MineField


def symbol_to_emoji(symbol):
    mapping = {
        '0': '0️⃣',
        '1': '1️⃣',
        '2': '2️⃣',
        '3': '3️⃣',
        '4': '4️⃣',
        '5': '5️⃣',
        '6': '6️⃣',
        '7': '7️⃣',
        '8': '8️⃣',
        '*': '💣'
    }
    return mapping.get(symbol, symbol)


def wrap_emoji_with_spoiler(emoji):
    return f'||{emoji}||'  # Discord spoiler syntax


def minefield_to_emoji_grid(minefield, use_spoilers=False):
    emoji_grid = []
    for row in minefield.field:
        if use_spoilers:
            emoji_row = [wrap_emoji_with_spoiler(
                symbol_to_emoji(symbol)) for symbol in row]
        else:
            emoji_row = [symbol_to_emoji(symbol) for symbol in row]
        emoji_grid.append(emoji_row)
    return emoji_grid


def display_emoji_grid(emoji_grid):
    for row in emoji_grid:
        print(' '.join(row))


def export_emoji_grid_to_file(minefield, out_path='minefield_emoji.txt', use_spoilers=True):
    """Write the emoji grid to `out_path` and append metadata.

    `use_spoilers` controls whether each emoji is wrapped in Discord spoilers.
    """
    emoji_grid = minefield_to_emoji_grid(minefield, use_spoilers=use_spoilers)
    with open(out_path, 'w', encoding='utf-8') as f:
        for row in emoji_grid:
            # Add a trailing space before the newline. When a spoiler (||...||)
            # appears at the end of a line, Discord's parser can drop/trim
            # the final spoiler token in some clients. Appending a space
            # prevents that and preserves the displayed spoiler emoji.
            f.write(' '.join(row) + ' \n')
        f.write(
            f"Size: {minefield.width} x {minefield.height} Mines: {minefield.num_mines}\n")
        seed = getattr(minefield, 'seed', None)
        f.write(f"Seed: {seed}\n")


def _build_parser():
    p = argparse.ArgumentParser(
        description="Generate a minesweeper field and export emoji or text outputs")
    p.add_argument('--width', type=int, default=8, help='Field width')
    p.add_argument('--height', type=int,
                   help='Field height (defaults to width)')
    p.add_argument('--mines', type=int, default=15, help='Number of mines')
    p.add_argument('--seed', type=int, default=None, help='Optional RNG seed')
    p.add_argument(
        '--emoji-out', help='Write emoji (spoiler-wrapped if --spoilers) to this file')
    p.add_argument(
        '--field-out', help='Write the plain field (numbers/0/*) to this file')
    p.add_argument('--no-spoilers', action='store_true',
                   help='Do not wrap emoji in spoilers')
    p.add_argument('--no-display', action='store_true',
                   help='Do not print the grid to stdout')
    return p


if __name__ == "__main__":
    parser = _build_parser()
    args = parser.parse_args()

    width = args.width
    height = args.height if args.height is not None else width
    num_mines = args.mines

    mine_field = MineField(width, height, num_mines, seed=args.seed)

    # Display to stdout unless disabled
    if not args.no_display:
        emoji_grid = minefield_to_emoji_grid(
            mine_field, use_spoilers=not args.no_spoilers)
        display_emoji_grid(
            emoji_grid if args.emoji_out or not args.field_out else mine_field.field)

    # Save plain field if requested
    if args.field_out:
        # Use MineField.display-like format but write to file
        mine_field.save_to_file(args.field_out) if hasattr(
            mine_field, 'save_to_file') else None

    # Save emoji grid if requested
    if args.emoji_out:
        export_emoji_grid_to_file(
            mine_field, out_path=args.emoji_out, use_spoilers=not args.no_spoilers)
