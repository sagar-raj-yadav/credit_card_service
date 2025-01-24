from django_cron import CronJobBase, Schedule
from loan.tasks import generate_billing

class BillingCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'loan.billing_cron_job'

    def do(self):
        try:
            generate_billing()
        except Exception as e:
            print(f"Error in BillingCronJob: {e}")
