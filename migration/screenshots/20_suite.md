# 20_suite screenshot work list

Handed after Fx.2 (2026-10-05). Capture on the **enterprise** review database
http://127.0.0.1:18236/web/login (`admin`/`admin`, `demo`/`demo`, `en_US`,
kept until 2026-10-08 18:39). The community twin is
http://127.0.0.1:18235/web/login. One PDF per module is in Downloads
(`20_suite-<module>-screenshots.pdf`): 19.0 `module.pic` file name, title and alt,
then the PNG from that module's `static/description`. 73 rows. `icon.png`,
`main.png`, `main_nopromo.png` and the app icons are omitted.

Demo to reuse: two From addresses (Sales, Support) on the Mailpit server,
one Email From rule, two lost messages, one edited message with history,
and four drafts. Send privately, CC/BCC, route, quote, extra details and
the composer From pickers are on. Editing uses the full composer.
Admin opens Lost Messages. The standard demo user has drafts.

Recapture every row below on 20.0. Icons are Material Symbols.

| Module | File | What the 19.0 shot shows | Why recapture |
|---|---|---|---|
| mail_manual_routing | button_wizard.png | Open the Route Manual action for a lost email | 20.0 chrome |
| mail_manual_routing | lost_message_routing_wizard.png | Choose the target Odoo record for routing | 20.0 chrome |
| mail_manual_routing | final_thread.png | Recovered email attached to the correct thread | 20.0 chrome |
| mail_manual_routing | unattached_messages.png | Lost messages list and batch routing action | 20.0 chrome |
| mail_manual_routing | notify_conf.png | Configure users to notify about lost messages | 20.0 chrome |
| mail_manual_routing | mail_manual_routing_manager.png | Lost Messages Manager access right | 20.0 chrome |
| message_citing | final_composer.png | Cited messages inserted at the cursor in the email composer | 20.0 chrome |
| message_citing | cite_widget_composer.png | Quick link to find and cite any Odoo message | 20.0 chrome |
| message_citing | message_select_cite.png | Search and filter messages before citing them | 20.0 chrome |
| message_citing | original_message_header.png | Configure the optional header for the cited messages | 20.0 chrome |
| message_edit | chatter_message_editing.png | Edit and delete messages, notes, and activity feedback | 20.0 chrome |
| message_edit | message_editing_rights.png | Assign own or any-message editing rights per user | 20.0 chrome |
| message_edit | message_edit_wizard.png | Full composer popup for rich message editing | 20.0 chrome |
| message_edit | changed_messages.png | Highlighted Changed Messages | 20.0 chrome |
| message_edit | history_of_changes.png | Detailed version history for every message edit | 20.0 chrome |
| message_edit | deleted_message_track.png | Tracking Removed Messages | 20.0 chrome |
| message_edit | deleted_messages_history.png | Complete History of Deleted Content and Attachments | 20.0 chrome |
| message_edit | channel_editing.png | Advanced Message Editor Window in Discuss Channels | 20.0 chrome |
| message_edit | live_chat_edit.png | Advanced Message Editor Window in Odoo Live chats | 20.0 chrome |
| message_edit | message_edit_delete_super_rights.png | Super Rights for Message Management | 20.0 chrome |
| message_edit | message_edit_full_composer.png | Full Composer Configuration | 20.0 chrome |
| message_edit | message_edit_standard_odoo_inline_mode.png | Standard Odoo Inline Message Editing | 20.0 chrome |
| odoo_email_from | odoo_email_from_settings.png | Turn on Email From pickers from Settings | 20.0 chrome |
| odoo_email_from | composer_email_from.png | From and Reply-To pickers in the composer | 20.0 chrome |
| odoo_email_from | email_from_address_book.png | Managed From and Reply-To address book | 20.0 chrome |
| odoo_email_from | email_template_email_from_reply_to.png | Managed Send From and Reply-To on email templates | 20.0 chrome |
| odoo_email_from | metadata_rules.png | Automatic sender rules by document type | 20.0 chrome |
| odoo_email_from | rule_to_assign_email_from.png | Metadata rule with domain filter | 20.0 chrome |
| odoo_email_from | email_template_from.png | Template sender prevails when rules defer | 20.0 chrome |
| odoo_email_from_accounting | invoice_email_from_reply_to.png | From and Reply-To on invoice Send and Print | 20.0 chrome |
| email_suite | email_suite_optional_features.png | Turn every native feature on or off (from Messaging Suite administration) | 20.0 chrome |
| email_suite | email_suite_email_from_and_lost_messages.png | Central settings for Email From and Lost Message Routing | 20.0 chrome |
| email_suite | messaging_actions.png | Open the extra chatter message actions menu (from Message actions and email metadata) | 20.0 chrome |
| email_suite | composer_cc_bcc.png | Add CC, BCC and configurable actions to the composer (from Compose like a real email client) | 20.0 chrome |
| email_suite | message_draft.png | Restore a saved draft back into the composer | 20.0 chrome |
| email_suite | list_of_message_drafts.png | List of message drafts | 20.0 chrome |
| email_suite | attachment_needed.png | Catch mentions of attachments before sending (from Catch missing attachments) | 20.0 chrome |
| email_suite | attachment_warning.png | No Attachment Found confirmation dialog (from Catch missing attachments) | 20.0 chrome |
| email_suite | flexible_configure_next_schedule_message.png | Set Scheduled Date dialog with your own presets (from Configurable send-later presets) | 20.0 chrome |
| email_suite | configurable_schedule_options.png | Manage Scheduled Sending Options in Discuss (from Configurable send-later presets) | 20.0 chrome |
| email_suite | message_route.png | Route Message wizard to attach an email to any record | 20.0 chrome |
| email_suite | message_extra_details.png | Inspect full email metadata from the chatter | 20.0 chrome |
| email_suite | button_wizard.png | Route lost emails to the correct record (from Lost Messages Routing) | 20.0 chrome |
| email_suite | lost_message_routing_wizard.png | Choose the target Odoo record for routing | 20.0 chrome |
| email_suite | unattached_messages.png | Lost messages list and batch routing action | 20.0 chrome |
| email_suite | final_thread.png | Recovered email attached to the correct thread | 20.0 chrome |
| email_suite | composer_email_from.png | From and Reply-To pickers in the composer | 20.0 chrome |
| email_suite | email_from_address_book.png | Managed From and Reply-To address book | 20.0 chrome |
| email_suite | email_template_email_from_reply_to.png | Managed Send From and Reply-To on email templates | 20.0 chrome |
| email_suite | rule_to_assign_email_from.png | Metadata rule with domain filter | 20.0 chrome |
| email_suite | email_template_from.png | Template sender prevails when rules defer | 20.0 chrome |
| email_suite | metadata_rules.png | Automatic sender rules by document type | 20.0 chrome |
| email_suite | private_message_composer.png | Send privately via the full composer (from Private Thread) | 20.0 chrome |
| email_suite | confidential_thread.png | Guaranteed Privacy for Correspondence | 20.0 chrome |
| email_suite | private_message_inline_composer.png | Quick Private Messaging Directly from Chatter | 20.0 chrome |
| email_suite | chatter_message_editing.png | Edit and delete messages, notes, and feedback (from Message/Note Editing) | 20.0 chrome |
| email_suite | message_edit_wizard.png | Full Composer Mode for Advanced Editing | 20.0 chrome |
| email_suite | changed_messages.png | Highlighted Changed Messages | 20.0 chrome |
| email_suite | history_of_changes.png | Detailed Version History Log | 20.0 chrome |
| email_suite | deleted_message_track.png | Tracking Removed Messages | 20.0 chrome |
| email_suite | deleted_messages_history.png | Complete History of Deleted Content and Attachments | 20.0 chrome |
| email_suite | channel_editing.png | Advanced Message Editor Window in Discuss Channels | 20.0 chrome |
| email_suite | live_chat_edit.png | Advanced Message Editor Window in Odoo Live chats | 20.0 chrome |
| email_suite | message_edit_delete_super_rights.png | Super Rights for Message Management | 20.0 chrome |
| email_suite | message_edit_standard_odoo_inline_mode.png | Standard Odoo Inline Message Editing | 20.0 chrome |
| email_suite | cite_widget_composer.png | Find and cite any Odoo message (from Message Citing) | 20.0 chrome |
| email_suite | message_select_cite.png | Filter and select the message(s) you want to reply to | 20.0 chrome |
| email_suite | final_composer.png | Add citations for any position in the email composer | 20.0 chrome |
| email_suite_accounting | invoice_email_suite.png | Cc, Bcc, From, and Reply-To on invoice Send and Print | 20.0 chrome |
| internal_thread | private_message_composer.png | Send privately from Compose Email | 20.0 chrome |
| internal_thread | confidential_thread.png | Only chosen recipients are notified | 20.0 chrome |
| internal_thread | private_message_inline_composer.png | Send privately from chatter | 20.0 chrome |
| internal_thread_accounting | send_invoices_privately.png | Send invoices privately from Send and Print | 20.0 chrome |
