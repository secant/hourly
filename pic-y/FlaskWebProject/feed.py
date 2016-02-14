//pull images from database from today
//display first 30
//button to load more

/

@app.route('/')
def show_pics():
	cur = g.db.execute('select user, title, description, location, url from food where theme = gettheme()')
	entries = [dict(user=row[0],title=row[1],desc=row[2],loc=row[3], url=row[4]) for row in cur.fetchall()]
	return render_template('show_entries.html', entries=entries)