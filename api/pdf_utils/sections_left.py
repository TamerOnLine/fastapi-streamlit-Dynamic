"""
Rendering logic for the left column of the resume, including personal info,
skills, languages, and additional custom sections.
"""

from reportlab.pdfgen import canvas
from reportlab.lib import colors

from .config import *  # uses LEFT_* and general styles
from .icons import ICON_PATHS, draw_icon_line, get_section_icon, draw_heading_with_icon
from .text import wrap_text, draw_par
from .social import extract_social_handle
from .labels import t
from .config import UI_LANG


def info_line(
    c: canvas.Canvas,
    x: float,
    y: float,
    key: str,
    value: str,
    max_w: float,
    line_gap: float = LEFT_LINE_GAP,
    size: int = LEFT_TEXT_SIZE,
) -> float:
    """
    Draw a single line with icon + text + optional hyperlink (for social).
    Adjusted to match icons.draw_icon_line signature.
    """
    raw = (value or "").strip()
    display = raw
    link = None

    # Normalize key for icon lookup
    key_lc = (key or "").strip().lower()
    icon = ICON_PATHS.get(key_lc) or ICON_PATHS.get(key)  # fallback for original keys

    # Transform social fields into links / clean handles
    if key in ("GitHub", "LinkedIn"):
        got = extract_social_handle(key, raw)
        if got:
            display, link = got
        else:
            import re
            v = raw.lower().strip()
            for pref in ("github:", "linkedin:"):
                if v.startswith(pref):
                    v = v[len(pref):].strip()
                    break
            v = re.sub(r'^(https?://)?(www\.)?', '', v, flags=re.I).strip()
            v = v.lstrip('@').strip()

            if key == "GitHub":
                if v.startswith("github.com/"):
                    v = v.split("/", 1)[1]
                v = v.split("/")[0]
                if v:
                    display = v
                    link = f"https://github.com/{v}"

            elif key == "LinkedIn":
                if v.startswith("linkedin.com/"):
                    parts = v.split("/", 2)
                    if len(parts) >= 3:
                        v = parts[2]
                v = v.split("/")[0]
                if v:
                    display = v
                    link = f"https://www.linkedin.com/in/{v}"

    # Use draw_icon_line(text first, then pass icon, link)
    return draw_icon_line(
        c=c,
        x=x,
        y=y,
        text=display,
        icon=icon,
        icon_w=ICON_SIZE,
        icon_h=ICON_SIZE,
        pad_x=ICON_PAD_X,
        size=size,
        line_gap=line_gap,
        max_w=max_w,
        link=link,
    )


def draw_left_extra_sections(
    c: canvas.Canvas,
    inner_x: float,
    inner_w: float,
    cursor: float,
    sections_left: list[dict],
) -> float:
    """Draws user-defined sections on the left column."""
    for sec in (sections_left or []):
        title = (sec.get("title") or "").strip()
        lines = [str(x).strip() for x in (sec.get("lines") or []) if str(x).strip()]
        if not title or not lines:
            continue

        cursor -= LEFT_SEC_TITLE_TOP_GAP
        # Heading + icon + underline
        cursor = draw_heading_with_icon(
            c=c,
            x=inner_x,
            y=cursor,
            title=title,
            icon=None,  # custom sections: no icon by default
            font="Helvetica-Bold",
            size=LEFT_SEC_HEADING_SIZE,
            color=HEADING_COLOR,
            underline_w=inner_w,
            rule_color=LEFT_SEC_RULE_COLOR,
            rule_width=LEFT_SEC_RULE_WIDTH,
            gap_below=LEFT_SEC_TITLE_BOTTOM_GAP / 2,
        )
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP

        c.setFont("Helvetica", LEFT_SEC_TEXT_SIZE)
        c.setFillColor(colors.black)
        for ln in lines:
            c.circle(inner_x + LEFT_SEC_BULLET_X_OFFSET, cursor + 3, LEFT_SEC_BULLET_RADIUS, stroke=1, fill=1)
            c.drawString(inner_x + LEFT_SEC_TEXT_X_OFFSET, cursor, ln)
            cursor -= LEFT_SEC_LINE_GAP
        cursor -= LEFT_SEC_SECTION_GAP
    return cursor


