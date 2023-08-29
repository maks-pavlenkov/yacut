import string
from random import choice, randint, shuffle
from . import app, db
from flask import abort, flash, redirect, render_template
from .forms import LinksForm
from .models import URLMap


def get_unique_short_id():
    # short_version = 'http://127.0.0.1:5000/'
    final = ''
    for _ in range(2):
        random_upper = choice(string.ascii_uppercase)
        random_lower = choice(string.ascii_lowercase)
        random_num = randint(0, 9)
        mix = random_upper + random_lower + str(random_num)
        mixed = list(mix)
        shuffle(mixed)
        mixed = ''.join(mixed)
        final += mixed
    return final


@app.route('/', methods=['GET', 'POST'])
def generate_link():
    short_version = 'http://127.0.0.1:5000/'
    form = LinksForm()
    if form.validate_on_submit():
        user_link = form.custom_id.data
        if user_link:
            if URLMap.query.filter_by(short=user_link).first():
                flash('Такая ссылка уже существует!')
                return render_template('link_part.html', form=form)
            pair_of_links = URLMap(
                original=form.original_link.data,
                short=form.custom_id.data
            )
            db.session.add(pair_of_links)
            db.session.commit()
            return render_template('link_part.html', form=form, link=short_version + form.custom_id.data)
        else:
            short_generated = get_unique_short_id()
            pair_of_links = URLMap(
                original=form.original_link.data,
                short=short_generated
            )
            db.session.add(pair_of_links)
            db.session.commit()
            return render_template('link_part.html', form=form, link=short_generated)
    return render_template('link_part.html', form=form)


@app.route(r'/<string:short_id>')
def redirecting(short_id):
    original_link = URLMap.query.filter_by(short=short_id).first()
    if not original_link:
        abort(404)
    return redirect(original_link.original)


if __name__ == '__main__':
    app.run()