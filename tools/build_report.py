from argparse import ArgumentParser
from re import fullmatch
from pathlib import Path

from PIL import Image
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parent.parent
parser = ArgumentParser()
parser.add_argument("--repository-url", required=True)
repository_url = parser.parse_args().repository_url.rstrip("/")
if not fullmatch(r"https://github[.]com/[A-Za-z0-9-]+/[A-Za-z0-9_.-]+", repository_url):
    parser.error("Enter the HTTPS GitHub repository URL for this project.")

W, H = A4
M = 44
WIDTH = W - 2 * M
INK = HexColor("#14253C")
MUTED = HexColor("#4A5D73")
LINE = HexColor("#D2DEE9")
for name, filename in [("Segoe", "segoeui.ttf"), ("Segoe Bold", "segoeuib.ttf")]:
    pdfmetrics.registerFont(TTFont(name, f"C:/Windows/Fonts/{filename}"))
pdfmetrics.registerFontFamily("Segoe", normal="Segoe", bold="Segoe Bold")


class Report:
    def __init__(self, project, title, goal, accent, pages, author):
        self.project, self.title, self.goal = project, title, goal
        self.author = author
        self.accent, self.pages = HexColor(accent), pages
        self.path = ROOT / f"SDG_{project}_{author}.pdf"
        self.canvas = Canvas(str(self.path), pagesize=A4)
        self.canvas.setTitle(f"{title} – AI Final Project")
        self.canvas.setSubject(f"United Nations Sustainable Development Goal {goal}")
        self.canvas.setAuthor(author)

    def text(self, text, x, y, size=11, bold=False, color=INK):
        self.canvas.setFont("Segoe Bold" if bold else "Segoe", size)
        self.canvas.setFillColor(color)
        self.canvas.drawString(x, H - y, text)

    def para(self, text, y, size=11, color=INK, width=WIDTH):
        style = ParagraphStyle("body", fontName="Segoe", fontSize=size,
                               leading=size * 1.43, textColor=color)
        body = Paragraph(text, style)
        _, height = body.wrap(width, H)
        assert y + height < H - 42, (self.title, y, height, text)
        body.drawOn(self.canvas, M, H - y - height)
        return y + height

    def page(self, number, section, title, subtitle):
        self.text(f"AI FINAL PROJECT   /   SDG {self.goal}", M, 39, 10, True, self.accent)
        self.canvas.setStrokeColor(LINE)
        self.canvas.line(M, H - 51, W - M, H - 51)
        self.text(section, M, 77, 10, True, self.accent)
        self.text(title, M, 112, 29, True)
        self.para(subtitle, 126, 11.5, MUTED)
        self.canvas.line(M, 38, W - M, 38)
        self.text(f"{self.title}  |  {self.author}", M, H - 23, 9, True, MUTED)
        self.text(f"{number} / {self.pages}", W - M - 25, H - 23, 9, True, MUTED)

    def section(self, title, y, paragraph):
        self.text(title, M, y + 16, 16, True)
        return self.para(paragraph, y + 26) + 17

    def item(self, label, message, y):
        return self.para(f"<b>{label}</b> {message}", y) + 12

    def link(self, title, path, y, x=M):
        length = pdfmetrics.stringWidth(title, "Segoe Bold", 11)
        self.text(title, x, y, 11, True, self.accent)
        self.canvas.setStrokeColor(self.accent)
        self.canvas.line(x, H - y - 2, x + length, H - y - 2)
        self.canvas.linkURL(path, (x, H - y - 4, x + length, H - y + 12), relative=0)

    def shot(self, basename, caption, y, width=WIDTH):
        path = ROOT / "screenshots" / f"sdg-{basename}.png"
        with Image.open(path) as image:
            height = width * image.height / image.width
        assert y + height < H - 56
        self.canvas.drawImage(str(path), M, H - y - height, width, height)
        self.canvas.setStrokeColor(LINE)
        self.canvas.rect(M, H - y - height, width, height, stroke=1, fill=0)
        return self.para(caption, y + height + 6, size=10, color=MUTED) + 17

    def sources(self, y, scope):
        self.text("7 Open source repository", M, y + 16, 16, True)
        y = self.para(
            "The MIT-licensed source package includes the standalone application, a README "
            "with run instructions, and the license.",
            y + 27,
        )
        self.link("Open the offline demo", self.project + ".html", y + 25)
        self.link("Open the source ZIP", self.project + "-Source.zip", y + 25, M + 153)
        self.link(repository_url, repository_url, y + 46)
        y = self.para(
            "Keep this PDF, the HTML file and the ZIP together. If a PDF viewer blocks these local "
            "links, open the HTML or ZIP directly from the folder.",
            y + 57, size=10, color=MUTED,
        )
        return self.section("8 Future scope", y + 18, scope)

    def finish(self):
        self.canvas.save()
        pdf = PdfReader(self.path)
        assert len(pdf.pages) == self.pages
        assert pdf.metadata.author == self.author
        assert all(self.author in page.extract_text() for page in pdf.pages)
        urls = {
            annotation.get_object()["/A"]["/URI"]
            for page in pdf.pages for annotation in (page.get("/Annots") or [])
        }
        assert {f"https://sdgs.un.org/goals/goal{self.goal}", self.project + ".html",
                self.project + "-Source.zip", repository_url} <= urls
        print(f"Verified {self.path.name}, {len(pdf.pages)} pages with reference and artifact links.")


