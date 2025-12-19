import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import math
    from PIL import Image
    from Hexagonal import Hexagonal
    return Hexagonal, mo


@app.cell
def _(mo):
    input_file = mo.ui.text(value="img/screenshot.jpg", label="Path")
    mo.md(f"Path of the input file :\n{input_file}")

    size = mo.ui.slider(start=5, stop=100, value=10, label="Size of the Hexa")
    mo.md(f"Size :\n{size}")

    output_file = mo.ui.text(value="img/wallpaper.svg", label="Path")
    mo.md(f"Path of the output file :\n{output_file}")

    button = mo.ui.run_button(label="Generate Wallpaper")
    mo.vstack([input_file, size, output_file, button])
    return button, input_file, output_file, size


@app.cell
def _(Hexagonal, button, input_file, mo, output_file, size):
    mo.stop(not button.value)
    print("Good job, the wallpaper is generate.")
    hex = Hexagonal(input_file.value, size.value)
    hex.create_hexas()
    hex.generate_img(output_file.value)

    with open(output_file.value, "r") as f:
        svg_data = f.read()

    mo.Html(svg_data)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Testing on different picture of different size
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Cat picture
    """)
    return


@app.cell
def _(Hexagonal):
    cat_gen = Hexagonal("img/cat.jpg", 10)
    cat_gen.create_hexas()
    cat_gen.generate_img("img/cat.svg")
    return


@app.cell
def _(mo):
    with open("img/cat.svg", "r") as f2:
        cat_svg = f2.read()

    mo.Html(cat_svg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Nuit etoilee -- size 50
    """)
    return


@app.cell
def _(Hexagonal):
    night = Hexagonal("img/NuitEtoilee.jpg", 50)
    night.create_hexas()
    night.generate_img("img/NuitEtoilee.svg")
    return


@app.cell
def _(mo):
    with open("img/NuitEtoilee.svg", "r") as f3:
        night_svg = f3.read()

    mo.Html(night_svg)
    return


if __name__ == "__main__":
    app.run()
