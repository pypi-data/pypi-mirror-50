"""
This example prints the download URLs for files returned from an 'as-is' data
export request. Note that there is no "Request URL" for method 'url_quick'.
"""
from __future__ import absolute_import, division, print_function
import example_helpers
import drms

# Print the doc string of this example.
print(__doc__)


# This example requires a registered export email address. You can register
# JSOC exports at: http://jsoc.stanford.edu/ajax/register_email.html
#
# You will be asked for your registered email address during execution of
# this example. If you don't want to enter it every time you run this script,
# you can set the environment variable JSOC_EXPORT_EMAIL or the variable
# below to your registered email address.
email = ''

# Data export query string
qstr = 'hmi.ic_720s[2015.01.01_00:00:00_TAI/10d@1d]{continuum}'

# Create DRMS client, use debug=True to see the query URLs.
c = drms.Client(verbose=True)

# Check if the email address was set at the top of this script. If not, ask for
# a registered email address.
if not email:
    email = example_helpers.get_export_email()
if not email or not c.check_email(email):
    raise RuntimeError('Email address is not valid or not registered.')

# Submit export request, defaults to method='url_quick' and protocol='as-is'
print('Data export query:\n  %s\n' % qstr)
print('Submitting export request...')
r = c.export(qstr, email=email)
print('%d file(s) available for download.\n' % len(r.urls))

# Print download URLs.
for i, row in r.urls[['record', 'url']].iterrows():
    print('REC: %s' % row.record)
    print('URL: %s\n' % row.url)
