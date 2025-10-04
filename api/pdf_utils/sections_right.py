"""
Rendering logic for the right column of the resume, including projects,
continuing education, and customizable extra sections.
"""

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

from .config import *
from .text import draw_par
from .fonts import AR_FONT
from .labels import t  # dynamic labels
from .icons import get_section_icon, draw_heading_with_icon


def draw_right_extra_sections(
    c: canvas.Canvas,
    right_x: float,
    right_w: float,
    yR: float,
    sections_right: list[dict],
) -> float:
    """
    يرسم السكاشن النصّية الإضافية في العمود الأيمن (مثل About Me).
    يستخدم BODY_LEADING من config.py لتباعد الأسطر داخل الفقرات.
    """
    for sec in (sections_right or []):
        title = (sec.get("title") or "").strip()
        lines = [str(x).strip() for x in (sec.get("lines") or []) if str(x).strip()]
        if not title or not lines:
            continue

        # عنوان + خط تحتي (لا نضع أيقونة لسكاشن مخصّصة)
        yR = draw_heading_with_icon(
            c=c,
            x=right_x,
            y=yR,
            title=title,
            icon=None,
            font="Helvetica-Bold",
            size=RIGHT_SEC_HEADING_SIZE,
            color=HEADING_COLOR,
            underline_w=right_w,
            rule_color=RIGHT_SEC_RULE_COLOR,
            rule_width=RIGHT_SEC_RULE_WIDTH,
            gap_below=GAP_AFTER_HEADING / 2,
        )
        yR -= RIGHT_SEC_RULE_TO_TEXT_GAP

        # نص الفقرة: أسود + تباعد أسطر من BODY_LEADING
        c.setFont("Helvetica", RIGHT_SEC_TEXT_SIZE)
        c.setFillColor(colors.black)
        yR = draw_par(
            c, right_x, yR, lines, "Helvetica", RIGHT_SEC_TEXT_SIZE,
            right_w, "left", False, BODY_LEADING, RIGHT_SEC_PARA_GAP
        )

        yR -= RIGHT_SEC_SECTION_GAP

    return yR



def draw_projects(
    c: canvas.Canvas,
    right_x: float,
    right_w: float,
    yR: float,
    projects: list[tuple[str, str, str | None]],
    rtl_mode: bool = False,
) -> float:
    """
    Draws the "Selected Projects" section with optional RTL support and links.
    """
    clean_projects = []
    for title, desc, link in (projects or []):
        ttitle = (title or "").strip()
        d = (desc or "").strip()
        l = (link or "").strip() if link else None
        if ttitle or d or l:
            clean_projects.append((ttitle, d, l))

    if not clean_projects:
        return yR

    # Heading + icon + underline
    yR = draw_heading_with_icon(
        c=c,
        x=right_x,
        y=yR,
        title=t("selected_projects", UI_LANG),
        icon=get_section_icon("selected_projects"),
        font="Helvetica-Bold",
        size=HEADING_SIZE,
        color=HEADING_COLOR,
        underline_w=right_w,
        rule_color=RIGHT_SEC_RULE_COLOR,
        rule_width=RIGHT_SEC_RULE_WIDTH,
        gap_below=GAP_AFTER_HEADING / 2,
    )
    yR -= RIGHT_SEC_RULE_TO_TEXT_GAP

    # Projects content
    for title, desc, link in clean_projects:
        c.setFont("Helvetica-Bold", PROJECT_TITLE_SIZE)
        c.setFillColor(SUBHEAD_COLOR)
        c.drawString(right_x, yR, title)
        yR -= PROJECT_TITLE_GAP_BELOW

        c.setFillColor(colors.black)
        yR = draw_par(
            c=c,
            x=right_x,
            y=yR,
            lines=(desc or "").split("\n"),
            font=(AR_FONT if rtl_mode else "Helvetica"),
            size=TEXT_SIZE,
            max_w=right_w,
            align=("right" if rtl_mode else "left"),
            rtl_mode=rtl_mode,
            leading=PROJECT_DESC_LEADING,
        )

        yR -= PROJECT_LINK_GAP_ABOVE
        if link:
            font_name = "Helvetica-Oblique"
            c.setFont(font_name, PROJECT_LINK_TEXT_SIZE)
            c.setFillColor(HEADING_COLOR)
            link_text = f"Repo: {link}"
            c.drawString(right_x, yR, link_text)
            tw = pdfmetrics.stringWidth(link_text, font_name, PROJECT_LINK_TEXT_SIZE)
            asc = pdfmetrics.getAscent(font_name) / 1000.0 * PROJECT_LINK_TEXT_SIZE
            dsc = abs(pdfmetrics.getDescent(font_name)) / 1000.0 * PROJECT_LINK_TEXT_SIZE
            c.linkURL(link, (right_x, yR - dsc, right_x + tw, yR + asc * 0.2), relative=0, thickness=0)
        yR -= PROJECT_BLOCK_GAP

    return yR

