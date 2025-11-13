# Use the official Odoo 19.0 image as a base
FROM odoo:19.0

# Set environment variables for non-interactive setup
ENV ODOO_RC=/etc/odoo/odoo.conf
ENV DEBIAN_FRONTEND=noninteractive

# Copy the custom addons into the Odoo addons path
COPY ./addons /mnt/extra-addons

# Set permissions for the Odoo user
USER root
RUN chown -R odoo:odoo /mnt/extra-addons
USER odoo