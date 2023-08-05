# Copyright (C) 2018 - TODAY, Open Source Integrators
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Field Service - Skills",
    "summary": "Manage your FS workers skills",
    "version": "11.0.0.2.0",
    "category": "Field Service",
    "license": "AGPL-3",
    "author": "Open Source Integrators, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/field-service",
    "depends": [
        "hr_skill",
        "fieldservice",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/fsm_person.xml",
        "views/fsm_category.xml",
        "views/fsm_person_skill.xml",
        "views/fsm_order.xml",
        "views/hr_skill.xml",
        "views/fsm_template.xml"
    ],
    "development_status": "Beta",
    "maintainers": [
        "osi-scampbell",
        "max3903",
    ],
}
