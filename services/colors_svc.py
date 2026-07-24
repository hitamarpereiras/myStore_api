from colorthief import ColorThief
import webcolors as wc
import json


def get_this_colors(byte_image_path):
    ct = ColorThief(byte_image_path)

    palet_colors = {
        "cor_1": '',
        "cor_2": '',
        "cor_3": '',
        "cor_4": ''
    } 

    # Paleta com N cores
    colors = ct.get_palette(color_count=4, quality=10)

    for color in colors:
        rgb_color = (color[0], color[1], color[2])
        hex_color = wc.rgb_to_hex(rgb_color)

        if palet_colors["cor_1"] == '':
            palet_colors["cor_1"] = hex_color
        elif palet_colors["cor_2"] == '':
            palet_colors["cor_2"] = hex_color
        elif palet_colors["cor_3"] == '':
            palet_colors["cor_3"] =hex_color
        elif palet_colors["cor_4"] == '':
            palet_colors["cor_4"] = hex_color

    palet_jason = json.dumps(palet_colors)
    
    return palet_jason