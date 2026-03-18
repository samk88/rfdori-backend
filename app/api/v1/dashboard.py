from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import get_current_user
from app.services import dashboard as dashboard_service

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stage1-overview")
def get_stage1_overview(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return {"success": True, "message": "Stage-1 overview retrieved successfully.", "data": dashboard_service.get_stage1_overview(db)}

@router.get("/waves")
def get_wave_distribution(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return {"success": True, "message": "Wave distribution retrieved successfully.", "data": dashboard_service.get_wave_distribution(db)}

@router.get("/countries")
def get_country_distribution(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return {"success": True, "message": "Country distribution retrieved successfully.", "data": dashboard_service.get_country_distribution(db)}

@router.get("/institution-types")
def get_institution_type_summary(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return {"success": True, "message": "Institution type summary retrieved successfully.", "data": dashboard_service.get_institution_type_summary(db)}

@router.get("/follow-up-queue")
def get_follow_up_queue(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return {"success": True, "message": "Follow-up queue retrieved successfully.", "data": dashboard_service.get_follow_up_queue(db)}

@router.get("/score-leaderboard")
def get_score_leaderboard(db: Session = Depends(get_db), _: dict = Depends(get_current_user)):
    return {"success": True, "message": "Score leaderboard retrieved successfully.", "data": dashboard_service.get_score_leaderboard(db)}
