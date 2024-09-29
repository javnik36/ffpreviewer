import pathlib as pl
import fontforge as ff
#from PIL import Image as pim

__ff_path__ = pl.Path("F:\FontForgeBuilds").joinpath("bin", "ffpython.exe")
__font_path__ = pl.Path("Arkhamic.ttf")
__glyphs_folder__ = pl.Path("glyphs")
__kern_pairs_folder__ = pl.Path("kern-pairs")
__glyph_pairs_folder__ = pl.Path("glyph-pairs")

worth_glyphs = []

font_holder = ff.open(str(__font_path__)) # ff.font obj
for glyph in font_holder.glyphs():
    if font_holder[glyph.glyphname].isWorthOutputting():
        worth_glyphs.append(font_holder[glyph.glyphname])

def generate_glyph_files():
    for item in worth_glyphs:
        glyph_name = ""
        glyph_repr = repr(item).split(" ")
        if glyph_repr[3].startswith("U+"):
            glyph_name = glyph_repr[3]
        else:
            glyph_name = item.glyphname
        #item.export(f"{str(__glyphs_folder__.joinpath(item.glyphname))}.png")
        item.export(f"{str(__glyphs_folder__.joinpath(glyph_name))}.png")

def generate_kern_pairs():
    kerning_table = []
    table_name="'kern' Horizontal Kerning lookup 0 subtable"
    for glyph in worth_glyphs:
        kernings = glyph.getPosSub(table_name)
        for kerning in kernings:
            if kerning[1] == "Pair":
                # glyph1.name, glyph2.name, alignement
                kerning_table.append((glyph.glyphname, kerning[2], kerning[5]))
                # glyph1, glyph2, alignement
                #kerning_table.append((glyph, kerning[2], kerning[5]))

    #ff.printSetup('pdf-file','z.pdf',2000,2000)
    #comd = "gswin64c -dSAFER -dBATCH -dQUIET -dNOPAUSE -dEPSCrop -r600 -sDEVICE=png256 -sOutputFile='sampel.png'"
    #ff.printSetup('command',comd)
    #ff.printSetup('ps-file',"z.ps",300,200)
    print_sample = ""
    divider = "    "
    ff.printSetup('pdf-file',"z.pdf")
    for kern in kerning_table:
        #sample_text = f"{kern[0]}{kern[1]}"
        #font_holder.printSample('chars', 0, sample_text, f"{str(__kern_pairs_folder__.joinpath(sample_text))}.png")
        #font_holder.selection.select(kern[0])
        #font_holder.selection.select(('more', None),kern[1])
        ####1 file - 1 pair
        #sample_text = f"{chr(font_holder[kern[0]].encoding)}{chr(font_holder[kern[1]].encoding)}"
        #sample_name = f"{kern[0]}{kern[1]}"
        #font_holder.printSample('fontsample', 0, sample_text, f"{str(__kern_pairs_folder__.joinpath(sample_name))}.ps")#remove sample text from .ps
        #font_holder.selection.none()
        print_sample += f"{chr(font_holder[kern[0]].encoding)}{chr(font_holder[kern[1]].encoding)}"
        print_sample += divider
    font_holder.printSample('fontsample', 14, print_sample, f"{str(__kern_pairs_folder__.joinpath('kern-pairs'))}.pdf")#remove sample text from .ps


    #glyph.getPosSub('*')
    #(("'kern' Horizontal Kerning lookup 0 subtable", 'Pair', 'W', 0, 0, 12, 0, 0, 0, 0, 0),)
    #name,typeoftable,leter,>,>,horizontal_advance
    #font.getLookupInfo
    #font.printSample

def generate_all_permutations():
    glyph_pairs_worth = []
    for item in worth_glyphs:
        glyph_repr = repr(item).split(" ")
        if not glyph_repr[3].startswith("U+"):
            continue
        else:
            glyph_pairs_worth.append(item)

    ff.printSetup('pdf-file',"z.pdf")

    print_sample = ""
    divider = "    "

    for i in range(len(glyph_pairs_worth)-1):
        print_sample += f"\n\nPermutations of '{chr(glyph_pairs_worth[i].encoding)}'\n"
        for j in range(len(glyph_pairs_worth)-1):
            print_sample += f"{chr(glyph_pairs_worth[i].encoding)}{chr(glyph_pairs_worth[j].encoding)}"
            print_sample += divider
            #print_sample = f"{chr(glyph_pairs_worth[i].encoding)}{chr(glyph_pairs_worth[j].encoding)}"
            #sample_name = f"{glyph_pairs_worth[i].glyphname}{glyph_pairs_worth[j].glyphname}"
            #font_holder.printSample('fontsample', 20, print_sample, f"{str(__glyph_pairs_folder__.joinpath(sample_name))}.ps")#remove sample text from .ps

    font_holder.printSample('fontsample', 14, print_sample, f"{str(__glyph_pairs_folder__.joinpath('sample_graph_pairs'))}.pdf")#remove sample text from .ps



generate_kern_pairs()
generate_all_permutations()