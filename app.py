from flask import Flask, render_template, request, url_for, session, send_file, redirect
from pytube import YouTube
from io import BytesIO

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

@app.route('/home')
def homepage():
        return redirect(url_for('main'))

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        session['link'] = request.form.get('vidoe_link')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template('error.html', title='Yt-Down | Error', custom_css='error')
        video_title_letters = 0
        for i in url.title:
            video_title_letters += 1
        if video_title_letters <= 55:
            video_title = url.title
        else:
            video_title = f'Video Creator ( {url.author} )'
        return render_template('download.html', title='Yt-Down | Download', custom_css='download', url=url, video_title_text=video_title)
    return render_template('index.html', title="Yt-Down | Home", custom_css='home')

@app.route('/download', methods=['GET', 'POST'])
def download_video():
    if request.method == 'POST':
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=f"Yt-Down | {url.title}.mp4", mimetype="video/mp4")
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True)