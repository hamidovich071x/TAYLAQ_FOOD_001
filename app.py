
from flask import Flask, request, redirect, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io, requests, os

app = Flask(__name__)
app.secret_key = "taylaqfood"

TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def send_to_telegram(text):
    if TELEGRAM_TOKEN and CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=5)
        except:
            pass

ADMIN_PASSWORD = "1234"
orders = []
cart = []

menu = {
    "Osh": {"price": 25000, "img": "https://images.unsplash.com/photo-1604908177522-0409cfe7c36d"},
    "Lag‘mon": {"price": 30000, "img": "https://images.unsplash.com/photo-1625944525533-473f1a3f87b5"},
}

def page(title, body):
    return f"<html><head><title>{title}</title></head><body>{body}</body></html>"

def price_of(n):
    return menu.get(n, {}).get("price", 0)

@app.route("/")
def home():
    h=""
    for n,i in menu.items():
        h+=f"<p>{n} - {i['price']} so'm <a href='/add/{n}'>Savatga</a></p>"
    return page("Home", h)

@app.route("/add/<n>")
def add(n):
    if price_of(n)>0:
        cart.append(n)
    return redirect("/")

@app.route("/payment", methods=["POST","GET"])
def pay():
    if request.method=="POST":
        total=sum(price_of(i) for i in cart)
        send_to_telegram(f"Yangi buyurtma: {cart} | {total}")
        cart.clear()
        return page("OK","Yuborildi")
    return page("Pay","<form method='post'><button>To'lash</button></form>")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000)