def draw_education(
    c: canvas.Canvas,
    right_x: float,
    right_w: float,
    yR: float,
    education_items: list[str],
) -> float:
    """
    Draws the 'Professional Training' section.
    - أول سطر من كل بلوك يُرسم غامقًا بلون EDU_TITLE_COLOR.
    - أي سطر يبدأ بـ http/https يُرسم كرابط أزرق (HEADING_COLOR) مع linkURL.
    - بقية السطور تُرسم بالأسود.
    - يستخدم EDU_TEXT_LEADING لتباعد الأسطر داخل الفقرة،
      و EDU_BLOCK_TITLE_GAP_BELOW للمسافة تحت عنوان البلوك.
    """
    items = [str(b).strip() for b in (education_items or []) if str(b).strip()]
    if not items:
        return yR

    # العنوان الرئيسي + الأيقونة + خط تحتي
    yR = draw_heading_with_icon(
        c=c,
        x=right_x,
        y=yR,
        title=t("professional_training", UI_LANG),
        icon=get_section_icon("professional_training"),
        font="Helvetica-Bold",
        size=HEADING_SIZE,
        color=HEADING_COLOR,
        underline_w=right_w,
        rule_color=RIGHT_SEC_RULE_COLOR,
        rule_width=RIGHT_SEC_RULE_WIDTH,
        gap_below=GAP_AFTER_HEADING / 2,
    )
    yR -= RIGHT_SEC_RULE_TO_TEXT_GAP

    # محتوى البلوكات
    for block in items:
        parts = [ln.strip() for ln in block.splitlines() if ln.strip()]
        if not parts:
            continue

        # عنوان البلوك (أول سطر)
        c.setFont("Helvetica-Bold", TEXT_SIZE)
        c.setFillColor(EDU_TITLE_COLOR)
        c.drawString(right_x, yR, parts[0])
        yR -= EDU_BLOCK_TITLE_GAP_BELOW   # 👈 مسافة إضافية بين العنوان وبداية النص

        # بقية السطور
        for ln in parts[1:]:
            if ln.startswith("http://") or ln.startswith("https://"):
                # رسم كرابط
                font_name = "Helvetica-Oblique"
                c.setFont(font_name, PROJECT_LINK_TEXT_SIZE)
                c.setFillColor(HEADING_COLOR)
                c.drawString(right_x, yR, ln)

                tw = pdfmetrics.stringWidth(ln, font_name, PROJECT_LINK_TEXT_SIZE)
                asc = pdfmetrics.getAscent(font_name) / 1000.0 * PROJECT_LINK_TEXT_SIZE
                dsc = abs(pdfmetrics.getDescent(font_name)) / 1000.0 * PROJECT_LINK_TEXT_SIZE
                c.linkURL(
                    ln,
                    (right_x, yR - dsc, right_x + tw, yR + asc * 0.2),
                    relative=0,
                    thickness=0,
                )
                yR -= EDU_TEXT_LEADING
            else:
                # نص عادي
                c.setFont("Helvetica", RIGHT_SEC_TEXT_SIZE)
                c.setFillColor(colors.black)
                yR = draw_par(
                    c,
                    right_x,
                    yR,
                    [ln],
                    "Helvetica",
                    RIGHT_SEC_TEXT_SIZE,
                    right_w,
                    "left",
                    False,
                    EDU_TEXT_LEADING,
                )

        yR -= RIGHT_SEC_SECTION_GAP

    return yR




