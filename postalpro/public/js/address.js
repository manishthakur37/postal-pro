frappe.ui.form.on('Address', {
    pincode: function(frm) {
        // Check if the postal code is entered
        if (frm.doc.pincode) {
            frappe.call({
                method: "bookstore.api.get_circle_name_by_pincode",
                args: {
                    pincode: frm.doc.pincode  // Pass the postal code from the form
                },
                callback: function(r) {
                    if (r.message) {
                        // Set the respective fields with returned values
                        frm.set_value('address_line1', r.message.taluk); 
                        frm.set_value('city', r.message.districtname); 
                        frm.set_value('state', r.message.circlename); 

                        // Create the address title
                        const address_title = `${frm.doc.city}, ${frm.doc.address_line1}`;
                        frm.set_value('address_title', address_title);
                    } else {
                        frappe.msgprint({ message: __('No data found for the given postal code'), title: __('Warning'), indicator: 'orange' });
                    }
                },
                error: function(err) {
                    return
                }
            });
        }
    }
});






