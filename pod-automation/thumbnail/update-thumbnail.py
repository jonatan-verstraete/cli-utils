import sys, os
from html2image import Html2Image
from pathlib import Path
from PIL import Image


def usage():
    print('Usage: update_thumbnail 21 "Guest Lastname" ~/Downloads/guest.png')
    sys.exit(1)

if len(sys.argv) < 3:
    print('Error: missing arguments, must be 3')
    usage()

try:
    podCount = sys.argv[1]
    podNameGuest = sys.argv[2]
    pathImgGuest = sys.argv[3]
except Exception as _:
    usage()


try:
    int(podCount)
except Exception as _:
    print(f'Error: passed post count "{podCount}" is not a valid number')
    usage()
    print('DEV:', _)


try:
    firstname, lastname = podNameGuest.split(' ')
except Exception as _:
    pass


if not firstname or not lastname:
    print(f'Error: need to pass both firstname and lastname with a space in between. Current: "{podNameGuest}"')
    usage()

if not os.path.exists(pathImgGuest) or not os.path.isfile(pathImgGuest):
    print(f'Error: the passed image is not a valid image path: {pathImgGuest}')
    usage()


base_dir = Path(__file__).parent
html_path = base_dir / "template.html"

with open(html_path, "r", encoding="utf-8") as f:
    original_html = f.read()

html_updated = original_html.replace('[[img_guest]]', pathImgGuest)
html_updated = html_updated.replace('[[count]]', podCount)
html_updated = html_updated.replace('[[firstname]]', firstname)
html_updated = html_updated.replace('[[lastname]]', lastname)

html_updated = html_updated.replace('./static_background.png', str(base_dir / 'static_background.png'))


outputDir = os.path.expanduser(f'~/Desktop')
outputName = f"thumbnail-{podCount}-{firstname}-{lastname}.png"


hti = Html2Image(output_path=outputDir)
hti.screenshot(
    html_str=html_updated,
    save_as=outputName,
    size=(682, 965),
)


# note: made the css body 100px smaller due to "idk issue", now we drop it back.
imagePath = f'{outputDir}/{outputName}'
img = Image.open(imagePath)
cropped = img.crop((0, 0, img.width, img.height - 100))
cropped.save(imagePath)

print(f"✅ Saved to: {imagePath}")
