
from flask import Flask, render_template, request, redirect, send_file
from extractors.indeed import extract_indeed_jobs
from save_file import save_to_file

app = Flask("WebScrapper")

@app.route("/")
def home():
    return render_template("home.html")

database = {}

@app.route("/search")
def search():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword in database:
        jobs = database[keyword]
    else:
        indeed = extract_indeed_jobs(keyword)
        jobs = indeed
        database[keyword] = jobs
    return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
    keyword = request.args.get("keyword")
    if keyword == None:
        return redirect("/")
    if keyword not in database:
        return redirect(f"/search?keyword={keyword}")
    save_to_file(keyword, database[keyword])
    return send_file(f"{keyword}.csv", as_attachment=True)

app.run("0.0.0.0") 