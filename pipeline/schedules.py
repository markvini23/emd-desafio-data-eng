from datetime import timedelta, datetime
from prefect.schedules import IntervalSchedule
import pytz


#Set Schedule interval to run every minute starting on execute at SP timezone
minute_brt_data = IntervalSchedule(
    start_date=datetime.now(pytz.timezone('America/Sao_Paulo')) + timedelta(seconds=1),
    end_date=datetime.now(pytz.timezone("America/Sao_Paulo")) + timedelta(minutes=11),
    interval=timedelta(minutes=1)
)
