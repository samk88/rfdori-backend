"""seed demo stage1 data

Revision ID: 0003_seed_demo_stage1_data
Revises: 0002_seed_reference_data
Create Date: 2026-03-17 19:20:00
"""
from alembic import op
import sqlalchemy as sa

revision = "0003_seed_demo_stage1_data"
down_revision = "0002_seed_reference_data"
branch_labels = None
depends_on = None

def upgrade() -> None:
    conn = op.get_bind()

    conn.execute(sa.text("""
        INSERT INTO rfdori.users (user_role_id, full_name, email, is_active, created_at, updated_at)
        SELECT ur.user_role_id, 'System Seed User', 'system.seed@buffaloquarter.local', TRUE, now(), now()
        FROM rfdori.user_roles ur
        WHERE ur.role_code = 'SYS_ADMIN'
        ON CONFLICT (email) DO NOTHING
    """))

    conn.execute(sa.text("""
        INSERT INTO rfdori.institutions (
            institution_code, institution_name, short_name, country_id, institution_type_id, primary_wave_id,
            current_stage_id, institution_status_id, stage_layer, stakeholder_class, relevance_rationale,
            continuity_role_summary, is_bank_layer, is_anchor_target, is_priority_target, is_active,
            website_url, headquarters_city, created_at, updated_at
        )
        SELECT
            x.institution_code, x.institution_name, x.short_name, c.country_id, it.institution_type_id, w.wave_id,
            s.stage_id, ist.institution_status_id, x.stage_layer, x.stakeholder_class, x.relevance_rationale,
            x.continuity_role_summary, x.is_bank_layer, x.is_anchor_target, x.is_priority_target, TRUE,
            x.website_url, x.headquarters_city, now(), now()
        FROM (
            VALUES
            ('KEN-CBK','Central Bank of Kenya','CBK','KEN','CENTRAL_BANK','W1','S1','TARGET','Regulatory / Monetary','Public Financial Authority','National monetary and payment-system oversight relevance to continuity recognition.','Core policy and financial-system continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.centralbank.go.ke','Nairobi'),
            ('TZA-BOT','Bank of Tanzania','BoT','TZA','CENTRAL_BANK','W1','S1','TARGET','Regulatory / Monetary','Public Financial Authority','National monetary and payment-system oversight relevance to continuity recognition.','Core policy and financial-system continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.bot.go.tz','Dodoma'),
            ('KEN-SAFARICOM','Safaricom PLC','Safaricom','KEN','TELCO','W1','S1','ENGAGED','Connectivity Infrastructure','Private Critical Infrastructure','Mobile financial services and telecommunications continuity relevance.','Critical network and digital-services continuity actor.',FALSE,TRUE,TRUE,'https://www.safaricom.co.ke','Nairobi'),
            ('REG-SEACOM','SEACOM','SEACOM','KEN','TELCO','W1','S1','TARGET','Regional Connectivity','Private Critical Infrastructure','Regional connectivity backbone relevance for digital and financial continuity.','Cross-border connectivity continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.seacom.com','Nairobi'),
            ('REG-MASTERCARD','Mastercard','Mastercard','KEN','CARD_NETWORK','W1','S1','TARGET','Payments Infrastructure','Private Payments Network','Scheme and payment-network relevance for transaction continuity.','Card-network and ecosystem continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.mastercard.com','Nairobi'),
            ('KEN-INTERSWITCH','Interswitch Kenya Limited','Interswitch Kenya','KEN','PAYMENT_OPERATOR','W1','S1','ENGAGED','Payments Infrastructure','Private Market Infrastructure','Regional payments processing and switching relevance.','Payments-switch and processing continuity actor.',FALSE,TRUE,TRUE,'https://www.interswitchgroup.com','Nairobi'),
            ('UGA-BOU','Bank of Uganda','BoU','UGA','CENTRAL_BANK','W2','S1','TARGET','Regulatory / Monetary','Public Financial Authority','Completes Stage-1 monetary authority coverage across the four-country corridor.','National monetary, settlement and payment-system continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.bou.or.ug','Kampala'),
            ('RWA-NBR','National Bank of Rwanda','NBR','RWA','CENTRAL_BANK','W2','S1','TARGET','Regulatory / Monetary','Public Financial Authority','Completes Stage-1 monetary authority coverage across the four-country corridor.','National monetary, settlement and payment-system continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.bnr.rw','Kigali'),
            ('TZA-EAC','East African Community Secretariat','EAC Secretariat','TZA','OTHER_STRATEGIC','W2','S1','TARGET','Regional Governance','Regional Institutional Actor','Regional governance relevance to cross-border continuity and settlement coordination.','Regional policy and coordination stakeholder.',FALSE,TRUE,TRUE,'https://www.eac.int','Arusha'),
            ('KEN-IPSL','Integrated Payment Services Limited','IPSL / PesaLink','KEN','PAYMENT_OPERATOR','W2','S1','TARGET','National Payment Rails','Private Market Infrastructure','Instant account-to-account rail relevance to domestic financial continuity.','Kenya payment switching and interoperability stakeholder.',FALSE,TRUE,TRUE,'https://pesalink.co.ke','Nairobi'),
            ('TZA-UMOJA','UmojaSwitch Company Limited','UmojaSwitch','TZA','PAYMENT_OPERATOR','W2','S1','TARGET','National Payment Rails','Private Market Infrastructure','Shared banking switch relevance to Tanzania transaction continuity and fallback capability.','Tanzania shared banking and payments infrastructure stakeholder.',FALSE,TRUE,TRUE,'https://www.umojaswitch.co.tz','Dar es Salaam'),
            ('RWA-RSWITCH','Rwanda National Digital Payments Switch','RSwitch','RWA','PAYMENT_OPERATOR','W2','S1','TARGET','National Payment Rails','National Payments Infrastructure','National switch relevance to Rwanda interoperability and transaction continuity.','Rwanda digital-payments switch and interoperability stakeholder.',FALSE,TRUE,TRUE,NULL,'Kigali'),
            ('KEN-CAK','Communications Authority of Kenya','CA Kenya','KEN','OTHER_STRATEGIC','W3','S1','TARGET','Communications Regulation','Public Communications Regulator','National communications regulation relevance to network resilience and continuity governance.','Kenya communications oversight stakeholder.',FALSE,TRUE,TRUE,'https://www.ca.go.ke','Nairobi'),
            ('UGA-UCC','Uganda Communications Commission','UCC','UGA','OTHER_STRATEGIC','W3','S1','TARGET','Communications Regulation','Public Communications Regulator','National communications regulation relevance to network resilience and continuity governance.','Uganda communications oversight stakeholder.',FALSE,TRUE,TRUE,'https://www.ucc.co.ug','Kampala'),
            ('TZA-TCRA','Tanzania Communications Regulatory Authority','TCRA','TZA','OTHER_STRATEGIC','W3','S1','TARGET','Communications Regulation','Public Communications Regulator','National communications regulation relevance to network resilience and continuity governance.','Tanzania communications oversight stakeholder.',FALSE,TRUE,TRUE,'https://www.tcra.go.tz','Dodoma'),
            ('RWA-RURA','Rwanda Utilities Regulatory Authority','RURA','RWA','OTHER_STRATEGIC','W3','S1','TARGET','Utilities / Communications Regulation','Public Utilities Regulator','Utilities and electronic communications oversight relevance to continuity governance.','Rwanda utilities and connectivity oversight stakeholder.',FALSE,TRUE,TRUE,'https://rura.rw','Kigali'),
            ('UGA-MTN','MTN Uganda Limited','MTN Uganda','UGA','TELCO','W3','S1','TARGET','Connectivity Infrastructure','Private Critical Infrastructure','Large-scale mobile network and digital-finance access relevance in Uganda.','Uganda connectivity and mobile-money continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.mtn.co.ug','Kampala'),
            ('TZA-AIRTEL','Airtel Tanzania PLC','Airtel Tanzania','TZA','TELCO','W3','S1','TARGET','Connectivity Infrastructure','Private Critical Infrastructure','Mobile network and digital-finance access relevance in Tanzania.','Tanzania connectivity and mobile-money continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.airtel.co.tz','Dar es Salaam'),
            ('KEN-LIQUID','Liquid Intelligent Technologies Kenya','Liquid Kenya','KEN','TELCO','W4','S1','TARGET','Regional Connectivity','Private Critical Infrastructure','Backbone fibre and enterprise connectivity relevance to continuity architecture.','Regional terrestrial connectivity stakeholder.',FALSE,TRUE,TRUE,'https://liquid.tech','Nairobi'),
            ('KEN-ICOLO','iColo Limited','iColo','KEN','DATA_INFRA','W4','S1','TARGET','Digital Infrastructure','Private Hosting / Data Infrastructure','Carrier-neutral data-centre relevance to hosting, recovery and digital continuity.','Kenya hosting and colocation continuity stakeholder.',FALSE,TRUE,TRUE,'https://icolo.io','Nairobi'),
            ('UGA-AIRTEL','Airtel Uganda Limited','Airtel Uganda','UGA','TELCO','W4','S1','TARGET','Connectivity Infrastructure','Private Critical Infrastructure','Mobile network and digital-finance access relevance in Uganda.','Uganda connectivity and mobile-money continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.airtel.co.ug','Kampala'),
            ('RWA-MTN','MTN Rwandacell Plc','MTN Rwanda','RWA','TELCO','W4','S1','TARGET','Connectivity Infrastructure','Private Critical Infrastructure','Mobile network and digital-finance access relevance in Rwanda.','Rwanda connectivity and mobile-money continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.mtn.co.rw','Kigali'),
            ('TZA-VODACOM','Vodacom Tanzania PLC','Vodacom Tanzania','TZA','TELCO','W4','S1','TARGET','Connectivity Infrastructure','Private Critical Infrastructure','Large-scale mobile network and M-Pesa ecosystem relevance in Tanzania.','Tanzania connectivity and mobile-money continuity stakeholder.',FALSE,TRUE,TRUE,'https://www.vodacom.co.tz','Dar es Salaam'),
            ('KEN-KPLC','Kenya Power and Lighting Company PLC','KPLC','KEN','PUBLIC_INFRA','W4','S1','TARGET','Power Infrastructure','Public Utility Infrastructure','Power continuity relevance to upstream failure prevention and recovery capability.','Power-layer continuity stakeholder affecting financial and digital services.',FALSE,TRUE,TRUE,'https://www.kplc.co.ke','Nairobi'),
            ('BANK-KEN-EQTY','Equity Bank (Kenya) Limited','Equity Bank Kenya','KEN','BANK','W4','S1','TARGET','Commercial Banking Layer','Commercial Bank','Large retail and regional banking footprint relevance for continuity-demand testing.','Commercial bank layer institution for continuity-impact and demand validation.',TRUE,TRUE,TRUE,'https://equitygroupholdings.com/ke/','Nairobi'),
            ('BANK-KEN-KCB','KCB Bank Kenya Limited','KCB Bank Kenya','KEN','BANK','W4','S1','TARGET','Commercial Banking Layer','Commercial Bank','Large retail and regional banking footprint relevance for continuity-demand testing.','Commercial bank layer institution for continuity-impact and demand validation.',TRUE,TRUE,TRUE,'https://ke.kcbgroup.com','Nairobi'),
            ('BANK-UGA-STANBIC','Stanbic Bank Uganda Limited','Stanbic Uganda','UGA','BANK','W4','S1','TARGET','Commercial Banking Layer','Commercial Bank','Uganda commercial banking layer anchor with institutional relevance.','Commercial bank layer institution for continuity-impact and demand validation.',TRUE,TRUE,TRUE,'https://www.stanbicbank.co.ug','Kampala'),
            ('BANK-TZA-CRDB','CRDB Bank Plc','CRDB Bank','TZA','BANK','W4','S1','TARGET','Commercial Banking Layer','Commercial Bank','Tanzania commercial banking layer anchor with strong domestic footprint.','Commercial bank layer institution for continuity-impact and demand validation.',TRUE,TRUE,TRUE,'https://crdbbank.co.tz/en','Dar es Salaam'),
            ('BANK-RWA-BK','Bank of Kigali Plc','Bank of Kigali','RWA','BANK','W4','S1','TARGET','Commercial Banking Layer','Commercial Bank','Rwanda commercial banking layer anchor with strong domestic footprint.','Commercial bank layer institution for continuity-impact and demand validation.',TRUE,TRUE,TRUE,'https://bk.rw','Kigali')
        ) AS x(
            institution_code, institution_name, short_name, country_code, institution_type_code, wave_code, stage_code,
            institution_status_code, stage_layer, stakeholder_class, relevance_rationale, continuity_role_summary,
            is_bank_layer, is_anchor_target, is_priority_target, website_url, headquarters_city
        )
        JOIN rfdori.countries c ON c.country_code = x.country_code
        JOIN rfdori.institution_types it ON it.type_code = x.institution_type_code
        JOIN rfdori.waves w ON w.wave_code = x.wave_code
        JOIN rfdori.stages s ON s.stage_code = x.stage_code
        JOIN rfdori.institution_statuses ist ON ist.status_code = x.institution_status_code
        ON CONFLICT (institution_code) DO NOTHING
    """))

    conn.execute(sa.text("""
        INSERT INTO rfdori.contacts (
            institution_id, full_name, title, department, seniority_level, email, phone,
            is_primary_contact, is_verified, is_active, verification_note, routing_relevance_note, created_at, updated_at
        )
        SELECT
            i.institution_id,
            'Stage-1 Contact - ' || COALESCE(i.short_name, i.institution_code),
            'Director, Strategic Operations',
            'Strategy / Operations',
            'director',
            lower(replace(i.institution_code, '-', '.')) || '@example.org',
            '+000000000',
            TRUE, TRUE, TRUE,
            'Demo seeded contact.',
            'Suitable first routing point for prototype walkthrough.',
            now(), now()
        FROM rfdori.institutions i
        ON CONFLICT DO NOTHING
    """))

    conn.execute(sa.text("""
        INSERT INTO rfdori.outreach (
            institution_id, contact_id, wave_id, stage_id, outreach_type_id, outreach_channel_id, outreach_status_id,
            sender_user_id, subject_line, message_summary, message_body, sent_at, read_confirmed_at, follow_up_due_at,
            stage_context, outreach_sequence_no, is_latest_for_contact, created_at, updated_at
        )
        SELECT
            i.institution_id,
            c.contact_id,
            i.primary_wave_id,
            i.current_stage_id,
            ot.outreach_type_id,
            oc.outreach_channel_id,
            os.outreach_status_id,
            u.user_id,
            'Exploratory institutional engagement on continuity and resilience architecture',
            'Stage-1 exploratory outreach dispatched.',
            'Prototype demo message body.',
            now() - interval '3 day',
            CASE WHEN os.status_code IN ('READ_CONFIRMED','REPLIED') THEN now() - interval '2 day' ELSE NULL END,
            now() + interval '4 day',
            'Stage-1 exploratory outreach',
            1,
            TRUE,
            now(), now()
        FROM rfdori.institutions i
        JOIN rfdori.contacts c ON c.institution_id = i.institution_id AND c.is_primary_contact = TRUE
        JOIN rfdori.outreach_types ot ON ot.type_code = 'EMAIL'
        JOIN rfdori.outreach_channels oc ON oc.channel_code = 'EMAIL_DIRECT'
        JOIN rfdori.outreach_statuses os ON os.status_code = CASE
            WHEN i.institution_code IN ('KEN-CBK','TZA-BOT') THEN 'READ_CONFIRMED'
            WHEN i.institution_code IN ('KEN-SAFARICOM','KEN-INTERSWITCH') THEN 'REPLIED'
            ELSE 'SENT'
        END
        JOIN rfdori.users u ON u.email = 'system.seed@buffaloquarter.local'
        WHERE i.institution_code IN ('KEN-CBK','TZA-BOT','KEN-SAFARICOM','REG-SEACOM','REG-MASTERCARD','KEN-INTERSWITCH')
        ON CONFLICT DO NOTHING
    """))

    conn.execute(sa.text("""
        INSERT INTO rfdori.responses (
            outreach_id, reviewer_user_id, response_type_id, response_sentiment_id, engagement_level_id,
            received_at, response_subject, response_summary, response_body, meeting_interest, referral_given,
            substantive_commentary, requests_more_info, no_response, next_step_signal, analyst_interpretation,
            created_at, updated_at
        )
        SELECT
            o.outreach_id,
            u.user_id,
            rt.response_type_id,
            rs.response_sentiment_id,
            el.engagement_level_id,
            now() - interval '1 day',
            'Re: Exploratory institutional engagement',
            CASE
                WHEN i.institution_code = 'KEN-SAFARICOM' THEN 'Acknowledged with technical interest.'
                ELSE 'Acknowledged and routed internally.'
            END,
            'Prototype demo response body.',
            CASE WHEN i.institution_code = 'KEN-SAFARICOM' THEN TRUE ELSE FALSE END,
            TRUE,
            CASE WHEN i.institution_code = 'KEN-INTERSWITCH' THEN TRUE ELSE FALSE END,
            FALSE,
            FALSE,
            'Await internal routing',
            'Soft-positive routing signal.',
            now(), now()
        FROM rfdori.outreach o
        JOIN rfdori.institutions i ON i.institution_id = o.institution_id
        JOIN rfdori.users u ON u.email = 'system.seed@buffaloquarter.local'
        JOIN rfdori.response_types rt ON rt.type_code = 'ACKNOWLEDGEMENT'
        JOIN rfdori.response_sentiments rs ON rs.sentiment_code = 'POSITIVE'
        JOIN rfdori.engagement_levels el ON el.level_code = 'LOW'
        WHERE i.institution_code IN ('KEN-SAFARICOM','KEN-INTERSWITCH')
        ON CONFLICT DO NOTHING
    """))

    conn.execute(sa.text("""
        INSERT INTO rfdori.institution_scores (
            institution_id, scoring_model_id, strategic_relevance_score, upstream_criticality_score,
            engagement_signal_score, influence_convening_score, demand_formation_score,
            progression_readiness_score, weighted_total, score_band, score_rationale, scored_at, is_current
        )
        SELECT
            i.institution_id,
            sm.scoring_model_id,
            CASE
                WHEN it.type_code = 'CENTRAL_BANK' THEN 92.00
                WHEN it.type_code IN ('TELCO','PAYMENT_OPERATOR','CARD_NETWORK') THEN 86.00
                WHEN it.type_code IN ('DATA_INFRA','PUBLIC_INFRA') THEN 82.00
                WHEN i.is_bank_layer = TRUE THEN 72.00
                ELSE 70.00
            END,
            CASE
                WHEN it.type_code IN ('TELCO','PAYMENT_OPERATOR','CARD_NETWORK','DATA_INFRA','PUBLIC_INFRA') THEN 88.00
                WHEN it.type_code = 'CENTRAL_BANK' THEN 83.00
                WHEN i.is_bank_layer = TRUE THEN 70.00
                ELSE 65.00
            END,
            CASE
                WHEN i.institution_code IN ('KEN-SAFARICOM','KEN-INTERSWITCH') THEN 35.00
                WHEN i.institution_code IN ('KEN-CBK','TZA-BOT') THEN 20.00
                ELSE 10.00
            END,
            CASE
                WHEN it.type_code = 'CENTRAL_BANK' THEN 90.00
                WHEN it.type_code IN ('OTHER_STRATEGIC','PUBLIC_INFRA') THEN 80.00
                WHEN it.type_code IN ('TELCO','PAYMENT_OPERATOR','CARD_NETWORK') THEN 76.00
                WHEN i.is_bank_layer = TRUE THEN 66.00
                ELSE 68.00
            END,
            CASE
                WHEN i.is_bank_layer = TRUE THEN 80.00
                WHEN it.type_code IN ('TELCO','PAYMENT_OPERATOR','CARD_NETWORK') THEN 76.00
                WHEN it.type_code = 'CENTRAL_BANK' THEN 70.00
                ELSE 62.00
            END,
            CASE
                WHEN i.institution_code IN ('KEN-SAFARICOM','KEN-INTERSWITCH') THEN 45.00
                ELSE 15.00
            END,
            CASE
                WHEN it.type_code = 'CENTRAL_BANK' THEN 68.40
                WHEN i.institution_code IN ('KEN-SAFARICOM','KEN-INTERSWITCH') THEN 73.70
                WHEN it.type_code IN ('TELCO','PAYMENT_OPERATOR','CARD_NETWORK') THEN 67.70
                WHEN it.type_code IN ('DATA_INFRA','PUBLIC_INFRA') THEN 63.50
                WHEN i.is_bank_layer = TRUE THEN 58.70
                ELSE 55.40
            END,
            CASE
                WHEN i.institution_code IN ('KEN-SAFARICOM','KEN-INTERSWITCH') THEN 'HIGH_POTENTIAL'
                WHEN it.type_code = 'CENTRAL_BANK' THEN 'HIGH_POTENTIAL'
                ELSE 'MONITOR'
            END,
            'Demo seeded score for local prototype walkthrough.',
            now(),
            TRUE
        FROM rfdori.institutions i
        JOIN rfdori.institution_types it ON it.institution_type_id = i.institution_type_id
        JOIN rfdori.scoring_models sm ON sm.model_code = 'S1_DEFAULT'
        ON CONFLICT DO NOTHING
    """))

def downgrade() -> None:
    conn = op.get_bind()
    conn.execute(sa.text("DELETE FROM rfdori.institution_scores"))
    conn.execute(sa.text("DELETE FROM rfdori.responses"))
    conn.execute(sa.text("DELETE FROM rfdori.outreach"))
    conn.execute(sa.text("DELETE FROM rfdori.contacts"))
    conn.execute(sa.text("DELETE FROM rfdori.institutions"))
    conn.execute(sa.text("DELETE FROM rfdori.users WHERE email = 'system.seed@buffaloquarter.local'"))
