from os import getcwd, makedirs, remove
from os.path import basename, dirname, isdir, isfile, splitext
from urllib.request import urlopen

from PIL import Image
from unsplash.api import Api
from unsplash.auth import Auth
from unsplash.photo import Photo

import shutil

# Unsplash configuration
# Split strings to fight git scraping bots
_client_id = "cd356c3b262be554770bea925ce5119f"
_client_secret = "de43ef85676f1d417574938c19d89346"
_client_id += "0503605b31a6dc4f3e9365babfd1674c"
_client_secret += "7503fbe3ba9c89ada24192c5aa881eff"
_redirect_uri = ""
_code = ""
api = Api(Auth(_client_id, _client_secret, _redirect_uri, code=_code))

IMAGE_DIR = f"{getcwd()}/images"
CURRENT_IMAGE_DIR = f"{IMAGE_DIR}/current"


def download(photo):
    """ Downloads image from a url to the filepath """
    if not isdir(dirname(photo.filepath)):
        makedirs(dirname(photo.filepath))
    if isfile(photo.filepath):
        print(f"File {photo.filepath} already exists, using cached image")
        pass
    else:
        #print(f"Downloading {photo.filepath} from {url}")
        with open(photo.filepath, "wb") as f:
            f.write(urlopen(photo.urls.raw).read())


def unsplash_get_image(width, height, query="wallpaper"):
    """ Downloads random photos and returns a list of filepaths """
    directory = IMAGE_DIR + '/unsplash'
    try:
        results = api.photo.random(w=width, h=height, query=query)
    except unsplash.errors.UnsplashError as e:
        print("Failed to get random image:", e)
        return None

    photo = results[0]

    photo.filepath = f"{directory}/{photo.id}.jpg"
    download(photo)

    print(photo.width, photo.height)
    # Print author info
    print(f"Image found from random({width}x{height} q={query})")
    print(f" -- Description: {photo.description}")
    print(f" -- Artist: {photo.user.name}")
    print(f" -- Artist Profile: https://unsplash.com/@{photo.user.id}")
    print(f" -- Full Image: {photo.urls.raw}")

    return photo


def get_images(dimensions, source="unsplash", query="wallpaper"):
    """ Downloads images

    Args:
        dimensions:  List of dicts containing width/height attributes
        source:      Name of the image source
    Sources:
        'unsplash'       -  unsplash.com
        'mikedrawsdota'  -  wallpapers.mikedrawsdota.com
    """
    images = []

    for monitor in dimensions:
        if source == 'unsplash':
            photo = unsplash_get_image(monitor.width, monitor.height, query=query)

            images.append(photo)

    return images


def stitch_images(monitors, images):
    """ Combines a list of images into one image and returns the filepath

    Args:
        monitors:  List of Monitors with height/width attributes
        images:    List of image file paths
    """
    filename = ""
    for image in images:
        base = basename(image.filepath)
        filename += splitext(base)[0] + '_'

    filepath = CURRENT_IMAGE_DIR + '/' + filename + '.jpg'
    #print(f"Stiching images: {images}")

    width = 0
    height = 0
    min_x = 0
    min_y = 0
    for monitor in monitors:
        width += monitor.width
        height = max(height, monitor.height)
        min_x = min(monitor.x, min_x)
        min_y = min(monitor.y, min_y)

    for monitor in monitors:
        monitor.x -= min_x
        monitor.y -= min_y

    img = Image.new('RGB', (width, height))
    print(f"Created image canvas ({width}x{height})")

    for i, monitor in enumerate(monitors):
        with Image.open(images[i].filepath) as photo:
            # Resize the image if it is too large
            if photo.height > monitor.height:
                ratio = monitor.width / photo.width
                h = int(photo.height * ratio)
                if h >= monitor.height:
                    print(f"a resizing from {photo.width}x{photo.height} to {monitor.width}x{h}")
                    photo = photo.resize((monitor.width, h), Image.BICUBIC)

            if photo.width > monitor.width:
                ratio = monitor.height / photo.height
                w = int(photo.width * ratio)
                if w >= monitor.width:
                    print(f"b resizing from {photo.width}x{photo.height} to {w}x{monitor.height}")
                    photo = photo.resize((w, monitor.height), Image.BICUBIC)

            img.paste(photo, (monitor.x, monitor.y))

    # Clean old files before saving new pic
    if isdir(CURRENT_IMAGE_DIR):
        shutil.rmtree(CURRENT_IMAGE_DIR)
    makedirs(CURRENT_IMAGE_DIR)
    img.save(filepath)

    return filepath
