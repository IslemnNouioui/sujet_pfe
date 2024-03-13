from odoo import api, fields, models


class ResPartner(models.Model):
    """Add some fields related to commissions"""

    _inherit = "res.partner"
    total_invoiced = fields.Monetary(string='Total Invoiced', compute='_compute_total_invoiced')
    currency_id = fields.Many2one('res.currency', string='Currency')
    agent_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="partner_agent_rel",
        column1="partner_id",
        column2="agent_id",
        domain=[("agent", "=", True)],
        readonly=False,
        string="Agents",
    )

    # Fields for the partner when it acts as an agent or creditor
    agent = fields.Boolean(
        string="Creditor/Agent",
        help="Check this field if the partner is a creditor or an agent.",
    )
    agent_type = fields.Selection(
        selection=[("agent", "External agent")],
        string="Type",
        default="agent",
    )
    commission_id = fields.Many2one(
        string="Commission",
        comodel_name="commission",
        help="This is the default commission used in the sales where this "
             "agent is assigned. It can be changed on each operation if "
             "needed.",
    )  # Champ Many2one qui lie le partenaire à une commission par défaut utilisée dans les ventes où cet agent est assigné
    settlement = fields.Selection(
        selection=[
            ("biweekly", "Bi-weekly"),
            ("monthly", "Monthly"),
            ("quaterly", "Quarterly"),
            ("semi", "Semi-annual"),
            ("annual", "Annual"),
        ],
        # Champ de sélection qui spécifie la période de règlement pour les commissions de cet agent, avec des options telles que bihebdomadaire, mensuelle, trimestrielle, semestrielle et annuelle
        string="Settlement period",
        default="monthly",
    )
    settlement_ids = fields.One2many(
        comodel_name="commission.settlement",
        inverse_name="agent_id",
        readonly=True,
    )  # Champ One2many lié aux règlements de commissions associés à ce partenaire

    @api.model
    def _commercial_fields(self):
        """Add agents to commercial fields that are synced from parent to childs."""
        res = super()._commercial_fields()
        res.append("agent_ids")
        return res