numeracy = Report("NumeracyPath", "Numeracy Path", 4, "#3755AD", 4, "Sakshi")
numeracy.page(1, "SDG SELECTION AND PROBLEM DEFINITION", "Numeracy Path",
              "An offline AI prototype for personalised fraction practice.")
y = numeracy.section(
    "1 Selected SDG and reason for selection", 163,
    "The project supports <b>SDG 4, Quality Education</b>, particularly Target 4.1 on primary and "
    "secondary education and effective learning outcomes. The UN tracks minimum mathematics "
    "proficiency under indicator 4.1.1. Fraction skills matter because students use them to "
    "compare quantities, follow measurements and solve later ratio problems.",
)
numeracy.link("United Nations SDG 4 and Target 4.1", "https://sdgs.un.org/goals/goal4", y + 2)
y = numeracy.section(
    "2 Problem statement", y + 22,
    "In upper-primary classrooms and after-school learning centres, students may receive the same "
    "fraction worksheets even when their individual gaps differ. A learner who can add like "
    "denominators may still struggle to compare unlike fractions. Learners with limited opportunities "
    "for one-to-one support may repeat the wrong strategy between lessons. If that gap persists, "
    "later work with ratios, percentages and measurement can become harder.",
)
y = numeracy.section(
    "3 Proposed solution and objective", y,
    "Numeracy Path aims to direct practice toward the fraction skill that needs attention. A learner "
    "answers a four-option question, sees an explanation and views a dashboard. The app updates the "
    "estimated mastery of the question’s skill and recommends the next skill. Students can use it "
    "independently on a shared or personal device. Teachers and tutors can use it for a short practice session.",
)
numeracy.canvas.showPage()

numeracy.page(2, "FEATURES AND TECHNOLOGY", "How the tutor adapts",
              "The prototype models three skills and updates the recommendation after each answer.")
y = 170
for label, body in [
    ("Guided practice.", "Twelve authored questions cover equivalent fractions, comparing fractions and adding fractions. The prototype shows one question at a time."),
    ("Answer explanations.", "Each choice triggers specific feedback and a worked explanation. For example, multiplying both parts of 1/2 by 2 produces 2/4."),
    ("Learning dashboard.", "Three progress bars show estimated mastery. The model starts each skill at 30% and selects the skill with the lowest estimate for the next question."),
    ("Session controls.", "Next question uses the current recommendation. Reset clears the session and restores the initial estimates. The app keeps answers in browser memory."),
]:
    if y == 170:
        numeracy.text("4 Project features", M, y, 16, True)
        y += 13
    y = numeracy.item(label, body, y)
y = numeracy.section(
    "5 Technology stack", y + 1,
    "<b>HTML and CSS</b> provide the practice form, feedback and responsive dashboard. "
    "<b>JavaScript</b> implements the question bank and Bayesian Knowledge Tracing. "
    "<b>Playwright and Chromium</b> automate interaction tests and capture evidence.",
)
y = numeracy.section(
    "Model decision", y,
    "The model uses Bayes’ rule to revise the current probability of knowing a skill. It allows "
    "for guessing (25%) and mistakes despite knowing the skill (12%). It then applies a 10% "
    "learning transition to the remaining probability of not knowing the skill. For example, a "
    "correct answer raises the starting estimate from 30% to 64%. The parameters are set for "
    "demonstration and have not been estimated from learner data.",
)
numeracy.section(
    "Verification", y,
    "Offline browser tests verified correct and incorrect answers, the change from 30% to 64% "
    "after a correct equivalence answer, a drop from 30% to 16% after an incorrect comparison, "
    "progression across all three skills, session reset and a 390-pixel mobile layout.",
)
numeracy.canvas.showPage()

numeracy.page(3, "6 PROJECT SCREENSHOTS", "Starting and adapting",
              "Screenshots captured from the running offline prototype.")
y = numeracy.shot("numeracy-start", "<b>Figure 1.</b> The opening screen shows the first question, "
                  "four answer choices, and all three skill estimates at 30%.", 165, 365)
numeracy.shot("numeracy-correct", "<b>Figure 2.</b> A correct answer brings equivalent fractions to "
              "64% and moves the recommendation to comparing fractions at 30%.", y, 365)
numeracy.canvas.showPage()

numeracy.page(4, "PROOF OF WORK AND NEXT STEPS", "Feedback and source",
              "After an incorrect answer, the app shows the reasoning and recommends more practice.")
y = numeracy.shot("numeracy-incorrect", "<b>Figure 3.</b> The incorrect comparison lowers that skill "
                  "estimate to 16%. The app explains the answer and keeps comparing fractions as the next focus.", 165, 425)
numeracy.sources(y, "Expand the question bank, test the interface with learners and teachers, and fit "
                    "model parameters using consented practice data. A pilot could compare performance "
                    "on new fraction questions before and after a session to check whether the adaptive practice helps.")
numeracy.canvas.showPage()
numeracy.finish()
