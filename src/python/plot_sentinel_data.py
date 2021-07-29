from PIL import Image


COLOUR_MAP = "RdYlGn"

def plot_image(satellite, overlay):
    width, height = satellite.size

    # scale overlay to fit satellite image
    overlay = overlay.resize((width, height), Image.ANTIALIAS)

    # make whites of heatmap transparent
    # make other pixels semi transparent
    thresh = 180
    pixdata = overlay.load()
    for y in range(height):
        for x in range(width):
            pixel = pixdata[x, y]
            if all([pix > thresh for pix in pixel]):
            # if pixdata[x, y] == (255, 255, 255, 255):
                pixdata[x, y] = (255, 255, 255, 0)
            else:
                semi_trans_pixel = (pixel[0], pixel[1], pixel[2], int(255/3.5))
                pixdata[x, y] = semi_trans_pixel
                pass

    # blend together
    satellite = satellite.convert("RGBA")
    overlay = overlay.convert("RGBA")

    satellite.paste(overlay, (0,0), overlay)
    return satellite

if __name__ == "__main__":
    plot_image()