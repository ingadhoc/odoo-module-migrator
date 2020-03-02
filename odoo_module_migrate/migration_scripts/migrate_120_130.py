# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import re

_TEXT_ERRORS = {
    "*": {
        "web_settings_dashboard":
        "[V13] Reference to 'web_settings_dashboard'"
        ". This module has been removed."
    },
    ".py": {
        r".*@api.returns.*\n":
        "[13] Use of deprecated decorator '@api.returns'",
        r".*@api.cr.*\n":
        "[13] Use of deprecated decorator '@api.cr'",
        r".*@api.model_cr.*\n":
        "[13] Use of deprecated decorator '@api.model_cr'",
    },
}

_TEXT_REPLACES = {
    ".py": {
        r".*@api.multi.*\n": "",
        r".*@api.one.*\n": "",
        r"\.sudo\((?P<user>[^/)]+?)\)": r".with_user(\g<user>)",
        r"\.suspend_security": ".sudo",
        r"\"base_suspend_security\",\n": "",
    },
    ".xml": {
        r"( |\t)*<field name=('|\")view_type('|\")>.*</field>\n": "",
    }
}


def find_compute_with_context(**kwargs):
    """ Return the name of the compute methods that depends on context """
    logger = kwargs['logger']
    res = []
    regex = r"(def compute|def _compute)(.*?)(def |@api\.)"
    matches = re.finditer(regex, kwargs['content'], re.MULTILINE | re.DOTALL)
    for matchNum, match in enumerate(matches, start=1):
        if 'context.get' in match.group(2) or 'with_context' in match.group(2):
            res.append((match.group(1) + match.group(2)).split('(')[0].replace('def ', ''))
    for item in res:
        logger.warning("[13] %s: add @api.depends_context() in compute method", item)


_VERSION_FUNCTIONS = [
    find_compute_with_context]
