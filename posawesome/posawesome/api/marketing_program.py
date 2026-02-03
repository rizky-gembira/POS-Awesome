import frappe
from frappe.utils import getdate

@frappe.whitelist()
def get_active_marketing_program():
    today = getdate()
    user = frappe.session.user

    # ambil POS Opening Shift paling terbaru untuk user ini
    pos_opening_shift_list = frappe.db.get_all(
        'POS Opening Shift',
        filters={'status': 'Open', 'user': user},
        fields=['name', 'period_start_date', 'pos_profile'],
        order_by='period_start_date desc',
        limit=1
    )

    recent_pos_opening_shift = pos_opening_shift_list[0] if pos_opening_shift_list else None
    if not recent_pos_opening_shift:
        return []

    # ambil POS Profile dari shift ini
    pos_profile = recent_pos_opening_shift.pos_profile
    cost_center = frappe.db.get_value("POS Profile", pos_profile, "cost_center")
    if not cost_center:
        return []

    # filter program aktif
    programs = frappe.get_all(
        "Marketing Program",
        filters={"docstatus": 1},
        fields=["name", "nama_program", "berlaku_dari", "berlaku_sampai", "details"],
    )

    active_programs = []
    for prog in programs:
        if getdate(prog.berlaku_dari) <= today <= getdate(prog.berlaku_sampai):
            toko_list = frappe.get_all(
                "Area Cost Center",
                filters={"parent": prog.name},
                pluck="nama_toko"
            )
            if cost_center in toko_list:
                active_programs.append(prog)

    return active_programs
