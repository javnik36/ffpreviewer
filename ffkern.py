import pathlib as pl
import fontforge as ff

__font_path__ = pl.Path("Arkhamic.ttf")
__glyphs_folder__ = pl.Path("glyphs")


def import_font(fontpath=__font_path__):
    worth_glyphs = []

    font_holder = ff.open(str(__font_path__)) # ff.font obj
    for glyph in font_holder.glyphs():
        if font_holder[glyph.glyphname].isWorthOutputting():
            worth_glyphs.append(font_holder[glyph.glyphname])
    return font_holder,worth_glyphs

def remove_non_unicode_glyphs(worth_glyphs):
    glyph_pairs_worth = []
    for item in worth_glyphs:
        glyph_repr = repr(item).split(" ")
        if not glyph_repr[3].startswith("U+"):
            continue
        else:
            glyph_pairs_worth.append(item)
    return glyph_pairs_worth

def setup_printing():
    ff.printSetup('pdf-file',"z.pdf")

def generate_glyph_files(worth_glyphs, glyphs_folder=__glyphs_folder__):
    for item in worth_glyphs:
        glyph_name = ""
        glyph_repr = repr(item).split(" ")
        if glyph_repr[3].startswith("U+"):
            glyph_name = glyph_repr[3]
        else:
            glyph_name = item.glyphname
        item.export(f"{str(glyphs_folder.joinpath(glyph_name))}.png")

def generate_kern_pairs(font_holder, worth_glyphs):
    kerning_table = []
    table_name="'kern' Horizontal Kerning lookup 0 subtable"
    for glyph in worth_glyphs:
        kernings = glyph.getPosSub(table_name)
        for kerning in kernings:
            if kerning[1] == "Pair":
                # glyph1.name, glyph2.name, alignment
                kerning_table.append((glyph.glyphname, kerning[2], kerning[5]))

    print_sample = ""
    divider = "    "
    setup_printing()
    for kern in kerning_table:
        print_sample += f"{chr(font_holder[kern[0]].encoding)}{chr(font_holder[kern[1]].encoding)}"
        print_sample += divider
    font_holder.printSample('fontsample', 14, print_sample, "kerning-pairs.pdf")#remove sample text from .ps
    #glyph.getPosSub('*')
    #(("'kern' Horizontal Kerning lookup 0 subtable", 'Pair', 'W', 0, 0, 12, 0, 0, 0, 0, 0),)
    #name,typeoftable,leter,>,>,horizontal_advance

def generate_all_permutations(font_holder):
    glyph_pairs_worth = remove_non_unicode_glyphs()

    setup_printing()

    print_sample = ""
    divider = "    "

    for i in range(len(glyph_pairs_worth)-1):
        print_sample += f"\n\nPermutations of '{chr(glyph_pairs_worth[i].encoding)}'\n"
        for j in range(len(glyph_pairs_worth)-1):
            print_sample += f"{chr(glyph_pairs_worth[i].encoding)}{chr(glyph_pairs_worth[j].encoding)}"
            print_sample += divider

    font_holder.printSample('fontsample', 14, print_sample, "all_permutations.pdf") #remove sample text from .pdf (?)

def generate_permitations_for_single_char(font_holder, target_character):
    glyph_pairs_worth = remove_non_unicode_glyphs()
    __target_character__ = 44 #ascii encoded period
    target_glyph = font_holder[__target_character__]
    target_glyph_unicode_repr = chr(target_glyph.encoding)

    setup_printing()

    print_sample = f"Permutations of {target_glyph_unicode_repr}\n"
    sample_1st_part = ""
    sample_2nd_part = ""
    divider = "    "

    for i in range(len(glyph_pairs_worth)-1):
        sample_1st_part += f"{target_glyph_unicode_repr}{chr(glyph_pairs_worth[i].encoding)}{divider}"
        sample_2nd_part += f"{chr(glyph_pairs_worth[i].encoding)}{target_glyph_unicode_repr}{divider}"

    print_sample += sample_1st_part
    print_sample += '\n\n\n\n'
    print_sample += sample_2nd_part
    font_holder.printSample('fontsample', 14, print_sample, "single_char_permutations.pdf")


generate_kern_pairs()
generate_all_permutations()