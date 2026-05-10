from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .excel_practice import (
    lesson_index as excel_index, lesson_payload as excel_payload, check_answer as excel_check,
)
from .powerbi_practice import (
    lesson_index as pbi_index, lesson_payload as pbi_payload, check_answer as pbi_check,
)
from .tableau_practice import (
    lesson_index as tab_index, lesson_payload as tab_payload, check_answer as tab_check,
)
from .aptitude_practice import (
    lesson_index as apt_index, lesson_payload as apt_payload, check_answer as apt_check,
)
from .case_study_practice import (
    lesson_index as case_index, lesson_payload as case_payload, check_answer as case_check,
)
from .leadership_practice import (
    lesson_index as lp_index, lesson_payload as lp_payload, check_answer as lp_check,
)
from .data_interp_practice import (
    lesson_index as di_index, lesson_payload as di_payload, check_answer as di_check,
)

BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = BASE_DIR / "web"

app = FastAPI(title="BA Prep")

MODULES = {
    "excel": (excel_index, excel_payload, excel_check),
    "powerbi": (pbi_index, pbi_payload, pbi_check),
    "tableau": (tab_index, tab_payload, tab_check),
    "aptitude": (apt_index, apt_payload, apt_check),
    "case-study": (case_index, case_payload, case_check),
    "leadership": (lp_index, lp_payload, lp_check),
    "data-interp": (di_index, di_payload, di_check),
}


class CheckRequest(BaseModel):
    lessonId: str
    taskId: str
    answer: int | str | None = None


@app.get("/api/health")
async def health() -> dict:
    return {"ok": True}


@app.get("/api/modules")
async def list_modules() -> dict:
    return {
        "modules": [
            {"id": "excel", "title": "Excel Mastery", "icon": "📊", "color": "#217346",
             "desc": "VLOOKUP, INDEX MATCH, pivot tables, dashboards, data cleaning — the full Excel toolkit."},
            {"id": "powerbi", "title": "Power BI", "icon": "⚡", "color": "#F2C811",
             "desc": "DAX measures, data modeling, time intelligence, visualizations, and Power Query."},
            {"id": "tableau", "title": "Tableau", "icon": "📈", "color": "#E97627",
             "desc": "Calculated fields, LOD expressions, dashboard design, and table calculations."},
            {"id": "aptitude", "title": "Business Aptitude", "icon": "🧠", "color": "#6366F1",
             "desc": "Logical reasoning, quantitative aptitude, data sufficiency — real interview-level problems."},
            {"id": "case-study", "title": "Case Studies", "icon": "🔍", "color": "#EC4899",
             "desc": "Metric drops, root cause analysis, KPI definition, funnel analysis, A/B testing."},
            {"id": "leadership", "title": "Leadership Principles", "icon": "🎯", "color": "#FF9900",
             "desc": "Amazon LP-style scenarios — most/least likely format, STAR situations, behavioral alignment."},
            {"id": "data-interp", "title": "Data Interpretation", "icon": "📉", "color": "#14B8A6",
             "desc": "Tables, charts, dashboards — read data, calculate, and infer trends under time pressure."},
        ]
    }


@app.get("/api/{module}/lessons")
async def get_lessons(module: str) -> JSONResponse:
    if module not in MODULES:
        return JSONResponse({"ok": False, "error": "Unknown module."}, status_code=404)
    index_fn = MODULES[module][0]
    return JSONResponse({"lessons": index_fn()})


@app.get("/api/{module}/lessons/{lesson_id}")
async def get_lesson(module: str, lesson_id: str) -> JSONResponse:
    if module not in MODULES:
        return JSONResponse({"ok": False, "error": "Unknown module."}, status_code=404)
    payload_fn = MODULES[module][1]
    return JSONResponse({"lesson": payload_fn(lesson_id)})


@app.post("/api/{module}/check")
async def check(module: str, request: CheckRequest) -> JSONResponse:
    if module not in MODULES:
        return JSONResponse({"ok": False, "error": "Unknown module."}, status_code=404)
    check_fn = MODULES[module][2]
    try:
        result = check_fn(request.lessonId, request.taskId, request.answer)
    except Exception as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=400)
    return JSONResponse({"ok": True, **result})


# ---------- HTML page routes ----------

@app.get("/")
async def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


for _mod in MODULES:
    _slug = _mod

    def _make_page(slug: str):
        async def page() -> FileResponse:
            return FileResponse(WEB_DIR / "index.html")
        page.__name__ = f"page_{slug}"
        return page

    def _make_lesson_page(slug: str):
        async def page(lesson_id: str) -> FileResponse:
            return FileResponse(WEB_DIR / "index.html")
        page.__name__ = f"lesson_{slug}"
        return page

    app.get(f"/{_slug}")(_make_page(_slug))
    app.get(f"/{_slug}/{{lesson_id}}")(_make_lesson_page(_slug))


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
