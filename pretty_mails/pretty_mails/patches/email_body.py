
import frappe
from frappe.email.doctype.email_account.email_account import EmailAccount
from frappe.utils import (
	get_url,
	scrub_urls,
)

from frappe.email.email_body import get_header, get_footer, get_brand_logo, inline_style_in_html
from frappe.email import email_body

def pretty_mails_get_formatted_html(
	subject,
	message,
	footer=None,
	print_html=None,
	email_account=None,
	header=None,
	unsubscribe_link: frappe._dict | None = None,
	sender=None,
	with_container=False,
	raw_html=False,
	add_css=True,
):
	"""Replacement for frappe.email.email_body.get_formatted_html (Frappe v16 signature)."""
	email_account = email_account or EmailAccount.find_outgoing(match_by_email=sender)

	params = {
		"site_url": get_url(),
		"title": subject,
		"print_html": print_html,
		"subject": subject,
	}

	if raw_html:
		rendered_email = frappe.render_template(message, params)
	else:
		params.update(
			{
				"brand_logo": get_brand_logo(email_account) if with_container or header else None,
				"with_container": with_container,
				"header": get_header(header),
				"content": message,
				"footer": get_footer(email_account, footer),
			}
		)
		rendered_email = frappe.get_template("pretty_mails/templates/emails/standard.html").render(params)

	html = scrub_urls(rendered_email)

	if unsubscribe_link:
		html = html.replace("<!--unsubscribe link here-->", unsubscribe_link.html)

	return inline_style_in_html(html) if add_css else html

email_body.get_formatted_html = pretty_mails_get_formatted_html