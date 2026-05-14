from apscheduler.schedulers.background import BackgroundScheduler
from app.core.company_cycle import DevForgeCompany
from app.core.audit import AuditLog
import logging

# Configure basic logging for the scheduler
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DevForgeScheduler")

scheduler = BackgroundScheduler()
company = DevForgeCompany()
audit = AuditLog()

def scheduled_business_cycle():
    """
    Triggers the full DevForge AI business cycle.
    Automatically called every day at 1 PM.
    """
    logger.info("Starting scheduled DevForge Business Cycle...")
    audit.log_action("scheduler", "triggered_cycle", {"time": "13:00"})
    
    try:
        result = company.execute_business_cycle()
        logger.info(f"Scheduled cycle completed. Result summary: {len(result.get('results', []))} products launched.")
    except Exception as e:
        logger.error(f"Scheduled cycle failed: {str(e)}")

def start_scheduler():
    """
    Initializes and starts the background scheduler.
    """
    # Schedule the job for 1 PM (13:00) every day
    scheduler.add_job(
        scheduled_business_cycle,
        'cron',
        hour=13,
        minute=0,
        id='daily_devforge_cycle'
    )
    
    if not scheduler.running:
        scheduler.start()
        logger.info("DevForge Scheduler started. Daily cycle set to 13:00.")

def stop_scheduler():
    """
    Stops the background scheduler.
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("DevForge Scheduler stopped.")
