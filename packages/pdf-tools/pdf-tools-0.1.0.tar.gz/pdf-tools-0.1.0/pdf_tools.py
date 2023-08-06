import os
import glob
import click
import fitz

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<meta http-equiv="X-UA-Compatible" content="IE=edge">
</head>
<body>
{divs}
</body>
</html> 
"""

def _filename_key(filename):
    basename = os.path.basename(filename)
    name, _ = os.path.splitext(basename)
    if name.isdigit():
        return int(name)
    else:
        return name

def get_images(folder):
    images = glob.glob(os.path.join(folder, "*"))
    images.sort(key=_filename_key)
    return images

def get_doc(filename, password=None):
    doc = fitz.open(filename)
    if password:
        doc.authenticate(password)
    return doc

def get_info(doc):
    info = {}
    info.update(doc.metadata)
    info["pageCount"] = doc.pageCount
    return info

def get_text(doc):
    text = ""
    for i in range(doc.pageCount):
        text += doc.getPageText(i, "text")
    return text

def get_html(doc):
    title = doc.metadata["title"]
    divs = ""
    for i in range(doc.pageCount):
        div = doc.getPageText(i, "html")
        divs += div
    html = HTML_TEMPLATE.format(
        title=title,
        divs=divs,
    )
    return html


def convert_pdf_to_images(filename, output, type="png", password=None):
    doc = get_doc(filename, password)
    output = _get_output_folder(output, filename)
    images = []
    for i in range(doc.pageCount):

        image = os.path.join(output, "{0}.{1}".format(i+1, type))
        images.append(image)
        page = doc.loadPage(i)
        im = page.getPixmap()
        im.writeImage(image, type)
    return images

def make_pdf_from_images(folder, output=None):
    images = get_images(folder)
    doc = fitz.Document()
    pno = 0
    for image in images:
        pix = fitz.Pixmap(image)
        rect = fitz.Rect(0, 0, pix.width, pix.height)
        page = doc.newPage(pno, pix.width, pix.height)
        page.insertImage(rect, pixmap=pix, overlay=True)
        pno += 1
    if output:
        doc.save(output, garbage=4, clean=True, deflate=True, pretty=True)
    return doc

def _get_output_folder(output, filename):
    if not output:
        dirname = os.path.dirname(filename)
        basename = os.path.basename(filename)
        name, _ = os.path.splitext(basename)
        output = os.path.join(dirname, name)
        if output == filename:
            output += ".images"
    if not os.path.exists(output):
        os.makedirs(output, exist_ok=True)
    return output


@click.group()
def pdf_tools():
    pass


@pdf_tools.command()
@click.option("-p", "--password")
@click.argument("filename", nargs=1, required=True)
def pdfmeta(password, filename):
    doc = get_doc(filename, password)
    info = get_info(doc)
    for key, value in info.items():
        click.echo("{0}: {1}".format(key, value))


@pdf_tools.command()
@click.option("-p", "--password")
@click.argument("filename", nargs=1, required=True)
def pdf2text(password, filename):
    doc = get_doc(filename, password)
    text = get_text(doc)
    click.echo(text)


@pdf_tools.command()
@click.option("-p", "--password")
@click.argument("filename", nargs=1, required=True)
def pdf2html(password, filename):
    doc = get_doc(filename, password)
    html = get_html(doc)
    click.echo(html)


@pdf_tools.command()
@click.option("-p", "--password")
@click.option("-o", "--output")
@click.option("-t", "--type", type=click.Choice(["png", "jpg"]), default="png")
@click.argument("filename", nargs=1, required=True)
def pdf2images(password, output, type, filename):
    images = convert_pdf_to_images(filename, output, type, password)
    click.echo("PDF file {0} converted to {1} images.".format(filename, len(images)))


@pdf_tools.command()
@click.option("-o", "--output", help="PDF filename.", required=True)
@click.argument("folder", nargs=1, required=True)
def images2pdf(output, folder):
    make_pdf_from_images(folder, output)
    click.echo("PDF file {0} created.".format(output))


if __name__ == "__main__":
    pdf_tools()
