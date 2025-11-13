from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AskScheduler(models.AbstractModel):
    _name = 'ask.scheduler'
    _description = 'Ask Scheduler Methods'

    def _process_daily_ask_cutoff(self):
        """
        This method is called by a cron job.
        It copies ask_qty to valid_ask_qty for submitted asks and locks them.
        """
        _logger.info("Starting daily ask cutoff process...")
        submitted_asks = self.env['ask.ask'].search([('state', '=', 'submitted')])
        if not submitted_asks:
            _logger.info("No submitted asks to process.")
            return

        for ask in submitted_asks:
            for line in ask.line_ids:
                if line.ask_qty > 0:
                    log_message = (
                        "Copied ask_qty ({ask_qty}) to valid_ask_qty. "
                        "Triggered by cron at {timestamp}. "
                        "User: {user}.\n"
                    ).format(
                        ask_qty=line.ask_qty,
                        timestamp=fields.Datetime.now(),
                        user=self.env.user.name,
                    )
                    new_log = (line.cutoff_log or '') + log_message
                    line.write({
                        'valid_ask_qty': line.ask_qty,
                        'cutoff_log': new_log
                    })
            ask.write({'state': 'locked'})
            _logger.info(f"Processed and locked Ask Order: {ask.name}")

        _logger.info("Finished daily ask cutoff process.")