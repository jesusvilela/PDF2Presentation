import nltk
import PyPDF2
import fitz
import openai
import torch
import re
from pptx import Presentation
from pptx.util import Inches
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler
from io import BytesIO
from PIL import Image
import os


nltk.download('punkt')

openai.api_key = "your_openai_key"


def extract_text_from_pdf(file_path):
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfFileReader(file)
        text = []
        for page in range(reader.getNumPages()):
            text.append(reader.getPage(page).extract_text())
    return text


def extract_images_from_pdf(file_path):
    doc = fitz.open(file_path)
    images = []
    image_indices = []
    for i in range(len(doc)):
        for img in doc.get_page_images(i):
            xref = img[0]
            img_data = doc.extract_image(xref)
            images.append(img_data['image'])
            image_indices.append(i)
    return images, image_indices


def structure_text(pages):
    sections = []
    for page in pages:
        page = page.replace('\n', ' ').replace('....', '.')
        page = re.sub(' +', ' ', page)
        sections.append([section.strip() for section in page.split(":")])
    return sections


def generate_summary(section):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=section,
        temperature=0.3,
        max_tokens=60
    )
    summary = response.choices[0].text.strip()
    summary = re.sub('[^a-zA-Z0-9 \n\.]', '', summary)
    return summary


def generate_title(section, summary):
    prompt = section[0].split(".")[0] + " " + summary
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=10
    )
    return response.choices[0].text.strip()


def generate_cover(title):
    model_id = "stabilityai/stable-diffusion-2-1-base"
    scheduler = EulerDiscreteScheduler.from_pretrained(model_id, subfolder="scheduler")
    pipe = StableDiffusionPipeline.from_pretrained(model_id, scheduler=scheduler, torch_dtype=torch.float32)
    pipe = pipe.to("cpu")
    if len(title.split(' ')) > 77:
        prompt = ' '.join(title.split(' ')[:77])
    image = pipe(title).images[0]
    image_path = f"{title.replace(' ', '_')}_cover.png"
    image.save(image_path)
    return image_path

def add_image_to_slide(slide, image_data_or_path):
    if isinstance(image_data_or_path, bytes):
        img_stream = BytesIO(image_data_or_path)
    else:  # Assuming it's a filepath if it's not bytes
        with open(image_data_or_path, 'rb') as f:
            image_data = f.read()
        img_stream = BytesIO(image_data)
    slide.shapes.add_picture(img_stream, Inches(2), Inches(2), height=Inches(5))


def add_bullet_points_to_slide(slide, points):
    bullet_slide = slide.shapes
    for point in points:
        bullet_slide.text = point

def generate_presenter_notes(content):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=content,
        temperature=0.3,
        max_tokens=60
    )
    notes = response.choices[0].text.strip()
    notes = re.sub('[^a-zA-Z0-9 \n\.]', '', notes)
    return notes


def create_presentation(titles, contents, images, image_indices, cover_image_path):
    presentation = Presentation()
    slide_layout = presentation.slide_layouts[0]
    slide = presentation.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Your Presentation Title"
    # Adding the cover image
    add_image_to_slide(presentation.slides[0], cover_image_path)

    for i, (title_text, content) in enumerate(zip(titles, contents)):
        slide_layout = presentation.slide_layouts[1]
        slide = presentation.slides.add_slide(slide_layout)
        title = slide.shapes.title
        title.text = title_text
        add_bullet_points_to_slide(slide, content)
        if i in image_indices:
            add_image_to_slide(slide, images[image_indices.index(i)])
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = generate_presenter_notes(content)
    presentation.save("my_presentation.pptx")
    return presentation

def main():
    file_path = "document.pdf"
    pages = extract_text_from_pdf(file_path)
    images, image_indices = extract_images_from_pdf(file_path)
    sections = structure_text(pages)
    summaries = [generate_summary(page) for page in sections]
    titles = [generate_title(page, summary) for page, summary in zip(sections, summaries)]
    cover_image_path = generate_cover(titles[0])
    presentation = create_presentation(titles, sections, images, image_indices, cover_image_path)
    # Adding the cover image
    with open(cover_image_path, "rb") as img_file:
        cover_image_data = img_file.read()
    add_image_to_slide(presentation.slides[0], cover_image_data)

if __name__ == "__main__":
    main()
