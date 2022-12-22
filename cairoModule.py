import cairosvg

def convert2Png(svgFile):
    cairosvg.svg2png(url= svgFile, write_to="output{}.png".format(svgFile[:-4]))
    return "output{}.png".format(svgFile[:-4])