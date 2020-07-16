from models import db
import dateutil.parser
import babel

#----------------------------------------------------------------------------#
# Helpers.
#----------------------------------------------------------------------------#

def safe_commit():
  status = False
  try:
    db.session.commit()
    status = True
  except:
    db.session.rollback()
  finally:
    db.session.close()
    return status

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  value = str(value)
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)