def draw_left_column(
    c: canvas.Canvas,
    *,
    name: str,
    location: str,
    phone: str,
    email: str,
    github: str,
    linkedin: str,
    birthdate: str,
    skills: list[str],
    languages: list[str],
    inner_x: float,
    inner_w: float,
    cursor: float,
) -> float:
    """Draws the full left column including contact, skills, and language sections."""
    # -------- Name --------
    if name:
        c.setFont("Helvetica-Bold", NAME_SIZE)
        c.setFillColor(HEADING_COLOR)
        c.drawCentredString(inner_x + inner_w / 2, cursor, name)
        cursor -= NAME_GAP

    # -------- Contact --------
    has_contact = any([location, phone, email, birthdate, github, linkedin])
    if has_contact:
        cursor -= LEFT_SEC_TITLE_TOP_GAP
        # Heading + icon (pin) optional — نستخدم العنوان الديناميكي
        cursor = draw_heading_with_icon(
            c=c,
            x=inner_x,
            y=cursor,
            title=t("personal_info", UI_LANG),
            icon=None,  # يمكنك لاحقًا وضع أيقونة مخصّصة لعنوان "Personal Information"
            font="Helvetica-Bold",
            size=LEFT_SEC_HEADING_SIZE,
            color=HEADING_COLOR,
            underline_w=inner_w,
            rule_color=LEFT_SEC_RULE_COLOR,
            rule_width=LEFT_SEC_RULE_WIDTH,
            gap_below=LEFT_SEC_TITLE_BOTTOM_GAP / 2,
        )
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP

        if location:
            cursor = info_line(c, inner_x, cursor, "Ort", location, inner_w)
        if phone:
            cursor = info_line(c, inner_x, cursor, "Telefon", phone, inner_w)
        if email:
            cursor = info_line(c, inner_x, cursor, "E-Mail", email, inner_w)
        if birthdate:
            cursor = info_line(c, inner_x, cursor, "Geburtsdatum", birthdate, inner_w)
        if github:
            cursor = info_line(c, inner_x, cursor, "GitHub", github, inner_w)
        if linkedin:
            cursor = info_line(c, inner_x, cursor, "LinkedIn", linkedin, inner_w)

        cursor -= LEFT_AFTER_CONTACT_GAP

    # -------- Key Skills --------
    if skills:
        cursor -= LEFT_SEC_TITLE_TOP_GAP
        cursor = draw_heading_with_icon(
            c=c,
            x=inner_x,
            y=cursor,
            title=t("key_skills", UI_LANG),
            icon=get_section_icon("key_skills"),
            font="Helvetica-Bold",
            size=LEFT_SEC_HEADING_SIZE,
            color=HEADING_COLOR,
            underline_w=inner_w,
            rule_color=LEFT_SEC_RULE_COLOR,
            rule_width=LEFT_SEC_RULE_WIDTH,
            gap_below=LEFT_SEC_TITLE_BOTTOM_GAP / 2,
        )
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP

        c.setFont("Helvetica", LEFT_SEC_TEXT_SIZE)
        c.setFillColor(colors.black)
        max_text_w = inner_w - (LEFT_SEC_TEXT_X_OFFSET + 2)
        for sk in skills:
            wrapped = wrap_text(sk, "Helvetica", LEFT_SEC_TEXT_SIZE, max_text_w)
            for i, ln in enumerate(wrapped):
                if i == 0:
                    c.circle(inner_x + LEFT_SEC_BULLET_X_OFFSET, cursor + 3, LEFT_SEC_BULLET_RADIUS, stroke=1, fill=1)
                c.drawString(inner_x + LEFT_SEC_TEXT_X_OFFSET, cursor, ln)
                cursor -= LEFT_SEC_LINE_GAP
        cursor -= LEFT_SEC_SECTION_GAP

    # -------- Languages --------
    if languages:
        cursor -= LEFT_SEC_TITLE_TOP_GAP
        cursor = draw_heading_with_icon(
            c=c,
            x=inner_x,
            y=cursor,
            title=t("languages", UI_LANG),
            icon=get_section_icon("languages"),
            font="Helvetica-Bold",
            size=LEFT_SEC_HEADING_SIZE,
            color=HEADING_COLOR,
            underline_w=inner_w,
            rule_color=LEFT_SEC_RULE_COLOR,
            rule_width=LEFT_SEC_RULE_WIDTH,
            gap_below=LEFT_SEC_TITLE_BOTTOM_GAP / 2,
        )
        cursor -= LEFT_SEC_RULE_TO_LIST_GAP

        # النص بالأسود
        c.setFillColor(colors.black)
        c.setFont("Helvetica", LEFT_SEC_TEXT_SIZE)

        # اطبع كل لغة كسطر مستقل مع لفّ أسطر
        max_text_w = inner_w - (LEFT_SEC_TEXT_X_OFFSET + 2)
        for lang in languages:
            wrapped = wrap_text(str(lang), "Helvetica", LEFT_SEC_TEXT_SIZE, max_text_w)
            for i, ln in enumerate(wrapped):
                if i == 0:
                    # نقطة (bullet) صغيرة مثل قسم المهارات
                    c.circle(inner_x + LEFT_SEC_BULLET_X_OFFSET, cursor + 3, LEFT_SEC_BULLET_RADIUS, stroke=1, fill=1)
                c.drawString(inner_x + LEFT_SEC_TEXT_X_OFFSET, cursor, ln)
                cursor -= LEFT_SEC_LINE_GAP

        cursor -= LEFT_SEC_SECTION_GAP




    return cursor
