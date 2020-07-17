from models import db, Show, Venue, Artist
from flask import render_template, request, flash
from forms import ShowForm
from helpers import safe_commit


#  Get Crete Show form
#  ----------------------------------------------------------------
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

#  Crete Show
#  ----------------------------------------------------------------
def create_show_submission():
    new_show = Show(
        artist_id=request.form.get('artist_id'),
        venue_id=request.form.get('venue_id'),
        start_time=request.form.get('start_time'),
    )

    db.session.add(new_show)
    if safe_commit():
        flash('Show was successfully listed!')
    else:
        flash('An error occurred. Show could not be listed.')

    return render_template('pages/home.html')

#  List Shows
#  ----------------------------------------------------------------
def shows():
    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)

#  Search Shows
#  ----------------------------------------------------------------
def search_shows():
    search_term = request.form.get('search_term', '')
    results = Show.query.join(Venue, Artist).filter(Venue.name.ilike('%' + search_term + '%') | Artist.name.ilike('%' + search_term + '%')).distinct().all()

    response = {
        "count": len(results),
        "data": results
    }
    return render_template('pages/show.html', results=response,
                           search_term=request.form.get('search_term', ''))