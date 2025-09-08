from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path


def create_icon(size: int, out_path: Path) -> None:
	img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
	draw = ImageDraw.Draw(img)

	# Background rounded rectangle
	radius = max(4, size // 6)
	bg_color_top = (229, 57, 53, 255)      # #e53935
	bg_color_bottom = (211, 47, 47, 255)   # #d32f2f

	# Gradient background
	for y in range(size):
		r = int(bg_color_top[0] + (bg_color_bottom[0] - bg_color_top[0]) * (y / size))
		g = int(bg_color_top[1] + (bg_color_bottom[1] - bg_color_top[1]) * (y / size))
		b = int(bg_color_top[2] + (bg_color_bottom[2] - bg_color_top[2]) * (y / size))
		draw.line([(0, y), (size, y)], fill=(r, g, b, 255))

	# Mask to round corners
	mask = Image.new('L', (size, size), 0)
	mask_draw = ImageDraw.Draw(mask)
	mask_draw.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
	img.putalpha(mask)

	# Shield glyph using a simple polygon
	pad = size * 0.18
	shield = [
		(pad, size * 0.30),
		(size * 0.50, pad),
		(size - pad, size * 0.30),
		(size * 0.80, size * 0.75),
		(size * 0.50, size - pad),
		(size * 0.20, size * 0.75),
	]
	# Shadow
	shadow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
	sd = ImageDraw.Draw(shadow)
	sd.polygon(shield, fill=(0, 0, 0, 80))
	shadow = shadow.filter(ImageFilter.GaussianBlur(radius=max(1, size // 32)))
	img = Image.alpha_composite(img, shadow)
	# Foreground glyph
	draw = ImageDraw.Draw(img)
	draw.polygon(shield, fill=(255, 255, 255, 235))

	# Subtle inner highlight
	hl = Image.new('RGBA', (size, size), (0, 0, 0, 0))
	hld = ImageDraw.Draw(hl)
	hld.ellipse([size * 0.10, size * 0.05, size * 0.90, size * 0.70], fill=(255, 255, 255, 28))
	hl = hl.filter(ImageFilter.GaussianBlur(radius=max(1, size // 24)))
	img = Image.alpha_composite(img, hl)

	out_path.parent.mkdir(parents=True, exist_ok=True)
	img.save(out_path, format='PNG')


def main() -> None:
	root = Path(__file__).resolve().parent
	icons = root / 'icons'
	create_icon(16, icons / 'icon16.png')
	create_icon(48, icons / 'icon48.png')
	create_icon(128, icons / 'icon128.png')
	print('Icons generated at:', icons)


if __name__ == '__main__':
	main()


