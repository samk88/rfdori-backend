from sqlalchemy import text
from sqlalchemy.orm import Session

def _one(db: Session, sql: str):
    row = db.execute(text(sql)).mappings().first()
    return dict(row) if row else {}

def _all(db: Session, sql: str):
    return [dict(r) for r in db.execute(text(sql)).mappings().all()]

def get_stage1_overview(db: Session):
    return _one(db, '''
        SELECT
            'S1' AS stage_code,
            COUNT(*) AS total_institutions,
            COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM rfdori.outreach o WHERE o.institution_id = i.institution_id)) AS contacted_count,
            COUNT(*) FILTER (WHERE EXISTS (
                SELECT 1 FROM rfdori.outreach o
                JOIN rfdori.responses r ON r.outreach_id = o.outreach_id
                WHERE o.institution_id = i.institution_id
            )) AS responded_count,
            COUNT(*) FILTER (WHERE i.is_bank_layer = TRUE) AS bank_layer_count,
            COUNT(*) FILTER (WHERE i.is_priority_target = TRUE) AS high_priority_count,
            COUNT(*) FILTER (WHERE ist.status_code = 'ENGAGED') AS engaged_count,
            COUNT(*) FILTER (WHERE ist.status_code = 'DORMANT') AS dormant_count
        FROM rfdori.institutions i
        JOIN rfdori.stages s ON s.stage_id = i.current_stage_id
        JOIN rfdori.institution_statuses ist ON ist.institution_status_id = i.institution_status_id
        WHERE s.stage_code = 'S1'
    ''')

def get_wave_distribution(db: Session):
    return _all(db, '''
        SELECT
            w.wave_code,
            COUNT(*) AS institution_count,
            COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM rfdori.outreach o WHERE o.institution_id = i.institution_id)) AS contacted_count,
            COUNT(*) FILTER (WHERE EXISTS (
                SELECT 1 FROM rfdori.outreach o
                JOIN rfdori.responses r ON r.outreach_id = o.outreach_id
                WHERE o.institution_id = i.institution_id
            )) AS responded_count
        FROM rfdori.institutions i
        JOIN rfdori.waves w ON w.wave_id = i.primary_wave_id
        JOIN rfdori.stages s ON s.stage_id = i.current_stage_id
        WHERE s.stage_code = 'S1'
        GROUP BY w.wave_code, w.wave_sequence
        ORDER BY w.wave_sequence
    ''')

def get_country_distribution(db: Session):
    return _all(db, '''
        SELECT
            c.country_code,
            c.country_name,
            COUNT(*) AS institution_count,
            COUNT(*) FILTER (WHERE i.is_bank_layer = TRUE) AS bank_layer_count,
            COUNT(*) FILTER (WHERE EXISTS (SELECT 1 FROM rfdori.outreach o WHERE o.institution_id = i.institution_id)) AS contacted_count,
            COUNT(*) FILTER (WHERE EXISTS (
                SELECT 1 FROM rfdori.outreach o
                JOIN rfdori.responses r ON r.outreach_id = o.outreach_id
                WHERE o.institution_id = i.institution_id
            )) AS responded_count
        FROM rfdori.institutions i
        JOIN rfdori.countries c ON c.country_id = i.country_id
        JOIN rfdori.stages s ON s.stage_id = i.current_stage_id
        WHERE s.stage_code = 'S1'
        GROUP BY c.country_code, c.country_name
        ORDER BY c.country_name
    ''')

def get_institution_type_summary(db: Session):
    return _all(db, '''
        SELECT
            it.type_code AS institution_type_code,
            it.type_name AS institution_type_name,
            COUNT(*) AS institution_count,
            COALESCE(ROUND(AVG(sc.weighted_total)::numeric, 2), 0) AS avg_score
        FROM rfdori.institutions i
        JOIN rfdori.institution_types it ON it.institution_type_id = i.institution_type_id
        JOIN rfdori.stages s ON s.stage_id = i.current_stage_id
        LEFT JOIN rfdori.institution_scores sc ON sc.institution_id = i.institution_id AND sc.is_current = TRUE
        WHERE s.stage_code = 'S1'
        GROUP BY it.type_code, it.type_name
        ORDER BY it.type_name
    ''')

def get_follow_up_queue(db: Session):
    return _all(db, '''
        SELECT
            o.outreach_id,
            i.institution_code,
            i.institution_name,
            c.full_name AS contact_name,
            o.subject_line,
            COALESCE(o.follow_up_due_at, o.sent_at) AS follow_up_due_at,
            os.status_code AS outreach_status_code
        FROM rfdori.outreach o
        JOIN rfdori.institutions i ON i.institution_id = o.institution_id
        LEFT JOIN rfdori.contacts c ON c.contact_id = o.contact_id
        JOIN rfdori.outreach_statuses os ON os.outreach_status_id = o.outreach_status_id
        ORDER BY COALESCE(o.follow_up_due_at, o.sent_at) NULLS LAST, o.outreach_id DESC
        LIMIT 20
    ''')

def get_score_leaderboard(db: Session):
    return _all(db, '''
        SELECT
            i.institution_id,
            i.institution_code,
            i.institution_name,
            COALESCE(sc.weighted_total, 0) AS weighted_total,
            COALESCE(sc.score_band, 'UNSCORED') AS score_band
        FROM rfdori.institutions i
        LEFT JOIN rfdori.institution_scores sc ON sc.institution_id = i.institution_id AND sc.is_current = TRUE
        JOIN rfdori.stages s ON s.stage_id = i.current_stage_id
        WHERE s.stage_code = 'S1'
        ORDER BY COALESCE(sc.weighted_total, 0) DESC, i.institution_name
        LIMIT 10
    ''')
